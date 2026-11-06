```table-of-contents
```

1. bridge to appointments = consult but prioritize (is_npe = 1 desc, occur_datetime_local desc, )NPE 
# AI Review
https://m365.cloud.microsoft/hwav2/chat/conversation/1732384b-1753-4a4d-adc9-61fbd177426b?version=19.2608.54041.0&capabilities=interopPromise%2CsuspendOnClose%2CautoStart&client-request-id=&fromCode=cmm6j3rjue2&appstate=suspended&SSRDesktopTest=2

> 1. create void-pool via `patient + date`
> 2. bridge to contracts via sum() over 
> 3. consume and allocate, remainder

Recommended: aggregate voids into a positive void pool, sequence eligible contracts FIFO, then calculate how much of each contract falls inside that pool using cumulative ranges. This handles your $8,160 = 2 × $4,080 case without generating one row per cent.

```sql
/* Assumption:
   GrossContractAmount is the allocation basis.
   Allocation partition = SourceSystemId + patGUID + void_date_value.
*/

;with void_pool as
(
    select
        SourceSystemId,
        patGUID,
        void_date_value,
        abs(sum(void_amount)) as void_pool_amount
    from #gold__transaction_void
    group by
        SourceSystemId,
        patGUID,
        void_date_value
),
eligible_contracts as
(
    select
        v.SourceSystemId,
        v.patGUID,
        v.void_date_value,
        v.void_pool_amount,
        c.ContractKey,
        c.DateKey,
        c.GrossContractAmount as contract_amount,

        /* Contract's ending position in the FIFO queue */
        sum(c.GrossContractAmount) over
        (
            partition by
                v.SourceSystemId,
                v.patGUID,
                v.void_date_value
            order by
                c.DateKey,
                c.ContractKey
            rows unbounded preceding
        ) as contract_range_end
    from void_pool as v
    join Playground.jbi.vw_F_Contracts as c
        on c.SourceSystemId = v.SourceSystemId
       and c.patGUID       = v.patGUID
       and c.DateKey      <= v.void_date_value
),
contract_ranges as
(
    select
        *,
        contract_range_end - contract_amount as contract_range_start
    from eligible_contracts
),
allocation as
(
    select
        *,
        case
            when contract_range_start >= void_pool_amount then 0

            when contract_range_end <= void_pool_amount
                then contract_amount

            else void_pool_amount - contract_range_start
        end as allocated_void_amount
    from contract_ranges
)
select
    SourceSystemId,
    patGUID,
    void_date_value,
    ContractKey,
    DateKey,
    contract_amount,
    allocated_void_amount,
    row_number() over
    (
        partition by SourceSystemId, patGUID, void_date_value
        order by DateKey, ContractKey
    ) as allocation_sequence
from allocation
where allocated_void_amount > 0
order by DateKey, ContractKey;
```

Result for your example
Void pool: $8,160

ContractKey  Contract amount  Allocated
1098670      $4,080           $4,080
1099952      $4,080           $4,080
1100187      $4,080           $0


The cumulative ranges are:

1098670 → $0     to $4,080
1099952 → $4,080 to $8,160
1100187 → $8,160 to $12,240


The $8,160 pool overlaps only the first two ranges.

Next decision: this currently creates a daily aggregate-to-contract bridge. The next step would be distributing those allocations back down to the two transGUID rows, also FIFO.

# Draft 1
```sql
/*

-- stacked-union table with gold.contract
-- playground.gold.cms__contract_void_history --> match transGUID to contractKey
    -- exact deterministic match (same patient, same amount)
    -- aggregate match

*/
drop table if exists
    #bronze__transaction_void,
    #silver__transaction_void,
    #gold__transaction_void,
    #gold__transaction_contract_attribution;

declare @now datetime2 = sysutcdatetime();
declare @me sysname = 'jonas-adam.pascua@smiledoctors.com';

-- #1: get all voids in a given time frame
select
    t.SourceSystemId,
    t.locGUIDAssigned,
    t.patGUID,
    t.transDateTime,
    tt.ttypCode,
    t.transDueNowAmount void_amount,
    t.transNote,
    t.transGUID,
    t.empGUID,
    t.SD_LastModifiedUtc,
    t.transLastModified,
    @now load_datetime_utc,
    @me loaded_by_email
into
    #bronze__transaction_void
from CentralC9.dbo.[Transaction] as t
    join CentralC9.dbo.Patient as p
        on p.SourceSystemId = t.SourceSystemId
       and p.patGUID = t.patGUID
    join CentralC9.dbo.TransactionType as tt
        on tt.SourceSystemId = t.SourceSystemId
       and tt.ttypGUID = t.ttypGUID
where 1 = 1
  and t.transDateTime >= '2026-06-01'
  and t.transDateTime < '2026-07-01'
  and tt.ttypCode in ('ADJVC', 'ADJVAO');

-- 
select
    cast(t.transDateTime as date) void_date_value,
    trim(nullif(t.transNote, '')) void_trans_note,
    ce.employee_code, -- unified-dimension-enrichment
    --
    *
into
    #silver__transaction_void
from #bronze__transaction_void as t
    left join Playground.gold.cl9_employee as ce
        on ce.empGUID = t.empGUID
       and ce.SourceSystemId = t.SourceSystemId
;

select * from #silver__transaction_void as stv
return

-- #2: get subsample --> detail --> agg by clinic-patient-date --> nullify amount? --> step #3
;
with sample
as ( -- get 10 samples
   select distinct top 10 gtv.patGUID from #gold__transaction_void as gtv),
     date_agg__void
as (select
        SourceSystemId,
        locGUIDAssigned,
        patGUID,
        void_date_value,
        isnull(sum(void_amount), 0) void_amount
    from #gold__transaction_void
    where patGUID in (select patGUID from sample)
    group by SourceSystemId,
             locGUIDAssigned,
             patGUID,
             void_date_value)

-- #3: via agg-bridge, fifo match group-by:patient-net_contract_amount, prio by datekey asc
-- creates #gold__transaction_contract_attribution --> generate negative count
select
    v.*,
    -- match by person and amount, prioritized by datekey earliest (FIFO)
    case when row_number() over (partition by ctr.PersonKey, ctr.NetContractAmount order by ctr.DateKey) = 1 then 1
         else null end * -1 is_first_match,
    ctr.ContractKey,
    ctr.DateKey,
    ctr.patID,
    ctr.IsContractStart,
    ctr.TxCode,
    ctr.TxCodeGroup,
    ctr.NetContractAmount
into
    #gold__transaction_contract_attribution
from date_agg__void v
    left join Playground.jbi.vw_F_Contracts as ctr
        on ctr.patGuid = v.patGuid
       and ctr.SourceSystemid = v.SourceSystemid
       and v.void_date_value >= ctr.DateKey -- after or on same date
       and isnull(v.void_amount, 0) + isnull(ctr.NetContractAmount, 0) = 0
where 1 = 1;

-- ========================
-- final-view: evaluate matches
select * from #gold__transaction_contract_attribution as gtcad;

-- ========================
-- actual table to persist
select
    gtv.*,
    ContractKey
from #gold__transaction_contract_attribution as gtca
    join #gold__transaction_void as gtv
        on gtv.locGUIDAssigned = gtca.locGUIDAssigned
       and gtv.patGUID = gtca.patGUID
       and gtv.SourceSystemId = gtca.SourceSystemId;


-- 
--select * from #gold__transaction_void as gtv
---- 
--select * from Playground.jbi.vw_F_Contracts as ctr
--where ctr.patID = 'GCE127255'
```
[] --> **list**: ordered single items (array) --> "here are 5 things in order"
{} --> **dictionary**: key-value pairs (lookup table) --> "given x (key), return y"
- order doesn't matter

```json
{
  "name": "referral_group_impact",

  "original_table": "jbi.fs24990__referralsources__currentstate",
  "change_artifact": "jbi.fs24990__referralsources__changeproposed",

  "join_key": "ReferralSourceKey",

  "columns": {
    "current_source_column": "ReferralGroupKey",
    "artifact_current_column": "ReferralGroupKey_Current",
    "artifact_target_column": "ReferralGroupKey_Target"
  },

  "include_columns": [
    "snapshotdtutc",
    "ReferralSourceKey",
    "ReferralGroupKey",
    "ReferralSourceDescription",
    "ReferralSourceDescriptionRAW"
  ],

  "change_state_sort": {
    "Retain": 1,
    "Modify": 2,
    "Remove": 3,
    "Add": 4
  },

  "output_column_case": "snake_case",
  "sql_dialect": "tsql"
}
```

```sql
;with impact_base as (

    select
        {%- for col in include_columns %}
        frc.{{ col }}{% if not loop.last %},{% endif %}
        {%- endfor %},

        frc2.{{ artifact_current_column }},
        frc2.{{ artifact_target_column }},

        case
            when isnull(frc.{{ current_source_column }}, -1)
               = isnull(frc2.{{ artifact_target_column }}, -1)
                then 'Retain'

            when frc.{{ current_source_column }} is not null
             and frc2.{{ artifact_target_column }} is not null
             and frc.{{ current_source_column }} <> frc2.{{ artifact_target_column }}
                then 'Modify'

            when frc.{{ current_source_column }} is not null
             and frc2.{{ artifact_target_column }} is null
                then 'Remove'

            when frc.{{ current_source_column }} is null
             and frc2.{{ artifact_target_column }} is not null
                then 'Add'
        end as change_state,

        case
            when isnull(frc.{{ current_source_column }}, -1)
               = isnull(frc2.{{ artifact_current_column }}, -1)
                then 0
            else 1
        end as safety_mismatch_flag

    from {{ original_table }} as frc

    left join {{ change_artifact }} as frc2
        on frc2.{{ join_key }} = frc.{{ join_key }}
),

impact_summary as (

    select
        change_state,
        count(*) as qty
    from impact_base
    group by change_state
)

select
    change_state,
    qty
from impact_summary

union all

select
    'Total' as change_state,
    sum(qty) as qty
from impact_summary

order by
    case change_state
        {%- for state, sort_value in change_state_sort.items() %}
        when '{{ state }}' then {{ sort_value }}
        {%- endfor %}
        when 'Total' then 99
        else 100
    end;
```
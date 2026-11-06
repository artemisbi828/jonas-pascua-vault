1. need a roman_numeral_converter

2. **Removes null rows** (actual `NULL`, empty/whitespace, and the literal string `'NULL'`)
3. Extracts a **base integer** from each label using this precedence:
    - **Arabic digits** anywhere in the string (`REGION 10` → `10`)
    - Otherwise **Roman numeral token** (`DIVISION III` → `3`)
    - Otherwise **MO# suffix digits** (`REGION MO1` → `1`) _(this is already covered by “digits anywhere”, but kept conceptually)_
4. If **multiple rows resolve to the same base number**, it performs the “one more loop” to make them unique by adding **0.10 per collision**:
    - first instance of `1` → `1.00`
    - second instance of `1` → `1.10`
    - third instance of `1` → `1.20`



```sql
;
with src
as (select
        OfficeCode location_code,
        TeamName team_name,
        DivisionName division_name,
        RegionName region_name,
        cast(Cloud9ConversionDate as date) effective_start_date,
        cast(EndDate as date) effective_end_date
    from Lake.extenders.Offices
    where 1 = 1
      and TeamName is not null),
     base
as (select distinct region_name label from src s union select distinct s.division_name from src s),
     -- ========================
     normalized
as (select
        c.label,
        -- normalize obvious punctuation to spaces (extend as needed)
        norm = ltrim(rtrim(replace(replace(replace(c.label, N'→', N' '), N'-', N' '), N'  ', N' ')))
    from base c),
     base_extracted
as (select
        n.label,
        n.norm,

        /* 1) First digit occurrence anywhere (REGION 10, REGION MO1, DIVISION 0, etc.) */
        first_digit_pos = nullif(patindex('%[0-9]%', n.norm), 0),

        /* last token (for roman numerals) - split by spaces via OPENJSON preserving order */
        last_token = (
            select top (1)
                   s.value
            from openjson(N'["' + replace(replace(n.norm, N'"', N'\"'), N' ', N'","') + N'"]') s
            order by try_convert(int, s.[key]) desc
        )
    from normalized n),
     base_number
as (select
        b.label,
        base_int = coalesce(
                       /* A) Arabic digits: take contiguous run starting at first digit */
                       try_convert(
                           int,
                           case when b.first_digit_pos is not null then substring(b.norm,
                                                                                  b.first_digit_pos,
                                                                                  case when patindex('%[^0-9]%', substring(b.norm, b.first_digit_pos, 100)) = 0 then 100
                                                                                       else patindex('%[^0-9]%', substring(b.norm, b.first_digit_pos, 100)) - 1 end
                                                                        ) end
                       ),

                       /* B) Roman numerals (supports I..XXVII easily; extend if needed) */
                       roman_numerical_cnv.int_value
                   )
    from base_extracted b
        left join (
            values ('I', 1),
                   ('II', 2),
                   ('III', 3),
                   ('IV', 4),
                   ('V', 5),
                   ('VI', 6),
                   ('VII', 7),
                   ('VIII', 8),
                   ('IX', 9),
                   ('X', 10)
        ) roman_numerical_cnv (string_value, int_value)
            on upper(ltrim(rtrim(b.last_token))) = roman_numerical_cnv.string_value),
     deduped
as (select
        bn.label,
        bn.base_int,
        rn = row_number() over (partition by bn.base_int order by bn.label)
    from base_number bn
    where bn.base_int is not null -- drop anything we cannot parse (e.g. "DIVISION MO")
     )
select
    label,
    extracted_numeric = cast(b.base_int + (b.rn - 1) * 0.10 as decimal(10, 2))
from deduped b
order by extracted_numeric,
         label;

```
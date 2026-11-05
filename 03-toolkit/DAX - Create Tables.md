Model View → New Table → 

```shell
Toggles =
DATATABLE (
    "Toggle", STRING,
    {
        { "See All" },
        { "See All SSS" },
        { "Same Store" },
        { "See All WDE" },
        { "Work Day Equivalent" }
    }
)

# 2 columns
Measure Map = 
DATATABLE(
    "SemanticModel_MeasureName", STRING,
    "MeasureName", STRING,
    {
        { "Spend Digital",        "Marketing Spend" },
        { "Spend Local",        "Marketing Spend" },
        { "Impressions",    "Google Performance" },
        { "Clicks",    "Google Performance" },
        { "CPC",    "Google Performance" },
        { "Overall",               "Overall" },
        { "Digital",               "Digital" },
        { "Non-Digital",           "Non-Digital" },
        { "NPS Responses",            "NPS Score %" },
        { "NPS Score %",            "NPS Score %" },
        { "Schedule Availability", "Schedule Availability" }
    }
)

```

# After Copy
Fix visual by redoing filter
```sql
declare @test nvarchar(max) = -- 
(select '''' + 
    concat([pat].[SourceSystemId], '''',
    ';' + char(13),  '''', [pat].[patGuid],'''',
    ';' + char(13), 'null', -- transGUID
    ';' + char(13),  '''', caa.[ppGUID],'''',
    ';' + char(13),  '''', [pp].[persGUIDRelated],'''',
    ';' + char(13), 'null', -- tfpGUID
    ';' + char(13), 'null', -- tfppGUID
    ';' + char(13),  '''', [pp].[persGUID], '''',-- persGUIDPatient
    ';' + char(13), 'null', -- pipGUID
    ';' + char(13),  '''', [ofc].[locGuid], '''',
    ';' + char(13), 'null', -- ttypGUID
    ';' + char(13),  '''', [ofc].[OfficeCode], '''',
    ';'
    ) as test
from [EDW].[help].[vw_bi_Patient] as [pat]
    inner join Lake.C9.[CurrentArAging] as [caa]
        on [caa].[SourceSystemId] = [pat].[SourceSystemId]
       and [caa].[patGUID] = [pat].[patGuid]
    inner join CentralC9.dbo.PersonPerson as pp
        on [pp].[ppGUID] = [caa].[ppGUID]
       and [pp].[SourceSystemId] = [caa].[SourceSystemId]
    left join EDW.bi.Contracts as ctr
        on [ctr].[PersonKey] = [pat].[PersonKey]
    left join EDW.bi.[vw_pds_Offices] as [ofc]
        on ofc.[OfficeKey] = pat.[OfficeKey]
where [pat].[patID] = 'MWZ336432')
print @test
```

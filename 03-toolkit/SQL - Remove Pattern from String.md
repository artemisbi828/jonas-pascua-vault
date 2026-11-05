```sql
SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
CREATE FUNCTION [std].[udf_RemovePattern] (
    @strText varchar(1000), -- pass in a string
    @pattern varchar(100)   -- pass in a pattern
)
returns varchar(1000) -- return this datatype
as begin
 
    while patindex(@pattern, @strText) > 0 -- while the pattern exists in the string (>0)
    begin
        -- stuff :: find and replace
        -- while (looping) -- pattern exists in string at least 1x
        -- find and replace pattern with ''
        -- redefine str to remove pattern until done 
        -- return final string 
 
        set @strText = stuff(@strText, patindex(@pattern, @strText), 1, '');
    end;
    return @strText;
 
end;
GO

```

#status/deferred/quick-paste-merge-later 
```sql
SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
CREATE   FUNCTION [std].[udf_RemoveLettersAllCapsFromString]  (@strText varchar(1000))
returns varchar(1000)
as begin
 
    return trim([std].[udf_RemovePattern] (@strText, '%[a-zA-Z]%'));
 
end;
GO
 
SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
create function std.udf_RemoveParenthesisAndDashesFromString (@strText varchar(1000))
returns varchar(1000)
as begin

    -- excludes spaces 
	-- may want to include charindex 
    return trim(std.udf_RemovePattern(@strText, '%[() -]%'));

end;
GO

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
CREATE   FUNCTION [std].[udf_GetNumbersFromString] (@strText varchar(1000))
returns varchar(1000)
as begin

    -- excludes spaces 
	-- may want to include charindex 
    return trim([std].[udf_RemovePattern] (@strText, '%[^0-9]%'));

end;
GO

SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
CREATE   FUNCTION [std].[udf_FormatPhone]
(
    @strtext VARCHAR(32)
)
RETURNS VARCHAR(32)
AS
BEGIN

    -- build US standard phone number
    SET @strtext = [std].[udf_RemoveLettersAllCapsFromString](@strtext);
    SET @strtext = [std].[udf_GetNumbersFromString](@strtext);
    SET @strtext = CONCAT(LEFT(@strtext, 3), '-', SUBSTRING(@strtext, 4, 3), '-', RIGHT(@strtext, 4));
    /* if -- return null */
    RETURN NULLIF(@strtext, '--');
END;
GO


```
```sql
--formatting variables
declare @crlf as varchar(16) = char(13) + char(10);
declare @crlf2 as varchar(16) = @crlf + @crlf;
declare @t as varchar(16) = char(9);
declare @t2 as varchar(16) = @t + @t;
declare @crlft as varchar(16) = @crlf + @t;

----
SET QUOTED_IDENTIFIER ON
SET ANSI_NULLS ON
GO
 
ALTER function [dbo].[fnLeftPad] (@SourceString varchar(max), @FinalLength int, @PadChar char(1))
returns varchar(max)
as begin
    /*
        2021-11-10 : gregg.rousslle
            - if the sourceString is greater than @final length an error is returned. During the statement process it was
            extremely difficult to figure out which call to this function was the problem, so we used a clever trick to return
            a more meaningful error by casting a string to an int.    
    */
 
    if @SourceString is null set @SourceString = '';
 
    declare @padLen as int = @FinalLength - datalength(@SourceString);
    if @padLen < 0 begin
        declare @msg as nvarchar(max) = N'** Error in dbo.fnLeftPad `' + @SourceString + N'` is longer than the final length (' + cast(@FinalLength as varchar(max)) + N')';
        declare @fakeInt as int = cast(@msg as int);
    end;
 
    return replicate(@PadChar, @padLen) + @SourceString;
end;
 
GO
```
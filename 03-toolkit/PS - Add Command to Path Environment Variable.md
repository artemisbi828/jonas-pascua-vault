
### Add To Path
`[Environment]::SetEnvironmentVariable("Path", $env:Path + ";C:\Repos\sd-edw\toolkit", "User")`

### Test Command
Test: `where.exe logger.cmd`
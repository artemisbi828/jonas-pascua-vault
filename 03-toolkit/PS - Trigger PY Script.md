
```shell
python .\script.py
python3 .\script.py
"C:\Path\To\Python.exe" "C:\Path\To\script.py"
```

# Scheduled Task
```shell
$action = New-ScheduledTaskAction -Execute "python.exe" -Argument "C:\scripts\job.py"
$trigger = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1)
Register-ScheduledTask -TaskName "RunPythonJob" -Action $action -Trigger $trigger
Start-ScheduledTask -TaskName "RunPythonJob"
```

`taskkill /IM PBIDesktop.exe /F`

```
tasklist /SVC | sort
tasklist /FI "Imagename eq PBIDesktop.exe"
tasklist /? >> help command


taskkill /IM PBIDesktop.exe /F
taskkill /IM excel.exe /F 
taskkill / PID 18484 /F
```
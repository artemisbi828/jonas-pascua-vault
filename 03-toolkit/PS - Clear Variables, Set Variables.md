`clear-variable listItems`


# 1. Set it just for this session
```
$env:DOCKER_USERNAME = "jpascua313"
echo $env:DOCKER_USERNAME                                        # Shows value
[Environment]::GetEnvironmentVariable('DOCKER_USERNAME', 'User') # Shows nothing
```

# 2. Set it permanently with setx
`setx DOCKER_USERNAME "jpascua313"`
# At this point you need to open a new PowerShell window to see the change!

# 3. In the new window:
```
echo $env:DOCKER_USERNAME                                        # Shows value
[Environment]::GetEnvironmentVariable('DOCKER_USERNAME', 'User') # Also shows value
```

```bash
git clone <url>

# example
git clone https://SmileDoctorsIT@dev.azure.com/SmileDoctorsIT/Project%20Ascend/_git/Project%20Ascend 
```


# Initialize
Go to folder

```shell
# go to target folder
cd C:\vsWorkspace\jpascua313
git init
git config user.name "jpascua313"
git config user.email "jpascua@gmail.com"
git remote add origin https://github.com/jpascua313/intro  
```

```shell
# initialize current folder as git
git init                                                                   
git checkout main # (optional) -- switch to main

# bind current folder to remote
git remote -v  ## what is remote?
git remote add origin https://github.com/artemisBI/shared-utils     
```

# Install CLI + Authenticate
### Step 1: Install GitHub CLI (if not already installed)
```
# Using winget (recommended)
winget install GitHub.cli

# Or download from: https://cli.github.com/
```

### Step 2: Authenticate with GitHub
```
gh auth login
# Follow the prompts:
# 1. Select "GitHub.com"
# 2. Select "HTTPS" or "SSH" (HTTPS is easier)
# 3. Choose "Paste authentication token" or "Authorize with browser"
# 4. If browser, you'll be taken to GitHub to authorize
```

### Step 3: Then clone
```
# Now try cloning again
git clone https://github.com/SmileDoctorsIT/data-platform
```
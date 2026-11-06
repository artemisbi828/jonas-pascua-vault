If you've switched from work → personal and back, most likely -- Windows Credential Manager has saved and has cached the login and you have to remove it. 

STEP 1
Press Win + R
Type `control /name Microsoft.CredentialManager`
Go to Windows Credentials
Find git:https://github.com or similar
Click it and select Remove

STEP 2 -- Re-authenticate
`git ls-remote origin HEAD`

STEP 3 -- Verify
`git pull origin main`
These are steps to keep my local clones aligned with origin - remote
### Discard Commit
`git reset --hard`
- without a target, it's the syn-sugar `git reset --hard HEAD` --> commit I am currently on (last save)
- I have to **specify a target** `git reset --hard origin/feat/26274-addon-attachment-contract-field` --> "make my current local branch exactly match the remote-tracking copy of this particular branch"
- You can also try to use `git reset --hard @{u}` next time
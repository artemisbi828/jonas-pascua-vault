* **`origin`** → *most used remote name*
* **`main`** → *most used default branch name*
	* **`master`** → alt name for default branch

They are **not interchangeable**.

To rename main → master
```
- make sure to go on UI\Settings\DefaultBranch → rename
```shell
git branch -m master main
```



## What each one is (clean mental model)

### ✅ `origin`

*   A **remote alias**
*   Points to *where the repo lives* (GitHub, Azure DevOps, etc.)
*   Created automatically when you clone

```bash
origin = remote
```

Example:

```bash
git pull origin main
```

Meaning: *pull from the remote called `origin`, branch `main`*

✅ **`origin` is universal and ubiquitous**

***

### ✅ `main`

*   A **branch name**
*   Replaced `master` as the default branch starting \~2020
*   Lives both locally and remotely

```bash
main = branch
```

Example:

```bash
git checkout main
```

✅ **`main` is now the industry default branch name**

***

## Usage frequency (real-world)

| Concept    | More used?   | Why                            |
| ---------- | ------------ | ------------------------------ |
| `origin`   | ✅ Yes        | Every repo needs a remote      |
| `main`     | ✅ Yes        | Default branch in modern repos |
| `master`   | ⬇️ Declining | Legacy only                    |
| `upstream` | Contextual   | Fork-based workflows           |

***

## Common commands (this usually clicks)

```bash
git pull origin main
git push origin main
git fetch origin
```

Think:

    origin = WHERE
    main   = WHAT

***

## Common beginner confusion (important)

❌ “Is `origin` or `main` more used?”  
✅ Better question: *“Which layer am I talking about?”*

They exist at **different conceptual layers**:

    Remote layer:   origin, upstream
    Branch layer:   main, develop, feature/*

***

## Best practice today (what you should expect)

*   ✅ Default branch: **`main`**
*   ✅ Default remote: **`origin`**
*   ✅ Additional remotes (optional): `upstream`

***

## One-liner to remember forever

> **You push a branch (`main`) to a place (`origin`).**

If you want next:

*   `origin/main` vs `main`
*   local vs remote branches
*   why `git pull` sometimes surprises people
*   how Azure DevOps handles defaults
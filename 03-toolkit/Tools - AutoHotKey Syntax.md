You’re very close — the issue isn’t that `---` is being treated as a “comment line” (AHK v1 comments are `;`), it’s that **hotstring options + the hotstring “ending character” behavior** are interacting with your trigger and what you type next.

## Why you’re seeing `--→` (and not `---→`)

In AutoHotkey v1, a hotstring like:

```ahk
::--->::→
```

fires when AHK sees the trigger text **and then an “ending character”** (space, Enter, punctuation, etc.), unless you change that behavior with options.

So what often happens in practice is:

1.  You type `---`
2.  You type `>`
3.  AHK is waiting for an ending character to decide it’s a complete hotstring.
4.  Depending on what you type immediately after (`space`, another symbol, backspace habits, etc.), AHK may:
    *   **erase only part** of what it thinks matched, or
    *   fire in a way that leaves some characters behind

That’s how you can end up with something like `--→` (two dashes remain) instead of the full replacement.

This is especially common when the trigger ends with punctuation and you type punctuation immediately after, because AHK’s default “end char” logic wasn’t designed for “operator-like” sequences.

***

## The fix (best practice): use the `*` option

Use the `*` hotstring option to make it fire **without requiring an ending character**.

```ahk
#Requires AutoHotkey v1.1
#SingleInstance Force

:*:--->::→
```

### What `*` does

*   `*` = “trigger immediately” (no ending character required)
*   This is ideal for symbolic sequences like `--->`, `=>`, `...`, etc.

✅ Now, as soon as you type the final `>` in `--->`, it will replace the whole thing with `→`.

***

## If you want it to behave even more “literal” (no backspacing quirks): use `B0`

Sometimes punctuation-heavy triggers can still be finicky if you backspace or if other hotstring options are in play. You can force “no backspacing” behavior with `B0` (rarely needed, but useful to know).

```ahk
:*B0:--->::→
```

*   `B0` tells AHK not to use backspaces to erase the trigger (it uses a different method).
*   If you have any odd “leftover characters” issues, `B0` can help.

***

## Alternative robust method: `:::` hotstring with `SendInput` (when you want custom behavior)

If you ever want the arrow plus something else (or want to avoid hotstring parsing entirely), you can do:

```ahk
::--->::
SendInput, →
return
```

This is “heavier” than the `:*:` approach, but gives you full control.

***

## Quick sanity checklist (common gotchas)

1.  **Make sure you’re using the right arrow character**
    *   `→` (U+2192) not `->` or some font substitute.

2.  **Make sure you don’t have another overlapping hotstring**
    *   For example, if you also have `::-->::` or `::---::` defined, it can “steal” the match earlier.

3.  **Reload the script after edits**
    *   Right-click AHK tray icon → Reload Script.

***

## Final recommended snippet (clean + correct)

```ahk
#Requires AutoHotkey v1.1
#SingleInstance Force

:*:--->::→
```

***

If you tell me **exactly what keystrokes you type right after** `---` / `>` (space? enter? another character?), I can explain precisely why your current one leaves two dashes behind in your specific typing pattern.

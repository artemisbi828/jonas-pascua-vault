1. create anchor link block: `^name` (no space)
2. call anchor link block: `#^` after `[[]]
3. preview by `hold + ctrl` + `mouse-over`



It’s a bit like digital magic when Obsidian "remembers" a part of your note you didn't even name, isn't it? That little code—like `^5842da`—is Obsidian's way of ensuring that even if you move things around, your links don't break.

Here is the breakdown of how Block IDs work and why they appear "unmarked."

---

## 1. What is a Block ID?

In Obsidian, a **block** is any individual unit of content: a paragraph, a list item, a quote, or even a heading. While a standard link `[Note Name]` points to a whole file, a **Block Link** `[Note Name#^id]` points to a specific spot inside that file.

* **Custom IDs:** You can create these manually by typing ` ^your-id` at the end of a paragraph.
* **Generated IDs:** These are the random alphanumeric strings (e.g., `^5842da`) that you’re seeing.

---

## 2. How it "Recognizes" Unmarked Blocks

You might be surprised to see a Block ID for something you didn't label, but Obsidian actually **only generates that ID the moment you try to link to it.**

Here is the "Invisible" process:

1. **The Search:** When you type `[Note Name#^` in a note, Obsidian scans the target note for every single "block" (paragraph, bullet, etc.).
2. **The Selection:** As you scroll through the autocomplete menu and pick a paragraph that *doesn't* have an ID yet, Obsidian says, "Okay, I need a way to find this later."
3. **The Injection:** The moment you press `Enter` to create that link, Obsidian **silently modifies the original source note**. It goes back to that paragraph and appends a unique ID (like `^5842da`) to the end of it.

> **Note:** If you look at your "PRJ - CRM App" note now, you will likely see that `^5842da` physically typed at the end of the text block. It wasn't there before, but it is there now!

---

## 3. Why does it work this way?

If Obsidian didn't use these IDs, it would have to rely on the exact text of the paragraph to find the link. If you fixed a typo or changed a word in that paragraph, the link would "break."

By attaching a permanent ID to the block:

* You can edit the text as much as you want.
* You can move the block to a different part of the note.
* The link remains functional because it is looking for the **ID**, not the words.

---

### Pro-Tip: Cleaner IDs

If those random strings look like "code vomit" to you, you can always manually type a space, a caret, and a name you prefer at the end of a block, like this:
`This is my important project detail. ^details`

Then, when you link to it, your link will look much cleaner: `[[PRJ - CRM App#^details]`.

Would you like me to show you how to use these Block IDs to create a "Table of Contents" or a summary page for your CRM app?
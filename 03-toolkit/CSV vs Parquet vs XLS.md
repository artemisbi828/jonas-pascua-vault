**CSV vs Parquet vs Excel**

- **CSV**: use it. Browsers can write it natively, it diffs cleanly, and Excel, DuckDB, and SQL all read it. It's ideal for small, append-only data.
- **Parquet**: skip it. It's built for read-heavy analytics, needs a WASM library to write from a browser, and gives you nothing at a few thousand rows.
- **Excel as the store**: skip it. You'd need SheetJS (about 1 MB) to write it, and you'd fight OneDrive co-authoring locks. Keep Excel as the **viewer**: users can open the CSVs to check their work.
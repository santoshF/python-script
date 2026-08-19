# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Running the script

```bash
# Dry run (default — no files are changed); -d defaults to current directory
python3 file_renamer/rename_files.py -d <directory> [--sequential | --replace OLD NEW | --regex PAT REPL | --lowercase | --remove-spaces]

# Apply changes
python3 file_renamer/rename_files.py -d <directory> <mode-flag> --execute
```

Mode-specific options:
- `--sequential`: `-p`/`--prefix` (default `"file"`), `-e`/`--extension` (force extension, e.g. `.jpg`)
- `--remove-spaces`: `-s`/`--separator` (default `_`)
- `--move`: `--dest <destination>` (required), `--pattern <glob>` (optional, e.g. `"*.jpg"`)

No dependencies beyond the Python 3 standard library. No build step, no virtual environment needed.

## Architecture

Single-file script (`file_renamer/rename_files.py`). Each renaming strategy is a standalone function:

- `rename_sequential` — sorts files lexicographically, then renames to `prefix_N[ext]`
- `rename_replace` — plain substring replace across filenames
- `rename_regex` — `re.sub` across filenames
- `rename_lowercase` — lowercases filenames
- `rename_remove_spaces` — replaces spaces with a configurable separator (default `_`)
- `move_files` — moves files to a destination directory; optional glob `pattern` filters which files move; uses `shutil.move` (safe across filesystems); skips collisions with a warning rather than overwriting

All functions share the same signature: `(folder_path, ..., dry_run=True)`. The `dry_run` flag is the inverse of `--execute` from the CLI and is the primary safety mechanism — no function writes to disk unless `dry_run=False`.

`main()` owns all argument parsing (`argparse`) and dispatches to exactly one of the above functions per invocation. The mode flags are mutually exclusive; passing none prints help and exits. The script operates only on the top-level files in the target directory (non-recursive).

# File Inventory Verify

Create SHA-256 inventories of local backup folders and verify files after a move.

## Quick start

Requires Python 3.11 or later. Uses the standard library and runs locally.

```bash
python3 tool.py snapshot /path/to/folder
```

Output is formatted JSON on standard output. Invalid inputs report an error on standard error and exit with status 1. Run the tool with --help for all arguments.

Run with Python 3.11 or later. Save the snapshot outside the scanned folder. Paths are relative and use slashes. Symbolic links are skipped.

## Example input

**fixture/hello.txt**

```
hello
```

## Example output

```json
{
  "algorithm": "sha256",
  "files": {
    "hello.txt": "5891b5b522d5df086d0ff0b110fbd9d21bb4fc7163af34d08286a2e846f6be03"
  }
}
```

## License

[MIT](LICENSE).

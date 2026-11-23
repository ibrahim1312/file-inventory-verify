"""Create SHA-256 inventories of local backup folders and verify files after a move."""

import argparse
import json
from decimal import InvalidOperation
from pathlib import Path
import hashlib


def main():
    parser = argparse.ArgumentParser(description='Create SHA-256 inventories of local backup folders and verify files after a move.')
    parser.add_argument("mode", choices=["snapshot", "verify"])
    parser.add_argument("directory", type=Path)
    parser.add_argument("manifest", type=Path, nargs="?")
    args = parser.parse_args()
    if not args.directory.is_dir():
        raise ValueError("directory must be an existing directory")
    if (args.mode == "verify") != (args.manifest is not None):
        raise ValueError("give a manifest path for verify only")
    inventory = {}
    exclude = args.manifest.resolve() if args.manifest else None
    for path in sorted(args.directory.rglob("*")):
        if not path.is_file() or path.is_symlink() or path.resolve() == exclude:
            continue
        with path.open("rb") as stream:
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
        inventory[path.relative_to(args.directory).as_posix()] = digest
    report = {"algorithm": "sha256", "files": inventory}
    if args.manifest:
        prior = json.loads(args.manifest.read_text(encoding="utf-8"))
        if not isinstance(prior, dict) or prior.get("algorithm") != "sha256":
            raise ValueError("expected a sha256 inventory")
        previous = prior.get("files")
        if not isinstance(previous, dict):
            raise ValueError("invalid inventory file map")
        report = {"added": sorted(inventory.keys() - previous.keys()),
                  "missing": sorted(previous.keys() - inventory.keys()),
                  "changed": sorted(key for key in inventory.keys() & previous.keys()
                                    if inventory[key] != previous[key])}
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, OverflowError, InvalidOperation, TypeError) as error:
        raise SystemExit(f"Error: {error}") from None

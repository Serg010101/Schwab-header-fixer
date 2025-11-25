#!/usr/bin/env python3
import sys
from pathlib import Path
import csv


def fix_trn_file(input_path: Path) -> Path:
    """
    Combine the first 3 header rows of a Schwab TRN file into a single header row
    and write out <original>_fixed.csv next to the source file.
    """
    input_path = input_path.expanduser().resolve()

    with input_path.open("r", encoding="utf-8", errors="ignore") as f:
        # Read and strip newlines
        lines = [line.rstrip("\r\n") for line in f]

    if len(lines) < 3:
        raise ValueError(f"{input_path.name}: file has fewer than 3 lines, cannot build headers")

    # Split each line on pipe and pad all rows to the same length
    rows = [line.split("|") for line in lines]
    max_cols = max(len(r) for r in rows)
    for r in rows:
        if len(r) < max_cols:
            r.extend([""] * (max_cols - len(r)))

    # First three rows are the Schwab header parts
    h1, h2, h3 = rows[0], rows[1], rows[2]
    data_rows = rows[3:]

    # Build combined header: "SCHWAB Custodian ID", "0008016283 MstrAcct Number", etc.
    header = []
    for c1, c2, c3 in zip(h1, h2, h3):
        parts = [c1.strip(), c2.strip(), c3.strip()]
        parts = [p for p in parts if p]          # drop empty pieces
        header.append(" ".join(parts))           # join with spaces

    # Output path: same folder, *_fixed.csv
    output_path = input_path.with_name(input_path.stem + "_fixed.csv")

    # Write out as pipe-delimited CSV
    with output_path.open("w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out, delimiter="|")
        writer.writerow(header)
        writer.writerows(data_rows)

    return output_path


def main(argv: list[str]) -> int:
    if len(argv) < 1:
        print("Usage: python3 combine_headers.py /path/to/TRN1.csv [/path/to/TRN2.csv ...]")
        return 1

    exit_code = 0

    for arg in argv:
        path = Path(arg)
        if not path.exists():
            print(f"[SKIP] {arg} – file not found")
            exit_code = 1
            continue

        try:
            out = fix_trn_file(path)
            print(f"✔ Fixed file created: {out}")
        except Exception as e:
            print(f"✖ Error processing {arg}: {e}")
            exit_code = 1

    return exit_code


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
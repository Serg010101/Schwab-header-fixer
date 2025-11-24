import sys
from pathlib import Path
import csv

def fix_schwab_headers(input_path: Path):
    with input_path.open("r", encoding="utf-8", errors="ignore") as f:
        lines = [line.rstrip("\n\r") for line in f]

    if len(lines) < 3:
        raise ValueError("File has fewer than 3 lines – cannot build headers.")

    rows = [line.split("|") for line in lines]
    max_cols = max(len(r) for r in rows)
    for r in rows:
        r.extend([""] * (max_cols - len(r)))

    h1, h2, h3 = rows[0], rows[1], rows[2]

    headers = []
    for i in range(max_cols):
        if i == 0:
            headers.append("RowType")
        else:
            p1 = h1[i].strip()
            p2 = h2[i].strip()
            p3 = h3[i].strip()
            parts = [p for p in (p1, p2, p3) if p]
            headers.append(" ".join(parts) if parts else f"col_{i:03d}")

    output_path = input_path.with_name(input_path.stem + "_fixed.csv")

    data_rows = rows[3:]

    with output_path.open("w", encoding="utf-8", newline="") as f_out:
        writer = csv.writer(f_out)
        writer.writerow(headers)
        for r in data_rows:
            writer.writerow(r)

    return output_path

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 combine_headers.py /path/to/TRN.csv")
        sys.exit(1)

    input_path = Path(sys.argv[1]).expanduser().resolve()
    if not input_path.exists():
        print(f"File not found: {input_path}")
        sys.exit(1)

    out = fix_schwab_headers(input_path)
    print(f"✔ Fixed file created:\n{out}")

if __name__ == "__main__":
    main()

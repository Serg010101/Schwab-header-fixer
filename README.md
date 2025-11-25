Schwab TRN Header Fixer

A small utility script that combines the first 3 header rows of Schwab TRN files into a single clean header row.
Useful for correcting malformed custodial files so they can be loaded into SQL, Python, or any processing pipeline.

⸻

🚀 What This Script Does

Schwab TRN files often contain:

	•	H1 row (file metadata)
	
	•	H2 row (grouping labels)
	
	•	H3 row (actual column titles)

Because these rows are split separately, the column names become unclear.

This tool:
	1.	Reads the TRN file
	2.	Merges row H1 + H2 + H3 into a single header per column
	3.	Outputs a new TRN-like file with unified headers
	4.	Leaves all D1 data rows untouched

⸻

📦 How to Use (Mac / Windows)

Step 1 — Download the script

Download combine_headers.py from this repository.

Step 2 — Run it on your TRN file

Open Terminal (or PowerShell on Windows) and run:

python combine_headers.py /path/to/input_file.TRN.csv /path/to/output_file.csv

Example:

python combine_headers.py ~/Downloads/CRS20250715.TRN.csv ~/Downloads/CRS20250715_fixed.csv

Output:

A new file with correct, combined headers.

⸻

📝 Requirements
	•	Python 3.x installed
	•	TRN file exported from Schwab

No external libraries required.

⸻

🛠 Example Output Header

RowType|Custodian ID|0008016283 MstrAcct Number|Master Account Name|Business Date|...


⸻

🤝 Contributing

Feel free to open issues or submit improvements via pull requests.

⸻

📬 Contact

If you have any questions, reach out to Serg010101 on GitHub.

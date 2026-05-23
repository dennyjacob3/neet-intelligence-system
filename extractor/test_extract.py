import pdfplumber
import pandas as pd
from pathlib import Path

RAW_PDF_FOLDER = Path("raw_pdfs")
OUTPUT_FOLDER = Path("output")

OUTPUT_FOLDER.mkdir(exist_ok=True)

for pdf_file in RAW_PDF_FOLDER.glob("*.pdf"):

    print(f"\n==============================")
    print(f"Processing: {pdf_file.name}")
    print(f"==============================")

    all_rows = []

    try:

        with pdfplumber.open(pdf_file) as pdf:

            print(f"Total pages: {len(pdf.pages)}")

            for page_number, page in enumerate(pdf.pages[:5]):

                print(f"\nProcessing page {page_number + 1}")

                try:

                    # Try table extraction first
                    table = page.extract_table()

                    if table:

                        print(f"Table found with {len(table)} rows")

                        for row in table:

                            cleaned_row = []

                            for cell in row:

                                if cell:
                                    cell = str(cell)
                                    cell = cell.replace("\n", " ")
                                    cell = cell.strip()

                                cleaned_row.append(cell)

                            all_rows.append(cleaned_row)

                    else:

                        print("No table found. Trying text extraction...")

                        text = page.extract_text()

                        if text:

                            lines = text.split("\n")

                            for line in lines:
                                all_rows.append([line])

                            print(f"Extracted {len(lines)} text lines")

                        else:
                            print("No text found.")

                except Exception as e:
                    print(f"Error on page {page_number + 1}: {e}")

        print(f"\nTotal extracted rows: {len(all_rows)}")

        if len(all_rows) > 0:

            df = pd.DataFrame(all_rows)

            output_file = OUTPUT_FOLDER / f"{pdf_file.stem}.csv"

            df.to_csv(output_file, index=False)

            print(f"Saved CSV: {output_file}")

        else:

            print("No data extracted from this PDF.")

    except Exception as e:

        print(f"FAILED: {pdf_file.name}")
        print(e)

print("\nALL EXTRACTIONS COMPLETED")
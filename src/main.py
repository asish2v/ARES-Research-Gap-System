import os
import json
from pypdf import PdfReader

# ==============================
# CONFIGURATION
# ==============================

PDF_FOLDER = "data/pdfs"
TEXT_OUTPUT_FOLDER = "data/text"
METADATA_OUTPUT_FOLDER = "data/metadata"

# Ensure output folders exist
os.makedirs(TEXT_OUTPUT_FOLDER, exist_ok=True)
os.makedirs(METADATA_OUTPUT_FOLDER, exist_ok=True)

# ==============================
# HELPER FUNCTIONS
# ==============================

def get_all_pdf_files(folder):
    return [
        os.path.join(folder, f)
        for f in os.listdir(folder)
        if f.lower().endswith(".pdf")
    ]


def extract_full_text(pdf_path):
    reader = PdfReader(pdf_path)
    all_text = ""

    for i, page in enumerate(reader.pages):
        text = page.extract_text()
        if text:
            all_text += f"\n\n--- Page {i + 1} ---\n"
            all_text += text

    return all_text


def extract_metadata(text):
    lines = text.splitlines()

    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("--- Page"):
            continue
        clean_lines.append(line)

    title = clean_lines[0] if clean_lines else "UNKNOWN"

    authors = []
    for i in range(1, min(6, len(clean_lines))):
        if "abstract" in clean_lines[i].lower():
            break
        authors.append(clean_lines[i])

    return title, authors


def extract_abstract(text):
    lines = text.splitlines()
    abstract_lines = []
    inside_abstract = False

    for line in lines:
        line = line.strip()
        if not line:
            continue

        if line.lower().startswith("abstract"):
            inside_abstract = True
            continue

        if inside_abstract and (
            line.lower().startswith("keywords")
            or line.lower().startswith("index terms")
            or line.lower().startswith("introduction")
        ):
            break

        if inside_abstract:
            abstract_lines.append(line)

    return " ".join(abstract_lines)


# ==============================
# MAIN PIPELINE
# ==============================

def main():
    pdf_files = get_all_pdf_files(PDF_FOLDER)

    print(f"Found {len(pdf_files)} PDF file(s)")

    for pdf_path in pdf_files:
        paper_name = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"\nProcessing: {paper_name}")

        # Extract text
        full_text = extract_full_text(pdf_path)

        text_path = os.path.join(TEXT_OUTPUT_FOLDER, f"{paper_name}.txt")
        with open(text_path, "w", encoding="utf-8") as f:
            f.write(full_text)

        print(f"Text saved: {text_path}")

        # Metadata extraction
        title, authors = extract_metadata(full_text)
        abstract = extract_abstract(full_text)

        metadata = {
            "title": title,
            "authors": authors,
            "abstract": abstract,
            "source_file": os.path.basename(pdf_path)
        }

        metadata_path = os.path.join(
            METADATA_OUTPUT_FOLDER,
            f"{paper_name}_metadata.json"
        )

        with open(metadata_path, "w", encoding="utf-8") as f:
            json.dump(metadata, f, indent=4)

        print(f"Metadata saved: {metadata_path}")

    print("\nPIPELINE COMPLETED SUCCESSFULLY")


# ==============================
# ENTRY POINT
# ==============================

if __name__ == "__main__":
    main()

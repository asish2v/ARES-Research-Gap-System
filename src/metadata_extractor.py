# metadata_extractor.py

def load_paper_text(file_path):
    """
    Load extracted research paper text from a .txt file
    """
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()
    return text
def extract_basic_metadata(text):
    """
    Improved metadata extraction:
    - Skips page markers
    - Detects title and author block
    """

    lines = text.splitlines()

    # Clean lines: remove empty & page markers
    clean_lines = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith("--- Page"):
            continue
        clean_lines.append(line)

    # Title is usually the first meaningful line
    title = clean_lines[0] if clean_lines else "UNKNOWN"

    # Authors usually come immediately after title
    authors = []

    for i in range(1, min(6, len(clean_lines))):
        if "Abstract" in clean_lines[i]:
            break
        authors.append(clean_lines[i])

    return {
        "title": title,
        "authors": authors
    }


def extract_abstract(text):
    """
    Extract abstract section from research paper text
    """

    lines = text.splitlines()
    abstract_lines = []

    inside_abstract = False

    for line in lines:
        line = line.strip()

        if not line:
            continue

        # Start of abstract
        if line.lower().startswith("abstract"):
            inside_abstract = True
            continue

        # End of abstract (common patterns)
        if inside_abstract and (
            line.lower().startswith("keywords") or
            line.lower().startswith("index terms") or
            line.lower().startswith("introduction")
        ):
            break

        if inside_abstract:
            abstract_lines.append(line)

    return " ".join(abstract_lines)

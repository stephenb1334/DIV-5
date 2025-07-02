import os
import re
from pypdf import PdfReader
import email
from email import policy
from email.parser import BytesParser

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    try:
        reader = PdfReader(pdf_path)
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        print(f"Error extracting text from PDF {pdf_path}: {e}")
    return text

def extract_text_from_email(email_path):
    """Extracts text from an .eml email file."""
    text = ""
    try:
        with open(email_path, 'rb') as fp:
            msg = BytesParser(policy=policy.default).parse(fp)

        # Extract headers
        text += f"From: {msg['from']}\n" if msg['from'] else ""
        text += f"To: {msg['to']}\n" if msg['to'] else ""
        text += f"Subject: {msg['subject']}\n" if msg['subject'] else ""
        text += f"Date: {msg['date']}\n\n" if msg['date'] else ""

        # Extract body
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                cdisp = part.get('Content-Disposition')

                # Look for plain text parts, ignoring attachments
                if ctype == 'text/plain' and not cdisp:
                    try:
                        text += part.get_payload(decode=True).decode(part.get_content_charset() or 'utf-8') + "\n"
                    except UnicodeDecodeError:
                        text += part.get_payload(decode=True).decode('latin-1', errors='ignore') + "\n"
                elif ctype == 'text/html' and not cdisp:
                    # Optionally, you can try to convert HTML to text, but for V1, plain text is sufficient.
                    # For now, we'll just skip HTML if plain text is also present.
                    pass
        else:
            ctype = msg.get_content_type()
            if ctype == 'text/plain':
                try:
                    text += msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8') + "\n"
                except UnicodeDecodeError:
                    text += msg.get_payload(decode=True).decode('latin-1', errors='ignore') + "\n"
            elif ctype == 'text/html':
                # You might want to use a library like BeautifulSoup to parse HTML and extract text
                # For V1, we'll just get the raw HTML if no plain text alternative exists.
                text += msg.get_payload(decode=True).decode(msg.get_content_charset() or 'utf-8', errors='ignore') + "\n"

    except Exception as e:
        print(f"Error extracting text from email {email_path}: {e}")
    return text

def process_files_for_text_extraction(root_dir, output_dir):
    """
    Walks through the root_dir, extracts text from supported files,
    and saves them to the output_dir, preserving the directory structure.
    """
    os.makedirs(output_dir, exist_ok=True)
    print(f"Starting text extraction from '{root_dir}' to '{output_dir}'...")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        # Skip the output directory itself to prevent infinite loops
        if output_dir in dirpath:
            continue

        relative_path = os.path.relpath(dirpath, root_dir)
        current_output_dir = os.path.join(output_dir, relative_path)
        os.makedirs(current_output_dir, exist_ok=True)

        for filename in filenames:
            file_path = os.path.join(dirpath, filename)
            file_name_without_ext, file_ext = os.path.splitext(filename)
            extracted_text = ""

            if file_ext.lower() == '.pdf':
                print(f"  Extracting text from PDF: {filename}")
                extracted_text = extract_text_from_pdf(file_path)
            elif file_ext.lower() == '.eml':
                print(f"  Extracting text from Email: {filename}")
                extracted_text = extract_text_from_email(file_path)
            elif file_ext.lower() in ['.txt', '.md', '.rtf', '.docx', '.doc', '.pages']:
                # For V1, we'll just copy text files directly.
                # For .docx, .doc, .pages, you'd need additional libraries (e.g., python-docx, textract)
                # For now, we'll just note them and suggest manual conversion or future library integration.
                print(f"  Skipping (or manual conversion needed for) {filename} (type: {file_ext}).")
                continue # Skip for now, focus on PDF/EML
            else:
                print(f"  Skipping unsupported file type: {filename}")
                continue

            if extracted_text:
                output_file_path = os.path.join(current_output_dir, file_name_without_ext + '.txt')
                with open(output_file_path, 'w', encoding='utf-8') as f:
                    f.write(extracted_text)
                print(f"    Saved extracted text to: {output_file_path}")
    print("Text extraction complete.")

def search_extracted_text(extracted_text_dir, keyword):
    """
    Searches for a keyword in all .txt files within the extracted_text_dir.
    Returns a list of file paths where the keyword was found.
    """
    found_files = []
    print(f"\nSearching for '{keyword}' in extracted text files...")
    for dirpath, _, filenames in os.walk(extracted_text_dir):
        for filename in filenames:
            if filename.endswith('.txt'):
                file_path = os.path.join(dirpath, filename)
                try:
                    with open(file_path, 'r', encoding='utf-8') as f:
                        content = f.read()
                        if re.search(r'\b' + re.escape(keyword) + r'\b', content, re.IGNORECASE):
                            found_files.append(file_path)
                            print(f"  Found in: {file_path}")
                except Exception as e:
                    print(f"Error reading file {file_path}: {e}")
    if not found_files:
        print(f"No files found containing '{keyword}'.")
    return found_files

# --- Main execution ---
if __name__ == "__main__":
    # Define your base directory (DIV-5)
    BASE_DIR = "/Users/homebase/Desktop/1R-MASTER/DIV-5"
    SOURCE_DOCS_DIR = BASE_DIR # We want to process all files within DIV-5
    EXTRACTED_TEXT_DIR = os.path.join(BASE_DIR, "_extracted_text")

    # 1. Run text extraction
    process_files_for_text_extraction(SOURCE_DOCS_DIR, EXTRACTED_TEXT_DIR)

    # 2. Run a search query
    search_term = input("\nEnter a keyword to search for (e.g., 'alimony', 'discovery', 'custody'): ")
    if search_term:
        search_results = search_extracted_text(EXTRACTED_TEXT_DIR, search_term)
        print("\n--- Search Results ---")
        if search_results:
            for result in search_results:
                print(result)
        else:
            print("No matching documents found.")
    else:
        print("No search term entered. Exiting search.")
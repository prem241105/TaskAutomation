"""CodeAlpha Task 3: Task Automation with Python Scripts
Choose one small automation:
1. Move JPG/JPEG images from a source folder to a destination folder.
2. Extract email addresses from a text file and save them to another file.
3. Fetch and save the title of a webpage.

The first two features use only the Python standard library.
Webpage title extraction requires the optional 'requests' package.
"""

import os
import re
import shutil
from pathlib import Path
from html.parser import HTMLParser


class TitleParser(HTMLParser):
    """Minimal HTML parser that collects text inside the <title> element."""
    def __init__(self):
        super().__init__()
        self.in_title = False
        self.parts = []

    def handle_starttag(self, tag, attrs):
        if tag.lower() == "title":
            self.in_title = True

    def handle_endtag(self, tag):
        if tag.lower() == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.parts.append(data.strip())

    @property
    def title(self):
        return " ".join(part for part in self.parts if part).strip()


def move_jpg_files():
    source_text = input("Source folder path: ").strip().strip('"')
    destination_text = input("Destination folder path: ").strip().strip('"')
    source = Path(source_text).expanduser()
    destination = Path(destination_text).expanduser()

    if not source.is_dir():
        print("Error: source folder does not exist.")
        return
    if source.resolve() == destination.resolve():
        print("Error: source and destination folders must be different.")
        return

    destination.mkdir(parents=True, exist_ok=True)
    moved = 0
    for item in source.iterdir():
        if item.is_file() and item.suffix.lower() in {".jpg", ".jpeg"}:
            target = destination / item.name
            if target.exists():
                print(f"Skipped (destination already has this file): {item.name}")
                continue
            shutil.move(str(item), str(target))
            print(f"Moved: {item.name}")
            moved += 1
    print(f"Done. Moved {moved} image(s).")


def extract_emails():
    input_text = input("Path to input .txt file: ").strip().strip('"')
    output_text = input("Path for output file (e.g. emails_found.txt): ").strip().strip('"')
    input_path = Path(input_text).expanduser()
    output_path = Path(output_text).expanduser()

    if not input_path.is_file():
        print("Error: input file does not exist.")
        return

    content = input_path.read_text(encoding="utf-8", errors="replace")
    pattern = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"
    emails = sorted(set(re.findall(pattern, content, flags=re.IGNORECASE)))

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text("\n".join(emails) + ("\n" if emails else ""), encoding="utf-8")
    print(f"Found {len(emails)} unique email address(es). Saved to {output_path.resolve()}")


def scrape_title():
    url = input("Webpage URL (include https://): ").strip()
    if not url.startswith(("https://", "http://")):
        print("Please enter a URL beginning with http:// or https://")
        return

    try:
        import requests
    except ImportError:
        print("The optional 'requests' package is not installed.")
        print("Install it with: python -m pip install requests")
        return

    try:
        response = requests.get(
            url,
            timeout=15,
            headers={"User-Agent": "CodeAlphaTaskAutomation/1.0"}
        )
        response.raise_for_status()
        parser = TitleParser()
        parser.feed(response.text)
        title = parser.title or "(No page title found)"
        output_path = Path("webpage_title.txt")
        output_path.write_text(
            f"URL: {url}\nTitle: {title}\n",
            encoding="utf-8"
        )
        print(f"Page title: {title}")
        print(f"Saved to: {output_path.resolve()}")
    except requests.RequestException as exc:
        print(f"Could not fetch the webpage: {exc}")


def main():
    while True:
        print("\n" + "=" * 48)
        print("        PYTHON TASK AUTOMATION TOOL")
        print("=" * 48)
        print("1. Move JPG/JPEG files to another folder")
        print("2. Extract email addresses from a text file")
        print("3. Fetch a webpage title")
        print("0. Exit")
        choice = input("Choose an option: ").strip()

        if choice == "1":
            move_jpg_files()
        elif choice == "2":
            extract_emails()
        elif choice == "3":
            scrape_title()
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid option. Choose 0, 1, 2, or 3.")


if __name__ == "__main__":
    main()

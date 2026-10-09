# CodeAlpha Task 3 — Task Automation with Python Scripts

## What it does
This menu-driven program includes three small automation choices:
1. Move `.jpg` and `.jpeg` files from a source folder to a destination folder.
2. Extract unique email addresses from a `.txt` file and save them to another file.
3. Fetch a webpage and save its title in `webpage_title.txt`.

The PDF asks interns to choose one automation idea; this project includes all three options in one small tool.

## Requirements
- Python 3.9 or newer
- Standard library for options 1 and 2
- `requests` package for option 3

## Run
```bash
python main.py
```

To enable webpage title extraction:
```bash
python -m pip install -r requirements.txt
```

## Safety notes
- Try the file-moving feature on a test folder first.
- The program skips files when a same-named file already exists in the destination.
- Only run the email extractor on files you are authorized to process.
- Webpage access depends on network connectivity and the site's terms/access controls.

# TaskAutomation

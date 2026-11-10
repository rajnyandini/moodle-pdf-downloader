# Moodle PDF Downloader

A Python-based browser automation tool that downloads PDF resources from Moodle courses using an authenticated browser session.

Built with Python and Playwright, this project automates the repetitive process of opening individual course resources and saving their PDF files locally.

## Features

- Authenticated browser access through Playwright
- Supports Moodle resource links and PDF resources
- Automatically identifies PDF responses
- Preserves original filenames where available
- Validates downloaded files using PDF signatures
- Prevents accidental overwriting of duplicate filenames
- Saves downloaded documents into a dedicated folder

## Tech Stack

- Python
- Playwright
- Chromium
- JavaScript Fetch API

## Installation

Clone the repository:

```bash
git clone https://github.com/YOUR_USERNAME/moodle-pdf-downloader.git
cd moodle-pdf-downloader
```

Install dependencies:

```bash
pip install -r requirements.txt
python -m playwright install chromium
```

## Usage

1. Run the script:

```bash
python download_vit_pdfs.py
```

2. Log in to your Moodle account in the browser window.
3. Navigate to your desired course.
4. Expand the course sections containing resources.
5. Return to the terminal and press Enter.
6. The script identifies and downloads accessible PDF resources.

Downloaded files are stored in a dedicated output folder.

## How It Works

1. Playwright launches a Chromium browser.
2. The user authenticates manually through the Moodle login page.
3. The script collects resource URLs from the course page.
4. Browser-authenticated requests retrieve the actual PDF content.
5. The script validates the PDF signature before saving.
6. Files are stored locally using their original filenames.

## Limitations

- Designed for Moodle course pages.
- Requires valid access to the course.
- Does not bypass authentication, CAPTCHA or access restrictions.
- Currently collects resources linked from the course page; nested folders and additional pages may require further exploration.
- Some Moodle configurations may require modifications.

## Security & Responsible Use

- No passwords or session cookies are stored by the script.
- Authentication is performed manually.
- Only download materials you are authorized to access.
- Respect your institution's policies and copyright restrictions.
- Do not redistribute downloaded course materials without permission.

## License

MIT License
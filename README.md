# Project 04: Web Scraper for Headlines & Quotes

A beginner-friendly Python web scraper based on the supplied InternCircle Project 04 learner guide.

## Source selected

**https://quotes.toscrape.com/**

The learner guide identifies this as a practice website built for scraping and recommends it for the main exercise. This project uses only that public practice site; it does not scrape login-protected pages or collect personal data.

## Features

- Sends HTTP GET requests with the `requests` library.
- Uses a descriptive `User-Agent` and a 10-second timeout.
- Checks HTTP errors with `raise_for_status()`.
- Parses HTML with BeautifulSoup.
- Uses CSS selectors to extract each quote's text, author, and tags.
- Follows the Next link across pages, stopping when it disappears.
- Waits one second between requests to avoid overloading the site.
- Checks for missing HTML elements before extracting text.
- Handles request and file-saving errors.
- Saves results to `quotes.json` and readable `quotes.txt`.
- Prints the number of quotes, most quoted author, and most common tag.

## Project files

```text
Project-04-Web-Scraper-Headlines-Quotes/
├── scraper.py
├── requirements.txt
└── README.md
```

The `quotes.json` and `quotes.txt` output files are created automatically when you run the scraper.

## Requirements

- Python 3.10 or newer
- VS Code
- Internet connection
- `requests`
- `beautifulsoup4`

## Setup and run in VS Code

1. Extract the ZIP file.
2. Open the extracted project folder in VS Code.
3. Open **Terminal → New Terminal**.
4. (Recommended) Create a virtual environment:

   ```bash
   python -m venv .venv
   ```

5. Activate it on Windows:

   ```bash
   .venv\Scripts\activate
   ```

   If PowerShell blocks activation, you can still run the next commands using `python -m pip`, or use Command Prompt.

6. Install the dependencies:

   ```bash
   python -m pip install -r requirements.txt
   ```

7. Run the scraper:

   ```bash
   python scraper.py
   ```

   If `python` does not work on Windows, try `py scraper.py`.

## Output

After a successful run, the project folder contains:

- `quotes.json` — structured records with `text`, `author`, and `tags`.
- `quotes.txt` — the same records in a readable text format.

The terminal also prints how many pages and quotes were collected, the most quoted author, and the most common tag. The exact results may change if the source website changes.

## Politeness and safety rules

- Use only the practice source named in the learner guide.
- Send a descriptive User-Agent header.
- Set a request timeout.
- Wait one second between page requests.
- Do not scrape personal data or pages behind a login.
- Do not increase request frequency or repeatedly run the scraper unnecessarily.

## Troubleshooting

- **`ModuleNotFoundError`**: Run `python -m pip install -r requirements.txt`.
- **Connection or timeout error**: Check your internet connection and try again later.
- **HTTP error**: The practice website may be temporarily unavailable; try again later.
- **No output files**: Check that the terminal has permission to write in the project folder.

## Submission checklist from the learner guide

- [ ] Upload the code and README to GitHub.
- [ ] Include `quotes.json` (or the first 20 records) after running the scraper.
- [ ] Include a short note explaining the source selected and why it is allowed.

## Example source note for submission

I selected `quotes.toscrape.com` because the InternCircle Project 04 learner guide specifically identifies it as a practice website that is safe and allowed for the main scraping exercise. The scraper uses a timeout, a descriptive User-Agent, and a one-second delay between page requests. It only extracts the displayed quote text, author, and tags.

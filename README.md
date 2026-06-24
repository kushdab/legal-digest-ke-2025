# Legal-Digest-KE-2025

An AI-powered tool designed to parse the **Kenya Gazette**, extract legal notices, and summarize them into business-ready compliance briefs.

## Features
- **PDF Parsing**: Uses `pdfplumber` to extract structured text from official Gazette PDFs.
- **NLP Summarization**: Leverages the `facebook/bart-large-cnn` transformer model to condense complex legal jargon.
- **Business Categorization**: Automatically tags notices under Tax, Land, Licensing, or Liquidation.
- **Actionable Insights**: Highlights notices requiring immediate corporate action.

## Installation
1. Clone the repository.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place the PDF you wish to analyze in the root folder and rename it to `gazette.pdf`.

## Usage
Run the summarizer:
```bash
python summarizer.py
```

## Project Structure
- `summarizer.py`: Core logic for NLP and PDF extraction.
- `requirements.txt`: Python dependencies.
- `.gitignore`: Standard exclusions.
import os
import re
import pdfplumber
from transformers import pipeline
import json

class LegalDigestKE:
    def __init__(self):
        print("[*] Initializing NLP Engine (BART Large)...")
        # Using a reliable summarization pipeline
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.categories = {
            "Taxation": ["tax", "duty", "kra", "excise", "vat"],
            "Land": ["land", "title", "plot", "lease", "registration"],
            "Licensing": ["license", "permit", "authority", "board", "regulatory"],
            "Liquidation": ["winding up", "insolvency", "liquidator", "bankrupt"]
        }

    def extract_text_from_gazette(self, pdf_path):
        """Extracts raw text from PDF file."""
        print(f"[*] Extracting text from {pdf_path}...")
        full_text = ""
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages[:10]:  # Limiting to 10 pages for demo performance
                full_text += page.extract_text() + "\n"
        return full_text

    def segment_notices(self, text):
        """Splits gazette text into individual notices based on typical Kenyan formatting."""
        # Kenyan gazettes often use 'GAZETTE NOTICE NO.' as a delimiter
        notices = re.split(r'(?i)GAZETTE\s+NOTICE\s+NO\.', text)
        return [n.strip() for n in notices if len(n.strip()) > 100]

    def classify_notice(self, text):
        """Simple keyword-based classification for business relevance."""
        text_lower = text.lower()
        for category, keywords in self.categories.items():
            if any(kw in text_lower for kw in keywords):
                return category
        return "General"

    def generate_brief(self, pdf_path):
        """Main pipeline to generate the business brief."""
        raw_text = self.extract_text_from_gazette(pdf_path)
        segments = self.segment_notices(raw_text)
        
        briefs = []
        print(f"[*] Found {len(segments)} potential notices. Summarizing top relevant notices...")

        for i, notice in enumerate(segments[:5]):  # Process top 5 for speed
            category = self.classify_notice(notice)
            
            # NLP Summarization (handling token limits)
            input_text = notice[:1024] 
            summary = self.summarizer(input_text, max_length=60, min_length=20, do_sample=False)
            
            briefs.append({
                "notice_id": i + 1,
                "category": category,
                "summary": summary[0]['summary_text'],
                "actionable": "Review for compliance" if category != "General" else "Informational"
            })

        return briefs

if __name__ == "__main__":
    # Example usage
    # Ensure you have a 'gazette.pdf' in the root directory
    digest = LegalDigestKE()
    
    # Create a dummy run or point to a real PDF
    try:
        results = digest.generate_brief("gazette.pdf")
        print(json.dumps(results, indent=4))
    except FileNotFoundError:
        print("[!] Error: Please place a 'gazette.pdf' file in the directory to run analysis.")
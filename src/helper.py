import fitz # pymupdf
import os
from dotenv import load_dotenv
from apify_client import ApifyClient
from openai import OpenAI


   
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
APIFY_API_TOKEN = os.getenv("APIFY_API_TOKEN")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY
client=OpenAI(api_key==OPENAI_API_KEY)
apify_client = ApifyClient(APIFY_API_TOKEN)

def extract_text_from_pdf(uploaded_file):
    """Extract text from a PDF file using PyMuPDF."""
    try:
        doc = fitz.open(stream=uploaded_file.read(), filetype="pdf")
        text = ""
        for page in doc:
            text += page.get_text()
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
    return text

def ask_openai(prompt,model="gpt-4o",temperature=0.5,max_tokens=500):
    """Send a prompt to OpenAI's API and return the response."""
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "user", "content": prompt}
            ],
            temperature=temperature,max_tokens=max_tokens
        )
        answer = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error communicating with OpenAI: {e}")
        answer = ""
    return answer

def fetch_linkedin_jobs(query,location,limit=60):
    """Fetch job listings from LinkedIn using Apify's LinkedIn Job Scraper."""

    run_input = {
        "title": query, # keyword for the job search
        "location": location,
        "rows": limit,
        "proxy": {
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"],
        },
    }

    # Run the Actor and wait for it to finish
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)

    # Fetch and print Actor results from the run's dataset (if there are any)
    jobs= list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs


def fetch_naukri_jobs(query,location,limit=60):
    run_input = {
        "searchUrls": ["https://www.naukri.com/it-jobs"],
        "maxItems": limit,
        "proxyConfiguration": { "useApifyProxy": False },
        "keywords": query,
        "maxJobs": limit,
        "freshness": "all",
        "sortBy": "relevance",
        "experience": "all"
    }
    run = apify_client.actor("wsrn5gy5C4EDeYCcD").call(run_input=run_input)
    jobs= list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs
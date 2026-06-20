import json
import os
import requests
from datetime import datetime

GROQ_API_KEY = os.environ["GROQ_API_KEY"]
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"

PROFILE = os.environ["CANDIDATE_PROFILE"]

JOB_SITES = [
    "LinkedIn Jobs - machine learning engineer Zurich",
    "ETH Zürich Career Center - eth-gethired.ch",
    "Wellfound (AngelList) - ML engineer Zurich/EU",
    "Google Careers - machine learning Zurich",
    "DeepMind Careers - research engineer",
    "Mistral AI Jobs - research engineer",
    "OpenAI Careers - ML engineer EU",
    "Anthropic Careers - research engineer",
    "Indeed Switzerland - machine learning Zurich",
    "Jobs.ch - machine learning Switzerland",
]

def call_groq(prompt):
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": "llama-3.3-70b-versatile",
        "messages": [{"role": "user", "content": prompt}],
        "temperature": 0.7,
        "max_tokens": 4096
    }
    r = requests.post(GROQ_URL, json=body, headers=headers, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["choices"][0]["message"]["content"]

def fetch_jobs():
    prompt = f"""You are a job search agent for a highly qualified candidate. Here is their profile:

{PROFILE}

Based on your knowledge of the job market in late 2025, generate 8 realistic and plausible job listings that match this candidate well. Draw from these types of sources:
{chr(10).join(f'- {s}' for s in JOB_SITES)}

Return ONLY a valid JSON array. No markdown, no backticks, no explanation. Each object must have exactly:
{{
  "id": number,
  "title": string,
  "company": string (well-known reputable companies only),
  "location": string,
  "salary": string (realistic estimate),
  "source": string (which site type),
  "url": string (real company careers page URL),
  "posted": string (e.g. "2 days ago"),
  "tags": array of 3-5 short strings,
  "score": number 1-5 (how well ALL criteria match),
  "scoreLabel": string (one of: "Perfect Match", "Strong Match", "Good Match", "Partial Match", "Weak Match"),
  "scoreColor": string (hex: #22c55e for 5, #3b82f6 for 4, #f59e0b for 3, #ef4444 for 1-2),
  "reasoning": string (2-3 sentences why included, written like a smart friend advising),
  "mismatches": array of strings (criteria that don't fully match, empty if perfect)
}}

Score strictly:
- 5 = all criteria match perfectly (location, salary, company quality, role fit)
- 4 = one minor mismatch
- 3 = one notable mismatch
- 2 = two mismatches
- 1 = included for completeness only

Return only the JSON array."""

    text = call_groq(prompt)
    # Strip any accidental markdown
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    return json.loads(text)

def main():
    print("Fetching jobs via Groq...")
    jobs = fetch_jobs()
    print(f"Got {len(jobs)} jobs")

    output = {
        "jobs": jobs,
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
        "totalSites": len(JOB_SITES),
    }

    os.makedirs("docs", exist_ok=True)
    with open("docs/jobs.json", "w") as f:
        json.dump(output, f, indent=2)
    print("Saved to docs/jobs.json")

if __name__ == "__main__":
    main()

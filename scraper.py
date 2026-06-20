import json
import os
import requests
from datetime import datetime

GEMINI_API_KEY = os.environ["GEMINI_API_KEY"]
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

PROFILE = {
    "background": "ETH Zurich Master's in Computer Science, major in Secure & Reliable Systems. Master's thesis on grounding LLMs. Strong analytical thinking. Graduating September 2025.",
    "interests": "AI/ML engineering, LLM research, backend/systems engineering, data science, software engineering at reputable tech companies. Open to roles adjacent to cybersecurity if they involve AI/ML.",
    "locations": "Zurich (preferred), Madrid, other major EU cities, Latin America (Buenos Aires, São Paulo, Mexico City). EU citizen + Swiss work eligible.",
    "salary": "Minimum 7,000 CHF/month gross (or equivalent: ~7,500 EUR for Zurich, ~3,500 EUR for Madrid/EU).",
    "dealbreakers": "Consulting/body-shopping firms. Pure cybersecurity with no AI component. Companies with poor public image. Salary below threshold.",
    "companyQuality": "Well-known, reputable, innovative. Top tech firms, well-funded AI startups, leading research labs, prestigious finance/tech companies.",
    "startDate": "Available from November 2025 (taking at least 1 month vacation after September graduation).",
}

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

def call_gemini(prompt):
    body = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.7, "maxOutputTokens": 8192}
    }
    r = requests.post(GEMINI_URL, json=body, timeout=60)
    r.raise_for_status()
    data = r.json()
    return data["candidates"][0]["content"]["parts"][0]["text"]

def fetch_jobs():
    prompt = f"""You are a job search agent for a highly qualified candidate. Here is their profile:

{json.dumps(PROFILE, indent=2)}

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

    text = call_gemini(prompt)
    # Strip any accidental markdown
    text = text.strip()
    if text.startswith("```"):
        text = text.split("```")[1]
        if text.startswith("json"):
            text = text[4:]
    text = text.strip()
    return json.loads(text)

def main():
    print("Fetching jobs via Gemini...")
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

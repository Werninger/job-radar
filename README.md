# Job Radar 📡

A personal job tracking dashboard that automatically scans top tech job sites twice a day and uses AI to filter and rank listings based on custom criteria.

## How it works

A GitHub Actions workflow runs twice a day (CET timezone). It calls an LLM to generate and rank relevant job listings, saves them to `docs/jobs.json`, and deploys the result to GitHub Pages.

## Stack

- **Python** — scraper & AI filtering
- **Groq API** — LLM inference (Llama 3.3 70B)
- **GitHub Actions** — scheduling & automation
- **GitHub Pages** — free static hosting

## Sources monitored

- LinkedIn Jobs
- ETH Zürich Career Center
- Wellfound (AngelList)
- Google / DeepMind Careers
- Mistral AI / OpenAI / Anthropic Careers
- Indeed Switzerland
- Jobs.ch

## Setup

1. Fork this repo
2. Add your secrets under **Settings → Secrets → Actions**:
   - `GROQ_API_KEY` — from [console.groq.com](https://console.groq.com)
   - `CANDIDATE_PROFILE` — your profile as a JSON string
3. Enable GitHub Pages (source: GitHub Actions)
4. Trigger the first run manually under the **Actions** tab

## License

MIT License — feel free to fork and adapt for your own job search. No attribution required.

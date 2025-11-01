# Viral Russia News - Automated Daily Workflow

## Overview

This project automatically collects, analyzes, translates, and publishes the top 15 viral news stories from major Russian media outlets. The workflow now includes **automatic AI-powered enhancement** of all stories with comprehensive bilingual summaries.

## Features

✅ **Automated Data Collection** - Scrapes 6 major Russian news outlets  
✅ **Viral Score Calculation** - Ranks stories by prominence, recency, and topic relevance  
✅ **AI-Powered Translation** - Translates all titles to English using OpenAI GPT-4.1-mini  
✅ **Comprehensive Summaries** - Generates 2-3 sentence summaries in both English and Russian  
✅ **Trending Analysis** - Explains why each story is trending  
✅ **Automatic Deployment** - Pushes to GitHub → Netlify automatically deploys

## Data Sources

The workflow collects news from these 6 major Russian media outlets:

1. **RT Russian** (russian.rt.com)
2. **TASS** (tass.ru)
3. **RIA Novosti** (ria.ru)
4. **Rossiyskaya Gazeta** (rg.ru)
5. **Komsomolskaya Pravda** (kp.ru)
6. **Lenta.ru** (lenta.ru)

## Workflow Steps

### 1. Data Collection (Manual/Browser-based)
- Visit each of the 6 news outlets
- Extract top stories with titles, prominence, timestamps, and categories
- Save to `data/[outlet]_stories.txt`

### 2. Analysis & AI Enhancement (Automated)
Run the integrated analysis script:

```bash
cd /home/ubuntu/viral-russia-news
python3 analyze_stories.py
```

This single command will:
1. Read all collected stories from `data/*.txt` files
2. Calculate viral scores based on prominence, recency, and topic
3. Select top 15 stories
4. **Automatically enhance each story with AI:**
   - Translate title to English
   - Generate comprehensive English summary
   - Generate comprehensive Russian summary
   - Create "Why Trending" explanation
5. Create the final `public/viral_russia_news.json` file for the website
6. Save raw analysis results to `data/viral_stories.json`

### 3. Deployment (Automated)
After running the analysis script, commit and push the changes to GitHub:

```bash
cd /home/ubuntu/viral-russia-news
git add public/viral_russia_news.json data/viral_stories.json
git commit -m "Daily update - [Date]"
git push origin main
```

Netlify will automatically detect the push and deploy the updated website.

## Technical Details

### Main Script
- `analyze_stories.py`: The core script that orchestrates the entire automated workflow.

### AI Integration
- **Model:** OpenAI GPT-4.1-mini
- **API Calls:** 4 per story (title, summary EN, summary RU, why trending)
- **Total API Calls:** 60 per run (15 stories × 4 calls)

### Output Files
- `public/viral_russia_news.json`: Final JSON file for the website with all enhanced data
- `data/viral_stories.json`: Raw analysis results with viral scores

## Future Improvements

- **Fully Automated Collection:** The manual browser-based collection in Step 1 could be automated with a web scraping library like BeautifulSoup or Playwright.
- **Error Handling:** Add more robust error handling for API calls and file I/O.
- **CI/CD Integration:** Use GitHub Actions to run the `analyze_stories.py` script automatically on a daily schedule.

## Conclusion

The Viral Russia News workflow is now fully automated from analysis to deployment. Running a single script (`analyze_stories.py`) and pushing to GitHub is all that's needed to update the website with fresh, comprehensive, and bilingual news content every day.

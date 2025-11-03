# Troubleshooting Guide - Viral Russia News

## Issue: Site Not Updating Despite GitHub Push

### Root Causes Identified

1. **Filename Mismatch**
   - **Problem:** The `index.html` loads `viral_russia_news.json` but the script was generating `viral-news.json` (hyphen vs underscore)
   - **Solution:** Updated `generate_json.py` to use correct filename `viral_russia_news.json`

2. **JSON Structure Mismatch**
   - **Problem:** The `index.html` expects `jsonData.metadata` but script was generating `jsonData.meta`
   - **Expected Structure:**
     ```json
     {
       "metadata": {
         "generated_at": "2025-11-03T09:28:18.517747",
         "collection_period": "2025-11-03",
         "total_outlets": 6,
         "outlets": [
           {"name": "RT Russian", "url": "https://russian.rt.com/"},
           ...
         ]
       },
       "stories": [...]
     }
     ```
   - **Solution:** Updated `generate_json.py` to match expected structure

3. **Netlify Deployment**
   - **Problem:** Netlify does auto-deploy on GitHub push, but site shows cached version
   - **Cache Bust:** The site uses a cache bust parameter that may not update immediately
   - **Solution:** Netlify should rebuild within 1-3 minutes of push

### Verification Steps

1. **Check GitHub Repository**
   ```bash
   curl https://raw.githubusercontent.com/aroga2/viralrussianews/main/public/viral_russia_news.json | head -30
   ```

2. **Check Netlify CDN**
   ```bash
   curl https://viralrussianews.netlify.app/viral_russia_news.json | head -30
   ```

3. **Force Browser Refresh**
   - Use Ctrl+Shift+R (hard refresh)
   - Or add cache-busting parameter: `?v=$(date +%s)`

### Current Status

- ✅ GitHub repository updated with correct files
- ✅ JSON structure matches index.html expectations  
- ✅ Filename corrected to `viral_russia_news.json`
- ⏳ Waiting for Netlify to rebuild and deploy

### Manual Deployment Trigger

If automatic deployment fails, you can trigger manually:

1. Log into Netlify dashboard
2. Go to Deploys tab
3. Click "Trigger deploy" → "Deploy site"

### Daily Automation

The workflow should run automatically via scheduled task. If it fails:

1. Check the collection scripts are working
2. Verify GitHub credentials are valid
3. Ensure Netlify webhook is configured
4. Check for any API rate limits

### Key Files

- `public/viral_russia_news.json` - Main data file (MUST match this name)
- `public/index.html` - Frontend (expects specific JSON structure)
- `generate_json.py` - JSON generator (updated to match expectations)
- `analyze_stories.py` - Viral score calculator
- `run_daily_update.sh` - Automation script

### Common Errors

**"Error: Failed to load data"**
- JSON file not found or wrong filename
- JSON structure doesn't match expected format
- Network/CORS issues

**"No article found"**
- Empty stories array in JSON
- JavaScript error in loadData() function
- Browser caching old version

**Site shows old data**
- Netlify hasn't rebuilt yet (wait 2-3 minutes)
- Browser cache (hard refresh)
- CDN cache (may take up to 5 minutes)

---

**Last Updated:** November 3, 2025  
**Status:** Issues identified and fixed, awaiting Netlify deployment

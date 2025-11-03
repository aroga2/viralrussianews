# Quick Start Guide - Viral Russia News

## 🚀 Running the Workflow Manually

```bash
cd /home/ubuntu/viral-russia-news
./run_complete_workflow.sh
```

That's it! The script will:
- ✅ Analyze stories
- ✅ Calculate viral scores
- ✅ Generate JSON
- ✅ Validate structure
- ✅ Push to GitHub
- ✅ Trigger Netlify deployment

## 📊 Check Results

**Website:** https://viralrussianews.netlify.app/  
**JSON Data:** https://viralrussianews.netlify.app/viral_russia_news.json  
**GitHub:** https://github.com/aroga2/viralrussianews

## 🔍 Verify It's Working

The site should show:
- Generated date and time
- 6 monitored sources
- 15 ranked stories with:
  - Russian titles
  - Viral scores (0-100)
  - Categories
  - Timestamps
  - Source links

## ⏰ Automatic Schedule

**Runs daily at 6:00 AM UTC** (automatically scheduled)

No manual intervention needed!

## 📝 View Logs

```bash
ls -lt /home/ubuntu/viral-russia-news/logs/
cat /home/ubuntu/viral-russia-news/logs/workflow_*.log
```

## ❌ If Something Goes Wrong

1. **Check the log file** (most recent in logs/ directory)
2. **Verify JSON structure:**
   ```bash
   python3 generate_json.py
   ```
3. **Check GitHub status:**
   ```bash
   cd /home/ubuntu/viral-russia-news
   git status
   git log -1
   ```
4. **See full troubleshooting:** Read `TROUBLESHOOTING.md`

## 🔧 Key Files

- `run_complete_workflow.sh` - Main automation script
- `analyze_stories.py` - Viral score calculator
- `generate_json.py` - JSON generator with validation
- `public/viral_russia_news.json` - Output file (deployed)
- `public/index.html` - Website frontend

## 📚 Full Documentation

- `AUTOMATION_COMPLETE.md` - Complete automation guide
- `TROUBLESHOOTING.md` - Common issues and fixes
- `DEPLOYMENT_REPORT.md` - Initial setup details

---

**Status:** ✅ FULLY OPERATIONAL  
**Last Verified:** November 3, 2025

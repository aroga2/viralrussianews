import json

# Read the current JSON
with open('public/viral_russia_news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# English translations for each story
translations = {
    1: {
        "title_en": "What changes in laws from November 1, 2025: get rid of extra SIM cards and don't accumulate debts",
        "summary_en": "New laws taking effect in Russia from November 1, 2025, including restrictions on SIM card ownership and debt collection rules.",
        "why_trending_en": "This story is trending because new legislation directly affects millions of Russian citizens starting today."
    },
    2: {

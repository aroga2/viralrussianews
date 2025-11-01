#!/usr/bin/env python3
import json
from openai import OpenAI

# Initialize OpenAI client (API key is already in environment)
client = OpenAI()

# Read the JSON file
with open('public/viral_russia_news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Translating {len(data['stories'])} stories...")

# Translate each story
for i, story in enumerate(data['stories'], 1):
    print(f"Translating story {i}/{len(data['stories'])}...")
    
    # Get Russian title
    russian_title = story['title']
    
    # Translate title
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional translator. Translate the following Russian news headline to English. Provide only the translation, no explanations."},
            {"role": "user", "content": russian_title}
        ]
    )
    english_title = response.choices[0].message.content.strip()
    
    # Update story
    story['title_ru'] = russian_title
    story['title'] = english_title
    story['summary_ru'] = story.get('summary', russian_title)
    story['summary'] = f"Russian news story: {english_title}"
    story['why_trending'] = "This story is trending in Russian media due to its prominence and relevance."
    story['why_trending_ru'] = "Эта новость в тренде из-за её актуальности и важности."
    
    print(f"  RU: {russian_title[:60]}...")
    print(f"  EN: {english_title[:60]}...")

# Write updated JSON
with open('public/viral_russia_news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\nTranslation complete!")

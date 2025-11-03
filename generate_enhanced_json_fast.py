#!/usr/bin/env python3
"""
Fast enhanced JSON generator with batch translation
"""
import json
from datetime import datetime
from pathlib import Path
from openai import OpenAI

client = OpenAI()

def get_source_info():
    return [
        {"name": "RT Russian", "url": "https://russian.rt.com/"},
        {"name": "TASS", "url": "https://tass.ru/"},
        {"name": "RIA Novosti", "url": "https://ria.ru/"},
        {"name": "Rossiyskaya Gazeta", "url": "https://rg.ru/"},
        {"name": "Komsomolskaya Pravda", "url": "https://www.kp.ru/"},
        {"name": "Lenta.ru", "url": "https://lenta.ru/"},
    ]

def batch_translate_stories(stories):
    """Translate all stories in a single LLM call"""
    
    # Prepare batch request
    stories_text = ""
    for i, story in enumerate(stories, 1):
        stories_text += f"\n{i}. Title: {story['title']}\n   Category: {story.get('category', 'General')}\n   Source: {story.get('source', 'Unknown')}\n"
    
    prompt = f"""Translate these {len(stories)} Russian news headlines to English and provide brief summaries.

{stories_text}

For each story, provide:
1. English title (concise, news-style)
2. 2-3 sentence English summary explaining the story
3. 1-2 sentence explanation of why it's trending

Format as JSON array:
[
  {{
    "id": 1,
    "title_en": "...",
    "summary_en": "...",
    "why_trending_en": "..."
  }},
  ...
]"""

    try:
        print("Calling LLM for batch translation...")
        response = client.chat.completions.create(
            model="gpt-4.1-mini",
            messages=[
                {"role": "system", "content": "You are a professional news translator specializing in Russian media. Provide accurate, concise translations."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )
        
        result = json.loads(response.choices[0].message.content)
        # LLM returns translations in 'news' array
        translations = result.get('news', result.get('translations', []))
        print(f"✓ Received translations for {len(translations)} stories")
        return translations
    except Exception as e:
        print(f"Error in batch translation: {e}")
        return []

def generate_tags(title, category):
    tags = []
    title_lower = title.lower()

    if category == "Ukraine Conflict": tags.append("ukraine-conflict")
    if "трамп" in title_lower: tags.append("trump")
    if "путин" in title_lower: tags.append("putin")
    return tags[:3]

def main():
    data_dir = Path("/home/ubuntu/viral-russia-news/data")
    input_file = data_dir / "analyzed_stories.json"
    output_file = Path("/home/ubuntu/viral-russia-news/public/viral_russia_news.json")

    with open(input_file, "r", encoding="utf-8") as f:
        stories = json.load(f)

    translations = batch_translate_stories(stories)
    if not translations:
        print("No translations received, exiting.")
        return

    enhanced_stories = []
    for i, story in enumerate(stories):
        translation = next((t for t in translations if t["id"] == i + 1), None)
        if not translation:
            continue

        enhanced_story = {
            "rank": i + 1,
            "title": translation["title_en"],
            "title_ru": story["title"],
            "source": story["source"],
            "source_url": next((s["url"] for s in get_source_info() if s["name"] == story["source"]), ""),
            "time": story.get("time", "Recent"),
            "category": story.get("category", "General News"),
            "viral_score": story["viral_score"],
            "prominence": story.get("prominence", "main"),
            "summary": translation["summary_en"],
            "summary_ru": "",
            "why_trending": translation["why_trending_en"],
            "why_trending_ru": "",
            "tags": generate_tags(story["title"], story.get("category", "")),
            "outlets": [story["source"]],
            "outlet_count": 1,
            "date": datetime.utcnow().strftime("%Y-%m-%d"),
            "topic": story.get("category", "General News").replace(" ", "_").lower(),
            "vk_engagement": "moderate"
        }
        enhanced_stories.append(enhanced_story)

    enhanced_data = {
        "metadata": {
            "generated_at": datetime.utcnow().isoformat(),
            "collection_period": datetime.utcnow().strftime("%Y-%m-%d"),
            "total_outlets": 6,
            "outlets": get_source_info()
        },
        "stories": enhanced_stories
    }

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(enhanced_data, f, ensure_ascii=False, indent=2)

    print(f"\n✓ Enhanced JSON generated: {output_file}")

if __name__ == "__main__":
    main()

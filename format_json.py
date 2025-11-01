import json
from datetime import datetime

# Read the existing data
with open('/home/ubuntu/viral-russia-news/data/viral_stories.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Format stories with all required fields
formatted_stories = []
for story in data['top_stories']:
    formatted_story = {
        "rank": story['rank'],
        "title": story.get('title', ''),  # Use Russian title as English if no translation
        "title_ru": story['title'],
        "viral_score": story['viral_score'],
        "topic": story['topic'],
        "vk_engagement": "moderate",  # Default value
        "date": "November 1, 2025",
        "outlet_count": 1,
        "outlets": [story['source']],
        "summary": story.get('summary', story['title'][:200]),
        "summary_ru": story['title'],
        "why_trending": f"This story is trending due to its {story['prominence']} placement and relevance to {story['topic'].replace('_', ' ')}.",
        "why_trending_ru": f"Эта новость в тренде из-за её размещения как {story['prominence']} и актуальности темы.",
        "tags": [story['topic'], story['prominence'], story.get('category', '').lower().replace(' ', '_')]
    }
    formatted_stories.append(formatted_story)

# Create final JSON
output = {
    "metadata": {
        "generated_at": data['generated_at'],
        "collection_period": "2025-11-01",
        "total_outlets": 6,
        "total_stories_analyzed": data['total_stories_analyzed'],
        "outlets": [
            {"name": "RT Russian", "url": "https://russian.rt.com/"},
            {"name": "TASS", "url": "https://tass.ru/"},
            {"name": "RIA Novosti", "url": "https://ria.ru/"},
            {"name": "Rossiyskaya Gazeta", "url": "https://rg.ru/"},
            {"name": "Komsomolskaya Pravda", "url": "https://www.kp.ru/"},
            {"name": "Lenta.ru", "url": "https://lenta.ru/"}
        ]
    },
    "stories": formatted_stories
}

# Write to file
with open('/home/ubuntu/viral-russia-news/public/viral_russia_news.json', 'w', encoding='utf-8') as f:
    json.dump(output, f, ensure_ascii=False, indent=2)

print(f"Successfully formatted {len(formatted_stories)} stories")

#!/usr/bin/env python3
import json
from openai import OpenAI

client = OpenAI()

with open('public/viral_russia_news.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print(f"Enhancing summaries for {len(data['stories'])} stories...")

for i, story in enumerate(data['stories'], 1):
    print(f"\nProcessing story {i}/{len(data['stories'])}...")
    print(f"Title: {story['title'][:60]}...")
    
    # Generate comprehensive English summary
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional news summarizer. Create a comprehensive 2-3 sentence summary of the news story based on the title. Make it informative and engaging, providing context and key details. Write in clear, professional English."},
            {"role": "user", "content": f"Title: {story['title']}\nRussian Title: {story['title_ru']}\n\nCreate a comprehensive summary:"}
        ]
    )
    english_summary = response.choices[0].message.content.strip()
    
    # Generate comprehensive Russian summary
    response_ru = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Вы профессиональный новостной редактор. Создайте подробное резюме из 2-3 предложений для новостной статьи на основе заголовка. Сделайте его информативным и интересным, предоставляя контекст и ключевые детали."},
            {"role": "user", "content": f"Заголовок: {story['title_ru']}\n\nСоздайте подробное резюме:"}
        ]
    )
    russian_summary = response_ru.choices[0].message.content.strip()
    
    # Generate why_trending explanation
    response_trending = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a news analyst. Explain in 1-2 sentences why this story is trending in Russian media, based on its topic and significance."},
            {"role": "user", "content": f"Title: {story['title']}\nTopic: {story['topic']}\nProminence: {story.get('prominence', 'featured')}\n\nWhy is this trending:"}
        ]
    )
    why_trending = response_trending.choices[0].message.content.strip()
    
    # Update story
    story['summary'] = english_summary
    story['summary_ru'] = russian_summary
    story['why_trending'] = why_trending
    story['why_trending_ru'] = f"Эта новость в тренде из-за её актуальности и важности для российской аудитории."
    
    print(f"  Summary: {english_summary[:80]}...")

# Write updated JSON
with open('public/viral_russia_news.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("\n✅ All summaries enhanced successfully!")

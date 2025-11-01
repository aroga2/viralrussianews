#!/usr/bin/env python3
import json
from datetime import datetime
import os
from openai import OpenAI

# Initialize OpenAI client
client = OpenAI()

# Scoring weights
PROMINENCE_SCORES = {
    'top_story': 100,
    'featured': 80,
    'main': 60,
    'news_feed': 40
}

RECENCY_SCORES = {
    'minutes': 100,
    'hours': 80,
    'yesterday': 60,
    'days_ago': 40
}

TOPIC_SCORES = {
    'ukraine_conflict': 20,
    'international': 15,
    'domestic_politics': 15,
    'economy': 10,
    'society': 10,
    'culture': 5
}

def parse_time(time_str):
    """Parse time string and return recency score"""
    if not time_str:
        return RECENCY_SCORES['days_ago']
    
    time_lower = time_str.lower()
    if 'минут' in time_lower or 'minute' in time_lower:
        return RECENCY_SCORES['minutes']
    elif 'час' in time_lower or 'hour' in time_lower:
        return RECENCY_SCORES['hours']
    elif 'вчера' in time_lower or 'yesterday' in time_lower:
        return RECENCY_SCORES['yesterday']
    else:
        return RECENCY_SCORES['days_ago']

def classify_topic(title):
    """Classify story topic based on keywords"""
    title_lower = title.lower()
    
    # Ukraine conflict keywords
    ukraine_keywords = ['украин', 'всу', 'зеленск', 'киев', 'донбасс', 'красноармейск', 'спецоперац', 'сво']
    if any(kw in title_lower for kw in ukraine_keywords):
        return 'ukraine_conflict', TOPIC_SCORES['ukraine_conflict']
    
    # International keywords
    intl_keywords = ['сша', 'трамп', 'байден', 'европ', 'венесуэл', 'путин', 'лавров', 'nato', 'нато']
    if any(kw in title_lower for kw in intl_keywords):
        return 'international', TOPIC_SCORES['international']
    
    # Domestic politics keywords
    politics_keywords = ['путин', 'совбез', 'правительств', 'минобороны', 'дума', 'закон']
    if any(kw in title_lower for kw in politics_keywords):
        return 'domestic_politics', TOPIC_SCORES['domestic_politics']
    
    # Economy keywords
    economy_keywords = ['экономик', 'рубл', 'банк', 'цб', 'ставк', 'инфляц', 'налог', 'кредит']
    if any(kw in title_lower for kw in economy_keywords):
        return 'economy', TOPIC_SCORES['economy']
    
    # Default to society
    return 'society', TOPIC_SCORES['society']

def read_stories_file(filepath, source):
    """Read and parse stories from text file"""
    stories = []
    
    if not os.path.exists(filepath):
        print(f"Warning: {filepath} not found")
        return stories
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split by numbered entries
    lines = content.split('\n')
    current_story = {}
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        
        # Check if line starts with a number (new story)
        if line and line[0].isdigit() and '. ' in line[:5]:
            # Save previous story
            if current_story and 'title' in current_story:
                stories.append(current_story)
            
            # Start new story
            title = line.split('. ', 1)[1] if '. ' in line else line
            current_story = {
                'title': title,
                'source': source,
                'prominence': 'main',
                'time': '',
                'category': ''
            }
        elif 'Prominence:' in line:
            current_story['prominence'] = line.split(':', 1)[1].strip()
        elif 'Time:' in line:
            current_story['time'] = line.split(':', 1)[1].strip()
        elif 'Category:' in line or 'Tag:' in line:
            current_story['category'] = line.split(':', 1)[1].strip()
    
    # Add last story
    if current_story and 'title' in current_story:
        stories.append(current_story)
    
    return stories

def calculate_viral_score(story):
    """Calculate viral score for a story"""
    # Base score from prominence
    prominence = story.get('prominence', 'main')
    score = PROMINENCE_SCORES.get(prominence, 50)
    
    # Add recency score
    time_str = story.get('time', '')
    score += parse_time(time_str)
    
    # Add topic score
    topic, topic_score = classify_topic(story['title'])
    score += topic_score
    story['topic'] = topic
    
    return score

def enhance_story_with_ai(story):
    """Enhance a single story with AI-generated summaries and translations"""
    print(f"\nEnhancing story: {story['title'][:60]}...")
    
    # 1. Translate title to English
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional translator. Translate the following Russian news headline to English. Provide only the translation."},
            {"role": "user", "content": story['title']}
        ]
    )
    story['title_en'] = response.choices[0].message.content.strip()
    story['title_ru'] = story['title'] # Keep original Russian title
    story['title'] = story['title_en'] # Set main title to English
    print(f"  EN Title: {story['title_en'][:60]}...")
    
    # 2. Generate comprehensive English summary
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a professional news summarizer. Create a comprehensive 2-3 sentence summary of the news story based on the title. Make it informative and engaging."},
            {"role": "user", "content": f"Title: {story['title_en']}\nRussian Title: {story['title_ru']}"}
        ]
    )
    story['summary'] = response.choices[0].message.content.strip()
    print(f"  EN Summary: {story['summary'][:60]}...")
    
    # 3. Generate comprehensive Russian summary
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "Вы профессиональный новостной редактор. Создайте подробное резюме из 2-3 предложений для новостной статьи на основе заголовка."},
            {"role": "user", "content": f"Заголовок: {story['title_ru']}"}
        ]
    )
    story['summary_ru'] = response.choices[0].message.content.strip()
    
    # 4. Generate 'Why Trending' explanation
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        messages=[
            {"role": "system", "content": "You are a news analyst. Explain in 1-2 sentences why this story is trending in Russian media, based on its topic and significance."},
            {"role": "user", "content": f"Title: {story['title_en']}\nTopic: {story['topic']}"}
        ]
    )
    story['why_trending'] = response.choices[0].message.content.strip()
    story['why_trending_ru'] = f"Эта новость в тренде из-за её актуальности и важности для российской аудитории."
    
    return story

def main():
    # Read stories from all sources
    all_stories = []
    
    sources = {
        'RT Russian': 'data/rt_stories.txt',
        'TASS': 'data/tass_stories.txt',
        'RIA Novosti': 'data/ria_stories.txt',
        'Rossiyskaya Gazeta': 'data/rg_stories.txt',
        'Komsomolskaya Pravda': 'data/kp_stories.txt',
        'Lenta.ru': 'data/lenta_stories.txt'
    }
    
    for source_name, filepath in sources.items():
        stories = read_stories_file(filepath, source_name)
        all_stories.extend(stories)
    
    print(f"Total stories collected: {len(all_stories)}")
    
    # Calculate viral scores
    for story in all_stories:
        story['viral_score'] = calculate_viral_score(story)
    
    # Sort by viral score
    all_stories.sort(key=lambda x: x['viral_score'], reverse=True)
    
    # Get top 15
    top_stories_raw = all_stories[:15]
    
    # Enhance top 15 stories with AI
    print("\n=== ENHANCING TOP 15 STORIES WITH AI ===\n")
    top_stories = [enhance_story_with_ai(story) for story in top_stories_raw]
    
    # Print results
    print("\n=== TOP 15 VIRAL RUSSIA NEWS ===\n")
    for i, story in enumerate(top_stories, 1):
        print(f"{i}. [{story['viral_score']}] {story['title'][:80]}...")
        print(f"   Source: {story['source']} | Topic: {story['topic']}")
        print()
    
    # Save to JSON
        # Prepare final JSON for website
    final_data = {
        'generated_at': datetime.now().strftime('%B %d, %Y at %I:%M %p UTC'),
        'collection_period': datetime.now().strftime('%Y-%m-%d'),
        'total_outlets': 6,
        'stories': []
    }
    
    for i, story in enumerate(top_stories, 1):
        final_data['stories'].append({
            'rank': i,
            'title': story['title'],
            'title_ru': story['title_ru'],
            'summary': story['summary'],
            'summary_ru': story['summary_ru'],
            'why_trending': story['why_trending'],
            'why_trending_ru': story['why_trending_ru'],
            'viral_score': story['viral_score'],
            'topic': story['topic'],
            'vk_engagement': 'moderate', # Placeholder
            'date': datetime.now().strftime('%B %d, %Y'),
            'outlet_count': 1, # Placeholder
            'outlets': [story['source']],
            'tags': [story['topic'], story.get('prominence', 'featured'), story.get('category', '')]
        })

    # Write to final JSON file for the website
    with open('public/viral_russia_news.json', 'w', encoding='utf-8') as f:
        json.dump(final_data, f, ensure_ascii=False, indent=2)
    
    print("\n✓ Website JSON created at public/viral_russia_news.json")

    # Save raw analysis to data/viral_stories.json
    output_data = {
        'generated_at': datetime.now().isoformat(),
        'total_stories_analyzed': len(all_stories),
        'top_stories': []
    }
    
    for i, story in enumerate(top_stories, 1):
        output_data['top_stories'].append({
            'rank': i,
            'title': story['title'],
            'source': story['source'],
            'viral_score': story['viral_score'],
            'topic': story['topic'],
            'prominence': story.get('prominence', 'main'),
            'time': story.get('time', ''),
            'category': story.get('category', '')
        })
    
    # Write to JSON file
    with open("data/viral_stories.json", 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print("✓ Analysis complete! Results saved to data/viral_stories.json")

if __name__ == '__main__':
    main()

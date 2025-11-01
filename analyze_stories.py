#!/usr/bin/env python3
import json
from datetime import datetime
import os

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
    top_stories = all_stories[:15]
    
    # Print results
    print("\n=== TOP 15 VIRAL RUSSIA NEWS ===\n")
    for i, story in enumerate(top_stories, 1):
        print(f"{i}. [{story['viral_score']}] {story['title'][:80]}...")
        print(f"   Source: {story['source']} | Topic: {story['topic']}")
        print()
    
    # Save to JSON
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
    with open('data/viral_stories.json', 'w', encoding='utf-8') as f:
        json.dump(output_data, f, ensure_ascii=False, indent=2)
    
    print("✓ Analysis complete! Results saved to data/viral_stories.json")

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""
Generate enhanced JSON file with complete metadata for web deployment
"""
import json
from datetime import datetime
from pathlib import Path

def get_source_url(source_name):
    """Get the homepage URL for each source"""
    urls = {
        'RT Russian': 'https://russian.rt.com/',
        'TASS': 'https://tass.ru/',
        'RIA Novosti': 'https://ria.ru/',
        'Rossiyskaya Gazeta': 'https://rg.ru/',
        'Komsomolskaya Pravda': 'https://www.kp.ru/',
        'Lenta.ru': 'https://lenta.ru/',
    }
    return urls.get(source_name, '')

def get_category(title):
    """Determine category based on title keywords"""
    title_lower = title.lower()
    
    if any(kw in title_lower for kw in ['трамп', 'сша', 'нато', 'европ', 'запад', 'нигери']):
        return 'International'
    elif any(kw in title_lower for kw in ['украин', 'всу', 'сво', 'зеленский', 'купянск', 'покровск', 'красноармейск']):
        return 'Ukraine Conflict'
    elif any(kw in title_lower for kw in ['путин', 'россия', 'рф', 'мвф', 'премия']):
        return 'Russia'
    elif any(kw in title_lower for kw in ['оружи', 'военн', 'армия', 'тэс', 'удар', 'экраноплан', 'tomahawk']):
        return 'Military & Defense'
    else:
        return 'General News'

def format_time_for_display(time_str):
    """Format time string for better display"""
    if not time_str:
        return 'Recent'
    
    # If it's already a formatted time, return as is
    if any(x in time_str for x in ['назад', 'ago', 'вчера', 'yesterday', 'ноября', 'Nov']):
        return time_str
    
    # If it's HH:MM format, add "today"
    if ':' in time_str and len(time_str) <= 5:
        return f"Today, {time_str}"
    
    return time_str

def main():
    data_dir = Path('/home/ubuntu/viral-russia-news/data')
    input_file = data_dir / 'analyzed_stories.json'
    output_file = Path('/home/ubuntu/viral-russia-news/public/viral_russia_news.json')
    
    # Read analyzed stories
    with open(input_file, 'r', encoding='utf-8') as f:
        stories = json.load(f)
    
    # Generate enhanced JSON
    enhanced_data = {
        'meta': {
            'generated_at': datetime.utcnow().isoformat() + 'Z',
            'collection_date': datetime.utcnow().strftime('%Y-%m-%d'),
            'total_stories': len(stories),
            'sources_count': len(set(s['source'] for s in stories)),
            'version': '2.0'
        },
        'stories': []
    }
    
    for i, story in enumerate(stories, 1):
        enhanced_story = {
            'id': i,
            'title': story['title'],
            'source': story['source'],
            'source_url': get_source_url(story['source']),
            'time': format_time_for_display(story.get('time', '')),
            'category': get_category(story['title']),
            'viral_score': story['viral_score'],
            'prominence': story.get('prominence', 'main'),
            'rank': i
        }
        enhanced_data['stories'].append(enhanced_story)
    
    # Save enhanced JSON
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
    
    print(f"Enhanced JSON generated: {output_file}")
    print(f"\nMetadata:")
    print(f"  Generated at: {enhanced_data['meta']['generated_at']}")
    print(f"  Total stories: {enhanced_data['meta']['total_stories']}")
    print(f"  Sources: {enhanced_data['meta']['sources_count']}")
    
    print(f"\nCategory breakdown:")
    categories = {}
    for story in enhanced_data['stories']:
        cat = story['category']
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()

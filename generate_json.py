#!/usr/bin/env python3
"""
Generate enhanced JSON file with complete metadata for web deployment
"""
import json
from datetime import datetime
from pathlib import Path

def get_source_info():
    """Get source information with URLs"""
    return [
        {"name": "RT Russian", "url": "https://russian.rt.com/"},
        {"name": "TASS", "url": "https://tass.ru/"},
        {"name": "RIA Novosti", "url": "https://ria.ru/"},
        {"name": "Rossiyskaya Gazeta", "url": "https://rg.ru/"},
        {"name": "Komsomolskaya Pravda", "url": "https://www.kp.ru/"},
        {"name": "Lenta.ru", "url": "https://lenta.ru/"},
    ]

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

def get_source_url(source_name):
    """Get the homepage URL for each source"""
    sources = get_source_info()
    for source in sources:
        if source['name'] == source_name:
            return source['url']
    return ''

def main():
    data_dir = Path('/home/ubuntu/viral-russia-news/data')
    input_file = data_dir / 'analyzed_stories.json'
    output_file = Path('/home/ubuntu/viral-russia-news/public/viral_russia_news.json')
    
    # Read analyzed stories
    with open(input_file, 'r', encoding='utf-8') as f:
        stories = json.load(f)
    
    # Generate enhanced JSON with the correct structure
    enhanced_data = {
        'metadata': {
            'generated_at': datetime.utcnow().isoformat(),
            'collection_period': datetime.utcnow().strftime('%Y-%m-%d'),
            'total_outlets': 6,
            'outlets': get_source_info()
        },
        'stories': []
    }
    
    for i, story in enumerate(stories, 1):
        enhanced_story = {
            'rank': i,
            'title': story['title'],
            'source': story['source'],
            'source_url': get_source_url(story['source']),
            'time': format_time_for_display(story.get('time', '')),
            'category': get_category(story['title']),
            'viral_score': story['viral_score'],
            'prominence': story.get('prominence', 'main')
        }
        enhanced_data['stories'].append(enhanced_story)
    
    # Save enhanced JSON
    output_file.parent.mkdir(parents=True, exist_ok=True)
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(enhanced_data, f, ensure_ascii=False, indent=2)
    
    print(f"Enhanced JSON generated: {output_file}")
    print(f"\nMetadata:")
    print(f"  Generated at: {enhanced_data['metadata']['generated_at']}")
    print(f"  Total stories: {len(enhanced_data['stories'])}")
    print(f"  Total outlets: {enhanced_data['metadata']['total_outlets']}")
    
    print(f"\nCategory breakdown:")
    categories = {}
    for story in enhanced_data['stories']:
        cat = story['category']
        categories[cat] = categories.get(cat, 0) + 1
    for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()

def validate_json_structure(data):
    """Validate that JSON matches expected structure for index.html"""
    errors = []
    
    # Check top-level structure
    if 'metadata' not in data:
        errors.append("Missing 'metadata' key")
    if 'stories' not in data:
        errors.append("Missing 'stories' key")
    
    # Check metadata structure
    if 'metadata' in data:
        meta = data['metadata']
        required_meta_fields = ['generated_at', 'collection_period', 'total_outlets', 'outlets']
        for field in required_meta_fields:
            if field not in meta:
                errors.append(f"Missing metadata.{field}")
        
        if 'outlets' in meta and not isinstance(meta['outlets'], list):
            errors.append("metadata.outlets must be a list")
    
    # Check stories structure
    if 'stories' in data and len(data['stories']) > 0:
        story = data['stories'][0]
        required_story_fields = ['rank', 'title', 'source', 'source_url', 'time', 'category', 'viral_score', 'prominence']
        for field in required_story_fields:
            if field not in story:
                errors.append(f"Missing story.{field} in first story")
    
    return errors

# Add validation call to main()
def main_with_validation():
    """Main function with validation"""
    main()  # Call original main
    
    # Validate the generated file
    output_file = Path('/home/ubuntu/viral-russia-news/public/viral_russia_news.json')
    with open(output_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    errors = validate_json_structure(data)
    if errors:
        print("\n⚠️  VALIDATION ERRORS:")
        for error in errors:
            print(f"  - {error}")
        sys.exit(1)
    else:
        print("\n✓ JSON structure validation passed")

if __name__ == '__main__':
    import sys
    main_with_validation()

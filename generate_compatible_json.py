#!/usr/bin/env python3
"""
Generate JSON in the format expected by the website.
"""

import json
from datetime import datetime
from pathlib import Path

def generate_compatible_json():
    """Generate JSON matching the website's expected structure."""
    
    # Load our ranked stories
    ranked_file = Path('/home/ubuntu/viral-russia-news/temp_news_data/ranked_stories.json')
    if not ranked_file.exists():
        print("Error: ranked_stories.json not found")
        return
    
    ranked_stories = json.loads(ranked_file.read_text(encoding='utf-8'))
    
    # Create compatible structure
    current_date = datetime.now()
    
    output_data = {
        "metadata": {
            "generated_at": current_date.isoformat(),
            "collection_period": current_date.strftime('%Y-%m-%d'),
            "total_outlets": 6,
            "outlets": [
                {"name": "RT Russian", "url": "https://russian.rt.com/"},
                {"name": "TASS", "url": "https://tass.ru/"},
                {"name": "RIA Novosti", "url": "https://ria.ru/"},
                {"name": "Rossiyskaya Gazeta", "url": "https://rg.ru/"},
                {"name": "Komsomolskaya Pravda", "url": "https://www.kp.ru/"},
                {"name": "Lenta.ru", "url": "https://lenta.ru/"}
            ]
        },
        "stories": []
    }
    
    # Convert stories to compatible format
    for i, story in enumerate(ranked_stories[:15], 1):
        # Clean title
        title = story['title']
        if title.startswith('Title:'):
            title = title[6:].strip()
        
        compatible_story = {
            "rank": i,
            "title": title,
            "title_ru": title,  # Same as title since already in Russian
            "viral_score": int(story['viral_score']),
            "outlet": story['outlet'],
            "outlet_url": get_outlet_url(story['outlet']),
            "published_date": current_date.strftime('%Y-%m-%d'),
            "category": story.get('category', ''),
            "tags": story.get('tags', []) if isinstance(story.get('tags'), list) else [],
            "prominence": story.get('prominence', 'normal'),
            "scores_breakdown": story.get('scores', {})
        }
        
        output_data["stories"].append(compatible_story)
    
    return output_data

def get_outlet_url(outlet_name):
    """Get URL for outlet."""
    urls = {
        'RT': 'https://russian.rt.com/',
        'TASS': 'https://tass.ru/',
        'RIA Novosti': 'https://ria.ru/',
        'Rossiyskaya Gazeta': 'https://rg.ru/',
        'Komsomolskaya Pravda': 'https://www.kp.ru/',
        'Lenta.ru': 'https://lenta.ru/'
    }
    return urls.get(outlet_name, '')

def main():
    print("Generating compatible JSON structure...")
    
    output_data = generate_compatible_json()
    
    if not output_data:
        print("Failed to generate JSON")
        return
    
    # Save to public directory
    output_file = Path('/home/ubuntu/viral-russia-news/public/viral_russia_news.json')
    output_file.write_text(json.dumps(output_data, ensure_ascii=False, indent=2), encoding='utf-8')
    
    print(f"\n✓ Generated compatible JSON: {output_file}")
    print(f"  - Total stories: {len(output_data['stories'])}")
    print(f"  - Generated at: {output_data['metadata']['generated_at']}")
    print(f"  - Collection period: {output_data['metadata']['collection_period']}")
    
    # Display sample
    print("\n=== SAMPLE STORY ===")
    sample = output_data['stories'][0]
    print(f"Rank: {sample['rank']}")
    print(f"Title: {sample['title']}")
    print(f"Outlet: {sample['outlet']}")
    print(f"Viral Score: {sample['viral_score']}")
    print(f"Tags: {', '.join(sample['tags'])}")

if __name__ == '__main__':
    main()

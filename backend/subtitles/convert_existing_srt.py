#!/usr/bin/env python3
"""
convert_existing_srt.py - Convert existing SRT file to JSON for interactive web app
"""

import re
import json
import os

def parse_srt_time(time_str):
    """Convert SRT time format to milliseconds"""
    # Format: HH:MM:SS,mmm
    time_parts = time_str.replace(',', ':').split(':')
    hours = int(time_parts[0])
    minutes = int(time_parts[1])
    seconds = int(time_parts[2])
    milliseconds = int(time_parts[3])
    
    total_ms = (hours * 3600 + minutes * 60 + seconds) * 1000 + milliseconds
    return total_ms

def detect_emotion_simple(text):
    """Simple emotion detection based on keywords"""
    text_lower = text.lower()
    
    # Joy indicators
    if any(word in text_lower for word in ['great', 'beautiful', 'glad', 'thanks', 'wow', 'amazing', 'love', 'happy', 'good']):
        return 'joy'
    # Sadness indicators
    elif any(word in text_lower for word in ['sad', 'sorry', 'miss', 'cry', 'tears', 'bad']):
        return 'sadness'
    # Anger indicators
    elif any(word in text_lower for word in ['angry', 'mad', 'hate', 'furious', 'rage']):
        return 'anger'
    # Fear indicators
    elif any(word in text_lower for word in ['scared', 'afraid', 'fear', 'terrified', 'panic']):
        return 'fear'
    # Surprise indicators
    elif '?' in text or any(word in text_lower for word in ['what', 'how', 'why', 'wow', 'oh']):
        return 'surprise'
    # Love indicators
    elif any(word in text_lower for word in ['love', 'heart', 'dear', 'sweet']):
        return 'love'
    else:
        return 'neutral'

def get_word_definition(word):
    """Simple word definitions"""
    definitions = {
        'hey': {'definition': 'Used to attract attention or express greeting', 'example': 'Hey, how are you doing?'},
        'look': {'definition': 'To direct one\'s gaze toward someone or something', 'example': 'Look at that beautiful sunset!'},
        'who': {'definition': 'What or which person or people', 'example': 'Who is coming to the party?'},
        'back': {'definition': 'Returning to a previous position or state', 'example': 'I\'ll be back in five minutes.'},
        'how': {'definition': 'In what way or manner', 'example': 'How did you do that?'},
        'was': {'definition': 'Past tense of \'be\'', 'example': 'It was a great day.'},
        'your': {'definition': 'Belonging to you', 'example': 'Is this your book?'},
        'vacation': {'definition': 'A period of time devoted to pleasure, rest, or relaxation', 'example': 'We went on vacation to Hawaii.'},
        'it': {'definition': 'Referring to a thing previously mentioned', 'example': 'It was raining yesterday.'},
        'amazing': {'definition': 'Causing great surprise or wonder', 'example': 'That magic trick was amazing!'},
        'i': {'definition': 'First person singular pronoun', 'example': 'I am going to the store.'},
        'went': {'definition': 'Past tense of \'go\'', 'example': 'I went to the movies yesterday.'},
        'to': {'definition': 'Expressing motion in the direction of', 'example': 'I\'m going to the store.'},
        'the': {'definition': 'Definite article', 'example': 'The cat is sleeping.'},
        'beach': {'definition': 'A pebbly or sandy shore, especially by the ocean', 'example': 'The children played on the beach.'},
        'did': {'definition': 'Past tense of \'do\'', 'example': 'Did you finish your homework?'},
        'you': {'definition': 'Second person pronoun', 'example': 'You are my best friend.'},
        'bring': {'definition': 'To carry or convey something to a place', 'example': 'Don\'t forget to bring your umbrella.'},
        'me': {'definition': 'First person object pronoun', 'example': 'Can you help me?'},
        'anything': {'definition': 'Any object, occurrence, or matter whatever', 'example': 'Do you need anything?'},
        'of': {'definition': 'Expressing the relationship between a part and a whole', 'example': 'A piece of cake.'},
        'course': {'definition': 'A series of lessons or lectures on a particular subject', 'example': 'I\'m taking a course in mathematics.'},
        'here': {'definition': 'In or at this place', 'example': 'Come here, I want to show you something.'},
        'a': {'definition': 'Indefinite article', 'example': 'A cat is sleeping.'},
        'seashell': {'definition': 'The shell of a marine mollusk', 'example': 'She collected colorful seashells on the shore.'},
        'wow': {'definition': 'Used to express astonishment or admiration', 'example': 'Wow, that\'s amazing!'},
        'beautiful': {'definition': 'Pleasing the senses or mind aesthetically', 'example': 'What a beautiful flower!'},
        'glad': {'definition': 'Feeling pleasure or happiness', 'example': 'I\'m glad you could make it to the party.'},
        'like': {'definition': 'To find agreeable, enjoyable, or satisfactory', 'example': 'I like chocolate ice cream.'},
        'let': {'definition': 'To allow or permit', 'example': 'Let me help you with that.'},
        'go': {'definition': 'To move from one place to another', 'example': 'Let\'s go to the movies.'},
        'work': {'definition': 'Activity involving mental or physical effort', 'example': 'I have a lot of work to do today.'},
        'now': {'definition': 'At the present time or moment', 'example': 'I\'m busy now.'},
        'ready': {'definition': 'Fully prepared or in fit condition', 'example': 'Are you ready to go?'},
        'for': {'definition': 'In support of or in favor of', 'example': 'I\'m voting for that candidate.'},
        'another': {'definition': 'One more of the same kind', 'example': 'I need another cup of coffee.'},
        'day': {'definition': 'A period of 24 hours', 'example': 'Have a great day!'}
    }
    
    clean_word = word.lower().strip('.,?!')
    if clean_word in definitions:
        return definitions[clean_word]
    else:
        return {
            'definition': f'A word meaning {clean_word}',
            'example': f'Example usage of {clean_word}'
        }

def convert_srt_to_json(srt_file, json_file):
    """Convert SRT file to JSON format for interactive subtitles"""
    print(f"Converting {srt_file} to {json_file}...")
    
    if not os.path.exists(srt_file):
        print(f"❌ Error: {srt_file} not found!")
        print("Please run your transcript script first to generate the SRT file.")
        return False
    
    json_data = []
    
    with open(srt_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Split into subtitle blocks
    blocks = content.strip().split('\n\n')
    
    for block in blocks:
        lines = block.strip().split('\n')
        if len(lines) >= 3:
            # Skip subtitle number
            time_line = lines[1]
            text_line = ' '.join(lines[2:])
            
            # Parse time
            time_parts = time_line.split(' --> ')
            if len(time_parts) == 2:
                start_time = parse_srt_time(time_parts[0])
                end_time = parse_srt_time(time_parts[1])
                
                # Clean text (remove HTML tags if present)
                clean_text = re.sub(r'<[^>]+>', '', text_line)
                clean_text = clean_text.strip()
                
                # Split into words
                words = clean_text.split()
                
                # Calculate time per word
                duration = end_time - start_time
                time_per_word = duration / len(words) if words else 1000
                
                # Detect emotion for the whole line
                emotion = detect_emotion_simple(clean_text)
                
                # Create entry for each word
                for i, word in enumerate(words):
                    word_start = start_time + (i * time_per_word)
                    word_end = word_start + time_per_word
                    
                    # Get definition
                    definition_data = get_word_definition(word)
                    
                    json_entry = {
                        "start": int(word_start),
                        "end": int(word_end),
                        "text": word,
                        "emotion": emotion,
                        "definition": definition_data["definition"],
                        "example": definition_data["example"]
                    }
                    json_data.append(json_entry)
    
    # Save to JSON file
    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, indent=4)
    
    print(f"✅ Successfully converted {len(json_data)} words to {json_file}")
    return True

def main():
    print("🎬 SRT to JSON Converter for Interactive Subtitles")
    print("=" * 50)
    
    srt_file = "subtitles.srt"
    json_file = "interactive_subs.json"
    
    if convert_srt_to_json(srt_file, json_file):
        print("\n🎉 Conversion complete!")
        print("=" * 50)
        print(f"📁 Generated: {json_file}")
        print("🌐 The web app will now use the real transcript data!")
        print("\n💡 If you don't see the SRT file, run your transcript script first:")
        print("   python burn_word_subs.py")
    else:
        print("\n❌ Conversion failed. Please check the error messages above.")

if __name__ == "__main__":
    main() 
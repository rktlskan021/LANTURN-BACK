"""
https://spacy.io/usage
"""

import json

# Sample JSON data
data = [
    {"text": "This is a 3.", "start": 4.22, "duration": 1.18},
    {"text": "It's sloppily written and rendered at an extremely low resolution of 28x28 pixels, ", "start": 6.06, "duration": 4.709},
    {"text": "but your brain has no trouble recognizing it as a 3.", "start": 10.769, "duration": 2.951},
    # ... (other subtitle entries)
]

merged_subtitles = []
current_subtitle = None

for elem in data:
    text = elem['text']
    start = elem['start']
    duration = elem['duration']
    end_time = start + duration

    if current_subtitle is None:
        # Start a new merged subtitle
        current_subtitle = {'text': text, 'start': start, 'end_time': end_time}
    else:
        # Continue merging
        current_subtitle['text'] += text
        current_subtitle['end_time'] = end_time

    # Check if the current text ends with a sentence-ending punctuation
    if current_subtitle['text'].strip()[-1] in '.!?':
        # Finish merging
        merged_duration = current_subtitle['end_time'] - current_subtitle['start']
        merged_element = {
            'text': current_subtitle['text'],
            'start': current_subtitle['start'],
            'duration': merged_duration
        }
        merged_subtitles.append(merged_element)
        current_subtitle = None

# Handle any remaining subtitle that didn't end with punctuation
if current_subtitle is not None:
    merged_duration = current_subtitle['end_time'] - current_subtitle['start']
    merged_element = {
        'text': current_subtitle['text'],
        'start': current_subtitle['start'],
        'duration': merged_duration
    }
    merged_subtitles.append(merged_element)

# Output the merged subtitles
print(json.dumps(merged_subtitles, indent=2))

import re
import os
from pathlib import Path

def strip_colors_and_icons(content):
    # Remove emoji/icons (most common Unicode ranges)
    content = re.sub(r'[\U0001F300-\U0001F9FF]', '', content)
    content = re.sub(r'[\u2600-\u26FF]', '', content)
    content = re.sub(r'[\u2700-\u27BF]', '', content)
    
    # Remove inline style attributes with colors/backgrounds/borders
    content = re.sub(r'style="[^"]*(?:color|background|border)[^"]*"', '', content)
    
    # Remove icon image tags
    content = re.sub(r'<img[^>]*icons/[^>]*>', '', content)
    
    # Remove empty style attributes
    content = re.sub(r'\s+style=""\s*', ' ', content)
    
    return content

# Find all HTML files
for html_file in Path('.').rglob('*.html'):
    if 'venv' in str(html_file) or 'node_modules' in str(html_file):
        continue
    
    print(f"Processing: {html_file}")
    with open(html_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = strip_colors_and_icons(content)
    
    if new_content != content:
        with open(html_file, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"  ✓ Updated")
    else:
        print(f"  - No changes")

print("\nDone!")

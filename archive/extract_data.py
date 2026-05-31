import re
import os

app_js_path = 'js/app.js'
data_js_path = 'js/data.js'
index_html_path = 'index.html'

with open(app_js_path, 'r', encoding='utf-8') as f:
    lines = f.readlines()

start_idx = -1
end_idx = -1

for i, line in enumerate(lines):
    if "const simulatedDatabase = {" in line:
        start_idx = i
        break

if start_idx != -1:
    # Find matching bracket by counting
    brace_count = 0
    for i in range(start_idx, len(lines)):
        brace_count += lines[i].count('{')
        brace_count -= lines[i].count('}')
        if brace_count == 0:
            end_idx = i
            break

if start_idx != -1 and end_idx != -1:
    simulated_db_lines = lines[start_idx:end_idx+1]
    
    # Write to data.js
    with open(data_js_path, 'w', encoding='utf-8') as f:
        f.write('// Data definitions\n')
        # Dedent by removing 12 spaces if it was indented
        for line in simulated_db_lines:
            if line.startswith('            '):
                f.write(line[12:])
            else:
                f.write(line)
                
    # Remove from app.js
    del lines[start_idx:end_idx+1]
    with open(app_js_path, 'w', encoding='utf-8') as f:
        f.writelines(lines)
        
    # Add script tag to index.html
    with open(index_html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    html_content = html_content.replace('<script src="js/app.js"></script>', '<script src="js/data.js"></script>\n    <script src="js/app.js"></script>')
    
    with open(index_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
        
    print("Extraction successful!")
else:
    print("Could not find simulatedDatabase.")

import re
import os

html_file = 'PRE-PUT DASHBOARD.html'

with open(html_file, 'r', encoding='utf-8') as f:
    content = f.read()

# Extract styles
style_match = re.search(r'<style>(.*?)</style>', content, re.DOTALL)
if style_match:
    styles_content = style_match.group(1).strip()
    with open('css/styles.css', 'w', encoding='utf-8') as f:
        f.write(styles_content)
    # Replace <style> block with <link>
    content = re.sub(r'<style>.*?</style>', '<link rel="stylesheet" href="css/styles.css">', content, flags=re.DOTALL)

# Extract scripts (skip the first config.js script and external scripts)
# Find the main massive script block
script_matches = list(re.finditer(r'<script>(.*?)</script>', content, re.DOTALL))

# We'll put all embedded scripts into app.js
app_js_content = ""
for match in script_matches:
    script_content = match.group(1).strip()
    # Skip small scripts if necessary, but here we just combine all embedded scripts
    if "setGlobalFontSize" in script_content or "wizardQuestions" in script_content:
        app_js_content += script_content + "\n\n"
        # Remove it from HTML
        content = content.replace(match.group(0), "")

# Add <script src="js/app.js"></script> before </body>
content = content.replace('</body>', '<script src="js/app.js"></script>\n</body>')

if app_js_content:
    with open('js/app.js', 'w', encoding='utf-8') as f:
        f.write(app_js_content)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Split completed successfully!")

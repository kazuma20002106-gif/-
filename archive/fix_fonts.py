import re

def process_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    content = re.sub(r'text-\[8px\]', 'text-xs', content)
    content = re.sub(r'text-\[9px\]', 'text-xs', content)
    content = re.sub(r'text-\[10px\]', 'text-xs', content)
    content = re.sub(r'text-\[11px\]', 'text-xs', content)
    content = re.sub(r'text-\[12px\]', 'text-xs', content)
    content = re.sub(r'text-\[13px\]', 'text-sm', content)
    content = re.sub(r'text-\[14px\]', 'text-sm', content)
    content = re.sub(r'text-\[15px\]', 'text-base', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

process_file('js/app.js')
print("app.js fonts updated.")

import re
import os

html_path = r"C:\Users\kazum\OneDrive\デスクトップ\フォルダー\クルーAI\第五段階テスト\PRE-PUT DASHBOARD.html"
py_path = r"C:\Users\kazum\OneDrive\デスクトップ\フォルダー\クルーAI\第五段階テスト\build_saas.py"

if os.path.exists(html_path) and os.path.exists(py_path):
    with open(html_path, 'r', encoding='utf-8') as f:
        html = f.read()
        
    with open(py_path, 'r', encoding='utf-8') as f:
        py_content = f.read()
        
    # Match the multiline r""" ... """ assignment for html_content
    # Use re.DOTALL and escape the replacement backslashes so re doesn't complain about invalid escapes
    escaped_html = html.replace('\\', '\\\\').replace('$', '\\$')
    
    # Simple search & replace based on r""" headers is safer than complex regex
    start_marker = 'html_content = r"""'
    end_marker = '"""\n\nwith open('
    
    start_idx = py_content.find(start_marker)
    end_idx = py_content.find(end_marker)
    
    if start_idx != -1 and end_idx != -1:
        new_content = py_content[:start_idx + len(start_marker)] + html + py_content[end_idx:]
        with open(py_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print("Successfully synchronized HTML content back to build_saas.py!")
    else:
        print("Could not find start/end markers in build_saas.py")
else:
    print("Files not found.")

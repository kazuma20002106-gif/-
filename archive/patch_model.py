import os

file_path = r"C:\Users\kazum\OneDrive\デスクトップ\フォルダー\クルーAI\第五段階テスト\build_saas.py"
if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Replace the incorrect model name
    content = content.replace("gemini-2.5-flash", "gemini-1.5-pro")
    
    # Fix the compiler model to gemini-1.5-flash (if specific call exists)
    content = content.replace(
        "callAgent(apiKey, builderSystem, `質問リスト:\\n${jsonInput}`, true, 2, 'gemini-1.5-pro')",
        "callAgent(apiKey, builderSystem, `質問リスト:\\n${jsonInput}`, true, 2, 'gemini-1.5-flash')"
    )
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Successfully patched build_saas.py")
else:
    print("build_saas.py not found, skipping.")

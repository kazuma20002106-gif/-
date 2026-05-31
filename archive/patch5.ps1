$path = "PRE-PUT DASHBOARD.html"
$content = Get-Content $path -Raw -Encoding UTF8

$patternSig = "(?s)async function callGeminiAgent\(apiKeyString, systemPrompt, userPrompt, isJson = false, retries = 2\) \{"
$replacementSig = "async function callGeminiAgent(apiKeyString, systemPrompt, userPrompt, isJson = false, retries = 2, model = 'gemini-2.5-flash') {"
$content = [regex]::Replace($content, $patternSig, $replacementSig)

$patternUrl = "(?s)const url = ``https://generativelanguage\.googleapis\.com/v1beta/models/gemini-2\.5-flash:generateContent\?key=`$\{key\}``;"
$replacementUrl = "const url = ``https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}``;"
$content = [regex]::Replace($content, $patternUrl, $replacementUrl)

Set-Content -Path $path -Value $content -Encoding UTF8

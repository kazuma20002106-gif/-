$path = "PRE-PUT DASHBOARD.html"
$content = Get-Content $path -Raw -Encoding UTF8

# Remove hardcoded h-[600px] from consoleLog and make it fully flexible
$content = $content -replace 'id="consoleLog" class="w-full max-w-4xl mx-auto h-\[600px\] overflow-y-auto', 'id="consoleLog" class="w-full max-w-4xl mx-auto flex-grow h-0 overflow-y-auto'

# Also, when hiding header in startAnalysisEngine, remove pb-20
$patternStart = "(?s)document\.body\.classList\.add\('h-screen', 'overflow-hidden'\);"
$replacementStart = "document.body.classList.add('h-screen', 'overflow-hidden');`r`n            document.body.classList.remove('pb-20');"
$content = [regex]::Replace($content, $patternStart, $replacementStart)

# Restore pb-20 in createNewProject
$patternCreate = "(?s)document\.body\.classList\.add\('min-h-screen'\);"
$replacementCreate = "document.body.classList.add('min-h-screen', 'pb-20');"
$content = [regex]::Replace($content, $patternCreate, $replacementCreate)

Set-Content -Path $path -Value $content -Encoding UTF8

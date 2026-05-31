$path = "PRE-PUT DASHBOARD.html"
$content = Get-Content $path -Raw -Encoding UTF8

# 1. Add ID to header
$content = $content -replace '<header class="flex flex-col', '<header id="appHeader" class="flex flex-col transition-all duration-500 overflow-hidden '

# 2. Add ID to TABS container and remove min-h-[700px]
$content = $content -replace 'class="flex-grow bg-white border border-slate-200 shadow-sm rounded-2xl overflow-hidden flex flex-col min-h-\[700px\]"', 'id="tabFramework" class="flex-grow bg-white border border-slate-200 shadow-sm rounded-2xl overflow-hidden flex flex-col min-h-[500px]"'

# 3. In createNewProject, show header
$patternCreate = "(?s)function createNewProject\(\) \{.*?(?=document\.getElementById\('projectIdea'\))"
$replacementCreate = "function createNewProject() {`r`n            document.getElementById('appHeader').classList.remove('hidden');`r`n            document.body.classList.remove('h-screen', 'overflow-hidden');`r`n            document.body.classList.add('min-h-screen');`r`n            document.getElementById('phase2').classList.add('hidden');`r`n            document.getElementById('phase2').classList.remove('flex');`r`n            document.getElementById('phase1').classList.remove('hidden');`r`n            document.getElementById('phase1').classList.add('flex');`r`n            `r`n            "
$content = [regex]::Replace($content, $patternCreate, $replacementCreate)

# 4. In loadSavedProject, hide header if entering Phase 2
$patternLoad = "(?s)document\.getElementById\('tabDiscovery'\)\.classList\.remove\('hidden'\);\s*document\.getElementById\('tabWizard'\)\.classList\.remove\('hidden'\);"
$replacementLoad = "document.getElementById('appHeader').classList.add('hidden');`r`n                document.body.classList.remove('min-h-screen');`r`n                document.body.classList.add('h-screen', 'overflow-hidden');`r`n                document.getElementById('tabDiscovery').classList.remove('hidden');`r`n                document.getElementById('tabWizard').classList.remove('hidden');"
$content = [regex]::Replace($content, $patternLoad, $replacementLoad)

# 5. In startAnalysisEngine, hide header
$patternStart = "(?s)document\.getElementById\('phase2'\)\.classList\.remove\('hidden'\);\s*document\.getElementById\('phase2'\)\.classList\.add\('flex'\);\s*window\.scrollTo\(\{ top: 0, behavior: 'smooth' \}\);"
$replacementStart = "document.getElementById('appHeader').classList.add('hidden');`r`n            document.body.classList.remove('min-h-screen');`r`n            document.body.classList.add('h-screen', 'overflow-hidden');`r`n            document.getElementById('phase2').classList.remove('hidden');`r`n            document.getElementById('phase2').classList.add('flex');`r`n            window.scrollTo({ top: 0, behavior: 'smooth' });"
$content = [regex]::Replace($content, $patternStart, $replacementStart)

Set-Content -Path $path -Value $content -Encoding UTF8

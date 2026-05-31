$path = "PRE-PUT DASHBOARD.html"
$content = Get-Content $path -Raw -Encoding UTF8

# 1. Update phase2 padding
$content = $content -replace 'id="phase2" class="hidden flex-col h-full fade-in w-full max-w-6xl mx-auto py-8"', 'id="phase2" class="hidden flex-col h-full fade-in w-full max-w-6xl mx-auto pt-2 pb-4"'

# 2. Update tabFramework min-height so it shrinks and enables internal scrolling
$content = $content -replace 'id="tabFramework" class="flex-grow bg-white border border-slate-200 shadow-sm rounded-2xl overflow-hidden flex flex-col min-h-\[500px\]"', 'id="tabFramework" class="flex-grow bg-white border border-slate-200 shadow-sm rounded-2xl overflow-hidden flex flex-col min-h-0"'

Set-Content -Path $path -Value $content -Encoding UTF8

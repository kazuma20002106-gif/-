$path = "PRE-PUT DASHBOARD.html"
$content = Get-Content $path -Raw -Encoding UTF8

# 1. Add CSS classes
$patternCss = "(?s)\.gradient-bg-light \{.*?\n\s*\}"
$replacementCss = @"
        .gradient-bg-light { background: linear-gradient(-45deg, #f8fafc, #f0fdfa, #f8fafc, #e0f2fe); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-indigo { background: linear-gradient(-45deg, #f8fafc, #e0e7ff, #f8fafc, #c7d2fe); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-cyan { background: linear-gradient(-45deg, #f8fafc, #cffafe, #f8fafc, #a5f3fc); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-purple { background: linear-gradient(-45deg, #f8fafc, #f3e8ff, #f8fafc, #d8b4fe); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-amber { background: linear-gradient(-45deg, #f8fafc, #fef3c7, #f8fafc, #fde68a); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-emerald { background: linear-gradient(-45deg, #f8fafc, #d1fae5, #f8fafc, #a7f3d0); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-rose { background: linear-gradient(-45deg, #f8fafc, #ffe4e6, #f8fafc, #fecdd3); background-size: 400% 400%; animation: gradient 10s ease infinite; }
"@
$content = [regex]::Replace($content, $patternCss, $replacementCss)

# 2. Update setActiveFlow
$patternVars = "(?s)const agentNames =.*?const agentTextColors =.*?\r?\n"
$replacementVars = @"
        const agentNames = ["", "STRATEGY", "TECH", "DESIGN", "BUSINESS", "COMPILER", "WIZARD"];
        const agentTextColors = ["", "text-indigo-500", "text-cyan-500", "text-purple-500", "text-amber-500", "text-emerald-500", "text-rose-500"];
        const agentBgColors = ["bg-teal-500", "bg-indigo-500", "bg-cyan-500", "bg-purple-500", "bg-amber-500", "bg-emerald-500", "bg-rose-500"];
        const agentShadows = ["shadow-[0_0_10px_rgba(20,184,166,0.8)]", "shadow-[0_0_10px_rgba(99,102,241,0.8)]", "shadow-[0_0_10px_rgba(6,182,212,0.8)]", "shadow-[0_0_10px_rgba(168,85,247,0.8)]", "shadow-[0_0_10px_rgba(245,158,11,0.8)]", "shadow-[0_0_10px_rgba(16,185,129,0.8)]", "shadow-[0_0_10px_rgba(244,63,94,0.8)]"];
        const agentGradients = ["gradient-bg-light", "gradient-bg-indigo", "gradient-bg-cyan", "gradient-bg-purple", "gradient-bg-amber", "gradient-bg-emerald", "gradient-bg-rose"];

"@
$content = [regex]::Replace($content, $patternVars, $replacementVars)

$patternSetActiveFlow = "(?s)function setActiveFlow\(id\) \{.*?\}(?=\s*function writeToConsole)"
$replacementSetActiveFlow = @"
        function setActiveFlow(id) {
            for (let i = 1; i <= 6; i++) {
                const el = document.getElementById(`stat-$\\{i\\}`);
                if (el) {
                    el.className = "flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 border border-transparent text-sm transition-colors";
                    document.getElementById(`stat-text-$\\{i\\}`).innerText = agentNames[i];
                    document.getElementById(`stat-text-$\\{i\\}`).className = `text-[10px] $\\{agentTextColors[i]\\} font-mono font-bold`;
                    
                    const avatar = el.querySelector('.h-8.w-8');
                    if (avatar) avatar.classList.remove('animate-bounce', 'ring-2', 'ring-offset-1');
                }
            }
            if (id >= 1 && id <= 6) {
                const el = document.getElementById(`stat-$\\{id\\}`);
                el.className = "flex items-center gap-3 px-4 py-2 rounded-xl bg-white border border-teal-200 text-sm shadow-md transition-colors";
                document.getElementById(`stat-text-$\\{id\\}`).innerText = "WORKING...";
                document.getElementById(`stat-text-$\\{id\\}`).className = `text-[10px] $\\{agentTextColors[id]\\} font-mono font-bold animate-pulse`;
                
                const avatar = el.querySelector('.h-8.w-8');
                if (avatar) avatar.classList.add('animate-bounce', 'ring-2', 'ring-offset-1');
            } else if (id === 0) {
                const globalStatusContainer = document.getElementById('currentGlobalStatus');
                if (globalStatusContainer) {
                    globalStatusContainer.classList.add('hidden');
                    globalStatusContainer.classList.remove('flex');
                }
            }
            
            if (id >= 0 && id <= 6) {
                const termArea = document.getElementById('terminalArea');
                if (termArea) {
                    termArea.className = termArea.className.replace(/gradient-bg-\w+/, agentGradients[id]);
                }
                const pBar = document.getElementById('progressBar');
                if (pBar) {
                    pBar.className = pBar.className.replace(/bg-\w+-500/, agentBgColors[id]);
                    pBar.className = pBar.className.replace(/shadow-\[[^\]]+\]/, agentShadows[id]);
                }
            }
        }
"@
$content = [regex]::Replace($content, $patternSetActiveFlow, $replacementSetActiveFlow)

# 3. Add window.scrollTo
$patternScroll = "(?s)document\.getElementById\('phase2'\)\.classList\.add\('flex'\);\s*"
$replacementScroll = "document.getElementById('phase2').classList.add('flex');`r`n            window.scrollTo({ top: 0, behavior: 'smooth' });`r`n            "
$content = [regex]::Replace($content, $patternScroll, $replacementScroll)

Set-Content -Path $path -Value $content -Encoding UTF8

$path = "PRE-PUT DASHBOARD.html"
$content = Get-Content $path -Raw -Encoding UTF8

$pattern = "(?s)async function callGeminiAgent\(apiKey, systemPrompt.*?^\s*\}\r?\n"
$replacement = @"
        let currentApiKeyIndex = 0;

        async function callGeminiAgent(apiKeyString, systemPrompt, userPrompt, isJson = false, retries = 2) {
            const keys = apiKeyString.split(',').map(k => k.trim()).filter(k => k);
            if (keys.length === 0) throw new Error("APIキーが入力されていません。");

            let lastError = null;
            const maxAttempts = Math.max(retries + 1, keys.length * 2);

            const payload = { contents: [{ parts: [{ text: "$\{systemPrompt\}\n\n【ユーザー入力】\n$\{userPrompt\}" }] }] };
            if (isJson) payload.generationConfig = { responseMimeType: "application/json" };
            
            for (let i = 0; i < maxAttempts; i++) {
                const key = keys[currentApiKeyIndex % keys.length];
                currentApiKeyIndex++;

                const url = `https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$\{key\}`;
                
                try {
                    const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
                    if (res.ok) {
                        const data = await res.json();
                        return data.candidates[0].content.parts[0].text;
                    }
                    
                    if (res.status === 429) {
                        lastError = new Error(`[ERROR-429] APIレート制限。キーを切り替えます...`);
                        if (keys.length > 1) {
                            writeToConsole('SYSTEM', `API制限(429)到達。予備キーへローテーションします...`, 'system');
                        }
                        await new Promise(r => setTimeout(r, 2000));
                        continue;
                    }
                    
                    if (res.status >= 500 && i < maxAttempts - 1) {
                        writeToConsole('SYSTEM', `APIエラー($\{res.status\})。待機して再試行します...`, 'system');
                        await new Promise(r => setTimeout(r, 3000));
                        continue;
                    }

                    throw new Error(`[ERROR-$\\{res.status\\}] $\\{res.statusText\\}`);
                } catch (e) {
                    lastError = e;
                    if (i === maxAttempts - 1 || !(e.message.includes('429') || e.message.includes('500') || e.message.includes('503'))) {
                        throw e;
                    }
                }
            }
            throw lastError;
        }

"@

$newContent = [regex]::Replace($content, $pattern, $replacement)
Set-Content -Path $path -Value $newContent -Encoding UTF8

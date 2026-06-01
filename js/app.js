function setGlobalFontSize(size) {
            const html = document.documentElement;
            html.classList.remove('font-size-medium', 'font-size-large', 'font-size-xl');
            html.classList.add(`font-size-${size}`);
            
            localStorage.setItem('preput-font-size', size);
            
            const btnMedium = document.getElementById('btn-font-medium');
            const btnLarge = document.getElementById('btn-font-large');
            const btnXl = document.getElementById('btn-font-xl');
            if (!btnMedium) return;
            
            const activeClass = 'bg-teal-50 border-teal-200 text-teal-600';
            const inactiveClass = 'bg-white border-slate-200 text-slate-600 hover:bg-slate-50';
            
            [btnMedium, btnLarge, btnXl].forEach(btn => {
                btn.className = `px-2.5 py-1 text-xs font-bold rounded-lg border transition-all cursor-pointer ${inactiveClass}`;
            });
            
            const targetBtn = document.getElementById(`btn-font-${size}`);
            if (targetBtn) {
                targetBtn.className = `px-2.5 py-1 text-xs font-bold rounded-lg border transition-all cursor-pointer ${activeClass}`;
            }
        }
        
        // Restore font size immediately on load to prevent flash of wrong size
        (function() {
            const savedSize = localStorage.getItem('preput-font-size') || 'medium';
            document.documentElement.classList.add(`font-size-${savedSize}`);
            document.addEventListener('DOMContentLoaded', () => {
                setGlobalFontSize(savedSize);
            });
        })();

        let currentTab = 'terminal';
        let projectHistory = [];
        let activeDepth = 'standard';
        const logArea = document.getElementById('consoleLog');
        const progressBar = document.getElementById('progressBar');

        let rawBaseVars = [];
        let rawDeepVars = [];
        let wizardQuestions = [];
        let wizardAnswers = {};
        let currentQuestionIndex = 0;

        function toggleHelp() {
            const popover = document.getElementById('helpPopover');
            if (popover.classList.contains('hidden')) {
                popover.classList.remove('hidden');
                setTimeout(() => {
                    popover.classList.remove('translate-y-4', 'opacity-0', 'pointer-events-none');
                }, 10);
            } else {
                popover.classList.add('translate-y-4', 'opacity-0', 'pointer-events-none');
                setTimeout(() => {
                    popover.classList.add('hidden');
                }, 300);
            }
        }

        function updateHelpContext(phaseStr) {
            const desc = document.getElementById('helpDescription');
            const tips = document.getElementById('helpTipsList');
            if (!desc || !tips) return;

            if (phaseStr === 'phase1') {
                desc.innerHTML = '現在「プロジェクト構成」フェーズです。<br>作りたいもののアイデアを入力するか、初心者のためのサンプルを選択してください。';
                tips.innerHTML = '<li>できるだけ具体的に書くとAIの精度が上がります。</li><li>こだわりがなければ空欄のままでもAIがうまく補ってくれます。</li>';
            } else if (phaseStr === 'terminal') {
                desc.innerHTML = '現在「仮想会議室（分析フェーズ）」です。<br>4人の専門AIがあなたのアイデアを多角的に検証・分析しています。';
                tips.innerHTML = '<li>右下の「処理ログを表示」から、裏側の動作を確認できます。</li><li>この処理には十数秒〜数十秒かかる場合があります。</li>';
            } else if (phaseStr === 'discovery') {
                desc.innerHTML = '現在「要件定義（発見フェーズ）」です。<br>AIが議論の末に抽出した必須要件と、見落としがちなプロの視点を確認してください。';
                tips.innerHTML = '<li>内容に問題がなければ、次の「ウィザード」へ進みます。</li><li>セーブしてここで終了し、後日再開することも可能です。</li>';
            } else if (phaseStr === 'wizard') {
                desc.innerHTML = '現在「プロンプト組み立て（ウィザード）」です。<br>AIが生成した具体的な選択肢を選んでいくだけで、極上のプロンプトが完成します。';
                tips.innerHTML = '<li>わからない場合は「今はわからない」を選んでも構いません。</li><li>自由記述でオリジナルな案を組み込むことも可能です。</li>';
            } else if (phaseStr === 'output') {
                desc.innerHTML = '現在「最終プロンプト出力」です。<br>生成されたプロンプトをコピーして、ChatGPTやClaude等のAIにそのまま貼り付けてください。';
                tips.innerHTML = '<li>「共創スタイル」を切り替えることで、AIの役割（PM・クリエイターなど）を調整できます。</li><li>追加で独自の指示を記述することも可能です。</li>';
            }
        }

        window.onload = function() {
            loadHistoryFromStorage();
            initCustomTemplates();
        };

        function openSaveModal() {
            const modal = document.getElementById('saveConfirmModal');
            const content = document.getElementById('saveConfirmContent');
            modal.classList.remove('hidden');
            setTimeout(() => {
                content.classList.remove('scale-95', 'opacity-0');
                content.classList.add('scale-100', 'opacity-100');
            }, 10);
        }

        function closeSaveModal() {
            const modal = document.getElementById('saveConfirmModal');
            const content = document.getElementById('saveConfirmContent');
            content.classList.remove('scale-100', 'opacity-100');
            content.classList.add('scale-95', 'opacity-0');
            setTimeout(() => {
                modal.classList.add('hidden');
            }, 200);
        }

        function confirmSaveAndFinish() {
            saveCurrentProject(true); // pass flag to indicate finishing
            closeSaveModal();
            setTimeout(() => {
                createNewProject();
                showToast('保存しました。新規画面に戻りました。', 'success');
            }, 500);
        }

        function toggleSaveDrawer() {
            const drawer = document.getElementById('saveDrawer');
            if (drawer.classList.contains('hidden')) drawer.classList.remove('hidden');
            else drawer.classList.add('hidden');
        }
        
        function toggleInitialInfo() {
            const popup = document.getElementById('initialInfoPopup');
            if (popup.classList.contains('hidden')) popup.classList.remove('hidden');
            else popup.classList.add('hidden');
        }

        function exportProject() {
            const history = localStorage.getItem('kazuma_booster_history_v2_1') || '[]';
            const templates = localStorage.getItem('kazuma_booster_custom_templates') || '[]';
            
            const exportData = {
                version: "2.1",
                timestamp: new Date().toISOString(),
                history: JSON.parse(history),
                customTemplates: JSON.parse(templates)
            };
            
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(exportData, null, 2));
            const dlAnchorElem = document.createElement('a');
            dlAnchorElem.setAttribute("href", dataStr);
            dlAnchorElem.setAttribute("download", `preput_dashboard_backup_${new Date().toISOString().split('T')[0]}.json`);
            dlAnchorElem.click();
            showToast("全データの書き出し（Export）が完了しました。", "success");
        }

        function importProject(event) {
            const file = event.target.files[0];
            if (!file) return;
            
            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const importedData = JSON.parse(e.target.result);
                    if (importedData.history) {
                        localStorage.setItem('kazuma_booster_history_v2_1', JSON.stringify(importedData.history));
                        projectHistory = importedData.history;
                    }
                    if (importedData.customTemplates) {
                        localStorage.setItem('kazuma_booster_custom_templates', JSON.stringify(importedData.customTemplates));
                        if (typeof customTemplates !== 'undefined') customTemplates = importedData.customTemplates;
                    }
                    renderHistoryList();
                    if (typeof renderCustomTemplatesList === 'function') renderCustomTemplatesList();
                    showToast("データの読み込み（Import）が完了しました！", "success");
                } catch (error) {
                    showToast("ファイルの読み込みに失敗しました。正しいJSONファイルを選択してください。", "error");
                    console.error("Import error:", error);
                }
            };
            reader.readAsText(file);
            event.target.value = ''; // Reset input
        }

        function loadHistoryFromStorage() {
            const data = localStorage.getItem('kazuma_booster_history_v2_1');
            projectHistory = data ? (JSON.parse(data) || []) : [];
            renderHistoryList();
        }

        function saveHistoryToStorage() {
            localStorage.setItem('kazuma_booster_history_v2_1', JSON.stringify(projectHistory));
            renderHistoryList();
        }

        function renderHistoryList() {
            const container = document.getElementById('historyList');
            document.getElementById('savedCount').innerText = `${projectHistory.length} Saves`;
            
            if (projectHistory.length === 0) {
                container.innerHTML = `<div class="text-slate-400 text-sm text-center py-12 col-span-full font-medium">保存されたプロジェクトはここにストックされます</div>`;
                return;
            }

            container.innerHTML = '';
            projectHistory.forEach(proj => {
                const item = document.createElement('div');
                item.className = "group relative flex flex-col p-5 rounded-2xl bg-white border border-slate-200 hover:border-teal-500 hover:shadow-lg transition-all cursor-pointer";
                item.setAttribute('onclick', `loadSavedProject('${proj.id}')`);
                
                item.innerHTML = `
                    <div class="flex justify-between items-start mb-3">
                        <div class="text-base font-bold text-slate-800 truncate pr-4 leading-tight">${proj.name}</div>
                        <button onclick="event.stopPropagation(); deleteSavedProject('${proj.id}')" 
                                class="opacity-0 group-hover:opacity-100 text-slate-400 hover:text-red-500 transition-all p-1">
                            <i class="fa-solid fa-trash-can text-base"></i>
                        </button>
                    </div>
                    <div class="text-xs text-slate-400 font-mono font-medium">${proj.timestamp}</div>
                `;
                container.appendChild(item);
            });
        }

        function saveCurrentProject(isSilent = false) {
            let name = document.getElementById('projectIdea').value.trim();
            if (!name) name = "無題のプロジェクト";

            const timeString = new Date().toLocaleString('ja-JP', { hour12: false });
            const existingIdx = projectHistory.findIndex(p => p.name === name);

            const savedDeepVars = rawDeepVars.map(v => ({
                ...v,
                checked: document.getElementById(v.id) ? document.getElementById(v.id).checked : true
            }));

            const goals = document.getElementById('level1Goals').value.trim();
            const constraints = document.getElementById('level1Constraints').value.trim();
            let level1Combined = "";
            if (goals) level1Combined += `【目標・ビジョン】\n${goals}\n\n`;
            if (constraints) level1Combined += `【前提ルール・制約】\n${constraints}`;
            if (!level1Combined) level1Combined = "(特になし)";

            const isFinished = !document.getElementById('outputArea').classList.contains('hidden');
            const finalPrompt = document.getElementById('finalPromptResult') ? document.getElementById('finalPromptResult').value : '';

            const projectObj = {
                id: existingIdx !== -1 ? projectHistory[existingIdx].id : crypto.randomUUID(),
                name: name,
                level1: level1Combined,
                goals: goals,
                constraints: constraints,
                depth: document.getElementById('analysisDepth').value,
                timestamp: timeString,
                answers: { ...wizardAnswers },
                deepVars: savedDeepVars,
                questions: wizardQuestions,
                rawBaseVars: rawBaseVars,
                
                // --- Extended persistence fields ---
                activePromptStyle: activePromptStyle,
                customInstructions: document.getElementById('customInstructionsInput') ? document.getElementById('customInstructionsInput').value : '',
                runMode: document.getElementById('runMode').value,
                isFinished: isFinished,
                finalPrompt: finalPrompt
            };

            if (existingIdx !== -1) {
                projectHistory[existingIdx] = projectObj;
                if(!isSilent) showToast('既存のセーブデータを更新しました！', 'info');
            } else {
                projectHistory.unshift(projectObj);
                if(!isSilent) showToast('新規セーブデータとして保存しました！', 'success');
            }
            saveHistoryToStorage();
        }

        function loadSavedProject(id) {
            const proj = projectHistory.find(p => p.id === id);
            if (!proj) return;

            document.getElementById('projectIdea').value = proj.name;
            if (proj.goals !== undefined || proj.constraints !== undefined) {
                document.getElementById('level1Goals').value = proj.goals || '';
                document.getElementById('level1Constraints').value = proj.constraints || '';
            } else if (proj.level1) {
                document.getElementById('level1Goals').value = proj.level1;
                document.getElementById('level1Constraints').value = '';
            } else {
                document.getElementById('level1Goals').value = '';
                document.getElementById('level1Constraints').value = '';
            }
            document.getElementById('analysisDepth').value = proj.depth || 'standard';

            // Restore runMode
            if (proj.runMode) {
                document.getElementById('runMode').value = proj.runMode;
            }

            showToast(`プロジェクト『${proj.name}』をロードしました。`, 'info');

            if (proj.rawBaseVars && proj.rawBaseVars.length > 0) {
                document.getElementById('phase1').classList.add('hidden');
                document.getElementById('appHeader').classList.add('hidden');
                document.getElementById('phase2').classList.remove('hidden');
                document.getElementById('phase2').classList.add('flex');
                const phase2El = document.getElementById('phase2');
                if (phase2El) {
                    phase2El.scrollIntoView({ behavior: 'smooth', block: 'start' });
                }
                document.getElementById('displayIdea').innerText = proj.name;
                document.getElementById('displayLevel1').innerText = proj.level1 || '(なし)';
                document.getElementById('displayDepth').innerText = proj.depth || 'STANDARD';
                
                const drawer = document.getElementById('saveDrawer');
                if (!drawer.classList.contains('hidden')) drawer.classList.add('hidden');
                
                rawBaseVars = proj.rawBaseVars;
                rawDeepVars = proj.deepVars || [];
                wizardQuestions = proj.questions || [];
                wizardAnswers = proj.answers || {};

                document.getElementById('appHeader').classList.add('hidden');
                document.getElementById('tabDiscovery').classList.remove('hidden');
                document.getElementById('tabWizard').classList.remove('hidden');

                // Restore custom instructions and styles if they exist
                if (proj.customInstructions !== undefined) {
                    const customInput = document.getElementById('customInstructionsInput');
                    if (customInput) {
                        customInput.value = proj.customInstructions;
                        customText = proj.customInstructions;
                    }
                }
                if (proj.activePromptStyle) {
                    activePromptStyle = proj.activePromptStyle;
                }

                // If project was finished (Phase 4), directly restore final prompt screen
                if (proj.isFinished) {
                    document.getElementById('tabOutput').classList.remove('hidden');
                    switchTab('output');
                    setAgentPhase(4); // Set to final phase
                    
                    // Activate setPromptStyle UI state
                    if (activePromptStyle) {
                        setPromptStyle(activePromptStyle);
                    }
                    
                    // Restore exact prompt text (in case of manual edits) or re-compile
                    const promptArea = document.getElementById('finalPromptResult');
                    if (promptArea) {
                        if (proj.finalPrompt) {
                            promptArea.value = proj.finalPrompt;
                        } else {
                            compileFinalPrompt();
                        }
                    }
                } else if (wizardQuestions.length > 0) {
                    renderDeepVarsReview();
                    switchTab('wizard');
                    setAgentPhase(3.5, 6);
                } else {
                    renderDiscoveryReport(rawBaseVars, rawDeepVars);
                    switchTab('discovery');
                    setAgentPhase(2.5);
                }
            } else {
                createNewProject();
            }
        }

        function deleteSavedProject(id) {
            projectHistory = projectHistory.filter(p => p.id !== id);
            saveHistoryToStorage();
            showToast('セーブデータを削除しました。', 'info');
        }

        function createNewProject() {
            document.getElementById('appHeader').classList.remove('hidden');
            document.getElementById('phase2').classList.add('hidden');
            document.getElementById('phase2').classList.remove('flex');
            document.getElementById('phase1').classList.remove('hidden');
            document.getElementById('phase1').classList.add('flex');
            
            document.getElementById('projectIdea').value = '';
            document.getElementById('level1Goals').value = '';
            document.getElementById('level1Constraints').value = '';
            const guideCard = document.getElementById('presetGuideCard');
            if (guideCard) guideCard.classList.add('hidden');
            
            document.getElementById('wizardContainer').classList.add('hidden');
            document.getElementById('deepVarsContainerUI').classList.add('hidden');
            document.getElementById('tabDiscovery').classList.add('hidden');
            document.getElementById('tabWizard').classList.add('hidden');
            document.getElementById('tabOutput').classList.add('hidden');
            
            const drawer = document.getElementById('saveDrawer');
            if (!drawer.classList.contains('hidden')) drawer.classList.add('hidden');
            
            setAgentPhase(1);
            showToast('新規プロジェクト用の入力画面を展開しました。', 'info');
        }

        function showToast(message, type = 'success') {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            let bgClass = 'bg-white border-slate-200 text-slate-800 shadow-2xl';
            let iconClass = 'fa-circle-check text-teal-500';
            if (type === 'error') iconClass = 'fa-circle-exclamation text-red-500';
            else if (type === 'info') iconClass = 'fa-circle-info text-blue-500';

            toast.className = `flex items-center gap-4 p-5 rounded-2xl border transition-all duration-300 transform translate-y-4 opacity-0 pointer-events-auto ${bgClass}`;
            toast.innerHTML = `<i class="fa-solid ${iconClass} text-2xl shrink-0"></i><div class="text-sm font-bold leading-relaxed">${message}</div>`;
            container.appendChild(toast);
            setTimeout(() => toast.classList.remove('translate-y-4', 'opacity-0'), 10);
            setTimeout(() => { toast.classList.add('translate-y-4', 'opacity-0'); setTimeout(() => toast.remove(), 300); }, 4500);
        }

        function switchTab(tab) {
            currentTab = tab;
            updateHelpContext(tab);
            const tabOrder = ['terminal', 'discovery', 'wizard', 'output'];
            const currentIndex = tabOrder.indexOf(tab);

            const btns = [document.getElementById('tabTerminal'), document.getElementById('tabDiscovery'), document.getElementById('tabWizard'), document.getElementById('tabOutput')];
            const areas = [document.getElementById('terminalArea'), document.getElementById('discoveryArea'), document.getElementById('wizardArea'), document.getElementById('outputArea')];

            btns.forEach((b, idx) => { 
                if(b) {
                    b.classList.remove('active', 'completed');
                    if (idx < currentIndex) b.classList.add('completed');
                }
            });
            areas.forEach(a => { if(a) a.classList.add('hidden'); });

            const activateTab = (btnId, areaId) => {
                const btn = document.getElementById(btnId);
                const area = document.getElementById(areaId);
                if (btn) { btn.classList.add('active'); btn.classList.remove('hidden'); }
                if (area) area.classList.remove('hidden');
            };

            if (tab === 'terminal') activateTab('tabTerminal', 'terminalArea');
            if (tab === 'discovery') { activateTab('tabDiscovery', 'discoveryArea'); document.getElementById('discoveryReadyBadge').classList.add('hidden'); }
            if (tab === 'wizard') { activateTab('tabWizard', 'wizardArea'); const wBadge = document.getElementById('wizardReadyBadge'); if (wBadge) wBadge.classList.add('hidden'); }
            if (tab === 'output') activateTab('tabOutput', 'outputArea');

            const pBar = document.getElementById('tabProgressBar');
            if(pBar) pBar.style.width = `${((currentIndex + 1) / 4) * 100}%`;
        }

                const agentNames = ["", "STRATEGY", "TECH", "DESIGN", "BUSINESS", "COMPILER", "WIZARD"];
        const agentTextColors = ["", "text-indigo-500", "text-cyan-500", "text-purple-500", "text-amber-500", "text-emerald-500", "text-rose-500"];
        const agentBgColors = ["bg-teal-500", "bg-indigo-500", "bg-cyan-500", "bg-purple-500", "bg-amber-500", "bg-emerald-500", "bg-rose-500"];
        const agentShadows = ["shadow-[0_0_10px_rgba(20,184,166,0.8)]", "shadow-[0_0_10px_rgba(99,102,241,0.8)]", "shadow-[0_0_10px_rgba(6,182,212,0.8)]", "shadow-[0_0_10px_rgba(168,85,247,0.8)]", "shadow-[0_0_10px_rgba(245,158,11,0.8)]", "shadow-[0_0_10px_rgba(16,185,129,0.8)]", "shadow-[0_0_10px_rgba(244,63,94,0.8)]"];
        const agentGradients = ["gradient-bg-light", "gradient-bg-indigo", "gradient-bg-cyan", "gradient-bg-purple", "gradient-bg-amber", "gradient-bg-emerald", "gradient-bg-rose"];

        function toggleLogWidget() {
            const widget = document.getElementById('logWidget');
            if (widget) {
                widget.classList.toggle('translate-y-[120%]');
            }
        }

        let activePromptStyle = 'pm';
        let customInstructionText = '';
        let compiledData = {
            idea: '',
            level1: '',
            knowns: [],
            unknowns: [],
            deepStates: []
        };

        function setAgentPhase(phase, activeAgentId = 0) {
            // phase: 1 (Setup), 2 (Analysis/Debate), 2.5 (Discovery Report), 3 (Wizard Builder Generating), 3.5 (Wizard Answering), 4 (Final Prompt)
            // activeAgentId: 0 to 6 (corresponds to Agent 1 to 6)
            
            const agentBaseColors = ["", "indigo", "cyan", "purple", "amber", "emerald", "rose"];
            
            for (let i = 1; i <= 6; i++) {
                const el = document.getElementById(`stat-${i}`);
                const statText = document.getElementById(`stat-text-${i}`);
                if (!el || !statText) continue;
                
                const avatar = el.querySelector('.h-8.w-8');
                
                // Clear any animations or border rings
                if (avatar) avatar.className = avatar.className.replace(/\banimate-\w+\b/g, '').replace(/\bring-\w+\b/g, '').replace(/\bring-offset-\d+\b/g, '');
                
                // Determine the state of this agent
                let state = 'standby'; // 'standby' | 'working' | 'active' | 'complete'
                
                if (phase === 1) {
                    state = 'standby';
                } else if (phase === 2) {
                    if (i < activeAgentId) state = 'complete';
                    else if (i === activeAgentId) state = 'working';
                    else state = 'standby';
                } else if (phase === 2.5) {
                    if (i <= 5) state = 'idle';
                    else state = 'standby';
                } else if (phase === 3) {
                    if (i <= 5) state = 'idle';
                    else if (i === 6) state = 'working';
                } else if (phase === 3.5) {
                    if (i <= 5) state = 'idle';
                    else if (i === 6) state = 'active';
                } else if (phase === 4) {
                    state = 'complete';
                }
                
                // Style according to state
                if (state === 'complete') {
                    el.className = "flex items-center gap-3 px-4 py-2 rounded-xl bg-emerald-50/60 border border-emerald-200 text-sm shadow-sm transition-all duration-300";
                    statText.innerText = "COMPLETE";
                    statText.className = "text-xs text-emerald-600 font-mono font-bold flex items-center gap-1";
                    
                    // Add a tiny check icon to indicate complete
                    if (!statText.innerHTML.includes('fa-circle-check')) {
                        statText.innerHTML = '<i class="fa-solid fa-circle-check text-xs"></i> COMPLETE';
                    }
                    
                    if (avatar) {
                        avatar.className = avatar.className.replace(/bg-\w+-100/g, 'bg-emerald-100').replace(/text-\w+-600/g, 'text-emerald-600');
                    }
                } else if (state === 'working') {
                    el.className = `flex items-center gap-3 px-4 py-2 rounded-xl bg-white border-2 border-${agentBaseColors[i]}-400 text-sm shadow-md transition-all duration-300`;
                    statText.innerText = "WORKING...";
                    statText.className = `text-xs ${agentTextColors[i]} font-mono font-bold animate-pulse`;
                    
                    if (avatar) {
                        avatar.classList.add('animate-pulse');
                    }
                } else if (state === 'active') {
                    el.className = `flex items-center gap-3 px-4 py-2 rounded-xl bg-white border-2 border-${agentBaseColors[i]}-400 text-sm shadow-md transition-all duration-300`;
                    statText.innerText = "ACTIVE";
                    statText.className = `text-xs ${agentTextColors[i]} font-mono font-bold flex items-center gap-1`;
                    statText.innerHTML = `<span class="h-1.5 w-1.5 rounded-full ${agentBgColors[i]} animate-ping"></span> ACTIVE`;
                    
                    if (avatar) {
                        avatar.classList.add('animate-pulse');
                    }
                } else if (state === 'idle') {
                    // Completed analysis - show original colors for reference
                    el.className = `flex items-center gap-3 px-4 py-2 rounded-xl bg-white border border-${agentBaseColors[i]}-100 text-sm transition-all duration-300`;
                    statText.className = `text-xs ${agentTextColors[i]} font-mono font-bold flex items-center gap-1`;
                    statText.innerHTML = `<i class="fa-solid fa-circle-check text-xs text-emerald-400 mr-0.5"></i> ${agentNames[i]}`;
                    
                    if (avatar) {
                        avatar.className = avatar.className.replace(/bg-\w+-100/g, `bg-${agentBaseColors[i]}-100`).replace(/text-\w+-600/g, `text-${agentBaseColors[i]}-600`);
                    }
                } else {
                    // Standby
                    el.className = "flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50/50 border border-slate-100 text-sm transition-all duration-300 opacity-60";
                    statText.innerText = "STANDBY";
                    statText.className = "text-xs text-slate-400 font-mono font-bold";
                    
                    // Restore original agent colors for the standby avatar
                    if (avatar) {
                        avatar.className = avatar.className.replace(/bg-\w+-100/g, `bg-${agentBaseColors[i]}-100`).replace(/text-\w+-600/g, `text-${agentBaseColors[i]}-600`);
                    }
                    
                    // If this is Agent 6 (Wizard) during Discovery Report, let's make it look ready with a subtle rose pulse to prompt user
                    if (phase === 2.5 && i === 6) {
                        el.className = "flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 border border-rose-100 text-sm transition-all duration-300";
                        statText.innerText = "READY";
                        statText.className = "text-xs text-rose-500 font-mono font-bold flex items-center gap-1";
                        statText.innerHTML = '<span class="h-1.5 w-1.5 rounded-full bg-rose-500 animate-pulse"></span> READY';
                    }
                }
            }
            
            // Set header/terminal background gradient and progress bar according to active agent
            if (activeAgentId >= 0 && activeAgentId <= 6) {
                const termArea = document.getElementById('terminalArea');
                if (termArea) {
                    termArea.className = termArea.className.replace(/gradient-bg-\w+/, agentGradients[activeAgentId]);
                }
                const pBar = document.getElementById('progressBar');
                if (pBar) {
                    pBar.className = pBar.className.replace(/bg-\w+-500/, agentBgColors[activeAgentId]);
                    pBar.className = pBar.className.replace(/shadow-\[[^\]]+\]/, agentShadows[activeAgentId]);
                }
            }
            
            // Toggle global status visibility
            if (phase === 1 || phase === 4 || phase === 2.5) {
                const globalStatusContainer = document.getElementById('currentGlobalStatus');
                if (globalStatusContainer) {
                    globalStatusContainer.classList.add('hidden');
                    globalStatusContainer.classList.remove('flex');
                }
            }
        }

        function getSection4Text(style, idea, customText) {
            const pIdea = idea || "無題のプロジェクト";
            if (style === 'pm') {
                return `『私は『${pIdea}』をプロジェクトマネージャー（PM）として開始します。
上記の「1階の基本確定要件」と「2階の見落としポイント対策」をロードし、これらを考慮した工程表（WBS）とマイルストーンを作成せよ。
まずは、この前提条件に対する合意と評価を簡潔に述べた後、以下のステップで進めてください：
1. 制作・開発マイルストーン（初期、中間、最終段階）の提示
2. 今すぐ実行すべき「3つのToDoタスク」
3. 推奨する進行スケジュール案』`;
            } else if (style === 'creator') {
                return `『私は『${pIdea}』のメインクリエイターおよびブレストパートナーとして起動します。
上記の「1階の基本確定要件」と「2階の見落としポイント対策」をベースの前提知識としてロードせよ。
まずは、この設定から感じられる本質的な魅力と方向性についてクリエイティブなフィードバックを述べた後、以下のステップで進めてください：
1. 初期ブレストとして、今すぐ形にできる具体的な「キャラクター設定案」や「デザイン／構成案」を3つ提案してください。
2. その提案がターゲットに響く理由と、その魅力を最大化するアプローチ。
3. 次に進むための具体的なドラフト案作成に向けた問いかけ』`;
            } else if (style === 'auditor') {
                return `『私は『${pIdea}』の最高リスク監査役（オフィシャルアドバイザー）として起動します。
上記の「1階の基本確定要件」と「2階の見落としポイント対策」を精査し、初心者が最も陥りやすい致命的なリスクをロードせよ。
まずは、この仕様に対するリスク監査コメントをプロフェッショナルとして辛口で述べた後、以下のステップで進めてください：
1. このまま進めた場合に発生しうる「法的リスク」や「規約違反」「品質低下」の具体的な3点
2. それぞれの致命傷を完全に回避するための「予防策・代替アプローチ」
3. 安全にリリースするための必須品質チェックリスト』`;
            } else if (style === 'custom') {
                const instructions = customText || '特にカスタムの指定はありません。';
                return `『私は『${pIdea}』の共創パートナーとして起動します。
上記の「1階の基本確定要件」と「2階の見落としポイント対策」をすべてベースの前提知識としてロードせよ。

【ユーザーによる追加・カスタム指示】
${instructions}

まずは、上記の前提条件と追加指示に対する確認と、このプロジェクトを成功に導くための最初のステップを具体的に提示してください。』`;
            }
            return '';
        }

        function setPromptStyle(style) {
            activePromptStyle = style;
            const buttons = {
                pm: { id: 'btn-style-pm', activeClass: 'bg-indigo-50 border-indigo-400 text-indigo-700 ring-1 ring-indigo-200 shadow-sm' },
                creator: { id: 'btn-style-creator', activeClass: 'bg-purple-50 border-purple-400 text-purple-700 ring-1 ring-purple-200 shadow-sm' },
                auditor: { id: 'btn-style-auditor', activeClass: 'bg-emerald-50 border-emerald-400 text-emerald-700 ring-1 ring-emerald-200 shadow-sm' },
                custom: { id: 'btn-style-custom', activeClass: 'bg-amber-50 border-amber-400 text-amber-700 ring-1 ring-amber-200 shadow-sm' }
            };

            // Reset buttons (keep layout classes like relative, pt-8, p-4, flex, bg-white, etc.)
            Object.keys(buttons).forEach(k => {
                const btn = document.getElementById(buttons[k].id);
                if (btn) {
                    btn.className = "relative pt-8 p-4 rounded-xl border text-left transition-all duration-200 flex flex-col gap-1.5 cursor-pointer bg-white border-slate-200 text-slate-500 hover:border-slate-300 hover:text-slate-700 shadow-sm animate-pulse-once";
                }
            });

            // Set active class (keep layout classes but merge activeColor classes)
            const activeBtn = document.getElementById(buttons[style].id);
            if (activeBtn) {
                activeBtn.className = `relative pt-8 p-4 rounded-xl border text-left transition-all duration-200 flex flex-col gap-1.5 cursor-pointer shadow-md ${buttons[style].activeClass}`;
            }

            // Show/hide custom text wrapper
            const customWrapper = document.getElementById('customInstructionsWrapper');
            if (customWrapper) {
                if (style === 'custom') {
                    customWrapper.classList.remove('hidden');
                    customWrapper.classList.add('flex');
                } else {
                    customWrapper.classList.add('hidden');
                    customWrapper.classList.remove('flex');
                }
            }

            // Update explanation and recommendations based on user idea keywords
            updateStyleGuidePanel(style);

            // Trigger prompt compile
            compileFinalPrompt();
            
            // Flash and glow effect on textarea for immediate visual feedback
            const promptArea = document.getElementById('finalPromptResult');
            if (promptArea) {
                promptArea.classList.add('ring-4', 'ring-teal-500/20', 'bg-teal-50/10', 'transition-all', 'duration-300');
                setTimeout(() => {
                    promptArea.classList.remove('ring-4', 'ring-teal-500/20', 'bg-teal-50/10');
                }, 500);
            }
        }

        function updateStyleGuidePanel(style) {
            const panel = document.getElementById('styleGuidePanel');
            if (!panel) return;

            const idea = (document.getElementById('projectIdea').value || '').trim();
            
            // Check keywords to determine the recommendation guide
            let isSticker = idea.includes('スタンプ') || idea.includes('イラスト') || idea.includes('画像');
            let isBlog = idea.includes('ブログ') || idea.includes('記事') || idea.includes('アフィリエイト');
            let isApp = idea.includes('アプリ') || idea.includes('SaaS') || idea.includes('開発') || idea.includes('システム');

            let styleInfo = {
                pm: {
                    title: '👔 プロジェクトマネジメント・段取り型 (PM Style)',
                    desc: 'プロジェクトの全体スケジュール設計、マイルストーン策定、そして「今何から始めるべきか」を具体的にToDoタスク化するのに最も適したプロンプトです。AIを優秀な伴走PMとして起動させます。',
                    stage: '',
                    bgColor: 'bg-indigo-100 text-indigo-700'
                },
                creator: {
                    title: '🎨 クリエイティブ共同制作型 (Creator Style)',
                    desc: 'AIをあなたの右腕クリエイター、ブレスト相手として起動します。具体的なアイデア出し、デザイン案のブレスト、文章の下書き・コピーライティングなど、コンテンツを一緒に生み出すクリエイティブ工程に最適です。',
                    stage: '',
                    bgColor: 'bg-purple-100 text-purple-700'
                },
                auditor: {
                    title: '🔍 プロのリスク監査・アドバイザー型 (Auditor Style)',
                    desc: 'AIを辛口な最高リスク監査役（アドバイザー）として起動します。規約違反、著作権問題、商用利用基準の抜け漏れ、初心者が陥る落とし穴などをチェックし、リリース前に安全性を確認するリスクヘッジ工程に最適です。',
                    stage: '',
                    bgColor: 'bg-emerald-100 text-emerald-700'
                },
                custom: {
                    title: '✍️ 自由カスタマイズ・指示追加型 (Custom Style)',
                    desc: '上記の確定した要件に加え、あなた独自の追加指示（「回答を表形式にする」「英語で出力する」「〜の口調にする」など）を自由に注入し、AIとの共創スタイルを完全オーダーメイドで設計します。',
                    stage: '【活用例】「回答は箇条書きの表形式で出力してください。」や「AIに特定のフォーマットで応答させたい」など、自分なりのやり方がある上級フェーズ',
                    bgColor: 'bg-teal-100 text-teal-700'
                }
            };

            // Dynamic recommendations based on category
            if (isSticker) {
                styleInfo.pm.stage = '<strong>【おすすめの作業・段階】</strong>：LINEスタンプ制作スケジュールや画材・ソフトの調達・手間の管理に適しています。';
                styleInfo.creator.stage = '<strong>【おすすめの作業・段階】</strong>：スタンプのキャラクターアイデア、表情、メッセージ（セリフ）のブレストに向いています。';
                styleInfo.auditor.stage = '<strong>【おすすめの作業・段階】</strong>：LINE公式の審査ガイドライン（知的財産権、公序良俗など）への準拠、AIモデルの商用利用チェックに適しています。';
            } else if (isBlog) {
                styleInfo.pm.stage = '<strong>【おすすめの作業・段階】</strong>：ブログ記事の骨組み（H2/H3構成案）の段取り、定期更新の執筆スケジュールの設計に向いています。';
                styleInfo.creator.stage = '<strong>【おすすめの作業・段階】</strong>：読者の心をつかむタイトル、キャッチコピー、または書き出し文章（リード文）の下書きのブレストに向いています。';
                styleInfo.auditor.stage = '<strong>【おすすめの作業・段階】</strong>：YMYL（健康・お金など）分野での信頼性チェックや、アフィリエイト表現のポリシー違反チェックに適しています。';
            } else if (isApp) {
                styleInfo.pm.stage = '<strong>【おすすめの作業・段階】</strong>：MVP（最小限機能）のスコープ決定や、機能の実装スケジュール（WBS）の策定に向いています。';
                styleInfo.creator.stage = '<strong>【おすすめの作業・段階】</strong>：アプリのUI設計、コンポーネント構成、コードの実装案の作成フェーズに向いています。';
                styleInfo.auditor.stage = '<strong>【おすすめの作業・段階】</strong>：セキュリティ上の脆弱性チェック、データベースのデータ破損対策、利用規約の整備監査に適しています。';
            } else {
                styleInfo.pm.stage = '<strong>【おすすめの作業・段階】</strong>：プロジェクトの全体スケジュール設計や、優先順位の高いToDoリストの作成に向いています。';
                styleInfo.creator.stage = '<strong>【おすすめの作業・段階】</strong>：具体的なアイデア出し、文章やコードの最初のドラフト作成に適しています。';
                styleInfo.auditor.stage = '<strong>【おすすめの作業・段階】</strong>：見落とした落とし穴（法的リスク、規約、品質など）をリリース前に監査・予防するのに適しています。';
            }

            const info = styleInfo[style];
            const explanationPreview = getSection4Text(style, idea, customInstructionText);

            panel.className = `p-5 bg-slate-50 border border-slate-200 rounded-xl flex flex-col gap-3.5 font-sans transition-all duration-300 shadow-sm`;
            panel.innerHTML = `
                <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                    <span class="px-2.5 py-0.75 rounded text-xs font-black tracking-wide ${info.bgColor}">${info.title}</span>
                </div>
                <p class="text-sm text-slate-700 leading-relaxed font-bold">
                    ${info.desc}
                </p>
                <div class="text-xs sm:text-sm text-teal-800 bg-teal-50 border border-teal-100 p-3.5 rounded-lg font-bold leading-relaxed">
                    ${info.stage}
                </div>
                <div class="mt-3 border-t border-slate-200 pt-3.5 flex flex-col gap-2">
                    <span class="text-xs text-slate-500 font-black tracking-wider uppercase flex items-center gap-1">
                        <i class="fa-solid fa-code"></i> AIへの具体的な追加指示（プレビュー）
                    </span>
                    <pre class="p-3.5 bg-white border border-slate-200 text-slate-600 shadow-inner rounded-lg text-xs leading-relaxed overflow-x-auto whitespace-pre-wrap font-mono font-bold select-all">${explanationPreview}</pre>
                </div>
            `;
        }

        function updateCustomInstructions(text) {
            customInstructionText = text.trim();
            compileFinalPrompt();
            updateStyleGuidePanel('custom');
        }

        function compileFinalPrompt() {
            const data = compiledData;
            const idea = data.idea || "無題のプロジェクト";
            
            const section4Text = getSection4Text(activePromptStyle, idea, customInstructionText);

            const formattedPrompt = `# 【設定済み】プロジェクト要件・コンテキスト指示書
このプロンプトは、プロジェクト開始前におけるすべての「基本制約」と「陥りやすい盲点」を網羅し、高い解像度でAIと共創を開始するためのものである。

---

## 1. コア・イニシアティブ
* **やろうとしていること:** ${idea}
* **初期の認識条件（レベル1）:**
${data.level1 ? data.level1.split('\n').map(line => `  * ${line}`).join('\n') : '  * 特になし'}

---

## 2. ■ 1階部分：必須基礎確定要件
AIは、以下の基本パラメータに100%厳格に従ったうえで、成果物の第一案を作成しなければならない。
${data.knowns && data.knowns.length > 0 ? data.knowns.join('\n') : '* ※全て未定'}${data.unknownsText || ''}

---

## 3. ■ 2階部分：プロの視点（見落としポイント）対策
AIは、初心者が自滅しやすい以下の「見落としがちな重要ポイント」について、仕様設計段階から完全に解決したロジックを強制的に組み込むこと。
${data.deepStates && data.deepStates.length > 0 ? data.deepStates.join('\n\n') : '* ※指定された重要ポイントはありません。'}

---

## 4. プロの共創開始アクション
この指示書を読み込んだAIは、以下の役割で直ちに起動すること：

${section4Text}`;

            const res = document.getElementById('finalPromptResult');
            if (res) res.value = formattedPrompt;
        }


        function setActiveFlow(id) {
            // Deprecated, mapped to setAgentPhase for backward compatibility
            if (id === 0) {
                setAgentPhase(2.5);
            } else if (id === 6) {
                setAgentPhase(3, 6);
            } else {
                setAgentPhase(2, id);
            }
        }

        function copyGeneratedPrompt() {
            const promptArea = document.getElementById('finalPromptResult');
            if (!promptArea) return;
            
            promptArea.select();
            promptArea.setSelectionRange(0, 99999); // Mobile compatibility
            
            navigator.clipboard.writeText(promptArea.value)
                .then(() => {
                    showToast('プロンプトをクリップボードにコピーしました！', 'success');
                })
                .catch(err => {
                    showToast('コピーに失敗しました。直接テキストを選択してコピーしてください。', 'error');
                    console.error('Failed to copy text: ', err);
                });
        }

        // --- Custom Instructions Templates Logic ---
        let customTemplates = [];

        function initCustomTemplates() {
            try {
                const data = localStorage.getItem('kazuma_booster_custom_templates');
                customTemplates = data ? JSON.parse(data) : [];
            } catch (e) {
                customTemplates = [];
            }
            renderCustomTemplateDropdown();
        }

        function saveCustomTemplate() {
            const text = document.getElementById('customInstructionsInput').value.trim();
            if (!text) {
                showToast('保存する指示テキストが入力されていません。', 'error');
                return;
            }
            const name = prompt('このテンプレートの名前を入力してください：', `テンプレート_${new Date().toLocaleDateString()}`);
            if (name === null) return; // Cancelled
            const finalName = name.trim() || `テンプレート_${Date.now()}`;

            customTemplates.push({
                id: crypto.randomUUID(),
                name: finalName,
                content: text
            });

            localStorage.setItem('kazuma_booster_custom_templates', JSON.stringify(customTemplates));
            renderCustomTemplateDropdown();
            showToast(`テンプレート『${finalName}』を保存しました！`, 'success');
        }

        function loadCustomTemplate(id) {
            if (!id) return;
            const template = customTemplates.find(t => t.id === id);
            if (template) {
                const textarea = document.getElementById('customInstructionsInput');
                textarea.value = template.content;
                updateCustomInstructions(template.content);
                showToast(`テンプレート『${template.name}』を適用しました。`, 'info');
            }
            document.getElementById('customTemplateSelect').value = ""; // Reset select
        }

        function renderCustomTemplateDropdown() {
            const select = document.getElementById('customTemplateSelect');
            if (!select) return;
            select.innerHTML = '<option value="">-- 保存データを選択 --</option>';
            customTemplates.forEach(t => {
                const opt = document.createElement('option');
                opt.value = t.id;
                opt.textContent = t.name;
                select.appendChild(opt);
            });
        }

        function insertCustomPresetText(text) {
            const textarea = document.getElementById('customInstructionsInput');
            if (!textarea) return;
            const start = textarea.selectionStart;
            const end = textarea.selectionEnd;
            const currentVal = textarea.value;
            
            // Insert at cursor or at the end
            if (start !== undefined && end !== undefined) {
                const prefix = currentVal.substring(0, start);
                const suffix = currentVal.substring(end);
                const spacePrefix = (start > 0 && !currentVal[start - 1].match(/\s/)) ? "\n" : "";
                const spaceSuffix = (suffix.length > 0 && !suffix[0].match(/\s/)) ? "\n" : "";
                textarea.value = prefix + spacePrefix + text + spaceSuffix + suffix;
                textarea.selectionStart = textarea.selectionEnd = start + spacePrefix.length + text.length;
            } else {
                textarea.value = (currentVal ? currentVal + "\n" : "") + text;
            }
            
            textarea.focus();
            updateCustomInstructions(textarea.value);
            showToast('追加指示チップを挿入しました！', 'success');
        }

        function writeToConsole(expertName, logText, type = 'strategy') {
            const time = new Date().toLocaleTimeString();
            let color = 'text-slate-400';
            let bgColor = 'text-slate-600';
            let icon = '<i class="fa-solid fa-robot mr-2"></i>';
            if (type === 'strategy') { color = 'text-indigo-400'; bgColor = 'text-indigo-600'; icon = '<i class="fa-solid fa-chess-knight mr-2"></i>'; }
            if (type === 'technical') { color = 'text-cyan-400'; bgColor = 'text-cyan-600'; icon = '<i class="fa-solid fa-ruler-combined mr-2"></i>'; }
            if (type === 'design') { color = 'text-purple-400'; bgColor = 'text-purple-600'; icon = '<i class="fa-solid fa-pen-nib mr-2"></i>'; }
            if (type === 'business') { color = 'text-amber-400'; bgColor = 'text-amber-600'; icon = '<i class="fa-solid fa-chart-line mr-2"></i>'; }
            if (type === 'compiler') { color = 'text-teal-400'; bgColor = 'text-teal-600'; icon = '<i class="fa-solid fa-filter mr-2"></i>'; }
            if (type === 'builder') { color = 'text-rose-400'; bgColor = 'text-rose-600'; icon = '<i class="fa-solid fa-wand-magic-sparkles mr-2"></i>'; }

            const block = document.createElement('div');
            block.className = `mb-6 pb-5 border-b border-slate-800/50 fade-in`;
            block.innerHTML = `<div class="font-bold text-sm ${color} mb-2 flex items-center">${icon}[${time}] ${expertName}</div><div class="pl-6 text-xs text-slate-300 whitespace-pre-wrap font-sans leading-relaxed">${logText}</div>`;
            logArea.appendChild(block);
            const cl = document.getElementById('consoleLog');
            if (cl) cl.scrollTo({ top: cl.scrollHeight, behavior: 'smooth' });

            // Update Global Status Indicator
            const globalStatusContainer = document.getElementById('currentGlobalStatus');
            const globalStatusText = document.getElementById('currentGlobalStatusText');
            if (globalStatusContainer && globalStatusText) {
                if (type === 'system' || logText.includes('完了') || logText.includes('出力しました') || logText.length > 50 || logText.includes('\n')) {
                    globalStatusContainer.classList.add('hidden');
                    globalStatusContainer.classList.remove('flex');
                } else {
                    globalStatusContainer.classList.remove('hidden');
                    globalStatusContainer.classList.add('flex');
                    globalStatusText.innerText = logText;
                    
                    const spinnerIcon = globalStatusContainer.querySelector('i');
                    const statusColorMap = { strategy: 'indigo', technical: 'cyan', design: 'purple', business: 'amber', marketing: 'amber', compiler: 'emerald', builder: 'rose' };
                    const sc = statusColorMap[type] || 'teal';
                    spinnerIcon.className = `fa-solid fa-circle-notch fa-spin text-xl mr-3 shrink-0 text-${sc}-500`;
                    globalStatusText.className = `text-xs md:text-sm font-extrabold tracking-wide break-words leading-snug w-full text-${sc}-600`;
                }
            }
        }

        let currentApiKeyIndex = 0;

        async function callGeminiAgent(apiKeyString, systemPrompt, userPrompt, isJson = false, retries = 2, model = 'gemini-2.5-flash') {
            const keys = apiKeyString.split(',').map(k => k.trim()).filter(k => k);
            if (keys.length === 0) throw new Error("APIキーが入力されていません。");

            let lastError = null;
            const maxAttempts = Math.max(retries + 1, keys.length * 2);

            const payload = { 
                contents: [{ parts: [{ text: `${systemPrompt}\n\n【ユーザー入力】\n${userPrompt}` }] }],
                generationConfig: { temperature: 0.2 }
            };
            if (isJson) payload.generationConfig.responseMimeType = "application/json";
            
            for (let i = 0; i < maxAttempts; i++) {
                const key = keys[currentApiKeyIndex % keys.length];
                currentApiKeyIndex++;

                const url = `https://generativelanguage.googleapis.com/v1beta/models/${model}:generateContent?key=${key}`;
                
                try {
                    const res = await fetch(url, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(payload) });
                    if (res.ok) {
                        const data = await res.json();
                        return data.candidates[0].content.parts[0].text;
                    }
                    
                    const globalStatusText = document.getElementById('currentGlobalStatusText');
                    const globalStatusContainer = document.getElementById('currentGlobalStatus');
                    
                    if (res.status === 429) {
                        lastError = new Error(`[ERROR-429] APIの無料枠制限に達しました。1分ほど待ってから再試行してください。`);
                        if (keys.length > 1) {
                            writeToConsole('SYSTEM', `API制限(429)を検知。予備キーへローテーションします...`, 'system');
                        }
                        if (globalStatusContainer) {
                            globalStatusContainer.classList.remove('hidden');
                            globalStatusContainer.classList.add('flex');
                        }
                        for(let w = 2; w > 0; w--) {
                            if(globalStatusText) globalStatusText.innerText = `API制限(429)待機中...残り ${w} 秒`;
                            await new Promise(r => setTimeout(r, 1000));
                        }
                        if(globalStatusText) globalStatusText.innerText = `API再試行中...`;
                        continue;
                    }
                    
                    if (res.status >= 500 && i < maxAttempts - 1) {
                        writeToConsole('SYSTEM', `APIエラー(${res.status})を検知。待機して再試行します...`, 'system');
                        if (globalStatusContainer) {
                            globalStatusContainer.classList.remove('hidden');
                            globalStatusContainer.classList.add('flex');
                        }
                        for(let w = 3; w > 0; w--) {
                            if(globalStatusText) globalStatusText.innerText = `API混雑(${res.status})待機中...残り ${w} 秒`;
                            await new Promise(r => setTimeout(r, 1000));
                        }
                        if(globalStatusText) globalStatusText.innerText = `API再試行中...`;
                        continue;
                    }

                    throw new Error(`[ERROR-${res.status}] ${res.statusText}`);
                } catch (e) {
                    lastError = e;
                    if (i === maxAttempts - 1 || !(e.message.includes('429') || e.message.includes('500') || e.message.includes('503'))) {
                        throw e;
                    }
                }
            }
            throw lastError;
        }

        // --- DYNAMIC PROMPT BUILDER ---
        function getDepthInstructions(depthMode) {
            if (depthMode === 'light') {
                return {
                    desc: "【ライトモード】マクロな視点のみで分析してください。極めて重要かつ大枠となる変数のみを少数取り上げ、細かいエッジケースや深すぎる仕様は意図的に除外してください。",
                    compiler: "抽出する項目は、最もクリティカルな大枠の要件を3〜5個、見落としがちな重要ポイントを1〜2個のみに厳選してください。内容が薄い無理やりな水増しは絶対に禁止です。"
                };
            } else if (depthMode === 'pro') {
                return {
                    desc: "【プロフェッショナルモード】極限までミクロな視点で徹底解析してください。大枠だけでなく、考えうるすべてのエッジケース、セキュリティ、スケーラビリティ、UX上の懸念点など、プロフェッショナルが考慮すべき全変数を網羅してください。",
                    compiler: "抽出する項目は、可能な限り細かく分解し、基本要件を10〜15個、プロの視点・見落としポイントを10〜15個など大量にリスト化してください。ただし、関連性の低い無意味な水増しは避け、すべてがプロ品質 of the view であること。"
                };
            }
            return {
                desc: "【スタンダードモード】通常のプロジェクトとして、基本要件とプロ視点での見落としがちなポイントをバランスよく分析してください。",
                compiler: "抽出する項目は、基本要件を6〜10個、プロの視点・見落としポイントを6〜10個程度抽出し、プロジェクトの骨組みを形成してください。"
            };
        }


        function updateStyleGuidePanel(style) {
            const panel = document.getElementById('styleGuidePanel');
            if (!panel) return;

            const idea = (document.getElementById('projectIdea').value || '').trim();
            
            // Check keywords to determine the recommendation guide
            let isSticker = idea.includes('スタンプ') || idea.includes('イラスト') || idea.includes('画像');
            let isBlog = idea.includes('ブログ') || idea.includes('記事') || idea.includes('アフィリエイト');
            let isApp = idea.includes('アプリ') || idea.includes('SaaS') || idea.includes('開発') || idea.includes('システム');

            let styleInfo = {
                pm: {
                    title: '👔 プロジェクトマネジメント・段取り型 (PM Style)',
                    desc: 'プロジェクトの全体スケジュール設計、マイルストーン策定、そして「今何から始めるべきか」を具体的にToDoタスク化するのに最も適したプロンプトです。AIを優秀な伴走PMとして起動させます。',
                    stage: '',
                    bgColor: 'bg-indigo-100 text-indigo-700'
                },
                creator: {
                    title: '🎨 クリエイティブ共同制作型 (Creator Style)',
                    desc: 'AIをあなたの右腕クリエイター、ブレスト相手として起動します。具体的なアイデア出し、デザイン案のブレスト、文章の下書き・コピーライティングなど、コンテンツを一緒に生み出すクリエイティブ工程に最適です。',
                    stage: '',
                    bgColor: 'bg-purple-100 text-purple-700'
                },
                auditor: {
                    title: '🔍 プロのリスク監査・アドバイザー型 (Auditor Style)',
                    desc: 'AIを辛口な最高リスク監査役（アドバイザー）として起動します。規約違反、著作権問題、商用利用基準の抜け漏れ、初心者が陥る落とし穴などをチェックし、リリース前に安全性を確認するリスクヘッジ工程に最適です。',
                    stage: '',
                    bgColor: 'bg-emerald-100 text-emerald-700'
                },
                custom: {
                    title: '✍️ 自由カスタマイズ・指示追加型 (Custom Style)',
                    desc: '上記の確定した要件に加え、あなた独自の追加指示（「回答を表形式にする」「英語で出力する」「〜の口調にする」など）を自由に注入し、AIとの共創スタイルを完全オーダーメイドで設計します。',
                    stage: '【活用例】「回答は箇条書きの表形式で出力してください。」や「AIに特定のフォーマットで応答させたい」など、自分なりのやり方がある上級フェーズ',
                    bgColor: 'bg-teal-100 text-teal-700'
                }
            };

            // Dynamic recommendations based on category
            if (isSticker) {
                styleInfo.pm.stage = '<strong>【おすすめの作業・段階】</strong>：LINEスタンプ制作スケジュールや画材・ソフトの調達・手間の管理に適しています。';
                styleInfo.creator.stage = '<strong>【おすすめの作業・段階】</strong>：スタンプのキャラクターアイデア、表情、メッセージ（セリフ）のブレストに向いています。';
                styleInfo.auditor.stage = '<strong>【おすすめの作業・段階】</strong>：LINE公式の審査ガイドライン（知的財産権、公序良俗など）への準拠、AIモデルの商用利用チェックに適しています。';
            } else if (isBlog) {
                styleInfo.pm.stage = '<strong>【おすすめの作業・段階】</strong>：ブログ記事の骨組み（H2/H3構成案）の段取り、定期更新の執筆スケジュールの設計に向いています。';
                styleInfo.creator.stage = '<strong>【おすすめの作業・段階】</strong>：読者の心をつかむタイトル、キャッチコピー、または書き出し文章（リード文）の下書きのブレストに向いています。';
                styleInfo.auditor.stage = '<strong>【おすすめの作業・段階】</strong>：YMYL（健康・お金など）分野での信頼性チェックや、アフィリエイト表現のポリシー違反チェックに適しています。';
            } else if (isApp) {
                styleInfo.pm.stage = '<strong>【おすすめの作業・段階】</strong>：MVP（最小限機能）のスコープ決定や、機能の実装スケジュール（WBS）の策定に向いています。';
                styleInfo.creator.stage = '<strong>【おすすめの作業・段階】</strong>：アプリのUI設計、コンポーネント構成、コードの実装案の作成フェーズに向いています。';
                styleInfo.auditor.stage = '<strong>【おすすめの作業・段階】</strong>：セキュリティ上の脆弱性チェック、データベース of the view のデータ破損対策、利用規約の整備監査に適しています。';
            } else {
                styleInfo.pm.stage = '<strong>【おすすめの作業・段階】</strong>：プロジェクトの全体スケジュール設計や、優先順位の高いToDoリストの作成に向いています。';
                styleInfo.creator.stage = '<strong>【おすすめの作業・段階】</strong>：具体的なアイデア出し、文章やコードの最初のドラフト作成に適しています。';
                styleInfo.auditor.stage = '<strong>【おすすめの作業・段階】</strong>：見落とした落とし穴（法的リスク、規約、品質など）をリリース前に監査・予防するのに適しています。';
            }

            const info = styleInfo[style];
            const explanationPreview = getSection4Text(style, idea, customInstructionText);

            panel.className = `p-5 bg-slate-50 border border-slate-200 rounded-xl flex flex-col gap-3 font-sans transition-all duration-300 shadow-sm`;
            panel.innerHTML = `
                <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                    <span class="px-2.5 py-0.5 rounded text-xs ${info.bgColor}">${info.title}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed font-semibold">
                    ${info.desc}
                </p>
                <div class="text-xs text-teal-700 bg-teal-50 border border-teal-100 p-3 rounded-lg font-medium">
                    ${info.stage}
                </div>
                <div class="mt-3 border-t border-slate-200 pt-3 flex flex-col gap-2">
                    <span class="text-xs text-slate-400 font-bold tracking-wider uppercase flex items-center gap-1">
                        <i class="fa-solid fa-code"></i> AIへの具体的な追加指示（プレビュー）
                    </span>
                    <pre class="p-3 bg-white border border-slate-200 text-slate-600 shadow-inner rounded-lg text-xs leading-relaxed overflow-x-auto whitespace-pre-wrap font-mono select-all">${explanationPreview}</pre>
                </div>
            `;
        }

        function updateCustomInstructions(text) {
            customInstructionText = text.trim();
            compileFinalPrompt();
        }

        function compileFinalPrompt() {
            const data = compiledData;
            const idea = data.idea || "無題のプロジェクト";
            
            // Render 4th section based on selected style
            let section4Text = '';
            if (activePromptStyle === 'pm') {
                section4Text = `『私は『${idea}』をプロジェクトマネージャー（PM）として開始します。
上記の「1階の基本確定要件」と「2階の見落としポイント対策」をロードし、これらを考慮した工程表（WBS）とマイルストーンを作成せよ。
まずは、この前提条件に対する合意と評価を簡潔に述べた後、以下のステップで進めてください：
1. 制作・開発マイルストーン（初期、中間、最終段階）の提示
2. 今すぐ実行すべき「3つのToDoタスク」
3. 推奨する進行スケジュール案』`;
            } else if (activePromptStyle === 'creator') {
                section4Text = `『私は『${idea}』のメインクリエイターおよびブレストパートナーとして起動します。
上記の「1階の基本確定要件」と「2階の見落としポイント対策」をベースの前提知識としてロードせよ。
まずは、この設定から感じられる本質的な魅力と方向性についてクリエイティブなフィードバックを述べた後、以下のステップで進めてください：
1. 初期ブレストとして、今すぐ形にできる具体的な「キャラクター設定案」や「デザイン／構成案」を3つ提案してください。
2. その提案がターゲットに響く理由と、その魅力を最大化するアプローチ。
3. 次に進むための具体的なドラフト案作成に向けた問いかけ』`;
            } else if (activePromptStyle === 'auditor') {
                section4Text = `『私は『${idea}』の最高リスク監査役（オフィシャルアドバイザー）として起動します。
上記の「1階の基本確定要件」と「2階の見落としポイント対策」を精査し、初心者が最も陥りやすい致命的なリスクをロードせよ。
まずは、この仕様に対するリスク監査コメントをプロフェッショナルとして辛口で述べた後、以下のステップで進めてください：
1. このまま進めた場合に発生しうる「法的リスク」や「規約違反」「品質低下」の具体的な3点
2. それぞれの致命傷を完全に回避するための「予防策・代替アプローチ」
3. 安全にリリースするための必須品質チェックリスト』`;
            } else if (activePromptStyle === 'custom') {
                const instructions = customInstructionText || '特にカスタムの指定はありません。';
                section4Text = `『私は『${idea}』の共創パートナーとして起動します。
上記の「1階の基本確定要件」と「2階の見落としポイント対策」をすべてベースの前提知識としてロードせよ。

【ユーザーによる追加・カスタム指示】
${instructions}

まずは、上記の前提条件と追加指示に対する確認と、このプロジェクトを成功に導くための最初のステップを具体的に提示してください。』`;
            }

            const formattedPrompt = `# 【設定済み】プロジェクト要件・コンテキスト指示書
このプロンプトは、プロジェクト開始前におけるすべての「基本制約」と「陥りやすい盲点」を網羅し、高い解像度でAIと共創を開始するためのものである。

---

## 1. コア・イニシアティブ
* **やろうとしていること:** ${idea}
* **初期の認識条件（レベル1）:**
${data.level1 ? data.level1.split('\n').map(line => `  * ${line}`).join('\n') : '  * 特になし'}

---

## 2. ■ 1階部分：必須基礎確定要件
AIは、以下の基本パラメータに100%厳格に従ったうえで、成果物の第一案を作成しなければならない。
${data.knowns && data.knowns.length > 0 ? data.knowns.join('\n') : '* ※全て未定'}

---

## 3. ■ 2階部分：プロの視点（見落としポイント）対策
AIは、初心者が自滅しやすい以下の「見落としがちな重要ポイント」について、仕様設計段階から完全に解決したロジックを強制的に組み込むこと。
${data.deepStates && data.deepStates.length > 0 ? data.deepStates.join('\n') : '* ※指定された重要ポイントはありません。'}

---

## 4. プロの共創開始アクション
この指示書を読み込んだAIは、以下の役割で直ちに起動すること：

${section4Text}`;

            const res = document.getElementById('finalPromptResult');
            if (res) res.value = formattedPrompt;
            
            const memoArea = document.getElementById('undecidedMemoArea');
            const memoList = document.getElementById('undecidedList');
            if (memoArea && memoList) {
                if (data.unknowns && data.unknowns.length > 0) {
                    memoList.innerHTML = data.unknowns.map(u => `<li>・${u}</li>`).join('');
                    memoArea.classList.remove('hidden');
                } else {
                    memoArea.classList.add('hidden');
                }
            }
        }



        // --- ORCHESTRATION ENGINE (PHASE 1: DISCOVERY) ---
        async function startAnalysisEngine() {
            let idea = document.getElementById('projectIdea').value.trim();
            if (!idea) { 
                showToast('プロジェクトのアイデアを入力してください。', 'error'); 
                return; 
            }
            
            const goals = document.getElementById('level1Goals').value.trim();
            const constraints = document.getElementById('level1Constraints').value.trim();
            let level1 = "";
            if (goals) level1 += `【目標・ビジョン】\n${goals}\n\n`;
            if (constraints) level1 += `【前提ルール・制約】\n${constraints}`;
            if (!level1) level1 = "(特になし)";
            
            const mode = document.getElementById('runMode').value;
            const depth = document.getElementById('analysisDepth').value;
            const apiKey = typeof GEMINI_API_KEY !== 'undefined' ? GEMINI_API_KEY : '';

            logArea.innerHTML = '';
            progressBar.style.width = '0%';
            switchTab('terminal');

            document.getElementById('phase1').classList.add('hidden');
            document.getElementById('appHeader').classList.add('hidden');
            document.getElementById('phase2').classList.remove('hidden');
            document.getElementById('phase2').classList.add('flex');
            const phase2El = document.getElementById('phase2');
            if (phase2El) {
                phase2El.scrollIntoView({ behavior: 'smooth', block: 'start' });
            } else {
                window.scrollTo({ top: 0, behavior: 'smooth' });
            }
            
            const displayIdea = document.getElementById('displayIdea');
            if (displayIdea) { displayIdea.innerText = idea; displayIdea.classList.add('break-keep'); }
            
            document.getElementById('displayLevel1').innerText = level1 || '(なし)';
            document.getElementById('displayDepth').innerText = depth.toUpperCase();
            
            writeToConsole('SYSTEM', `『${idea}』のアナリシス・シーケンス（${depth.toUpperCase()}モード）を起動します。`, 'system');

            if (mode === 'simulated') {
                await runSimulatedDebate();
            } else {
                if (!apiKey) { 
                    const errCard = document.getElementById('debateErrorCard');
                    if (errCard) {
                        errCard.innerHTML = `
                            <div class="p-6 bg-rose-50 border border-rose-200 rounded-2xl text-center">
                                <i class="fa-solid fa-triangle-exclamation text-rose-500 text-4xl mb-4"></i>
                                <h3 class="text-rose-900 font-bold mb-2">APIキー未設定</h3>
                                <p class="text-rose-700 text-sm mb-4">LiveモードにはGemini APIキーが必要です。設定ファイルを確認するか、デモモードを試してください。</p>
                                <button onclick="location.reload()" class="px-4 py-2 bg-rose-600 text-white rounded-lg text-sm font-bold">リロードして再試行</button>
                            </div>`;
                        errCard.classList.remove('hidden');
                    }
                    showToast('Liveモードを実行するには config.js に Gemini APIキーが必要です。', 'error'); 
                    return; 
                }
                await runLiveDiscoveryPhase(idea, level1, apiKey, depth);
            }
        }

        async function runSimulatedDebate() {
            const idea = document.getElementById('projectIdea').value.trim();
            
            // Determine active genre based on preset and keywords
            let genre = 'general';
            const presetVal = typeof activePreset !== 'undefined' ? activePreset : 'custom';
            
            if (presetVal === 'linestamp' || idea.includes('スタンプ') || idea.includes('キャラクター') || idea.includes('イラスト')) {
                genre = 'linestamp';
            } else if (presetVal === 'lecture' || idea.includes('スライド') || idea.includes('資料') || idea.includes('講義') || idea.includes('発表')) {
                genre = 'lecture';
            } else if (presetVal === 'youtube' || idea.includes('動画') || idea.includes('YouTube') || idea.includes('ユーチューブ') || idea.includes('解説')) {
                genre = 'youtube';
            } else if (idea.includes('アプリ') || idea.includes('SaaS') || idea.includes('システム') || idea.includes('開発') || idea.includes('ツール') || idea.includes('プログラム')) {
                genre = 'app';
            } else if (idea.includes('ブログ') || idea.includes('記事') || idea.includes('執筆') || idea.includes('サイト') || idea.includes('メディア') || idea.includes('アフィリエイト')) {
                genre = 'blog';
            } else if (idea.includes('画像') || idea.includes('絵') || idea.includes('クリエイティブ') || idea.includes('デザイン')) {
                genre = 'creative';
            }

            // High-fidelity domain-specific debate logs and data structures

            const data = simulatedDatabase[genre] || simulatedDatabase.general;
            rawBaseVars = data.questions;
            rawDeepVars = data.deepVars;

            // Display simulated debate progress
            const stepDelays = [1500, 1500, 1500, 1500, 1000];
            const statusMsgs = ["戦略の変数を分析中...", "技術要件と制約を検討中...", "意匠・デザイン要件を抽出中...", "収益とペルソナを分析中...", "前提条件と変数をコンパイル中..."];
            for (let i = 0; i < 5; i++) {
                setAgentPhase(2, i + 1);
                progressBar.style.width = `${(i + 1) * 20}%`;
                
                // 1. まず短いステータスを表示
                writeToConsole(data.steps[i].name, statusMsgs[i], data.steps[i].type);
                await new Promise(r => setTimeout(r, 800));
                
                // 2. その後、長文のログ（擬似AI回答）を出力
                writeToConsole(data.steps[i].name, data.steps[i].log, data.steps[i].type);
                await new Promise(r => setTimeout(r, stepDelays[i]));
            }

            renderDiscoveryReport(rawBaseVars, rawDeepVars);
            showToast('インテリジェントローカル分析が完了しました！（API消費ゼロ）', 'success');
        }

        async function runLiveDiscoveryPhase(idea, level1, apiKey, depth) {
            try {
                const depthInstructions = getDepthInstructions(depth);
                const baseContext = `アイデア: ${idea}\n知識: ${level1}`;

                setAgentPhase(2, 1); progressBar.style.width = '15%';
                writeToConsole('プロダクト・ストラテジスト', '戦略の変数を分析中...', 'strategy');
                const stratOutput = await callGeminiAgent(apiKey, `あなたは製品ストラテジストです。絶対に定義しておくべき必須変数と、見落としがちな重要ポイントを記述してください。出力は「〜です/ます」調の丁寧な口調を使用してください。\n${depthInstructions.desc}`, baseContext);
                writeToConsole('プロダクト・ストラテジスト', stratOutput, 'strategy');

                setAgentPhase(2, 2); progressBar.style.width = '30%';
                writeToConsole('仕様・規格監修', '技術的制約のデバッグと物理規格の分析中...', 'technical');
                const techOutput = await callGeminiAgent(apiKey, `あなたは技術監督です。物理規格や制約・ルールの基本変数を定義し、隠れた制約や見落としがちなポイントを洗い出してください。出力は「〜です/ます」調の丁寧な口調を使用してください。\n${depthInstructions.desc}`, baseContext);
                writeToConsole('仕様・規格監修', techOutput, 'technical');

                setAgentPhase(2, 3); progressBar.style.width = '45%';
                writeToConsole('UI/UX デザイナー', 'ビジュアルと意匠設計の要件を定義中...', 'design');
                const designOutput = await callGeminiAgent(apiKey, `あなたはデザイナーです。制作前に決めておくべきビジュアル設計変数と、デザインにおける見落としがちな重要ポイントを定義してください。出力は「〜です/ます」調の丁寧な口調を使用してください。\n${depthInstructions.desc}`, baseContext);
                writeToConsole('UI/UX デザイナー', designOutput, 'design');

                setAgentPhase(2, 4); progressBar.style.width = '60%';
                writeToConsole('マネタイズ・アナリスト', '収益変数とマーケティングの重要ポイントをモデリング中...', 'marketing');
                const businessOutput = await callGeminiAgent(apiKey, `あなたはビジネスアナリストです。プロジェクトの目的に応じて、収益変数、価格、集客目標を定義し、ビジネス面で見落としがちな重要ポイントを洗い出してください。※もし無料ツールや社内資料、非営利目的など、明らかに収益化が不要なプロジェクトの場合は、無理に価格や売上を定義せず、「利用されるための目標設定」や「維持コストの管理」に視点を切り替えて分析してください。出力は「〜です/ます」調の丁寧な口調を使用してください。\n${depthInstructions.desc}`, baseContext);
                writeToConsole('マネタイズ・アナリスト', businessOutput, 'marketing');

                setAgentPhase(2, 5); progressBar.style.width = '75%';
                
                // --- Step 5a: 統合レビュアー ---
                writeToConsole('統合レビュアー', '4人の議論結果を精読し、要件と盲点を統合したレポートを作成中...', 'compiler');
                const reviewerSystem = `あなたは「プロジェクト統合レビュアー」です。
4人の専門家（戦略、技術、デザイン、ビジネス）の議論を精読し、以下の2つのカテゴリに分類・統合した包括的レビューレポートを作成してください。

【カテゴリ1：基本確定要件（1階部分）】
プロジェクトを開始する前に、ユーザーが最低限決めなければならない前提条件。

【カテゴリ2：プロの見落とし盲点（2階部分）】
初心者が気づかず自滅しやすい、専門家だけが知る重要ポイント。

・元の4人の専門家から提示された意見のうち、「プロジェクトの目的に対して本当に考慮すべき重要な変数や制約（技術仕様、必要な場合のみの費用・価格、法的ルールなど）」は漏らさず抽出してください。
・ただし、プロジェクトの性質（無料ツール、社内資料、非営利の趣味など）に照らし合わせて明らかに不要な要素（無意味なマネタイズ、不要なコスト計算など）は、無理に抽出・捏造せず除外してください。
・重複は統合し、最も重要なものから順に並べてください。
・各項目には、どの専門家の視点から抽出されたか（戦略、技術、デザイン、ビジネス）を明記してください。
${depthInstructions.compiler}`;
                const integratedReport = await callGeminiAgent(apiKey, reviewerSystem, `アイデア: ${idea}\n戦略:\n${stratOutput}\n技術:\n${techOutput}\nデザイン:\n${designOutput}\nビジネス:\n${businessOutput}`);
                writeToConsole('統合レビュアー', '統合レポートが完成しました。構造化エンジンへ引き継ぎます。', 'compiler');

                // --- Step 5b: JSON構造化エンジン ---
                writeToConsole('構造化エンジン', '統合レポートから前提条件と見落としポイントリスト（JSON）を生成中...', 'compiler');
                const compileSystem = `あなたは「データ構造化エンジン」です。
与えられたレビューレポートを、以下の厳密なJSONスキーマに変換してください。
内容の追加や削除は一切行わず、レポートの情報を忠実に構造化することだけに集中してください。

【重要：出力のトーンおよび粒度規定】
・【厳守事項】1つの質問（question）に複数の要素（例：「販売価格とプロモーション計画」など）を絶対に混ぜないでください。複合的な要素を含む場合は、必ず独立した個別の質問（「販売価格」と「プロモーション計画」など）に分割し、1質問＝1テーマになるように細分化してください。
・各項目のタイトル（label）は、絶対に「〜です/ます」を含めず、名詞や体言止めの短いフレーズにしてください。（例：「ターゲット層の設定」「競合分析」など）
・各項目の説明文（description, detail）のみを、「〜です/ます」調の丁寧で分かりやすい口調にしてください。
・各項目には、どの専門AIの視点から抽出されたかを推測し、sourceプロパティ（"strategy" | "technical" | "design" | "business" のいずれか）を必ず付与してください。

出力は必ず以下のJSONスキーマに従ってください。選択肢(options)はここでは不要です。
{
  "questions": [
    { "id": "q1", "label": "ターゲット層の設定", "description": "誰に向けて作りますか？まずは対象を絞り込むことが重要です。", "source": "business" }
  ],
  "deepVars": [
    { "id": "d1", "label": "源泉徴収の見落とし", "detail": "初心者は税金周りの確認を忘れがちですので注意が必要です。", "source": "business" }
  ]
}`;
                const rawJson = await callGeminiAgent(apiKey, compileSystem, `統合レビューレポート:\n${integratedReport}`, true);
                
                let cleanJson = rawJson;
                if (typeof cleanJson === 'string' && cleanJson.includes('```')) {
                    cleanJson = cleanJson.replace(/```json?\s*/g, '').replace(/```\s*/g, '').trim();
                }
                const parsedData = JSON.parse(cleanJson);

                rawBaseVars = parsedData.questions || [];
                rawDeepVars = parsedData.deepVars || [];

                writeToConsole('要件抽出コンパイラ', `要件抽出完了。前提条件: ${rawBaseVars.length}件、見落としポイント: ${rawDeepVars.length}件。`, 'compiler');
                progressBar.style.width = '100%';
                
                renderDiscoveryReport(rawBaseVars, rawDeepVars);
                showToast('情報収集フェーズが完了しました。', 'success');

            } catch (err) {
                writeToConsole('SYSTEM-ERROR', `API実行エラーが発生しました: ${err.message}`, 'system');
                showToast('エラーが発生しました。コンソールをご確認ください。', 'error');
                setAgentPhase(1);
                
                // Show beautiful error recovery card
                const tutorial = document.getElementById('debateTutorialContent');
                if (tutorial) tutorial.classList.add('hidden');
                
                const errCard = document.getElementById('debateErrorCard');
                const errMsg = document.getElementById('debateErrorMessage');
                if (errCard && errMsg) {
                    errMsg.innerText = `エラー内容: ${err.message}\n(APIキーの有効性、アクセス上限、またはインターネット接続をご確認ください)`;
                    errCard.classList.remove('hidden');
                }
            }
        }

        function getAgentStyle(source) {
            switch(source) {
                case 'strategy': return { icon: 'fa-chess-knight', colorText: 'text-indigo-500', colorBase: 'indigo', bg: 'bg-indigo-100', label: 'STRATEGY' };
                case 'technical': return { icon: 'fa-ruler-combined', colorText: 'text-cyan-500', colorBase: 'cyan', bg: 'bg-cyan-100', label: 'TECH' };
                case 'design': return { icon: 'fa-pen-nib', colorText: 'text-purple-500', colorBase: 'purple', bg: 'bg-purple-100', label: 'DESIGN' };
                case 'business': return { icon: 'fa-chart-line', colorText: 'text-amber-500', colorBase: 'amber', bg: 'bg-amber-100', label: 'BUSINESS' };
                default: return { icon: 'fa-filter', colorText: 'text-emerald-500', colorBase: 'emerald', bg: 'bg-emerald-100', label: 'COMPILER' };
            }
        }

        function renderDiscoveryReport(questions, deepVars) {
            setAgentPhase(2.5);
            const tabBtn = document.getElementById('tabDiscovery');
            tabBtn.classList.remove('hidden');
            tabBtn.classList.add('slide-in-right');
            document.getElementById('discoveryReadyBadge').classList.remove('hidden');
            
            // Unhide tabWizard with ready badge to clearly guide user to Phase 3
            const wizardBtn = document.getElementById('tabWizard');
            if (wizardBtn) {
                wizardBtn.classList.remove('hidden');
                wizardBtn.classList.add('slide-in-right');
                const badge = document.getElementById('wizardReadyBadge');
                if (badge) badge.classList.remove('hidden');
            }
            
            const qContainer = document.getElementById('discoveryVariablesList');
            qContainer.innerHTML = '';
            
            if (questions.length === 0) {
                qContainer.innerHTML = '<div class="text-slate-400 text-sm">抽出された項目がありません。</div>';
            } else {
                questions.forEach(q => {
                    const style = getAgentStyle(q.source);
                    qContainer.innerHTML += `
                        <div class="p-5 rounded-xl bg-slate-50 border border-slate-200 hover:-translate-y-1 hover:shadow-md hover:border-${style.colorBase}-300 transition-all cursor-default relative overflow-hidden group">
                            <i class="fa-solid ${style.icon} absolute -right-3 -bottom-3 text-[5rem] opacity-[0.03] group-hover:opacity-[0.08] transition-opacity ${style.colorText}"></i>
                            <div class="text-sm font-bold text-slate-800 mb-2 relative z-10 flex flex-col sm:flex-row items-start sm:items-center gap-1.5 sm:gap-2">
                                <span class="text-xs px-2 py-0.5 rounded ${style.bg} ${style.colorText} font-extrabold shadow-sm tracking-wider inline-block">${style.label}</span>
                                <span class="leading-snug">${q.label}</span>
                            </div>
                            <div class="text-xs text-slate-500 font-medium relative z-10 mt-2">${q.description}</div>
                        </div>
                    `;
                });
            }

            const dContainer = document.getElementById('discoveryTrapsList');
            dContainer.innerHTML = '';
            
            if (deepVars.length === 0) {
                dContainer.innerHTML = '<div class="text-slate-400 text-sm">抽出された見落としポイントはありません。</div>';
            } else {
                deepVars.forEach((d, i) => {
                    const style = getAgentStyle(d.source);
                    dContainer.innerHTML += `
                        <div class="p-5 rounded-xl border border-rose-100 bg-rose-50/50 hover:-translate-y-1 hover:shadow-md hover:border-rose-300 transition-all cursor-default relative overflow-hidden group">
                            <i class="fa-solid ${style.icon} absolute -right-3 -bottom-3 text-[5rem] opacity-[0.03] group-hover:opacity-[0.08] transition-opacity ${style.colorText}"></i>
                            <div class="text-sm font-bold text-rose-800 mb-2 relative z-10 flex flex-col sm:flex-row items-start sm:items-center gap-1.5 sm:gap-2">
                                <span class="text-xs px-2 py-0.5 rounded ${style.bg} ${style.colorText} font-extrabold shadow-sm tracking-wider inline-block">${style.label}</span>
                                <span class="leading-snug">POINT ${i+1}. ${d.label}</span>
                            </div>
                            <div class="text-xs text-slate-600 font-medium relative z-10 mt-2">${d.detail}</div>
                        </div>
                    `;
                });
            }
            
            setTimeout(() => switchTab('discovery'), 800);
        }

        // --- PHASE 2: WIZARD BUILDER (AGENT 6) ---
        async function startWizardBuilder() {
            if (rawBaseVars.length === 0) {
                showToast('回答すべき質問がありません。', 'info');
                return;
            }

            document.getElementById('tabWizard').classList.remove('hidden');
            switchTab('wizard');
            document.getElementById('wizardLoadingState').classList.remove('hidden');
            document.getElementById('wizardLoadingState').classList.add('flex');
            document.getElementById('wizardContainer').classList.add('hidden');
            document.getElementById('deepVarsContainerUI').classList.add('hidden');

            const mode = document.getElementById('runMode').value;
            const apiKey = typeof GEMINI_API_KEY !== 'undefined' ? GEMINI_API_KEY : '';

            if (mode === 'simulated') {
                setAgentPhase(3, 6);
                writeToConsole('フォーム・ビルダー', 'ローカルエンジンで、具体的な選択肢を高速生成中...', 'builder');
                await new Promise(r => setTimeout(r, 1200));

                const simulatedOptions = {
                    // LINEスタンプ
                    linestamp_base_target: ["特定業界のエンジニア・オタク層", "日常の癒やしを求める女子大生・OL層", "シュールな笑いを好む男子高校生・大学生層", "ビジネスでスタンプを使うサラリーマン層"],
                    linestamp_base_count: ["8枚 (お試し・最速リリース)", "16枚 (標準的なボリューム)", "24枚 (初期費用と手間のベストバランス)", "32枚 (豪華セット・満足度最大)"],
                    linestamp_base_price: ["120円 (最低価格・バイラル重視)", "250円 (標準価格・利益バランス型)", "370円 (プレミアム価格)", "610円 (最高設定価格)"],
                    linestamp_base_schedule: ["3日以内 (超速リリース)", "1週間以内 (短期集中)", "2週間以内 (丁寧な作り込み)", "1ヶ月以内 (副業としてじっくり)"],
                    
                    // 講義スライド
                    lecture_base_target: ["実務でコードを書いている現役プログラマー（20〜30代）", "AI活用を検討している非エンジニアの経営・役員層", "プログラミング学習中のスクール生・初心者", "社内の開発メンバー・社内技術勉強会の参加者"],
                    lecture_base_time: ["15分 (ライトな技術紹介・デモ主体)", "20分 (スライド10枚前後・結論と実証コード)", "30分 (スライド15枚・質疑応答とデモあり)", "60分 (本格的なワークショップ形式)"],
                    lecture_base_design: ["クリーン＆ミニマル（開発者画面を模したSaaS系）", "サイバーパンク（暗めの背景にネオン色の強調線）", "ビジネスシック（落ち着いたネイビー＆ホワイト）", "親しみやすい手書き風イラストタッチ"],
                    lecture_base_tone: ["丁寧かつ、エンジニアのプライドを刺激する冷徹な論理トーン", "熱意に満ちた、開発モチベーションを爆上げする共感トーン", "優しく分かりやすい、専門用語を極力排除した解説トーン", "淡々と事実とコードを提示するアカデミックな客観トーン"],
                    
                    // YouTube
                    youtube_base_genre: ["AI自動化・実用系ハック（最新ニュースではなく実務活用）", "最新AIツールの速報・ニュース解説", "AIを活用した副業・マネタイズ手法の完全ロードマップ", "AIと人間社会の未来を考察する教養・ドキュメンタリー風"],
                    youtube_base_length: ["5分 (要点のみを極限まで凝縮したスピード解説)", "8分 (広告最適化と視聴維持率を両立するベストライン)", "15分 (深く理解できるハンズオン・チュートリアル)", "30分以上 (完全解説・保存版の超大作)"],
                    youtube_base_voice: ["自分の生声（マイク録音）＋画面キャプチャ（顔出しなし）", "ゆっくり音声（霊夢・魔理沙風の合成音声）", "Vocaloid/VOICEVOX（ずんだもん等のキャラクター音声）", "完全顔出し出演＋スタジオ風撮影"],
                    youtube_base_schedule: ["3日以内 (トレンドを最速で捉える強行スケジュール)", "5日以内 (企画から編集までバランスよくこなす標準)", "1週間以内 (週1本投稿目標・丁寧なクオリティ確保)", "2週間以内 (副業・片手間にマイペース進行)"],
                    
                    // アプリ開発
                    app_base_target: ["特定の個人ユーザー（プライベートの課題解決・B2C）", "特定業界 of ビジネスマン（業務効率化・B2B SaaS）", "個人開発者・プログラマー（開発効率化ツール）", "ITスキルがあまり高くない一般の初心者層"],
                    app_base_mvp: ["タスクやToDoの視覚的カード管理（カンバンボード）", "AIによる文章・画像・コードの自動生成アシスタント", "シンプルかつ美しいダッシュボード・計測器", "データの自動同期・クラウドバックアップ機能"],
                    app_base_tech: ["自分が一番使い慣れている既存の言語・フレームワーク", "Next.js / React + Supabase (モダンSaaS最速構成)", "NoCodeツール (Bubble / FlutterFlow 等の開発コストゼロ)", "Python / Django + SQLite (AI組み込み・ローカル重視)"],
                    app_base_schedule: ["2週間以内 (コア機能のみを最速でリリースするMVP)", "1ヶ月以内 (不要な機能は切り捨て、丁寧にビルド)", "3ヶ月以内 (ある程度のデザインや完成度を確保)", "期限なし (趣味として気が向いたときに開発する)"],
                    
                    // ブログ
                    blog_base_genre: ["自分の得意分野・実体験がある専門特化ジャンル", "最新トレンドや流行キーワードを網羅する雑記ジャンル", "金融・プログラミング・転職等のアフィリエイト高単価ジャンル", "自己開示や日々のライフスタイルを発信するエッセイ風"],
                    blog_base_pace: ["週に1〜2本の高品質な記事執筆（持続可能で最高品質）", "毎日更新（質よりスピード、ドメインパワー最速強化）", "月に2〜3本の徹底解説記事（1本で競合を駆逐する決定版）", "特に決めず、書きたいテーマが見つかったときに執筆"],
                    blog_base_seo: ["検索エンジン(SEO)からの自然流入を9割（キーワード設計）", "XやInstagram等のSNSからのフォロワー・ファン流入主軸", "note等の他社プラットフォームでのドメイン活用", "特に集客対策はせず、純粋な記事の質でバイラルを狙う"],
                    blog_base_money: ["ASPアフィリエイト（高単価成果報酬を主軸にする）", "Google AdSense（アドネットワークによるクリック報酬）", "自分のコンテンツ（note/Brain等）や個人コンサルの販売", "特に最初はマネタイズを意識せず、ファン作りに専念する"],
                    
                    // クリエイティブ
                    creative_base_style: ["手書き・オリジナルのデジタルイラスト", "AI画像生成モデル（Midjourney等）による高度な生成＆加工", "シンプルで実用性の高いフラットデザイン・アイコン", "3Dグラフィック・モデリングアセット"],
                    creative_base_count: ["8点 (お試し・最速でセットを用意する)", "16点 (標準的で使い勝手の良いボリューム)", "24点 (作成手間と購入者満足度のベストバランス)", "32点 (豪華セット・満足度最大)"],
                    creative_base_target: ["感情をSNS等で過激に代弁してほしいITエンジニアやオタク層", "日常の癒やしや可愛さを求める女子大生・OL層", "AIイラストやアセットを自分の作品の素材として使いたいクリエイター", "特定の趣味やジャンルに深いこだわりを持つニッチなファン"],
                    creative_base_schedule: ["3日以内 (超速リリース・トレンドに即乗りする)", "1週間以内 (集中して作り込む短期制作)", "2週間以内 (クオリティに一切妥協しない丁寧な制作)", "1ヶ月以内 (本業の合間にゆったり作成する)"],
                    
                    // 汎用プロジェクト
                    general_base_target: ["特定の強い課題や悩みを持つビジネスパーソン", "趣味や特定のライフスタイルを楽しんでいる一般の個人", "将来のためにスキルアップや自己投資を始めたい学習意欲の高い人", "流行に敏感な若者・学生・アーリーアダプター層"],
                    general_base_goal: ["まずは少額でも最初の売上（0→1）を達成する", "自身のスキルアップや自己実現・学習を最優先する", "多くの人に知ってもらい、ファンや認知（インプレッション）を拡大する", "業務効率化や自己のライフスタイル向上に直結するツール完成"],
                    general_base_time: ["週に数時間程度（本業の隙間時間を有効活用する副業スタイル）", "平日の夜と土日のまとまった時間（週15時間前後の本格推進）", "フルコミット（毎日3〜5時間以上を投下する最優先事項）", "特に決めておらず、仕事の空き時間でマイペースに進める"],
                    general_base_schedule: ["1〜2週間以内 (極小プロトタイプでまず動くものを作る)", "1ヶ月以内 (標準的なスケジュールで第1版を公開)", "3ヶ月以内 (クオリティを磨き抜いた決定版を作る)", "期限は設けず、進捗と出来栄えに合わせて調整する"]
                };

                wizardQuestions = rawBaseVars.map(q => {
                    const opts = simulatedOptions[q.id];
                    return {
                        ...q,
                        options: opts ? opts : ["手動で決める", "AIに任せる", "UNKNOWNに設定する"]
                    };
                });
            } else {
                try {
                    setAgentPhase(3, 6);
                    writeToConsole('フォーム・ビルダー', '抽出された前提条件に対して、具体的な選択肢を生成中...', 'builder');
                    
                    const builderSystem = `あなたはフォームビルダーAIです。与えられた「質問のリスト」に対して、ユーザーが直感的に選べるような「具体的で質の高い選択肢」をそれぞれ4〜5個ずつ生成してください。
出力はJSON配列として、元の質問IDに対応するように出力してください。
【選択肢の順序に関する厳格なポリシー】
・数値、個数、期間、日付などの変数に対する選択肢を生成する場合、混乱を防ぐため、必ず「昇順（小さい値から大きい値への並び）」または「時系列順」に論理的に並べて出力してください（例：「8枚」「16枚」「24枚」「32枚」のように規則正しく並べ、飛び石にしたり順序をバラバラにするのは厳禁です）。
・その他一般の選択肢は、重要度または論理的整合性の高い順に並べてください。

{
  "questions": [
    { "id": "q1", "options": ["選択肢1", "選択肢2", "選択肢3", "選択肢4"] }
  ]
}`;
                    const jsonInput = JSON.stringify({ questions: rawBaseVars });
                    const wizardTimeout = new Promise((_, reject) => setTimeout(() => reject(new Error('選択肢生成がタイムアウトしました（60秒）。再試行してください。')), 60000));
                    let rawJson = await Promise.race([
                        callGeminiAgent(apiKey, builderSystem, `質問リスト:\n${jsonInput}`, true, 2, 'gemini-2.5-flash'),
                        wizardTimeout
                    ]);
                    if (typeof rawJson === 'string' && rawJson.includes('```')) {
                        rawJson = rawJson.replace(/```json?\s*/g, '').replace(/```\s*/g, '').trim();
                    }
                    writeToConsole('フォーム・ビルダー', 'APIレスポンス受信。選択肢をパース中...', 'builder');
                    const parsed = JSON.parse(rawJson);
                    
                    let questionsArray = Array.isArray(parsed) ? parsed : (parsed.questions || []);

                    wizardQuestions = rawBaseVars.map(q => {
                        const matched = questionsArray.find(pq => pq.id === q.id);
                        return { ...q, options: matched && matched.options ? matched.options : ["手動で決める", "AIに任せる"] };
                    });

                    writeToConsole('フォーム・ビルダー', 'ウィザード選択肢の生成完了。', 'builder');
                } catch (err) {
                    writeToConsole('SYSTEM-ERROR', `Builder APIエラー: ${err.message}`, 'system');
                    showToast('選択肢の生成に失敗しました。', 'error');
                    wizardQuestions = rawBaseVars.map(q => ({ ...q, options: ["エラーにより自動生成失敗"] }));
                }
            }

            setAgentPhase(3.5, 6);
            document.getElementById('wizardLoadingState').classList.add('hidden');
            document.getElementById('wizardLoadingState').classList.remove('flex');
            wizardAnswers = {};
            currentQuestionIndex = 0;
            renderWizardStep();
            document.getElementById('wizardContainer').classList.remove('hidden');
        }

        // --- DETECT INITIAL HOPE FROM LEVEL 1 INPUT ---
        function detectInitialHope(qLabel, qId) {
            const goals = document.getElementById('level1Goals').value.trim();
            const constraints = document.getElementById('level1Constraints').value.trim();
            const fullText = (goals + "\n" + constraints).toLowerCase();
            
            if (!fullText.trim()) return null;

            const keywordMap = {
                count: { keywords: ["枚", "個数", "枚数", "ボリューム", "点数", "量"], pattern: /(\d+枚|\d+点|\d+個)/ },
                price: { keywords: ["円", "価格", "値段", "単価", "販売希望価格"], pattern: /(\d+円)/ },
                target: { keywords: ["ターゲット", "ペルソナ", "属性", "客", "誰に", "向け"], pattern: /(・|\n|^)[^\n]*(ターゲット|ペルソナ|向け|誰)[^\n]*(?=\n|$)/ },
                schedule: { keywords: ["期日", "目標期間", "スケジュール", "期間", "目標期日", "以内", "週間", "ヶ月", "日"], pattern: /(・|\n|^)[^\n]*(期日|期間|スケジュール|以内|週間|ヶ月|日)[^\n]*(?=\n|$)/ },
                mvp: { keywords: ["コア機能", "mvp", "開発範囲", "機能", "最小限"], pattern: /(・|\n|^)[^\n]*(機能|mvp|最小限)[^\n]*(?=\n|$)/ },
                tech: { keywords: ["技術", "言語", "スタンプ", "フレームワーク", " supabase", " react", " next", "手書き", "ai"], pattern: /(・|\n|^)[^\n]*(技術|言語|フレームワーク|手法|手書き|ai)[^\n]*(?=\n|$)/ },
                genre: { keywords: ["ジャンル", "テーマ", "発信テーマ", "作風", "作風ジャンル"], pattern: /(・|\n|^)[^\n]*(ジャンル|テーマ|作風|分野)[^\n]*(?=\n|$)/ },
                pace: { keywords: ["ペース", "更新ペース", "更新目標", "毎日", "週に"], pattern: /(・|\n|^)[^\n]*(ペース|頻度|毎日|週に|更新)[^\n]*(?=\n|$)/ },
                seo: { keywords: ["経路", "集客", "seo", "sns", "流入"], pattern: /(・|\n|^)[^\n]*(経路|集客|seo|sns|流入)[^\n]*(?=\n|$)/ },
                money: { keywords: ["マネタイズ", "収益化", "アフィリエイト", "アドセンス", "報酬"], pattern: /(・|\n|^)[^\n]*(マネタイズ|収益|アフィリエイト|アドセンス|報酬)[^\n]*(?=\n|$)/ }
            };

            let matchedCategory = null;
            const cleanId = qId.toLowerCase();
            const cleanLabel = qLabel.toLowerCase();

            for (const [cat, cfg] of Object.entries(keywordMap)) {
                if (cleanId.includes(cat) || cleanLabel.includes(cat) || cfg.keywords.some(k => cleanLabel.includes(k))) {
                    matchedCategory = cat;
                    break;
                }
            }

            if (!matchedCategory) return null;

            const lines = fullText.split('\n');
            const config = keywordMap[matchedCategory];

            for (let line of lines) {
                line = line.trim();
                if (!line) continue;

                const hasKeyword = config.keywords.some(k => line.includes(k));
                if (hasKeyword) {
                    const separators = ['：', ':', 'は', 'が'];
                    for (const sep of separators) {
                        const idx = line.indexOf(sep);
                        if (idx !== -1 && idx < line.length - 1) {
                            let value = line.substring(idx + 1).trim();
                            value = value.replace(/^[・\-\*\s]+/, '').trim();
                            if (value.length > 0 && value.length < 50) return value;
                        }
                    }
                    
                    if (config.pattern) {
                        const match = line.match(config.pattern);
                        if (match) return match[0].replace(/^[・\-\*\s]+/, '').trim();
                    }

                    let cleanLine = line.replace(/^[・\-\*\s]+/, '').trim();
                    if (cleanLine.length > 0 && cleanLine.length < 50) return cleanLine;
                }
            }
            return null;
        }

        // --- WIZARD UI LOGIC ---
        function renderWizardStep() {
            if (currentQuestionIndex >= wizardQuestions.length) {
                renderDeepVarsReview();
                return;
            }

            const q = wizardQuestions[currentQuestionIndex];
            document.getElementById('wizardProgress').innerText = `Step ${currentQuestionIndex + 1} / ${wizardQuestions.length}`;
            document.getElementById('wizardQuestionLabel').innerText = q.label;
            document.getElementById('wizardQuestionDesc').innerText = q.description || '選択肢から選ぶか、自由に入力してください。';
            
            // Detect initial hope and display alert
            const initialHope = detectInitialHope(q.label, q.id);
            const alertContainer = document.getElementById('wizardInitialHopeAlert');
            if (alertContainer) {
                if (initialHope) {
                    alertContainer.innerHTML = `
                        <div class="flex items-center gap-2.5 px-5 py-3.5 bg-teal-50/80 border border-teal-300/80 text-teal-900 rounded-2xl text-xs font-bold shadow-sm fade-in leading-relaxed">
                            <span class="px-2.5 py-1 bg-teal-600 text-white rounded-lg text-xs font-black shadow-sm tracking-wider whitespace-nowrap">💡 あなたの初期希望</span>
                            <span class="font-extrabold text-teal-900 bg-white px-3 py-1 rounded-lg border border-teal-200 shadow-sm">${initialHope}</span>
                            <span class="text-slate-700 font-extrabold ml-1.5 hidden sm:inline">プロのアドバイスを踏まえて最終確定してください。</span>
                        </div>
                    `;
                    alertContainer.classList.remove('hidden');
                } else {
                    alertContainer.classList.add('hidden');
                    alertContainer.innerHTML = '';
                }
            }

            const backBtn = document.getElementById('btnWizardBack');
            if (currentQuestionIndex > 0) backBtn.classList.remove('hidden');
            else backBtn.classList.add('hidden');

            const optsContainer = document.getElementById('wizardOptions');
            optsContainer.innerHTML = '';
            
            if (q.options) {
                q.options.forEach(opt => {
                    const row = document.createElement('div');
                    row.className = "flex gap-3 w-full";

                    // Check if this option matches initialHope
                    const isHope = initialHope && (
                        opt.includes(initialHope) || 
                        initialHope.includes(opt.replace(/\([^)]+\)/g, '').trim())
                    );

                    const btnSelect = document.createElement('button');
                    if (isHope) {
                        btnSelect.className = "flex-grow text-left px-6 py-5 bg-teal-50/20 border-2 border-teal-500 hover:border-teal-600 hover:bg-teal-50/40 rounded-2xl text-lg font-bold text-slate-800 transition-all shadow-md flex items-center justify-between group relative overflow-hidden";
                        btnSelect.innerHTML = `
                            <span class="relative z-10 flex items-center gap-2.5">
                                <span class="px-2 py-0.5 bg-teal-500 text-white rounded text-xs font-extrabold shadow-sm tracking-wider">初期希望</span>
                                <span>${opt}</span>
                            </span> 
                            <i class="fa-solid fa-circle-check text-teal-600 text-lg relative z-10"></i>
                            <div class="absolute -right-3 -bottom-3 text-[4rem] text-teal-500/5 rotate-12 pointer-events-none"><i class="fa-solid fa-star"></i></div>
                        `;
                    } else {
                        btnSelect.className = "flex-grow text-left px-6 py-5 bg-white border-2 border-slate-100 hover:border-teal-400 hover:bg-teal-50/50 rounded-2xl text-lg font-bold text-slate-700 transition-all shadow-sm flex items-center justify-between group";
                        btnSelect.innerHTML = `<span>${opt}</span> <i class="fa-solid fa-chevron-right text-slate-300 group-hover:text-teal-500 transition-colors"></i>`;
                    }
                    btnSelect.onclick = () => wizardNext(opt);

                    const btnEdit = document.createElement('button');
                    btnEdit.className = "w-16 flex items-center justify-center bg-white border-2 border-slate-100 hover:border-blue-400 hover:bg-blue-50 hover:text-blue-600 rounded-2xl text-slate-400 transition-all shadow-sm group";
                    btnEdit.title = "この選択肢を編集して使う";
                    btnEdit.innerHTML = '<i class="fa-solid fa-pen group-hover:scale-110 transition-transform"></i>';
                    btnEdit.onclick = () => {
                        const input = document.getElementById('wizardCustomInput');
                        input.value = opt;
                        input.focus();
                        input.scrollIntoView({ behavior: 'smooth', block: 'center' });
                        showToast('編集モード：内容を調整して「決定」を押してください', 'info');
                    };

                    row.appendChild(btnSelect);
                    row.appendChild(btnEdit);
                    optsContainer.appendChild(row);
                });
            }

            document.getElementById('wizardCustomInput').value = '';
            const container = document.getElementById('wizardContainer');
            container.classList.remove('fade-in');
            void container.offsetWidth; 
            container.classList.add('fade-in');
        }

        function wizardNext(value) {
            const q = wizardQuestions[currentQuestionIndex];
            wizardAnswers[q.id] = { label: q.label, value: value };
            currentQuestionIndex++;
            renderWizardStep();
        }

        function wizardNextWithCustom() {
            const val = document.getElementById('wizardCustomInput').value.trim();
            if (!val) { showToast('入力してください', 'error'); return; }
            wizardNext(val);
        }

        function wizardNextWithUnknown() {
            wizardNext("UNKNOWN");
        }

        function wizardBack() {
            if (currentQuestionIndex > 0) {
                currentQuestionIndex--;
                renderWizardStep();
            } else {
                document.getElementById('wizardContainer').classList.remove('hidden');
                document.getElementById('deepVarsContainerUI').classList.add('hidden');
                currentQuestionIndex = wizardQuestions.length - 1;
                renderWizardStep();
            }
        }

        // --- DEEP VARS & FINAL COMPILE ---
        function renderDeepVarsReview() {
            document.getElementById('wizardContainer').classList.add('hidden');
            document.getElementById('deepVarsContainerUI').classList.remove('hidden');

            const container = document.getElementById('deepVariablesList');
            container.innerHTML = '';

            if (rawDeepVars.length === 0) {
                container.innerHTML = '<div class="text-slate-400 text-center py-6">検知された見落としポイントはありません。そのまま生成できます。</div>';
            } else {
                rawDeepVars.forEach((v, idx) => {
                    const isChecked = v.checked === true;
                    const row = document.createElement('div');
                    
                    // Initialize card styling based on checked state
                    row.className = isChecked
                        ? "flex items-start gap-4 p-5 rounded-2xl border-2 border-teal-500 bg-teal-50/20 shadow-md transition-all cursor-pointer select-none"
                        : "flex items-start gap-4 p-5 rounded-2xl border border-slate-200 bg-slate-50 hover:bg-white hover:border-teal-300 transition-all cursor-pointer shadow-sm select-none";
                    
                    row.innerHTML = `
                        <div class="pt-1">
                            <input type="checkbox" id="${v.id}" ${isChecked ? 'checked' : ''} class="h-5 w-5 rounded border-slate-300 text-teal-600 focus:ring-teal-500 cursor-pointer pointer-events-none">
                        </div>
                        <div class="flex-grow cursor-pointer">
                            <span class="text-base sm:text-lg font-black text-slate-900 block mb-1.5"><span class="text-teal-600 mr-2">POINT ${idx+1}.</span>${v.label}</span>
                            <p class="text-sm sm:text-base text-slate-700 leading-relaxed font-bold">${v.detail}</p>
                        </div>
                    `;
                    
                    // Card click event handler
                    row.addEventListener('click', () => {
                        const checkbox = document.getElementById(v.id);
                        if (checkbox) {
                            checkbox.checked = !checkbox.checked;
                            v.checked = checkbox.checked;
                            
                            // Smooth active style transition
                            if (checkbox.checked) {
                                row.className = "flex items-start gap-4 p-5 rounded-2xl border-2 border-teal-500 bg-teal-50/20 shadow-md transition-all cursor-pointer select-none ring-1 ring-teal-500/10";
                            } else {
                                row.className = "flex items-start gap-4 p-5 rounded-2xl border border-slate-200 bg-slate-50 hover:bg-white hover:border-teal-300 transition-all cursor-pointer shadow-sm select-none";
                            }
                            
                            // High-quality micro scale feedback
                            row.style.transform = 'scale(0.985)';
                            setTimeout(() => {
                                row.style.transform = 'none';
                            }, 100);
                        }
                    });
                    
                    container.appendChild(row);
                });
            }
        }

        function finishWizard() {
            const idea = document.getElementById('projectIdea').value || "無題のプロジェクト";
            
            // Read split inputs instead of level1Knowledge
            const goals = document.getElementById('level1Goals').value.trim();
            const constraints = document.getElementById('level1Constraints').value.trim();
            let level1 = "";
            if (goals) level1 += `【目標・ビジョン】\n${goals}\n\n`;
            if (constraints) level1 += `【前提ルール・制約】\n${constraints}`;
            if (!level1) level1 = "(特になし)";
            
            const unknowns = [];
            const knowns = [];
            
            Object.values(wizardAnswers).forEach(ans => {
                if (ans.value === "UNKNOWN" || ans.value === "UNKNOWNに設定する") unknowns.push(ans.label);
                else knowns.push(`* **${ans.label}:** ${ans.value}`);
            });

            const currentDeepStates = [];
            rawDeepVars.forEach(v => {
                const el = document.getElementById(v.id);
                if (el && el.checked) {
                    currentDeepStates.push(`* ${v.label}に対する考慮・対策`);
                }
            });

            let unknownsText = '';
            if (unknowns.length > 0) {
                unknownsText = `\n\n### ⚠️ 【未定の必須項目（AIへの逆質問・提案要求）】
現在、以下の要素が未定となっています。AI側で最も成功確率が高いと思われるベストプラクティスを3つ提案し、議論の土台を作ってください。
${unknowns.map(l => `* ${l}`).join('\n')}`;
            }

            // Save variables to compiledData globally
            compiledData = {
                idea: idea,
                level1: level1,
                knowns: knowns,
                unknowns: unknowns,
                unknownsText: unknownsText,
                deepStates: currentDeepStates
            };

            // Switch to compile style output tab
            document.getElementById('tabOutput').classList.remove('hidden');
            switchTab('output');
            
            // Force status to completed
            setAgentPhase(4);

            // Set style selection to default (pm) and compile prompt
            setPromptStyle(activePromptStyle);
            
            showToast('最終プロンプトのコンパイルが完了しました！', 'success');
        }

        function retryLiveAnalysis() {
            document.getElementById('debateErrorCard').classList.add('hidden');
            document.getElementById('debateTutorialContent').classList.remove('hidden');
            startAnalysisEngine();
        }

        function switchToSimulatedModeAndProceed() {
            document.getElementById('debateErrorCard').classList.add('hidden');
            document.getElementById('debateTutorialContent').classList.remove('hidden');
            document.getElementById('runMode').value = 'simulated';
            showToast('デモモード（擬似演出）に切り替えました。処理を開始します。', 'info');
            startAnalysisEngine();
        }

        function applyExpertPreset(type) {
            const ideaInput = document.getElementById('projectIdea');
            const goalsInput = document.getElementById('level1Goals');
            const constraintsInput = document.getElementById('level1Constraints');
            const guideCard = document.getElementById('presetGuideCard');
            const guideContent = document.getElementById('presetGuideContent');

            if (!ideaInput || !goalsInput || !constraintsInput || !guideCard || !guideContent) return;

            let idea = "";
            let goals = "";
            let constraints = "";
            let guideHtml = "";

            if (type === 'line') {
                idea = "LINEクリエイターズスタンプを作して販売してみたい";
                goals = "・作画方針：手書き";
                constraints = "・申請枚数：24枚";
                guideHtml = `
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 rounded">作画方針：手書き</span>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：温かみや個性をアピールし、現在大量に流通している安易なAI生成スタンプと徹底的な差別化を狙うため。<br>
                            <span class="text-xs text-slate-400 font-medium">（※他には <code>AIイラスト</code> / <code>写真加工</code> からも自由に選択・書き換え可能です）</span>
                        </p>
                    </div>
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 rounded">申請枚数：24枚</span>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：制作の手間（コスト）と、購入したユーザーが日常使いする満足度のバランスが最も良いため。<br>
                            <span class="text-xs text-slate-400 font-medium">（※他には <code>8枚</code> / <code>16枚</code> / <code>32枚</code> からも選択可能です）</span>
                        </p>
                    </div>
                `;
            } else if (type === 'saas') {
                idea = "個人向けのタスク管理SaaSを作ってリリースしたい";
                goals = "・開発範囲：最小限の機能（MVP）のみ";
                constraints = "・開発手法：一番慣れているプログラミング言語";
                guideHtml = `
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-cyan-100 text-cyan-800 rounded">開発範囲：最小限の機能（MVP）</span>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：最初から多機能にせず、最も重要な1つのコア機能だけを最速でリリースしてユーザーの反応（市場適合性）を見るため。<br>
                            <span class="text-xs text-slate-400 font-medium">（※他には <code>複数機能のフルパッケージ</code> などからも書き換え可能です）</span>
                        </p>
                    </div>
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-cyan-100 text-cyan-800 rounded">開発手法：一番慣れているプログラミング言語</span>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：新しい言語やフレームワークの学習コストをゼロにし、リリースまでのスピードを最大化するため。<br>
                            <span class="text-xs text-slate-400 font-medium">（※他には <code>新規の勉強したい言語</code> などからも書き換え可能です）</span>
                        </p>
                    </div>
                `;
            } else if (type === 'ai_art') {
                idea = "AIイラストを販売してオンライン副収入を得たい";
                goals = "・作風ジャンル：特定のテーマに特化";
                constraints = "・画像サイズ：高解像度（アップスケール処理）";
                guideHtml = `
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-purple-100 text-purple-800 rounded">作風ジャンル：特定のテーマに特化</span>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：なんでも屋にならず、「ファンタジー背景」などの特定のニーズに絞ることで、熱狂的なファンやリピーターを確実に増やすため。<br>
                            <span class="text-xs text-slate-400 font-medium">（※他には <code>なんでも描くオールジャンル</code> などからも書き換え可能です）</span>
                        </p>
                    </div>
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-purple-100 text-purple-800 rounded">画像サイズ：高解像度</span>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：購入したユーザーが商用利用や印刷など、どんな用途でも綺麗に使える品質を担保し、顧客満足度を上げて低評価を防ぐため。<br>
                            <span class="text-xs text-slate-400 font-medium">（※他には <code>通常解像度</code> などからも書き換え可能です）</span>
                        </p>
                    </div>
                `;
            } else if (type === 'blog') {
                idea = "得意なテーマでブログを開設して収益化したい";
                goals = "・発信テーマ：自分の得意分野・実体験があるジャンル";
                constraints = "・更新目標：週に1〜2本の高品質な記事";
                guideHtml = `
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-amber-100 text-amber-800 rounded">発信テーマ：自分の得意分野・実体験があるジャンル</span>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：一般論ではなく、自分にしか書けない一次情報（体験談）を書くことで、現在乱立しているAI自動生成記事と徹底的に差別化するため。<br>
                            <span class="text-xs text-slate-400 font-medium">（※他には <code>流行のキーワード・雑記ブログ</code> などからも書き換え可能です）</span>
                        </p>
                    </div>
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-amber-100 text-amber-800 rounded">更新目標：週に1〜2本の高品質な記事</span>
                        </div>
                        <p class="text-xs text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：毎日更新で疲弊して低品質になるのを防ぎ、読者の検索意図（悩み）を完全に解決する本当に価値のある記事の執筆に集中するため。<br>
                            <span class="text-xs text-slate-400 font-medium">（※他には <code>毎日更新</code> などからも書き換え可能です）</span>
                        </p>
                    </div>
                `;
            }

            ideaInput.value = idea;
            goalsInput.value = goals;
            constraintsInput.value = constraints;
            
            guideContent.innerHTML = guideHtml;
            guideCard.classList.remove('hidden');
            showToast('熟練者のこだわり設定サンプルを適用しました！', 'success');
        }


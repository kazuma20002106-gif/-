import re

def refactor_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Color Replacements (Blue -> Lime Green)
    html = html.replace('blue-', 'lime-')
    html = html.replace('neon-text-blue', 'neon-text-lime')
    html = html.replace('cyber-glow-blue', 'cyber-glow-lime')
    html = html.replace('rgba(59, 130, 246', 'rgba(132, 204, 22')
    html = html.replace('#3b82f6', '#84cc16')

    # 2. Header Update (Add LOAD SAVE button)
    header_target = '<!-- API SETTINGS -->'
    header_replacement = '''<!-- EXTRA ACTIONS -->
        <div class="flex items-center gap-3">
            <button onclick="toggleSaveDrawer()" class="px-4 py-2 bg-slate-900 border border-lime-500/50 text-lime-400 rounded text-xs font-bold shadow-[0_0_10px_rgba(132,204,22,0.2)] hover:bg-lime-900/30 transition-all flex items-center gap-2">
                <i class="fa-solid fa-folder-open"></i> LOAD SAVES
            </button>
        </div>
        
        <!-- API SETTINGS -->'''
    html = html.replace(header_target, header_replacement)

    # 3. Main Layout Replacement
    start_marker = '<!-- MAIN INTERFACE -->'
    end_marker = '<!-- TOAST CONTAINERS -->'
    
    new_layout = '''<!-- MAIN INTERFACE -->
    <div id="mainContainer" class="flex-grow relative">
        
        <!-- SAVE DRAWER MODAL -->
        <div id="saveDrawer" class="hidden absolute inset-0 bg-[#060913]/95 backdrop-blur-md z-50 flex flex-col p-6 rounded-xl border border-lime-500/30">
            <div class="flex justify-between items-center mb-6">
                <span class="text-sm text-lime-400 font-bold uppercase tracking-wider">
                    <i class="fa-solid fa-folder-open mr-2"></i> セーブデータ履歴
                </span>
                <div class="flex items-center gap-4">
                    <span class="text-xs px-2 py-1 bg-lime-500/10 text-lime-400 rounded font-mono" id="savedCount">0 Saves</span>
                    <button onclick="toggleSaveDrawer()" class="text-slate-400 hover:text-white transition-colors"><i class="fa-solid fa-xmark text-xl"></i></button>
                </div>
            </div>
            <div id="historyList" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 flex-grow overflow-y-auto">
                <div class="text-slate-500 text-xs text-center py-8 col-span-full">保存されたプロジェクトはここにストックされます</div>
            </div>
        </div>

        <!-- PHASE 1: INPUT VIEW (Centered) -->
        <div id="phase1" class="flex flex-col max-w-3xl mx-auto w-full gap-6 mt-8">
            <div class="cyber-panel p-6 rounded-xl flex flex-col gap-5">
                <div class="text-center mb-2">
                    <i class="fa-solid fa-gamepad text-3xl text-lime-400 neon-text-lime mb-3"></i>
                    <h2 class="text-lg font-bold text-white tracking-widest uppercase">New Project Configuration</h2>
                    <p class="text-[11px] text-slate-400 mt-1">プロジェクトの基本変数をセットアップしてください</p>
                </div>
                
                <div>
                    <label class="block text-xs text-slate-400 uppercase font-bold tracking-wider mb-2">プロジェクト名 / 新規アイデア</label>
                    <input type="text" id="projectIdea" value="LINEクリエイターズスタンプを作して販売してみたい" 
                           class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-lg text-sm text-white focus:outline-none focus:border-lime-500 transition-colors font-semibold"
                           placeholder="例: LINEスタンプを作りたい、YouTube解説動画を作りたい、等">
                </div>

                <div>
                    <label class="block text-xs text-slate-400 mb-2 uppercase font-bold tracking-wider">
                        <i class="fa-solid fa-lightbulb text-lime-500 mr-1"></i> あなたが今知っている初期知識（レベル1）
                    </label>
                    <textarea id="level1Knowledge" rows="6" placeholder="現時点で知っているルール、決め事、制約などを殴り書きしてください。" 
                              class="w-full px-4 py-3 bg-slate-950 border border-slate-800 rounded-lg text-xs text-slate-300 focus:outline-none focus:border-lime-500 transition-colors resize-none code-font leading-relaxed">・価格は120円にしたい。
・自分でイラストを描くか、AIで作るか迷っている。
・パス（AI）に「スタンプのアイデアを考えて」と相談する前に、他に何を決めなきゃいけないのか知りたい。</textarea>
                </div>

                <div class="grid grid-cols-2 gap-4">
                    <div>
                        <label class="block text-[11px] text-slate-400 mb-1 uppercase font-bold">デモ動作モード</label>
                        <select id="runMode" class="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded text-xs text-slate-300 focus:outline-none focus:border-lime-500 font-mono">
                            <option value="simulated">Simulated (擬似演出)</option>
                            <option value="live">Live (Gemini API)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-[11px] text-slate-400 mb-1 uppercase font-bold">プリセットテーマ</label>
                        <select id="presetTheme" onchange="applyPreset()" class="w-full px-3 py-2 bg-slate-950 border border-slate-800 rounded text-xs text-slate-300 focus:outline-none focus:border-lime-500">
                            <option value="custom">-- 自由入力 (カスタム) --</option>
                            <option value="linestamp" selected>LINEスタンプ</option>
                            <option value="lecture">講義スライド資料</option>
                            <option value="youtube">YouTube解説動画</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-4 mt-2">
                    <button onclick="saveCurrentProject()" class="py-3 bg-slate-900 border border-slate-700 hover:border-lime-500/50 text-slate-200 rounded-lg text-xs font-bold flex items-center justify-center gap-2 transition-all">
                        <i class="fa-solid fa-floppy-disk"></i>
                        <span>データをセーブ</span>
                    </button>
                    <button id="btnExecute" onclick="startLevel30Engine()" 
                            class="py-3 bg-lime-600 hover:bg-lime-500 text-black font-extrabold rounded-lg shadow-[0_0_15px_rgba(132,204,22,0.5)] flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5 hover:shadow-[0_0_25px_rgba(132,204,22,0.7)]">
                        <i class="fa-solid fa-rocket"></i>
                        <span>5人委員会 起動</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- PHASE 2: RESULT VIEW (Full Width) -->
        <div id="phase2" class="hidden flex-col gap-4 w-full h-full pb-10">
            <!-- Top controls -->
            <div class="flex justify-between items-center mb-2">
                <button onclick="toggleInitialInfo()" class="px-3 py-1.5 bg-slate-900 border border-slate-800 hover:border-lime-500/30 text-lime-400 rounded text-xs font-mono flex items-center gap-2 transition-colors">
                    <i class="fa-solid fa-eye"></i> 入力情報を確認
                </button>
                <button onclick="createNewProject()" class="px-4 py-1.5 bg-slate-800 hover:bg-slate-700 text-white rounded text-xs font-bold flex items-center gap-2 transition-colors shadow-lg">
                    <i class="fa-solid fa-rotate-left"></i> 新規プロジェクトに戻る
                </button>
            </div>

            <!-- Initial Info Popup -->
            <div id="initialInfoPopup" class="hidden bg-slate-900/95 border border-lime-500/30 p-4 rounded-xl shadow-2xl mb-4">
                <h4 class="text-[10px] text-lime-400 font-bold uppercase mb-2">Initial Inputs</h4>
                <div class="text-xs text-white font-bold mb-1">アイデア: <span id="displayIdea" class="font-normal text-slate-300"></span></div>
                <div class="text-xs text-white font-bold">初期知識: <pre id="displayLevel1" class="font-normal text-slate-400 mt-1 whitespace-pre-wrap font-sans text-[11px]"></pre></div>
            </div>

            <!-- AGENT STATUS PANEL (Horizontal now) -->
            <div class="cyber-panel p-3 rounded-xl flex items-center justify-between gap-2 overflow-x-auto">
                <span class="text-[10px] text-lime-400 font-bold uppercase tracking-wider whitespace-nowrap mr-2">Status</span>
                <div class="flex gap-2 min-w-max">
                    <div id="stat-1" class="flex items-center gap-2 px-3 py-1.5 rounded bg-slate-950/30 border border-slate-900 text-xs"><div class="h-5 w-5 rounded-full bg-indigo-500/10 text-indigo-400 flex items-center justify-center font-bold text-[9px]">戦</div><div class="flex flex-col"><span class="font-bold text-slate-200 text-[10px]">ストラテジスト</span><span class="text-[8px] text-slate-500 font-mono" id="stat-text-1">Idle</span></div></div>
                    <div id="stat-2" class="flex items-center gap-2 px-3 py-1.5 rounded bg-slate-950/30 border border-slate-900 text-xs"><div class="h-5 w-5 rounded-full bg-cyan-500/10 text-cyan-400 flex items-center justify-center font-bold text-[9px]">規</div><div class="flex flex-col"><span class="font-bold text-slate-200 text-[10px]">仕様監修</span><span class="text-[8px] text-slate-500 font-mono" id="stat-text-2">Idle</span></div></div>
                    <div id="stat-3" class="flex items-center gap-2 px-3 py-1.5 rounded bg-slate-950/30 border border-slate-900 text-xs"><div class="h-5 w-5 rounded-full bg-purple-500/10 text-purple-400 flex items-center justify-center font-bold text-[9px]">意</div><div class="flex flex-col"><span class="font-bold text-slate-200 text-[10px]">デザイナー</span><span class="text-[8px] text-slate-500 font-mono" id="stat-text-3">Idle</span></div></div>
                    <div id="stat-4" class="flex items-center gap-2 px-3 py-1.5 rounded bg-slate-950/30 border border-slate-900 text-xs"><div class="h-5 w-5 rounded-full bg-amber-500/10 text-amber-400 flex items-center justify-center font-bold text-[9px]">収</div><div class="flex flex-col"><span class="font-bold text-slate-200 text-[10px]">マネタイズ</span><span class="text-[8px] text-slate-500 font-mono" id="stat-text-4">Idle</span></div></div>
                    <div id="stat-5" class="flex items-center gap-2 px-3 py-1.5 rounded bg-slate-950/30 border border-slate-900 text-xs"><div class="h-5 w-5 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center font-bold text-[9px]">パ</div><div class="flex flex-col"><span class="font-bold text-slate-200 text-[10px]">統合(パス)</span><span class="text-[8px] text-slate-500 font-mono" id="stat-text-5">Idle</span></div></div>
                </div>
            </div>

            <!-- Realtime Flow Chips -->
            <div class="bg-slate-950 border border-slate-800 p-2.5 rounded-xl flex items-center justify-center overflow-x-auto gap-3">
                <div id="chip-1" class="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-900 text-[10px] text-slate-500 font-mono transition-colors"><span class="h-1.5 w-1.5 rounded-full bg-slate-700" id="dot-1"></span><span>1.Strategy</span></div><i class="fa-solid fa-angle-right text-slate-800 text-[9px]"></i>
                <div id="chip-2" class="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-900 text-[10px] text-slate-500 font-mono transition-colors"><span class="h-1.5 w-1.5 rounded-full bg-slate-700" id="dot-2"></span><span>2.Rules</span></div><i class="fa-solid fa-angle-right text-slate-800 text-[9px]"></i>
                <div id="chip-3" class="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-900 text-[10px] text-slate-500 font-mono transition-colors"><span class="h-1.5 w-1.5 rounded-full bg-slate-700" id="dot-3"></span><span>3.Design</span></div><i class="fa-solid fa-angle-right text-slate-800 text-[9px]"></i>
                <div id="chip-4" class="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-900 text-[10px] text-slate-500 font-mono transition-colors"><span class="h-1.5 w-1.5 rounded-full bg-slate-700" id="dot-4"></span><span>4.Business</span></div><i class="fa-solid fa-angle-right text-slate-800 text-[9px]"></i>
                <div id="chip-5" class="flex items-center gap-1.5 px-2.5 py-1 rounded bg-slate-900 text-[10px] text-slate-500 font-mono transition-colors"><span class="h-1.5 w-1.5 rounded-full bg-slate-700" id="dot-5"></span><span>5.Compile</span></div>
            </div>

            <!-- TABS & OUTPUT FRAMEWORK -->
            <div class="flex-grow bg-slate-950 border border-slate-800 rounded-xl overflow-hidden flex flex-col min-h-[500px]">
                <!-- Tab Headers -->
                <div class="flex justify-between items-center bg-slate-900/90 px-4 py-2 border-b border-slate-800">
                    <div class="flex gap-1.5">
                        <button id="tabTerminal" onclick="switchTab('terminal')" class="px-3 py-1.5 text-xs font-bold text-lime-400 border-b-2 border-lime-500">
                            <i class="fa-solid fa-terminal mr-1"></i> DEBATE LOG
                        </button>
                        <button id="tabBuilder" onclick="switchTab('builder')" class="px-3 py-1.5 text-xs font-bold text-slate-400 hover:text-white transition-colors relative">
                            <i class="fa-solid fa-sliders mr-1"></i> LEVEL 300 FORM
                            <span id="formReadyBadge" class="hidden absolute -top-1 -right-2 h-2.5 w-2.5 bg-lime-500 rounded-full animate-ping"></span>
                        </button>
                        <button id="tabOutput" onclick="switchTab('output')" class="px-3 py-1.5 text-xs font-bold text-slate-400 hover:text-white transition-colors">
                            <i class="fa-solid fa-file-invoice mr-1"></i> FINAL PROMPT
                        </button>
                    </div>
                    <div class="flex gap-1.5">
                        <button onclick="copyGeneratedPrompt()" class="px-3 py-1.5 text-[10px] bg-lime-950/40 text-lime-400 rounded border border-lime-500/30 hover:bg-lime-900/60 transition-colors font-bold font-mono">
                            <i class="fa-regular fa-copy mr-1"></i> COPY PROMPT
                        </button>
                    </div>
                </div>

                <!-- TAB 1: DEBATE LOG -->
                <div id="terminalArea" class="flex-grow p-5 overflow-y-auto bg-[#020409] text-lime-400 code-font text-xs leading-relaxed shadow-[inset_0_0_20px_rgba(0,0,0,0.8)]">
                    <div class="text-slate-500 mb-2">// VIRTUAL COMMITTEE ENGINE ONLINE.</div>
                    <div id="consoleLog"></div>
                </div>

                <!-- TAB 2: LEVEL 300 INTERACTIVE BUILDER (Form) -->
                <div id="builderArea" class="hidden flex-grow p-6 overflow-y-auto bg-[#050915] text-slate-300 text-xs">
                    <div id="builderEmptyState" class="text-slate-500 text-center py-16">
                        <i class="fa-solid fa-circle-info text-3xl mb-3 block text-slate-600"></i>
                        エージェントによるハックが完了すると、ここに「基本条件」と「盲点デバッグ」を動的に選択・編集できるフォームが展開します。
                    </div>
                    <div id="builderContent" class="hidden space-y-6 max-w-4xl mx-auto">
                        <div class="p-4 bg-lime-950/10 border border-lime-500/20 rounded-lg shadow-[0_0_15px_rgba(132,204,22,0.05)]">
                            <h4 class="font-extrabold text-lime-400 text-sm uppercase mb-1 flex items-center gap-2">
                                <i class="fa-solid fa-layer-group"></i> レベル300・意思決定フォーム
                            </h4>
                            <p class="text-[11px] text-slate-400">以下を選択・編集するだけで、最下部のコピペ用プロンプトがリアルタイムで進化します。</p>
                        </div>

                        <!-- Level 1 Base Variables -->
                        <div class="bg-slate-900/30 p-4 rounded-xl border border-slate-800">
                            <span class="text-sm font-bold text-white border-b border-slate-700 pb-2 block mb-4 flex items-center gap-2">
                                <span class="bg-lime-500 text-black px-2 py-0.5 rounded text-[10px]">1階</span> 必須基礎確定要件
                            </span>
                            <div class="space-y-4" id="baseVariablesContainer"></div>
                        </div>

                        <!-- Level 30 Deep Variables -->
                        <div class="bg-slate-900/30 p-4 rounded-xl border border-slate-800">
                            <span class="text-sm font-bold text-white border-b border-slate-700 pb-2 block mb-4 flex items-center gap-2">
                                <span class="bg-lime-500 text-black px-2 py-0.5 rounded text-[10px]">2階</span> プロの盲点デバッグ
                            </span>
                            <div class="space-y-3" id="deepVariablesContainer"></div>
                        </div>
                    </div>
                </div>

                <!-- TAB 3: COMPILED FINAL PROMPT -->
                <div id="outputArea" class="hidden flex-grow p-6 overflow-y-auto bg-[#020409] text-slate-300 code-font text-xs leading-relaxed shadow-[inset_0_0_20px_rgba(0,0,0,0.8)]">
                    <textarea id="finalPromptResult" class="w-full h-full bg-transparent border-none text-slate-300 focus:outline-none resize-none leading-relaxed" readonly>ここに極上の指示プロンプトが編纂されます。</textarea>
                </div>

                <!-- Bottom Progress Bar -->
                <div class="h-1.5 bg-slate-900 relative">
                    <div id="progressBar" class="h-full bg-lime-500 w-0 transition-all duration-300 shadow-[0_0_10px_rgba(132,204,22,0.8)]"></div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- TOAST CONTAINERS -->'''
    
    start_idx = html.find(start_marker)
    end_idx = html.find(end_marker)
    if start_idx != -1 and end_idx != -1:
        html = html[:start_idx] + new_layout + html[end_idx:]

    # 4. JavaScript Updates for New UI behaviors
    js_additions = '''
        // --- NEW UI BEHAVIORS ---
        function toggleSaveDrawer() {
            const drawer = document.getElementById('saveDrawer');
            if (drawer.classList.contains('hidden')) {
                drawer.classList.remove('hidden');
            } else {
                drawer.classList.add('hidden');
            }
        }
        
        function toggleInitialInfo() {
            const popup = document.getElementById('initialInfoPopup');
            if (popup.classList.contains('hidden')) {
                popup.classList.remove('hidden');
            } else {
                popup.classList.add('hidden');
            }
        }

        // --- OVERRIDE CREATE NEW PROJECT ---
        function createNewProject() {
            document.getElementById('phase2').classList.add('hidden');
            document.getElementById('phase2').classList.remove('flex');
            document.getElementById('phase1').classList.remove('hidden');
            document.getElementById('phase1').classList.add('flex');
            
            document.getElementById('projectIdea').value = '新規アイデア';
            document.getElementById('level1Knowledge').value = '';
            document.getElementById('presetTheme').value = 'custom';
            activePreset = 'custom';
            
            document.getElementById('builderEmptyState').classList.remove('hidden');
            document.getElementById('builderContent').classList.add('hidden');
            document.getElementById('formReadyBadge').classList.add('hidden');
            
            const drawer = document.getElementById('saveDrawer');
            if (!drawer.classList.contains('hidden')) drawer.classList.add('hidden');
            
            showToast('新規プロジェクト用の入力画面を展開しました。', 'info');
        }
'''
    html = html.replace('// --- MAIN APP JAVASCRIPT ---', '// --- MAIN APP JAVASCRIPT ---\n' + js_additions)
    
    # 5. Inject Phase transitions in startLevel30Engine
    start_engine_target = '''            writeToConsole('SYSTEM', `『${idea}』の前提変数（解くべき変数）ハックシーケンスをロードします。`, 'system');
            await delay(800);'''
    start_engine_replacement = '''            // Transition to Phase 2
            document.getElementById('phase1').classList.add('hidden');
            document.getElementById('phase1').classList.remove('flex');
            document.getElementById('phase2').classList.remove('hidden');
            document.getElementById('phase2').classList.add('flex');
            
            document.getElementById('displayIdea').innerText = idea;
            document.getElementById('displayLevel1').innerText = level1 || '(なし)';
            
            writeToConsole('SYSTEM', `『${idea}』の前提変数（解くべき変数）ハックシーケンスをロードします。`, 'system');
            await delay(800);'''
    html = html.replace(start_engine_target, start_engine_replacement)
    
    # 6. Override loadSavedProject to also jump to phase 2 layout if variables are loaded
    load_save_target = '''            if (proj.baseVars || proj.deepVars) {
                renderLoadedInteractiveForm(proj);
            } else {'''
    load_save_replacement = '''            if (proj.baseVars || proj.deepVars) {
                document.getElementById('phase1').classList.add('hidden');
                document.getElementById('phase1').classList.remove('flex');
                document.getElementById('phase2').classList.remove('hidden');
                document.getElementById('phase2').classList.add('flex');
                document.getElementById('displayIdea').innerText = proj.name;
                document.getElementById('displayLevel1').innerText = proj.level1 || '(なし)';
                
                toggleSaveDrawer();
                renderLoadedInteractiveForm(proj);
            } else {'''
    html = html.replace(load_save_target, load_save_replacement)
    
    # 7. Add active/inactive logic in switchTab colors (lime instead of blue)
    switch_tab_target = '''            [btnTerm, btnBuild, btnOut].forEach(b => b.className = "px-3 py-1.5 text-xs font-bold text-slate-400 hover:text-white transition-colors");'''
    switch_tab_replacement = switch_tab_target
    html = html.replace(switch_tab_target, switch_tab_replacement)

    # Note: color replacements for btnTerm class string: 
    # original had text-blue-400 border-b-2 border-blue-500. After replace -> text-lime-400 border-lime-500.
    
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print("Refactor completed.")

refactor_html('Level 30 Booster.html')

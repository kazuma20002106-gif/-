html_content = r"""<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>PRE-PUT DASHBOARD - MULTI-AGENT SYSTEM</title>
    <!-- Tailwind CSS & FontAwesome -->
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css">
    <!-- Google Fonts -->
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Config file for API Key -->
    <script src="config.js"></script>

    <style>
        /* Dynamic Font Size Control */
        html {
            font-size: 16px;
            transition: font-size 0.15s ease;
        }
        html.font-size-medium { font-size: 16px; }
        html.font-size-large { font-size: 18px; }
        html.font-size-xl { font-size: 20px; }

        body {
            font-family: 'Inter', 'Segoe UI', 'BIZ UDPGothic', 'Hiragino Kaku Gothic ProN', 'Meiryo', sans-serif;
            background-color: #F8FAFC;
            color: #1E293B;
            -webkit-font-smoothing: antialiased;
            -moz-osx-font-smoothing: grayscale;
        }

        /* Accessibility Contrast Boost:
           灰色の補足テキストの視認性を、画面のメリハリ（階層構造）を100%保ったまま根本的に底上げします */
        .text-slate-300 { color: #94A3B8 !important; }
        .text-slate-400, .text-slate-400 * { color: #64748B !important; }
        .text-slate-500, .text-slate-500 * { color: #475569 !important; }
        .text-slate-600, .text-slate-600 * { color: #334155 !important; }

        /* Dynamic Tooltip Styles */
        .tooltip-container {
            position: relative;
            display: inline-flex;
            align-items: center;
        }
        .tooltip-box {
            position: absolute;
            bottom: calc(100% + 12px);
            left: 50%;
            transform: translateX(-50%) translateY(8px);
            width: 280px;
            padding: 1rem;
            background-color: rgba(15, 23, 42, 0.96);
            backdrop-filter: blur(8px);
            color: #f8fafc;
            border-radius: 1rem;
            font-size: 0.75rem;
            line-height: 1.5;
            font-weight: 500;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.3), 0 8px 10px -6px rgba(0, 0, 0, 0.3);
            border: 1px solid rgba(255, 255, 255, 0.1);
            opacity: 0;
            visibility: hidden;
            pointer-events: none;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
            z-index: 100;
            text-align: left;
            white-space: normal;
        }
        .tooltip-box::after {
            content: '';
            position: absolute;
            top: 100%;
            left: 50%;
            transform: translateX(-50%);
            border-width: 6px;
            border-style: solid;
            border-color: rgba(15, 23, 42, 0.96) transparent transparent transparent;
        }
        .tooltip-container:hover .tooltip-box,
        .tooltip-container:focus-within .tooltip-box {
            opacity: 1;
            visibility: visible;
            transform: translateX(-50%) translateY(0);
        }

        .code-font {
            font-family: 'Fira Code', monospace;
        }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: #CBD5E1; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #94A3B8; }
        
                .gradient-bg-light { background: linear-gradient(-45deg, #f8fafc, #f0fdfa, #f8fafc, #e0f2fe); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-indigo { background: linear-gradient(-45deg, #f8fafc, #e0e7ff, #f8fafc, #c7d2fe); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-cyan { background: linear-gradient(-45deg, #f8fafc, #cffafe, #f8fafc, #a5f3fc); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-purple { background: linear-gradient(-45deg, #f8fafc, #f3e8ff, #f8fafc, #d8b4fe); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-amber { background: linear-gradient(-45deg, #f8fafc, #fef3c7, #f8fafc, #fde68a); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-emerald { background: linear-gradient(-45deg, #f8fafc, #d1fae5, #f8fafc, #a7f3d0); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        .gradient-bg-rose { background: linear-gradient(-45deg, #f8fafc, #ffe4e6, #f8fafc, #fecdd3); background-size: 400% 400%; animation: gradient 10s ease infinite; }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        .blur-in { animation: blurIn 1.5s ease-out forwards; }
        @keyframes blurIn {
            0% { opacity: 0; filter: blur(10px); transform: scale(0.95); }
            100% { opacity: 1; filter: blur(0); transform: scale(1); }
        }
        .delayed-fade-in {
            opacity: 0;
            animation: fadeIn 1s ease-in-out 1.5s forwards;
        }

        .fade-in { animation: fadeIn 0.3s ease-in-out; }
        @keyframes fadeIn { from { opacity: 0; transform: translateY(10px); } to { opacity: 1; transform: translateY(0); } }
        
        @keyframes slideInRight { from { opacity: 0; transform: translateX(20px); } to { opacity: 1; transform: translateX(0); } }
        .slide-in-right { animation: slideInRight 0.4s ease-out forwards; }

        /* Stepper Tabs */
        .tab-btn { display: flex; align-items: center; padding: 1rem 1.25rem; font-size: 0.875rem; font-weight: 700; color: #64748b; border-bottom: 2px solid transparent; position: relative; transition: all 0.2s; cursor: pointer; background: transparent; }
        .tab-btn:hover:not(.active) { color: #1e293b; background-color: #f8fafc; }
        .tab-btn .step-num { display: flex; align-items: center; justify-content: center; width: 1.25rem; height: 1.25rem; border-radius: 9999px; background-color: #e2e8f0; color: #475569; font-size: 0.75rem; margin-right: 0.5rem; transition: all 0.2s; font-family: 'Fira Code', monospace; }
        .tab-btn.active { color: #0d9488; border-bottom-color: #14b8a6; }
        .tab-btn.active .step-num { background-color: #ccfbf1; color: #0f766e; }
        .tab-btn.completed .step-num { background-color: #10b981; color: white; border: none; }
        .tab-btn.completed .step-num::before { content: '\f00c'; font-family: 'Font Awesome 6 Free'; font-weight: 900; }
        .tab-btn.completed .step-num span { display: none; }
    </style>
</head>
<body class="min-h-screen flex flex-col p-4 md:p-8 pb-20 relative text-slate-800">

    <!-- Rich Background Decorations -->
    <div class="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div class="absolute top-[-10%] left-[-5%] w-[40%] h-[40%] rounded-full bg-teal-400/15 blur-[100px] animate-pulse" style="animation-duration: 8s;"></div>
        <div class="absolute bottom-[-10%] right-[-5%] w-[40%] h-[40%] rounded-full bg-blue-500/10 blur-[100px] animate-pulse" style="animation-duration: 10s; animation-delay: 2s;"></div>
    </div>
    
    <!-- HEADER -->
    <header id="appHeader" class="flex flex-col transition-all duration-500 overflow-hidden relative z-10 xl:flex-row justify-between items-start xl:items-center mb-8 pb-4 border-b border-slate-200 gap-4 max-w-[1400px] mx-auto w-full">
        <div>
            <div class="flex items-center gap-3">
                <span class="px-3 py-1 text-xs font-bold bg-teal-50 text-teal-600 rounded border border-teal-200 uppercase tracking-widest font-mono">SYSTEM ONLINE</span>
                <h1 class="text-3xl uppercase flex items-baseline">
                    <span class="font-black italic tracking-tighter text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-600 drop-shadow-sm pr-1 mr-2">PRE-PUT</span>
                    <span class="font-medium tracking-[0.2em] text-slate-400 text-xl">DASHBOARD</span>
                    <span class="px-2 py-1 bg-slate-200 text-slate-600 rounded text-[10px] font-bold ml-4 tracking-normal align-middle self-center">v2.1.0-Depth</span>
                </h1>
            </div>
            <p class="text-sm text-slate-500 mt-2 font-medium">前提を組み、スタートラインを突き抜ける。</p>
        </div>
        
        <!-- EXTRA ACTIONS -->
        <div class="flex flex-wrap items-center gap-3">
            <button onclick="toggleSaveDrawer()" class="px-5 py-2.5 bg-white border border-slate-200 text-slate-600 hover:text-teal-600 rounded-lg text-sm font-bold shadow-sm hover:shadow transition-all flex items-center gap-2">
                <i class="fa-regular fa-folder-open"></i> LOAD SAVES
            </button>
            <div class="flex items-center justify-between text-sm text-slate-500 bg-slate-100 px-4 py-2.5 rounded-lg border border-slate-200 shrink-0 gap-2 font-semibold">
                <div class="flex items-center">
                    <span class="h-2.5 w-2.5 rounded-full bg-teal-500 mr-2 shadow-[0_0_5px_rgba(20,184,166,0.5)]"></span>
                    <span class="font-mono">GEMINI-2.5-FLASH</span>
                </div>
            </div>
        </div>
    </header>

    <!-- MAIN INTERFACE -->
    <div id="mainContainer" class="flex-grow relative w-full max-w-7xl mx-auto">
        
        <!-- SAVE DRAWER MODAL -->
        <div id="saveDrawer" class="hidden absolute inset-0 bg-slate-900/40 backdrop-blur-sm z-50 flex flex-col p-6 rounded-2xl border border-slate-200">
            <div class="bg-white h-full w-full rounded-xl shadow-2xl flex flex-col overflow-hidden">
                <div class="flex justify-between items-center p-6 border-b border-slate-100 bg-slate-50">
                    <span class="text-base text-slate-800 font-bold uppercase tracking-wider flex items-center">
                        <i class="fa-regular fa-folder-open mr-2 text-teal-600"></i> セーブデータ履歴
                    </span>
                    <div class="flex items-center gap-4">
                        <span class="text-sm px-3 py-1 bg-teal-50 text-teal-700 rounded-full font-mono font-bold" id="savedCount">0 Saves</span>
                        <button onclick="toggleSaveDrawer()" class="text-slate-400 hover:text-slate-700 transition-colors"><i class="fa-solid fa-xmark text-2xl"></i></button>
                    </div>
                </div>
                <div id="historyList" class="p-6 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 overflow-y-auto bg-slate-50/50 flex-grow"></div>
            </div>
        </div>

        <!-- PHASE 1: INPUT VIEW (Centered) -->
        <div id="phase1" class="flex flex-col max-w-5xl mx-auto w-full gap-6 mt-4">
            <div class="bg-white p-6 md:p-8 rounded-2xl shadow-sm border border-slate-200 flex flex-col gap-5">
                <div class="text-center mb-1">
                    <div class="h-10 w-10 bg-teal-50 text-teal-600 rounded-full flex items-center justify-center mx-auto mb-3 shadow-sm">
                        <i class="fa-solid fa-sliders text-lg"></i>
                    </div>
                    <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight">New Project Configuration</h2>
                    <p class="text-base text-slate-500 mt-1 font-medium">プロジェクトの基本変数をセットアップしてください</p>
                </div>
                
                <div>
                    <label class="block text-base text-slate-600 font-bold tracking-wider mb-2">プロジェクト名 / 新規アイデア</label>
                    <input type="text" id="projectIdea" value="" 
                           class="w-full px-5 py-4 bg-slate-50 border border-slate-200 rounded-xl text-lg text-slate-800 focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 transition-all font-semibold"
                           placeholder="例: LINEクリエイターズスタンプを作って販売してみたい">
                </div>

                <!-- Quick Preset Tags (Mentoring Preset Guides) -->
                <div class="mb-6 bg-slate-50/50 border border-slate-200/60 rounded-2xl p-5">
                    <div class="flex items-center gap-2 text-slate-700 font-bold text-base tracking-wider mb-2">
                        <i class="fa-regular fa-lightbulb text-amber-500 text-base animate-pulse"></i>
                        <span>💡 熟練者のこだわりサンプル（初心者の方へおすすめ！）</span>
                    </div>
                    <p class="text-sm text-slate-500 mb-4 leading-relaxed font-medium">
                        「最初から何を決めればいいか分からない」という方は、以下のジャンルをタップしてみてください。プロや経験者が実際に設定している「こだわりの記入例」が自動セットされ、すぐ下に「その選択にしている論理的な理由」と「他の正しい選択肢」がビジュアル解説されます。ご自身のアイデアの参考にしながら自由に書き換えて使えます。※何も決まっていなければ空欄のままでスタートしても、AIがすべてを質問で引き出してくれます！
                    </p>
                    <div class="flex flex-wrap gap-2.5">
                        <button type="button" onclick="applyExpertPreset('line')" class="px-5 py-2.5 text-sm bg-white hover:bg-teal-50 text-slate-700 hover:text-teal-600 rounded-xl border border-slate-200 hover:border-teal-300 font-bold transition-all shadow-sm flex items-center gap-1.5 transform hover:-translate-y-0.5">
                            <span class="h-2 w-2 rounded-full bg-emerald-500"></span> LINEスタンプ販売
                        </button>
                        <button type="button" onclick="applyExpertPreset('saas')" class="px-5 py-2.5 text-sm bg-white hover:bg-blue-50 text-slate-700 hover:text-blue-600 rounded-xl border border-slate-200 hover:border-blue-300 font-bold transition-all shadow-sm flex items-center gap-1.5 transform hover:-translate-y-0.5">
                            <span class="h-2 w-2 rounded-full bg-cyan-500"></span> Webアプリ個人開発
                        </button>
                        <button type="button" onclick="applyExpertPreset('ai_art')" class="px-5 py-2.5 text-sm bg-white hover:bg-purple-50 text-slate-700 hover:text-purple-600 rounded-xl border border-slate-200 hover:border-purple-300 font-bold transition-all shadow-sm flex items-center gap-1.5 transform hover:-translate-y-0.5">
                            <span class="h-2 w-2 rounded-full bg-purple-500"></span> AIイラスト素材販売
                        </button>
                        <button type="button" onclick="applyExpertPreset('blog')" class="px-5 py-2.5 text-sm bg-white hover:bg-amber-50 text-slate-700 hover:text-amber-600 rounded-xl border border-slate-200 hover:border-amber-300 font-bold transition-all shadow-sm flex items-center gap-1.5 transform hover:-translate-y-0.5">
                            <span class="h-2 w-2 rounded-full bg-amber-500"></span> ブログ・アフィリエイト
                        </button>
                    </div>
                </div>

                <!-- Split Inputs -->
                <div class="mb-4 bg-slate-50/20 border border-slate-200/50 rounded-2xl p-5">
                    <div class="flex items-center gap-2 text-slate-700 font-bold text-base tracking-wider mb-4">
                        <i class="fa-solid fa-sliders text-teal-600"></i>
                        <span>こだわり設定（空欄のままでスタートしてもOK！）</span>
                    </div>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-5">
                        <div>
                            <label class="block text-base text-slate-600 mb-2 font-bold tracking-wider flex items-center gap-1.5">
                                <i class="fa-solid fa-bullseye text-teal-500"></i> 1. 目標・実現したいビジョン（こだわり）
                            </label>
                            <textarea id="level1Goals" rows="3" 
                                      class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-700 focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 transition-all resize-none leading-relaxed font-medium"
                                      placeholder="（例：価格は120円にしたい、AIイラストで作ってみたい、等。空欄でもOK！）"></textarea>
                        </div>
                        <div>
                            <label class="block text-base text-slate-600 mb-2 font-bold tracking-wider flex items-center gap-1.5">
                                <i class="fa-solid fa-shield-halved text-teal-500"></i> 2. 前提ルール・把握している制約（こだわり）
                            </label>
                            <textarea id="level1Constraints" rows="3" 
                                      class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-sm text-slate-700 focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 transition-all resize-none leading-relaxed font-medium"
                                      placeholder="（例：スタンプは8枚必要、商用利用可能モデルを使う、等。空欄でもOK！）"></textarea>
                        </div>
                    </div>
                </div>

                <!-- PRO REASONING PANEL (Hidden by Default) -->
                <div id="presetGuideCard" class="hidden bg-teal-50/40 border border-teal-100/80 rounded-2xl p-5 mt-4 shadow-sm fade-in">
                    <div class="flex items-center gap-2 text-teal-800 font-bold text-xs uppercase tracking-wider mb-3">
                        <i class="fa-regular fa-lightbulb text-teal-500 text-sm animate-pulse"></i>
                        <span>プロのこだわり思考プロセス（解説）</span>
                    </div>
                    <div id="presetGuideContent" class="text-xs text-slate-600 space-y-3 font-medium leading-relaxed">
                        <!-- JavaScriptで動的に注入 -->
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-6">
                    <div>
                        <label class="block text-xs text-slate-500 mb-2 uppercase font-bold">デモ動作モード</label>
                        <select id="runMode" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-700 focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 font-mono font-medium cursor-pointer">
                            <option value="live">Live (Gemini API)</option>
                            <option value="simulated">Simulated (擬似演出)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-xs text-slate-500 mb-2 uppercase font-bold">分析の深さ（情報量）</label>
                        <select id="analysisDepth" class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-lg text-sm text-slate-700 focus:outline-none focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 font-medium cursor-pointer">
                            <option value="light">🟢 Light（サクッと大枠のみ）</option>
                            <option value="standard" selected>🟡 Standard（基本と盲点を網羅）</option>
                            <option value="pro">🔴 Pro（失敗できない徹底解析）</option>
                        </select>
                    </div>
                </div>

                <div class="grid grid-cols-2 gap-6 mt-4 pt-8 border-t border-slate-100">
                    <button onclick="saveCurrentProject()" class="py-4 bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-700 rounded-xl text-sm font-bold flex items-center justify-center gap-2 transition-all shadow-sm">
                        <i class="fa-regular fa-floppy-disk"></i>
                        <span>データをセーブ</span>
                    </button>
                    <button id="btnExecute" onclick="startAnalysisEngine()" 
                            class="py-4 bg-teal-600 hover:bg-teal-700 text-white font-extrabold rounded-xl shadow-md shadow-teal-500/20 flex items-center justify-center gap-2 transition-all transform hover:-translate-y-0.5">
                        <i class="fa-solid fa-bolt"></i>
                        <span>分析を開始する</span>
                    </button>
                </div>
            </div>
        </div>

        <!-- PHASE 2: RESULT VIEW (Full Width) -->
        <div id="phase2" class="hidden flex-col gap-6 w-full pb-10">
            <!-- Top controls -->
            <div class="flex justify-between items-center mb-2">
                <button onclick="toggleInitialInfo()" class="px-5 py-2.5 bg-white border border-slate-200 hover:bg-slate-50 text-slate-700 rounded-lg text-sm font-bold flex items-center gap-2 transition-colors shadow-sm">
                    <i class="fa-regular fa-eye text-teal-600"></i> 初期入力を確認
                </button>
                <button onclick="createNewProject()" class="px-5 py-2.5 bg-slate-800 hover:bg-slate-900 text-white rounded-lg text-sm font-bold flex items-center gap-2 transition-colors shadow-sm">
                    <i class="fa-solid fa-rotate-left"></i> 新規プロジェクトに戻る
                </button>
            </div>

            <!-- Initial Info Popup -->
            <div id="initialInfoPopup" class="hidden bg-white border border-slate-200 p-6 rounded-2xl shadow-xl mb-4 relative overflow-hidden">
                <div class="absolute top-0 left-0 w-1.5 h-full bg-teal-500"></div>
                <h4 class="text-xs text-teal-600 font-bold uppercase mb-4 tracking-wider">Initial Inputs</h4>
                <div class="text-sm text-slate-800 font-bold mb-3">アイデア: <span id="displayIdea" class="font-medium text-slate-600 ml-2"></span></div>
                <div class="text-sm text-slate-800 font-bold">初期知識: <pre id="displayLevel1" class="font-medium text-slate-600 mt-3 bg-slate-50 p-4 rounded-xl whitespace-pre-wrap font-sans text-xs border border-slate-100 leading-relaxed"></pre></div>
                <div class="text-sm text-slate-800 font-bold mt-3">分析深度: <span id="displayDepth" class="font-medium text-slate-600 ml-2 uppercase"></span></div>
            </div>

            <!-- AGENT STATUS PANEL -->
            <div class="bg-white border border-slate-200 shadow-sm rounded-2xl flex flex-col">
                <div class="flex items-center gap-3 px-3 py-4 overflow-x-auto">
                    <span class="text-xs text-slate-400 font-bold uppercase tracking-wider whitespace-nowrap px-3">Agent Status</span>
                    <div class="flex gap-3 min-w-max">
                        <div id="stat-1" class="flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 border border-transparent text-sm transition-colors"><div class="h-8 w-8 rounded-full bg-indigo-100 text-indigo-600 flex items-center justify-center font-bold text-xs shadow-sm"><i class="fa-solid fa-chess-knight"></i></div><div class="flex flex-col"><span class="font-bold text-slate-700 text-xs">戦略分析</span><span class="text-[10px] text-indigo-500 font-mono font-bold" id="stat-text-1">STRATEGY</span></div></div>
                        <div id="stat-2" class="flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 border border-transparent text-sm transition-colors"><div class="h-8 w-8 rounded-full bg-cyan-100 text-cyan-600 flex items-center justify-center font-bold text-xs shadow-sm"><i class="fa-solid fa-ruler-combined"></i></div><div class="flex flex-col"><span class="font-bold text-slate-700 text-xs">仕様監査</span><span class="text-[10px] text-cyan-500 font-mono font-bold" id="stat-text-2">TECH</span></div></div>
                        <div id="stat-3" class="flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 border border-transparent text-sm transition-colors"><div class="h-8 w-8 rounded-full bg-purple-100 text-purple-600 flex items-center justify-center font-bold text-xs shadow-sm"><i class="fa-solid fa-pen-nib"></i></div><div class="flex flex-col"><span class="font-bold text-slate-700 text-xs">意匠設計</span><span class="text-[10px] text-purple-500 font-mono font-bold" id="stat-text-3">DESIGN</span></div></div>
                        <div id="stat-4" class="flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 border border-transparent text-sm transition-colors"><div class="h-8 w-8 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center font-bold text-xs shadow-sm"><i class="fa-solid fa-chart-line"></i></div><div class="flex flex-col"><span class="font-bold text-slate-700 text-xs">収益モデリング</span><span class="text-[10px] text-amber-500 font-mono font-bold" id="stat-text-4">BUSINESS</span></div></div>
                        <div id="stat-5" class="flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 border border-transparent text-sm transition-colors"><div class="h-8 w-8 rounded-full bg-emerald-100 text-emerald-600 flex items-center justify-center font-bold text-xs shadow-sm"><i class="fa-solid fa-filter"></i></div><div class="flex flex-col"><span class="font-bold text-slate-700 text-xs">要件抽出</span><span class="text-[10px] text-emerald-500 font-mono font-bold" id="stat-text-5">COMPILER</span></div></div>
                        <div id="stat-6" class="flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 border border-transparent text-sm transition-colors"><div class="h-8 w-8 rounded-full bg-rose-100 text-rose-600 flex items-center justify-center font-bold text-xs shadow-sm"><i class="fa-solid fa-wand-magic-sparkles"></i></div><div class="flex flex-col"><span class="font-bold text-slate-700 text-xs">選択肢生成</span><span class="text-[10px] text-rose-500 font-mono font-bold" id="stat-text-6">WIZARD</span></div></div>
                    </div>
                </div>
                <!-- GLOBAL STATUS INDICATOR -->
                <div id="currentGlobalStatus" class="hidden items-center gap-3 px-5 py-3 border-t border-slate-100 bg-slate-50/50 rounded-b-2xl">
                    <i class="fa-solid fa-circle-notch fa-spin text-teal-500 text-xl mr-3"></i>
                    <span id="currentGlobalStatusText" class="text-sm font-extrabold text-teal-700 tracking-wide truncate whitespace-nowrap block min-w-0">...</span>
                </div>
            </div>

            <!-- TABS & OUTPUT FRAMEWORK -->
            <div id="tabFramework" class="flex-grow bg-white border border-slate-200 shadow-sm rounded-2xl flex flex-col">
                <!-- Tab Headers -->
                <div class="sticky top-0 z-30 flex justify-between items-center bg-slate-50/95 backdrop-blur-md px-2 py-0 border-b border-slate-200 overflow-x-auto rounded-t-2xl">
                    <div class="flex items-center min-w-max">
                        <button id="tabTerminal" onclick="switchTab('terminal')" class="tab-btn active">
                            <span class="step-num"><span>1</span></span> DEBATE LOG
                        </button>
                        <button id="tabDiscovery" onclick="switchTab('discovery')" class="tab-btn hidden">
                            <i class="fa-solid fa-chevron-right text-slate-300 mr-4 text-[10px] font-normal"></i>
                            <span class="step-num"><span>2</span></span> DISCOVERY (発見)
                            <span id="discoveryReadyBadge" class="hidden absolute top-3 right-3 h-2.5 w-2.5 bg-teal-500 rounded-full animate-ping"></span>
                        </button>
                        <button id="tabWizard" onclick="switchTab('wizard')" class="tab-btn hidden relative">
                            <i class="fa-solid fa-chevron-right text-slate-300 mr-4 text-[10px] font-normal"></i>
                            <span class="step-num"><span>3</span></span> WIZARD (組み立て)
                            <span id="wizardReadyBadge" class="hidden absolute top-3 right-3 h-2.5 w-2.5 bg-teal-500 rounded-full animate-ping"></span>
                        </button>
                        <button id="tabOutput" onclick="switchTab('output')" class="tab-btn hidden">
                            <i class="fa-solid fa-chevron-right text-slate-300 mr-4 text-[10px] font-normal"></i>
                            <span class="step-num"><span>4</span></span> FINAL PROMPT
                        </button>
                    </div>
                    <div class="flex gap-3 ml-4 py-2 pr-3 relative z-10">
                        <button onclick="copyGeneratedPrompt()" class="px-4 py-2 text-xs bg-white text-slate-600 rounded-lg border border-slate-200 hover:border-slate-300 hover:bg-slate-50 transition-colors font-bold font-mono shadow-sm flex items-center whitespace-nowrap">
                            <i class="fa-regular fa-copy mr-2"></i> COPY PROMPT
                        </button>
                    </div>
                </div>
                <!-- Stepper Progress Bar -->
                <div class="relative w-full h-1 bg-slate-100 shrink-0">
                    <div id="tabProgressBar" class="absolute top-0 left-0 h-full bg-teal-500 transition-all duration-500 shadow-[0_0_8px_rgba(20,184,166,0.5)]" style="width: 25%;"></div>
                </div>

                <!-- TAB 1: DEBATE LOG (TUTORIAL) -->
                <div id="terminalArea" class="flex-grow relative overflow-hidden py-4 md:py-6 px-4 bg-slate-50 gradient-bg-light flex flex-col items-center justify-start md:justify-center min-h-[460px]">
                    
                    <!-- Tutorial Content -->
                    <div class="relative z-10 w-full px-4 md:px-10 text-center flex flex-col items-center">
                        <div class="w-12 h-12 md:w-16 md:h-16 rounded-full bg-white border border-teal-200 text-teal-600 flex items-center justify-center shadow-md mb-3 md:mb-4 relative">
                            <div class="absolute inset-0 rounded-full border-4 border-teal-100 animate-ping opacity-50"></div>
                            <i class="fa-solid fa-cube text-xl md:text-2xl animate-pulse"></i>
                        </div>
                        <h3 class="text-teal-600 text-[10px] md:text-xs font-extrabold tracking-[0.2em] mb-1 md:mb-2 drop-shadow-sm">VIRTUAL COMMITTEE ENGINE ONLINE</h3>
                        
                        <div class="text-center max-w-3xl blur-in">
                            <h1 class="text-base sm:text-lg md:text-xl lg:text-2xl font-black text-slate-800 mb-3 md:mb-4 leading-normal tracking-tight break-keep">
                                プロジェクトの成否を決める『前提条件』をセットアップしています...
                            </h1>
                        </div>
                        
                        <div class="delayed-fade-in bg-white/80 border border-slate-200/50 rounded-2xl p-4 md:p-5 lg:p-6 backdrop-blur-md max-w-2xl w-full text-left mx-auto shadow-[0_20px_50px_-12px_rgba(0,0,0,0.05)]">
                            <p class="text-slate-700 font-bold text-sm md:text-base mb-3 leading-relaxed">
                                4人の専門AIが、あなたのアイデアを多角的に検証中です。<br>まもなく、次の2つのインサイトが提示されます。
                            </p>
                            <div class="space-y-2 mb-4 bg-slate-50 rounded-xl p-3 md:p-4 border border-slate-100">
                                <div class="flex items-center gap-2.5 text-slate-800 font-extrabold text-sm md:text-base">
                                    <div class="w-7 h-7 rounded-full bg-teal-100 text-teal-600 flex items-center justify-center shadow-sm shrink-0"><i class="fa-solid fa-check text-xs"></i></div> 
                                    開発前に絶対に固めるべき【必須要件】
                                </div>
                                <div class="flex items-center gap-2.5 text-slate-800 font-extrabold text-sm md:text-base">
                                    <div class="w-7 h-7 rounded-full bg-amber-100 text-amber-600 flex items-center justify-center shadow-sm shrink-0"><i class="fa-solid fa-lightbulb text-xs"></i></div> 
                                    プロだけが知っている【見落としがちなポイント】
                                </div>
                            </div>
                            <p class="text-slate-600 font-bold text-xs md:text-sm leading-relaxed">
                                抽出された要件の「担当AIのスタンプ」に注目し、<br>アイデアを完璧な状態で起動（PRE-PUT）する準備を整えましょう。
                            </p>
                        </div>
                    </div>

                    <!-- Error Recovery Card (Hidden by Default) -->
                    <div id="debateErrorCard" class="hidden relative z-20 bg-white/95 border-2 border-red-200 rounded-3xl p-6 md:p-8 max-w-xl w-full text-center shadow-2xl backdrop-blur-md fade-in my-auto">
                        <div class="w-14 h-14 bg-red-50 text-red-500 rounded-full flex items-center justify-center mx-auto mb-4 shadow-sm">
                            <i class="fa-solid fa-circle-exclamation text-2xl"></i>
                        </div>
                        <h3 class="text-xl font-bold text-slate-800 mb-2">分析エンジンでエラーが発生しました</h3>
                        <p id="debateErrorMessage" class="text-sm text-slate-500 mb-6 leading-relaxed whitespace-pre-wrap">APIキーのエラーまたはアクセス制限が発生しました。</p>
                        
                        <div class="flex flex-col gap-3">
                            <button onclick="retryLiveAnalysis()" class="w-full py-3.5 bg-teal-600 hover:bg-teal-700 text-white rounded-xl text-sm font-bold shadow-md transition-all">
                                <i class="fa-solid fa-rotate-left mr-2"></i> APIキーで再試行する
                            </button>
                            <button onclick="switchToSimulatedModeAndProceed()" class="w-full py-3.5 bg-slate-800 hover:bg-slate-900 text-white rounded-xl text-sm font-bold shadow-md transition-all">
                                <i class="fa-solid fa-wand-magic-sparkles mr-2"></i> デモモード（擬似演出）に切り替えて進む
                            </button>
                            <button onclick="createNewProject()" class="w-full py-3.5 bg-white border border-slate-200 text-slate-500 hover:bg-slate-50 rounded-xl text-sm font-bold transition-all">
                                新規入力画面に戻る
                            </button>
                        </div>
                    </div>

                    <!-- Floating Terminal Widget -->
                    <div id="logWidget" class="absolute bottom-8 right-8 w-[500px] bg-slate-900/90 border border-slate-700 rounded-xl shadow-2xl overflow-hidden transition-all duration-300 translate-y-[120%] backdrop-blur-md z-50">
                        <div class="flex items-center justify-between px-4 py-3 bg-slate-800/80 border-b border-slate-700 cursor-pointer" onclick="toggleLogWidget()">
                            <div class="flex items-center gap-2">
                                <i class="fa-solid fa-terminal text-slate-400 text-sm"></i>
                                <span class="text-xs font-bold text-slate-300">SYSTEM.LOG</span>
                            </div>
                            <button class="text-slate-400 hover:text-white"><i class="fa-solid fa-chevron-down"></i></button>
                        </div>
                        <div id="consoleLog" class="h-48 overflow-y-auto p-4 code-font text-xs leading-relaxed text-slate-300"></div>
                    </div>

                    <!-- Open Log Button -->
                    <button onclick="toggleLogWidget()" class="absolute bottom-8 right-8 px-6 py-3 bg-white hover:bg-slate-50 border border-slate-200 rounded-full text-slate-600 hover:text-teal-600 text-sm font-extrabold transition-all flex items-center gap-3 shadow-lg z-40">
                        <i class="fa-solid fa-terminal"></i> 処理ログを表示
                    </button>
                </div>

                <!-- TAB 2: DISCOVERY REPORT -->
                <div id="discoveryArea" class="hidden flex-grow p-8 overflow-visible bg-slate-50 text-slate-700 relative">
                    <div class="max-w-4xl mx-auto w-full fade-in pb-10">
                        <div class="text-center mb-10">
                            <h3 class="text-3xl font-extrabold text-slate-900 mb-3">解くべき前提条件とプロの盲点</h3>
                            <p class="text-base text-slate-600 font-medium">エージェントが議論の末に洗い出した、プロジェクト開始前に確定させるべき項目です。</p>
                        </div>

                        <!-- Extracted Variables -->
                        <div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-md mb-8">
                            <h4 class="text-xl font-bold text-teal-700 mb-6 flex items-center border-b border-slate-100 pb-4"><i class="fa-solid fa-cube mr-3"></i> 1階部分：必須基礎確定要件</h4>
                            <div id="discoveryVariablesList" class="grid grid-cols-1 md:grid-cols-2 gap-4">
                                <!-- Discovery items injected here -->
                            </div>
                        </div>

                        <!-- Extracted Traps -->
                        <div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-md mb-10">
                            <h4 class="text-xl font-bold text-rose-700 mb-6 flex items-center border-b border-slate-100 pb-4"><i class="fa-solid fa-lightbulb mr-3"></i> 2階部分：プロの視点（見落としがちな重要ポイント）</h4>
                            <div id="discoveryTrapsList" class="space-y-4">
                                <!-- Trap items injected here -->
                            </div>
                        </div>

                        <!-- Action Buttons -->
                        <div class="flex flex-col sm:flex-row justify-center items-center gap-6 border-t border-slate-200 pt-10">
                            <button onclick="openSaveModal()" class="px-8 py-4 bg-white border-2 border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-600 rounded-xl text-base font-bold transition-all w-full sm:w-auto">
                                <i class="fa-solid fa-floppy-disk mr-2"></i> セーブして終了する
                            </button>
                            <button onclick="startWizardBuilder()" class="px-8 py-4 bg-teal-600 hover:bg-teal-700 text-white rounded-xl text-base font-extrabold shadow-lg shadow-teal-500/30 transition-all transform hover:-translate-y-1 w-full sm:w-auto">
                                <i class="fa-solid fa-wand-magic-sparkles mr-2"></i> プロンプト組み立て（ウィザード）に進む
                            </button>
                        </div>
                    </div>
                </div>

                <!-- TAB 3: DYNAMIC WIZARD (Form) -->
                <div id="wizardArea" class="hidden flex-grow p-8 overflow-visible bg-white text-slate-700 relative">
                    
                    <!-- Loading State for Builder -->
                    <div id="wizardLoadingState" class="hidden w-full min-h-[400px] bg-white flex-col items-center justify-center fade-in">
                        <i class="fa-solid fa-wand-magic-sparkles text-5xl text-rose-500 mb-6 animate-pulse"></i>
                        <h3 class="text-xl font-bold text-slate-800 mb-2">Form Builder AI 起動中...</h3>
                        <p class="text-sm text-slate-500">あなたのプロジェクト専用の「具体的な選択肢」を生成しています。</p>
                    </div>

                    <!-- WIZARD UI -->
                    <div id="wizardContainer" class="hidden max-w-3xl mx-auto w-full fade-in pb-10">
                        <div class="flex justify-between items-center mb-8">
                            <button id="btnWizardBack" onclick="wizardBack()" class="px-4 py-2 text-sm font-bold text-slate-500 hover:text-teal-600 hover:bg-teal-50 rounded-lg transition-all hidden"><i class="fa-solid fa-arrow-left mr-2"></i>前の質問へ</button>
                            <span id="wizardProgress" class="text-sm font-bold text-teal-600 bg-teal-50 px-4 py-2 rounded-full border border-teal-100 ml-auto">Step 1 / 5</span>
                        </div>

                        <div class="bg-white p-10 rounded-3xl border border-slate-200 shadow-xl mb-8">
                            <h3 id="wizardQuestionLabel" class="text-2xl font-extrabold text-slate-900 mb-3 leading-tight">質問</h3>
                            <p id="wizardQuestionDesc" class="text-base text-slate-500 mb-10 font-medium">詳細</p>
                            
                            <!-- Detected Initial Hope Alert -->
                            <div id="wizardInitialHopeAlert" class="hidden mb-8"></div>

                            <div id="wizardOptions" class="grid grid-cols-1 gap-4 mb-8">
                                <!-- Options dynamically injected -->
                            </div>

                            <div class="border-t border-slate-100 pt-8">
                                <label class="block text-sm text-slate-600 font-bold mb-3">自由に入力する（オリジナル案）</label>
                                <div class="flex gap-3">
                                    <input type="text" id="wizardCustomInput" class="flex-grow px-5 py-4 bg-slate-50 border border-slate-200 rounded-xl focus:border-teal-500 focus:ring-2 focus:ring-teal-500/20 text-base font-medium text-slate-800" placeholder="自由に入力...">
                                    <button onclick="wizardNextWithCustom()" class="px-8 py-4 bg-slate-800 hover:bg-slate-900 text-white rounded-xl text-base font-bold shadow-md whitespace-nowrap transition-all">決定</button>
                                </div>
                                
                                <div class="mt-8 flex flex-col items-center">
                                    <button onclick="wizardNextWithUnknown()" class="px-8 py-3.5 border-2 border-slate-200 text-slate-500 hover:text-slate-800 hover:border-slate-300 hover:bg-slate-50 rounded-full text-sm font-bold transition-all"><i class="fa-regular fa-circle-question mr-2"></i>今は未定にする（後でAIに相談する）</button>
                                    <p class="mt-3 text-[11px] text-slate-400 font-medium tracking-wide">※未定にした項目は最後のページでリストアップされ、後でAIからの提案を見ながら決めることができます。</p>
                                </div>
                            </div>
                        </div>
                    </div>

                    <!-- DEEP VARS REVIEW UI -->
                    <div id="deepVarsContainerUI" class="hidden max-w-4xl mx-auto w-full fade-in pb-10">
                        <div class="text-center mb-8">
                            <span class="inline-block px-3 py-1 bg-teal-100 text-teal-800 rounded-full text-xs font-bold mb-3">FINAL STEP</span>
                            <h3 class="text-2xl font-extrabold text-slate-900 mb-2">プロの視点（見落としポイント）の適用</h3>
                            <p class="text-base text-slate-600 font-bold">抽出された重要ポイントや対策をプロンプトに組み込みます。<br>必要なものにチェックを入れてください。</p>
                        </div>
                        <div class="bg-white p-8 rounded-3xl border border-slate-200 shadow-lg">
                            <!-- 初心者向けのアドバイスカード -->
                            <div class="mb-6 p-5 bg-amber-50/70 border border-amber-200/60 rounded-2xl flex items-start gap-3.5 text-left">
                                <div class="w-9 h-9 rounded-xl bg-amber-100/80 text-amber-600 flex items-center justify-center shrink-0 mt-0.5 shadow-sm">
                                    <i class="fa-solid fa-lightbulb text-base"></i>
                                </div>
                                <div class="flex flex-col gap-1.5">
                                    <span class="text-sm font-black text-amber-900 tracking-wide flex items-center gap-1.5">
                                        💡 初心者・初めて制作される方へのアドバイス
                                    </span>
                                    <p class="text-xs sm:text-sm text-amber-800 leading-relaxed font-bold">
                                        初期状態では安全のため、すべてのチェックを<strong>【オフ】</strong>にしています。最初の一歩目から難しい内容をAIに多く指示しすぎると、<strong>AIの注意が分散してしまい、的外れな回答になるリスク</strong>があります。<br>
                                        まずは、最も重要だと思う<strong>【1〜2点】のみに厳選してチェックを入れて</strong>プロンプトを生成し、残りのポイントはプロジェクトが進んだ段階で徐々に組み込んでいくことを強くおすすめします！
                                    </p>
                                </div>
                            </div>

                            <div class="space-y-4" id="deepVariablesList">
                                <!-- Checkboxes -->
                            </div>
                            <div class="mt-10 flex justify-center border-t border-slate-100 pt-8">
                                <button onclick="finishWizard()" class="px-10 py-5 bg-teal-600 hover:bg-teal-700 text-white rounded-2xl text-lg font-extrabold shadow-xl shadow-teal-500/20 transition-all transform hover:-translate-y-1">
                                    <i class="fa-solid fa-wand-magic-sparkles mr-2"></i> 最終プロンプトを生成する
                                </button>
                            </div>
                        </div>
                    </div>

                </div>

                <!-- TAB 4: COMPILED FINAL PROMPT -->
                <div id="outputArea" class="hidden flex-grow p-6 md:p-8 overflow-y-auto bg-slate-50 text-slate-800 rounded-b-2xl flex flex-col gap-6">
                    
                    <!-- Style Selector Panel (Glassmorphism) -->
                    <div class="bg-white border border-slate-200 p-6 rounded-2xl shadow-sm flex flex-col gap-5">
                        <div class="flex flex-col md:flex-row md:items-center justify-between gap-3">
                            <div class="flex items-center gap-2.5">
                                <div class="h-8 w-8 rounded-lg bg-teal-50 text-teal-600 flex items-center justify-center border border-teal-100">
                                    <i class="fa-solid fa-sliders text-sm"></i>
                                </div>
                                <div class="flex flex-col">
                                    <span class="text-xs text-slate-500 font-bold uppercase tracking-wider">Prompt Tuning</span>
                                    <span class="text-sm font-extrabold text-slate-800">生成プロンプトの共創スタイルを選択</span>
                                </div>
                            </div>
                            <span class="text-[10px] bg-slate-100 text-slate-500 px-3 py-1 rounded-full font-bold self-start md:self-auto border border-slate-200 font-mono">Real-time Compiler Active</span>
                        </div>

                        <!-- Buttons grid -->
                        <div class="grid grid-cols-2 lg:grid-cols-4 gap-3">
                            <button onclick="setPromptStyle('pm')" id="btn-style-pm" class="relative pt-8 p-4 rounded-xl border text-left transition-all duration-200 flex flex-col gap-1.5 cursor-pointer bg-white">
                                <!-- おすすめ案内バッジ -->
                                <span class="absolute top-2 left-2.5 px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-wider bg-indigo-100 text-indigo-700 border border-indigo-200/50 shadow-sm">👑 初心者・迷ったらこれ！</span>
                                <div class="flex items-center gap-2 font-bold text-xs">
                                    <i class="fa-solid fa-chess-knight"></i>
                                    <span>👔 PM・段取り型</span>
                                    <!-- ❓ ツールチップ -->
                                    <div class="tooltip-container ml-1">
                                        <i class="fa-regular fa-circle-question text-slate-400 hover:text-slate-600 cursor-help"></i>
                                        <div class="tooltip-box">
                                            <div class="font-bold text-teal-400 mb-1">👔 PM・段取り型 (PM Style)</div>
                                            <div class="text-[10px] text-slate-400 mb-2">プロジェクト進行の骨組み作りに適しています。</div>
                                            <div class="border-t border-slate-700/60 pt-1.5 text-[10px] text-slate-300">
                                                <strong>🎯 合う内容の一覧:</strong><br>
                                                ・LINEスタンプ制作スケジュール設計<br>
                                                ・開発スケジュール、優先順位ToDo整理<br>
                                                ・マイルストーンや具体的アクションプラン
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <span class="text-xs font-bold leading-normal text-slate-500">工程設計・ToDo整理</span>
                            </button>
                            <button onclick="setPromptStyle('creator')" id="btn-style-creator" class="relative pt-8 p-4 rounded-xl border text-left transition-all duration-200 flex flex-col gap-1.5 cursor-pointer bg-white">
                                <!-- おすすめ案内バッジ -->
                                <span class="absolute top-2 left-2.5 px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-wider bg-purple-100 text-purple-700 border border-purple-200/50 shadow-sm">💡 とりあえず形にしたい人向け！</span>
                                <div class="flex items-center gap-2 font-bold text-xs">
                                    <i class="fa-solid fa-pen-nib"></i>
                                    <span>🎨 クリエイター型</span>
                                    <!-- ❓ ツールチップ -->
                                    <div class="tooltip-container ml-1">
                                        <i class="fa-regular fa-circle-question text-slate-400 hover:text-slate-600 cursor-help"></i>
                                        <div class="tooltip-box">
                                            <div class="font-bold text-teal-400 mb-1">🎨 クリエイター型 (Creator Style)</div>
                                            <div class="text-[10px] text-slate-400 mb-2">ブレストや具体的なアイデアの創出に適しています。</div>
                                            <div class="border-t border-slate-700/60 pt-1.5 text-[10px] text-slate-300">
                                                <strong>🎯 合う内容の一覧:</strong><br>
                                                ・キャラクター名やスタンプのセリフ案<br>
                                                ・デザイン構成、イラスト作画案のブレスト<br>
                                                ・キャッチコピーや文章（下書き）の作成
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <span class="text-xs font-bold leading-normal text-slate-500">アイデア・ドラフト作成</span>
                            </button>
                            <button onclick="setPromptStyle('auditor')" id="btn-style-auditor" class="relative pt-8 p-4 rounded-xl border text-left transition-all duration-200 flex flex-col gap-1.5 cursor-pointer bg-white">
                                <!-- おすすめ案内バッジ -->
                                <span class="absolute top-2 left-2.5 px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-wider bg-emerald-100 text-emerald-700 border border-emerald-200/50 shadow-sm">⚠️ 仕上げ・リスク予防用！</span>
                                <div class="flex items-center gap-2 font-bold text-xs">
                                    <i class="fa-solid fa-shield-halved"></i>
                                    <span>🔍 監査・アドバイザー型</span>
                                    <!-- ❓ ツールチップ -->
                                    <div class="tooltip-container ml-1">
                                        <i class="fa-regular fa-circle-question text-slate-400 hover:text-slate-600 cursor-help"></i>
                                        <div class="tooltip-box">
                                            <div class="font-bold text-teal-400 mb-1">🔍 監査・アドバイザー型 (Auditor Style)</div>
                                            <div class="text-[10px] text-slate-400 mb-2">公開前の最終チェックやリスク予防に適しています。</div>
                                            <div class="border-t border-slate-700/60 pt-1.5 text-[10px] text-slate-300">
                                                <strong>🎯 合う内容の一覧:</strong><br>
                                                ・LINE公式審査規約や著作権侵害の確認<br>
                                                ・AI商用利用規約やセキュリティ対策<br>
                                                ・初心者が自滅する「罠・盲点」の予防監査
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <span class="text-xs font-bold leading-normal text-slate-500">リスク・品質の予防監査</span>
                            </button>
                            <button onclick="setPromptStyle('custom')" id="btn-style-custom" class="relative pt-8 p-4 rounded-xl border text-left transition-all duration-200 flex flex-col gap-1.5 cursor-pointer bg-white">
                                <!-- おすすめ案内バッジ -->
                                <span class="absolute top-2 left-2.5 px-2 py-0.5 rounded text-[8px] font-black uppercase tracking-wider bg-amber-100 text-amber-800 border border-amber-200/50 shadow-sm">🔧 完全オリジナル・上級者向け</span>
                                <div class="flex items-center gap-2 font-bold text-xs">
                                    <i class="fa-solid fa-keyboard text-amber-500"></i>
                                    <span>✍️ 自由カスタマイズ型</span>
                                    <!-- ❓ ツールチップ -->
                                    <div class="tooltip-container ml-1">
                                        <i class="fa-regular fa-circle-question text-slate-400 hover:text-slate-600 cursor-help"></i>
                                        <div class="tooltip-box">
                                            <div class="font-bold text-amber-400 mb-1">✍️ 自由カスタマイズ型 (Custom Style)</div>
                                            <div class="text-[10px] text-slate-400 mb-2">自分独自の要件や指示の追加に適しています。</div>
                                            <div class="border-t border-slate-700/60 pt-1.5 text-[10px] text-slate-300">
                                                <strong>🎯 合う内容の一覧:</strong><br>
                                                ・「回答は必ず表形式で行う」などの指定<br>
                                                ・特定のトーン・口調やフォーマット of the view の指定<br>
                                                ・自分だけのこだわり条件を流し込む
                                            </div>
                                        </div>
                                    </div>
                                </div>
                                <span class="text-xs font-bold leading-normal text-slate-500">独自の追加指示を付与</span>
                            </button>
                        </div>

                        <!-- Dynamic Explanation and Recommended Tasks Card (Glassmorphic) -->
                        <div id="styleGuidePanel" class="p-5 bg-slate-50 border border-slate-200 rounded-xl flex flex-col gap-3 font-sans transition-all duration-300">
                            <!-- Injected dynamically -->
                        </div>

                        <!-- Collapsible Custom Instructions Text Area -->
                        <div id="customInstructionsWrapper" class="hidden flex-col gap-3 mt-3">
                            <!-- テンプレート保存・選択ヘッダー -->
                            <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 bg-slate-50 p-3.5 rounded-xl border border-slate-200/80 shadow-sm">
                                <div class="flex items-center gap-2">
                                    <i class="fa-solid fa-floppy-disk text-teal-600 text-sm"></i>
                                    <span class="text-xs font-black text-slate-700">マイテンプレート</span>
                                </div>
                                <div class="flex items-center gap-2">
                                    <select id="customTemplateSelect" onchange="loadCustomTemplate(this.value)" class="px-2.5 py-1.5 bg-white border border-slate-200 rounded-lg text-[11px] font-bold text-slate-600 focus:outline-none focus:ring-1 focus:ring-teal-500 cursor-pointer max-w-[150px] truncate shadow-sm">
                                        <option value="">-- 保存データを選択 --</option>
                                    </select>
                                    <button onclick="saveCustomTemplate()" class="px-3 py-1.5 bg-teal-600 hover:bg-teal-700 text-white rounded-lg text-[11px] font-extrabold shadow-sm transition-all flex items-center gap-1 shrink-0">
                                        <i class="fa-solid fa-plus text-[9px]"></i> 保存
                                    </button>
                                </div>
                            </div>

                            <!-- ワンタップ追加指示チップ -->
                            <div class="flex flex-wrap gap-1.5">
                                <button onclick="insertCustomPresetText('回答は必ず【マークダウンの表形式（Table）】を用いて整理してください。')" class="px-2.5 py-1 bg-white border border-slate-200 hover:border-teal-400 hover:bg-teal-50 text-slate-600 hover:text-teal-700 rounded-full text-[10px] font-bold transition-all shadow-sm">
                                    📊 表形式で整理
                                </button>
                                <button onclick="insertCustomPresetText('小学生でも直感的に理解できるように、専門用語を一切使わず、身近な例え話を用いて説明してください。')" class="px-2.5 py-1 bg-white border border-slate-200 hover:border-teal-400 hover:bg-teal-50 text-slate-600 hover:text-teal-700 rounded-full text-[10px] font-bold transition-all shadow-sm">
                                    🏫 小学生向け解説
                                </button>
                                <button onclick="insertCustomPresetText('重要な専門用語や指示には、必ず【英語の対訳（英単語）】を括弧書きで併記してください。')" class="px-2.5 py-1 bg-white border border-slate-200 hover:border-teal-400 hover:bg-teal-50 text-slate-600 hover:text-teal-700 rounded-full text-[10px] font-bold transition-all shadow-sm">
                                    🇬🇧 英語併記
                                </button>
                                <button onclick="insertCustomPresetText('要点を3つの重要な箇条書きに絞り込み、それぞれに対して具体的なアクションToDoを1行ずつ明記してください。')" class="px-2.5 py-1 bg-white border border-slate-200 hover:border-teal-400 hover:bg-teal-50 text-slate-600 hover:text-teal-700 rounded-full text-[10px] font-bold transition-all shadow-sm">
                                    📝 3点箇条書き＆ToDo
                                </button>
                            </div>

                            <div class="flex items-center justify-between mt-1">
                                <label class="block text-[11px] font-bold text-slate-600 uppercase tracking-wider flex items-center gap-1">
                                    <span>✍️ 独自の追加指示（自由記入）</span>
                                </label>
                                <span class="text-[10px] text-teal-600 bg-teal-50 px-2 py-0.5 rounded font-bold">リアルタイム同期中</span>
                            </div>
                            <textarea id="customInstructionsInput" oninput="updateCustomInstructions(this.value)" rows="3" 
                                      class="w-full px-4 py-3 bg-slate-50 border border-slate-200 rounded-xl text-xs text-slate-700 focus:outline-none focus:border-teal-500 focus:ring-1 focus:ring-teal-500/20 transition-all font-mono resize-none leading-relaxed placeholder-slate-400"
                                      placeholder="（例）回答は必ず表形式で出力してください。/ プロ向けの専門用語を多めに使用してください。/ 小学生向けにわかりやすく解説してください。"></textarea>
                            <p class="text-[10px] text-slate-400 font-medium pl-1 leading-relaxed">※入力した追加指示は、最終プロンプトの末尾にリアルタイムでマージされます。</p>
                        </div>
                    </div>

                    <!-- Glowing Final Prompt Display Card -->
                    <div class="relative group bg-white border border-slate-200 rounded-2xl flex flex-col overflow-hidden shadow-2xl">
                        <!-- Glow effect -->
                        <div class="absolute -inset-[1px] bg-gradient-to-r from-teal-500/10 to-blue-500/10 rounded-2xl blur opacity-20 group-hover:opacity-40 transition duration-500 pointer-events-none"></div>
                        
                        <div class="relative flex items-center justify-between px-5 py-3.5 bg-slate-50 border-b border-slate-200 rounded-t-2xl z-10 shrink-0">
                            <span class="text-xs font-bold text-slate-500 tracking-wider flex items-center gap-2">
                                <i class="fa-solid fa-code text-teal-600 text-sm"></i>
                                <span>COMPILED_PROMPT.MD <span class="text-[10px] text-teal-600 bg-teal-50 border border-teal-200/80 px-2 py-0.5 rounded-md font-bold ml-2 shadow-sm">✏️ 直接編集・調整OK</span></span>
                            </span>
                            <div class="flex items-center gap-2">
                                <button onclick="saveCurrentProject()" class="px-4.5 py-2 text-xs bg-white border border-slate-200 hover:border-slate-300 hover:bg-slate-50 text-slate-700 rounded-lg transition-all font-extrabold flex items-center gap-1.5 shadow-sm">
                                    <i class="fa-regular fa-floppy-disk text-slate-500"></i> プロジェクトを保存
                                </button>
                                <button onclick="copyGeneratedPrompt()" class="px-4.5 py-2 text-xs bg-teal-600 hover:bg-teal-700 text-white rounded-lg transition-all font-extrabold flex items-center gap-1.5 shadow-md shadow-teal-500/10">
                                    <i class="fa-regular fa-copy text-sm"></i> コピーする
                                </button>
                            </div>
                        </div>

                        <div class="relative z-10 p-5 bg-white flex-grow rounded-b-2xl min-h-[450px] flex flex-col gap-4">
                            <!-- Undecided Memo Area -->
                            <div id="undecidedMemoArea" class="hidden bg-amber-50 border border-amber-200 rounded-xl p-4 shadow-sm shrink-0">
                                <h4 class="text-sm font-bold text-amber-800 flex items-center gap-2 mb-2"><i class="fa-solid fa-list-check"></i> 後で決めるToDoメモ（未定項目）</h4>
                                <p class="text-[11px] text-amber-700/80 mb-3 font-medium">※これらはAIには伝えず、後で決めるための備忘録としてここに表示しています。</p>
                                <ul id="undecidedList" class="text-sm text-amber-900 space-y-1.5 pl-2 font-bold tracking-wide">
                                </ul>
                            </div>
                            
                            <textarea id="finalPromptResult" class="w-full flex-grow bg-transparent border-none text-slate-700 focus:outline-none resize-y leading-relaxed font-mono text-base whitespace-pre-wrap selection:bg-teal-500/20" placeholder="ここに極上の指示プロンプトが編纂されます。直接自由に編集も可能です。">ここに極上の指示プロンプトが編纂されます。</textarea>
                        </div>
                    </div>
                </div>

                <!-- Bottom Progress Bar -->
                <div class="h-1.5 bg-slate-100 relative mt-auto overflow-hidden">
                    <div id="progressBar" class="h-full bg-teal-500 w-0 transition-all duration-500 ease-out shadow-[0_0_10px_rgba(20,184,166,0.8)] relative">
                        <div class="absolute top-0 right-0 bottom-0 w-20 bg-gradient-to-r from-transparent to-white/50 animate-pulse"></div>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- TOAST CONTAINERS -->
    <div id="toastContainer" class="fixed bottom-8 right-8 z-50 flex flex-col gap-3 max-w-sm w-full pointer-events-none"></div>

    <!-- FLOATING HELP WIDGET -->
    <div class="fixed bottom-24 right-8 z-40 flex flex-col items-end gap-4 pointer-events-none">
        <div id="helpPopover" class="pointer-events-auto w-[320px] bg-white/95 backdrop-blur-md border border-slate-200 rounded-2xl p-5 shadow-2xl transition-all duration-300 translate-y-4 opacity-0 pointer-events-none hidden">
            <div class="flex justify-between items-start mb-3 border-b border-slate-100 pb-3">
                <h3 class="font-bold text-slate-800 flex items-center gap-2 text-sm">
                    <i class="fa-solid fa-circle-info text-teal-500"></i> コンテキスト・ヘルプ
                </h3>
                <button onclick="toggleHelp()" class="text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
            </div>
            <p id="helpDescription" class="text-xs text-slate-600 leading-relaxed font-medium mb-3">
                現在「プロジェクト構成」フェーズです。
            </p>
            <div class="bg-teal-50/50 p-3 rounded-xl border border-teal-100">
                <h4 class="text-[10px] font-bold text-teal-800 mb-2 flex items-center"><i class="fa-regular fa-lightbulb text-amber-500 mr-1.5"></i> ワンポイント</h4>
                <ul id="helpTipsList" class="text-[10px] text-slate-600 space-y-1.5 list-disc list-inside font-medium leading-relaxed">
                    <li>ヒントをここに表示します。</li>
                </ul>
            </div>
        </div>
        
        <button onclick="toggleHelp()" class="pointer-events-auto w-12 h-12 bg-white border border-slate-200 text-slate-600 hover:text-teal-600 hover:border-teal-300 rounded-full shadow-lg flex items-center justify-center transition-all hover:scale-105">
            <i class="fa-solid fa-question text-lg"></i>
        </button>
    </div>

    <!-- SAVE CONFIRM MODAL -->
    <div id="saveConfirmModal" class="hidden absolute inset-0 bg-slate-900/60 backdrop-blur-sm z-[100] flex items-center justify-center p-4">
        <div class="bg-white rounded-3xl shadow-2xl max-w-md w-full p-8 border border-slate-200 transform scale-95 opacity-0 transition-all duration-200" id="saveConfirmContent">
            <div class="w-16 h-16 bg-teal-50 text-teal-600 rounded-full flex items-center justify-center mb-6 shadow-sm mx-auto">
                <i class="fa-regular fa-floppy-disk text-3xl"></i>
            </div>
            <h3 class="text-2xl font-extrabold text-slate-900 text-center mb-2">分析結果をセーブしますか？</h3>
            
            <div class="bg-slate-50 rounded-xl p-5 mb-6 mt-6 border border-slate-100">
                <h4 class="text-sm font-bold text-slate-700 mb-3 flex items-center"><i class="fa-solid fa-star text-amber-400 mr-2"></i> セーブするメリット</h4>
                <ul class="text-sm text-slate-600 space-y-3 font-medium">
                    <li class="flex items-start"><i class="fa-solid fa-check text-teal-500 mt-0.5 mr-2"></i> 抽出された重要ポイントや条件を後からいつでも見直せます。</li>
                    <li class="flex items-start"><i class="fa-solid fa-check text-teal-500 mt-0.5 mr-2"></i> 次回、最初からやり直すことなく「ウィザード（組み立て）」から再開できます。</li>
                    <li class="flex items-start"><i class="fa-solid fa-check text-teal-500 mt-0.5 mr-2"></i> 別のプロジェクトを考える際の比較や参考データになります。</li>
                </ul>
            </div>
            
            <div class="flex flex-col gap-3">
                <button onclick="confirmSaveAndFinish()" class="w-full py-3.5 bg-teal-600 hover:bg-teal-700 text-white rounded-xl text-sm font-extrabold shadow-md transition-all transform hover:-translate-y-0.5">セーブして新規画面に戻る</button>
                <button onclick="closeSaveModal()" class="w-full py-3.5 bg-white border border-slate-200 text-slate-500 hover:bg-slate-50 hover:text-slate-700 rounded-xl text-sm font-bold transition-all">キャンセル</button>
            </div>
        </div>
    </div>

    <script>
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
                    statText.className = "text-[10px] text-emerald-600 font-mono font-bold flex items-center gap-1";
                    
                    // Add a tiny check icon to indicate complete
                    if (!statText.innerHTML.includes('fa-circle-check')) {
                        statText.innerHTML = '<i class="fa-solid fa-circle-check text-[10px]"></i> COMPLETE';
                    }
                    
                    if (avatar) {
                        avatar.className = avatar.className.replace(/bg-\w+-100/g, 'bg-emerald-100').replace(/text-\w+-600/g, 'text-emerald-600');
                    }
                } else if (state === 'working') {
                    el.className = `flex items-center gap-3 px-4 py-2 rounded-xl bg-white border-2 border-${agentBaseColors[i]}-400 text-sm shadow-md transition-all duration-300`;
                    statText.innerText = "WORKING...";
                    statText.className = `text-[10px] ${agentTextColors[i]} font-mono font-bold animate-pulse`;
                    
                    if (avatar) {
                        avatar.classList.add('animate-pulse');
                    }
                } else if (state === 'active') {
                    el.className = `flex items-center gap-3 px-4 py-2 rounded-xl bg-white border-2 border-${agentBaseColors[i]}-400 text-sm shadow-md transition-all duration-300`;
                    statText.innerText = "ACTIVE";
                    statText.className = `text-[10px] ${agentTextColors[i]} font-mono font-bold flex items-center gap-1`;
                    statText.innerHTML = `<span class="h-1.5 w-1.5 rounded-full ${agentBgColors[i]} animate-ping"></span> ACTIVE`;
                    
                    if (avatar) {
                        avatar.classList.add('animate-pulse');
                    }
                } else if (state === 'idle') {
                    // Completed analysis - show original colors for reference
                    el.className = `flex items-center gap-3 px-4 py-2 rounded-xl bg-white border border-${agentBaseColors[i]}-100 text-sm transition-all duration-300`;
                    statText.className = `text-[10px] ${agentTextColors[i]} font-mono font-bold flex items-center gap-1`;
                    statText.innerHTML = `<i class="fa-solid fa-circle-check text-[8px] text-emerald-400 mr-0.5"></i> ${agentNames[i]}`;
                    
                    if (avatar) {
                        avatar.className = avatar.className.replace(/bg-\w+-100/g, `bg-${agentBaseColors[i]}-100`).replace(/text-\w+-600/g, `text-${agentBaseColors[i]}-600`);
                    }
                } else {
                    // Standby
                    el.className = "flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50/50 border border-slate-100 text-sm transition-all duration-300 opacity-60";
                    statText.innerText = "STANDBY";
                    statText.className = "text-[10px] text-slate-400 font-mono font-bold";
                    
                    // Restore original agent colors for the standby avatar
                    if (avatar) {
                        avatar.className = avatar.className.replace(/bg-\w+-100/g, `bg-${agentBaseColors[i]}-100`).replace(/text-\w+-600/g, `text-${agentBaseColors[i]}-600`);
                    }
                    
                    // If this is Agent 6 (Wizard) during Discovery Report, let's make it look ready with a subtle rose pulse to prompt user
                    if (phase === 2.5 && i === 6) {
                        el.className = "flex items-center gap-3 px-4 py-2 rounded-xl bg-slate-50 border border-rose-100 text-sm transition-all duration-300";
                        statText.innerText = "READY";
                        statText.className = "text-[10px] text-rose-500 font-mono font-bold flex items-center gap-1";
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
                if (type === 'system' || logText.includes('完了') || logText.includes('出力しました')) {
                    globalStatusContainer.classList.add('hidden');
                    globalStatusContainer.classList.remove('flex');
                } else {
                    globalStatusContainer.classList.remove('hidden');
                    globalStatusContainer.classList.add('flex');
                    let cleanLog = logText.length > 30 ? logText.substring(0, 30) + "..." : logText;
                    globalStatusText.innerText = cleanLog;
                    
                    const spinnerIcon = globalStatusContainer.querySelector('i');
                    const statusColorMap = { strategy: 'indigo', technical: 'cyan', design: 'purple', business: 'amber', marketing: 'amber', compiler: 'emerald', builder: 'rose' };
                    const sc = statusColorMap[type] || 'teal';
                    spinnerIcon.className = `fa-solid fa-circle-notch fa-spin text-xl mr-3 shrink-0 text-${sc}-500`;
                    globalStatusText.className = `text-xs md:text-sm font-extrabold tracking-wide truncate whitespace-nowrap block min-w-0 text-${sc}-600`;
                }
            }
        }

        let currentApiKeyIndex = 0;

        async function callGeminiAgent(apiKeyString, systemPrompt, userPrompt, isJson = false, retries = 2, model = 'gemini-2.5-flash') {
            const keys = apiKeyString.split(',').map(k => k.trim()).filter(k => k);
            if (keys.length === 0) throw new Error("APIキーが入力されていません。");

            let lastError = null;
            const maxAttempts = Math.max(retries + 1, keys.length * 2);

            const payload = { contents: [{ parts: [{ text: `${systemPrompt}\n\n【ユーザー入力】\n${userPrompt}` }] }] };
            if (isJson) payload.generationConfig = { responseMimeType: "application/json" };
            
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
                    
                    if (res.status === 429) {
                        lastError = new Error(`[ERROR-429] APIの無料枠制限に達しました。1分ほど待ってから再試行してください。`);
                        if (keys.length > 1) {
                            writeToConsole('SYSTEM', `API制限(429)を検知。予備キーへローテーションします...`, 'system');
                        }
                        await new Promise(r => setTimeout(r, 2000));
                        continue;
                    }
                    
                    if (res.status >= 500 && i < maxAttempts - 1) {
                        writeToConsole('SYSTEM', `APIエラー(${res.status})を検知。待機して再試行します...`, 'system');
                        await new Promise(r => setTimeout(r, 3000));
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
                    <span class="px-2.5 py-0.5 rounded text-[10px] ${info.bgColor}">${info.title}</span>
                </div>
                <p class="text-xs text-slate-600 leading-relaxed font-semibold">
                    ${info.desc}
                </p>
                <div class="text-[11px] text-teal-700 bg-teal-50 border border-teal-100 p-3 rounded-lg font-medium">
                    ${info.stage}
                </div>
                <div class="mt-3 border-t border-slate-200 pt-3 flex flex-col gap-2">
                    <span class="text-[10px] text-slate-400 font-bold tracking-wider uppercase flex items-center gap-1">
                        <i class="fa-solid fa-code"></i> AIへの具体的な追加指示（プレビュー）
                    </span>
                    <pre class="p-3 bg-white border border-slate-200 text-slate-600 shadow-inner rounded-lg text-[10px] leading-relaxed overflow-x-auto whitespace-pre-wrap font-mono select-all">${explanationPreview}</pre>
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
${data.deepStates && data.deepStates.length > 0 ? data.deepStates.join('\n\n') : '* ※指定された重要ポイントはありません。'}

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
            const simulatedDatabase = {
                linestamp: {
                    steps: [
                        { name: "プロダクト・ストラテジスト", type: "strategy", log: "【目的・ターゲット変数抽出】\nLINEスタンプ開発。まずは『誰がいつ、なぜ使うか』を決定しなければ、画風すら決まりません。\n◆プロの盲点:\n「友人がこれ欲しいと言った」は信用してはいけません。彼らは120円でも財布を開きません。本当に身銭を切って買う人間は誰か？今回は『感情をSNSで過激に代弁してほしいITエンジニア層』に絞り、徹底的なニッチ市場での勝利を設計するべきです。" },
                        { name: "仕様・規格監修", type: "technical", log: "【プラットフォーム物理制約の罠】\nLINE Creators Marketは極めて融通のきかない物理制約と審査ポリシーを持ちます。\n◆プロの盲点:\n画像の周囲に『4pxの透明な余白』がないと一発で審査落ちします。また、1ピクセルでも完全に透過しきれていないゴミドットが残っていると不合格になります。この物理的チェック要件を最初から指示書に叩き込まなければ、完成後に全ファイルの修正地獄を味わうことになります。" },
                        { name: "UI/UX デザイナー", type: "design", log: "【視認性・意匠崩壊の防止】\nイラストのクオリティが高ければ売れるというのは初心者の大いなる誤解です。スマートフォンの画面サイズでの『実用性』が全てを支配します。\n◆プロの盲点:\n『透過背景での完全同化バグ』。現在スマホユーザーの約半数はダークモードを使用しています。背景が黒いトークルームで『黒線のイラスト』をそのまま送信すると、デザインが背景に溶けて完全に視認不可能になります。全ての画像に対し、輪郭線に『3px以上の白フチ（Stroke）』をかけることを絶対命令に含めましょう。" },
                        { name: "マネタイズ・アナリスト", type: "marketing", log: "【限界利益とリテンション設計】\n単発でリリースして誰も得しない赤字プロジェクトにさせないための、ビジネス変数設計。\n◆プロの盲点:\n売上の取り分35%からさらに源泉徴収10.21%が自動控除されるため、120円販売時の真の純手取りは『約37円』。さらに分配金は1,000円を超えなければ出金できません。つまり、最初に最低27個売るためのプロモーション経路をあらかじめ持っていなければ資金は死蔵します。また、日常の挨拶にスロットを16枚以上アサインする設計を行い、バイラル効果を狙います。" },
                        { name: "要件抽出コンパイラ", type: "compiler", log: "【1階・2階変数の完全マージ、検品完了】\n全員、素晴らしいデバッグです。専門的な深掘り項目（源泉徴収、白フチ、余白、バイラル）が完璧に出揃いました。1階の必須基礎確定要件と、2階のプロの見落とし対策をマージした仕様合意書をコンパイルしました。組み立て用ウィザードを起動します。" }
                    ],
                    questions: [
                        { id: "linestamp_base_target", label: "ターゲット属性", description: "このスタンプを主に誰に使ってもらいますか？画風やセリフの基礎になります。", source: "strategy" },
                        { id: "linestamp_base_count", label: "提供個数（スタンプ枚数）", description: "プラットフォーム規定の枚数（8/16/24/32/40枚）から、作成コストとのバランスを考えて選択してください。", source: "technical" },
                        { id: "linestamp_base_price", label: "販売希望価格", description: "クリエイターズマーケットでの販売価格（120円〜610円）を決定してください。", source: "marketing" },
                        { id: "linestamp_base_schedule", label: "制作目標期日", description: "イラストの制作から申請、リリース完了までの目標期間を設定します。", source: "strategy" }
                    ],
                    deepVars: [
                        { id: "linestamp_deep_dark", label: "ダークモード同化問題", detail: "スマホをダークモードにしている相手の画面で、スタンプの輪郭線が同化して消滅しないよう「境界線に太さ3px以上の白ふち（外光彩）」を自動適用して視認性を確保する。", source: "design" },
                        { id: "linestamp_deep_fee", label: "分配金引き出し手数料と源泉徴収の罠", detail: "売上の35%が取り分となるが、源泉所得税が約10.21%引かれ、さらに出金時の振込手数料（550円）を考慮し、手取りを最大化する『LINE Pay出金ルート』を最初から計画に組み込む。", source: "business" },
                        { id: "linestamp_deep_retention", label: "リテンション（3日の壁）対策", detail: "買われて3日で飽きられないよう、日常会話の送信頻度を分析。日常の『挨拶・了解・リアクション』の必須スロットに最低16枚をアサインし、バイラル拡散を促す。", source: "business" }
                    ]
                },
                lecture: {
                    steps: [
                        { name: "プロダクト・ストラテジスト", type: "strategy", log: "【講義ターゲット変数分析】\nテーマ：プログラマー向け生存戦略スライド資料。プログラマーは『論理的な整合性』と『自分で実際に動かせるか』しか信じない極めて硬派な集団です。\n◆プロの盲点:\n「AIで開発が楽になるよ」という啓蒙はエンジニアの反発を招きます。「AIに仕事を奪われるのでは？」という恐怖を、むしろ「AI組織をマネジメントする指揮官になれ」という優位性提示に転換するストーリー変数が必要です。" },
                        { name: "仕様・規格監修", type: "technical", log: "【プレゼン・デモ時間物理制約】\n20分〜30分という講義時間は極めて短いです。スライドは10枚以内、テキストは極小にする必要があります。\n◆プロの盲点:\nプログラマーはビジュアルだけのスライドよりも、コードスニペットやWBSなどの『構造データ』を好みます。MarpによるMarkdownプレゼン形式を採用し、『このスライド自体もエンジニアライクにビルドされたものである』という物理仕様を事前に設定しなければなりません。" },
                        { name: "UI/UX デザイナー", type: "design", log: "【エンジニアの美意識に刺さる意匠】\nプログラマーは、いかにもビジネスライクな「虹色のグラデーション」や「かわいいイラスト」をダサいと感じます。\n◆プロの盲点:\n文字量は徹底的に減らし、余白（Whitespace）を60%以上確保します。コードブロックが綺麗にシンタックスハイライトされるCSSを事前に定義し、ビジュアルに開発環境のリアリティを持たせます。" },
                        { name: "マネタイズ・アナリスト", type: "marketing", log: "【バズ（波及効果）とQ&Aの設計】\n講義をやりっぱなしで終わらせず、その後の自身のブランドや関係値構築に繋げるためのマーケティング変数の組み込み。\n◆プロの盲点:\n『Q&Aでの技術的質問に対する防衛壁』。エンジニアは講義後のQ&Aで『裏側のライブラリは何ですか？』という鋭い質問を投げてきます。これに対し、『実はその質問に対する解答プロセスも、このツールにセーブされており一瞬で呼び出せる』という圧倒的な優位性を演出するための伏線を事前に張り巡らせます。" },
                        { name: "要件抽出コンパイラ", type: "compiler", log: "【講義資料前提条件プロンプトのコンパイル完了】\n素晴らしい議論です。プログラマーの誇りと美意識を逆手に取った、論理的で刺さるスライド構成の変数が固まりました。1階と、2階（ボキャブラリ制限、種明かし伏線、Marp物理制約、Q&A防御）を分離したフォームをコンパイルしました。" }
                    ],
                    questions: [
                        { id: "lecture_base_target", label: "ターゲット受講生", description: "誰に向けて発表しますか？プログラマーのレベルや関心に合わせます。", source: "strategy" },
                        { id: "lecture_base_time", label: "想定講義時間", description: "発表の持ち時間を設定してください（通常20〜30分程度）。", source: "technical" },
                        { id: "lecture_base_design", label: "デザインテーマ", description: "スライドの視覚的雰囲気を指定してください（クリーン、開発者画面風など）。", source: "design" },
                        { id: "lecture_base_tone", label: "台本の言葉遣い・トーン", description: "解説台本やスライドのトーン（論理的、丁寧、フランクなど）を決定します。", source: "strategy" }
                    ],
                    deepVars: [
                        { id: "lecture_deep_vocabulary", label: "エンジニア向けボキャブラリ制限の罠", detail: "一般向けの「AIは魔法」という言葉は、プログラマーには1ミリも刺さらず不信感を抱かせます。「RAG」「コンテキスト窓」「マルチエージェント」といったシステムアーキテクチャの専門用語だけでスライドの言語を統一します。", source: "technical" },
                        { id: "lecture_deep_demolink", label: "デモンストレーションの伏線回収設計", detail: "スライドの最後に『実はこの講義スライド、台本、そして今見せたデモツールはすべて、私が自作したAI自律エージェント組織が全自動で作ったものだ』という伏線を回収し、強烈な焦燥感と熱狂を与える仕掛けを仕込みます。", source: "strategy" },
                        { id: "lecture_deep_timewalls", label: "スライド枚数の物理制約と時間配分", detail: "プログラマーは無駄に長いスライドを激しく嫌います。1枚につき2分で読了できる「箇条書き主体の10枚」を限界とし、各スライドの「結論・課題・コード」を3行以内にします。", source: "design" }
                    ]
                },
                youtube: {
                    steps: [
                        { name: "プロダクト・ストラテジスト", type: "strategy", log: "【動画コンセプト・ポジショニング変数】\nYouTube自動化動画企画。AIチャンネルは乱立しており、一般論をわかりやすく解説するだけでは大手やゆっくり解説に勝てません。\n◆プロの盲点:\n『役に立つ動画は再生されません。自分ごとになる動画が再生されます』。動画のタイトルは『Geminiの解説』ではなく、『Geminiで自分の日々のメール返信をゼロにした方法』のように、ターゲットの生活に1秒で結びつく前提パラメータが必要です。" },
                        { name: "仕様・規格監修", type: "technical", log: "【編集・解像度の物理的仕様】\nYouTubeのアップロードとプレイヤーには厳格な推奨規格があります。\n◆プロの盲点:\nスマホ視聴率が70%を超える現在、サムネイルは縦横比16:9で、スマホ画面に縮小された時に『3文字の強烈な太字フォント』でないと完全に無視されます。このサムネイル逆算仕様を企画の第1前提に置くべきです。" },
                        { name: "UI/UX デザイナー", type: "design", log: "【アテンション（視聴維持）をコントロールする意匠設計】\nYouTube編集において『画面が2秒変化しないと離脱する』という冷酷な実態があります。\n◆プロの盲点:\n生顔出しをしない場合、画面が静止画のままだと視聴維持率は即崩壊します。画面ズームイン/アウト、テロップの自動強調、効果音の挿入を『最低3秒に1回』強制的に実行するためのカットリスト前提を台本に最初から組み込むべきです。" },
                        { name: "マネタイズ・アナリスト", type: "marketing", log: "【アドセンス単価と集客導線設計】\n再生数が少なくても、確実にビジネスとしてマネタイズを成立させる変数。\n◆プロの盲点:\n『広告収入だけに頼るチャンネルは1年で潰れます』。動画の最終目的は、視聴者を概要欄から自身の自動化ツールへ誘導すること。1動画あたり最低1%のユーザーを『リスト化』するためのプレゼント提供を、台本後半で必ず告知します。" },
                        { name: "要件抽出コンパイラ", type: "compiler", log: "【YouTubeトレンド解説動画のプロンプトコンパイル】\n全員、素晴らしいデバッグです。アドセンス、視聴維持率、サムネ視認性、リスト誘導という冷酷なYouTubeの勝ちパターンが出揃いました。1階と、2階（冒頭30秒フック、スマホサムネ、3秒画面変化、無料プレゼント誘導）を分離したフォームを構築しました。" }
                    ],
                    questions: [
                        { id: "youtube_base_genre", label: "動画の具体的なジャンル", description: "解説するAI技術のジャンルや具体的な活用シナリオを設定してください。", source: "strategy" },
                        { id: "youtube_base_length", label: "想定動画尺（秒数）", description: "動画の長さを設定します。広告最適化や視聴維持の観点から決定します（通常8〜10分程度）。", source: "technical" },
                        { id: "youtube_base_voice", label: "音声・出演スタイル", description: "誰がどのように喋るか（生声、合成音声、顔出しの有無など）を選択してください。", source: "design" },
                        { id: "youtube_base_schedule", label: "1本あたりの制作目標時間", description: "企画から動画の撮影・編集、サムネイル作成、投稿までの目標日数です。", source: "marketing" }
                    ],
                    deepVars: [
                        { id: "youtube_deep_retention", label: "冒頭30秒（視聴維持率の壁）の罠", detail: "YouTubeアルゴリズムは冒頭30秒で60%以上の視聴者が離脱すると動画のインプレッションを完全停止させます。挨拶や自己紹介を完全に排除し、動画の結論を冒頭15秒以内に強制配置します。", source: "strategy" },
                        { id: "youtube_deep_metadata", label: "アルゴリズム自動マッチング用のタグと概要欄の罠", detail: "タイトル（30文字以内、スマホ切れ対策）に加えて、概要欄の最初の2行に重要キーワードを埋め込み、検索エンジンに動画のコンテキストを誤解なく認識させます。", source: "technical" },
                        { id: "youtube_deep_audio", label: "音響透過性とカット編集の物理制約", detail: "視聴者は画質よりも「音の聞き取りにくさ」で離脱します。ノイズキャンセリング、および会話の『間』を0.1秒単位で全自動でカットする無音トリム前提を台本に組み込みます。", source: "design" }
                    ]
                },
                app: {
                    steps: [
                        { name: "プロダクト・ストラテジスト", type: "strategy", log: "【アプリ開発戦略スキャニング】\nターゲットと提供コア価値を絞り込まないと、いつまでもリリースできない典型的な開発地獄に陥ります。\n◆プロの盲点:\n「多機能で完璧なアプリ」は開発期間が延びるだけで誰も使いません。最も解決したい『たった1つのコアの課題』だけを解くMVP（最小限実用製品）を定義し、他はすべて削るべきです。" },
                        { name: "仕様・規格監修", type: "technical", log: "【技術スタックとインフラ物理制約】\n開発効率とスケーラビリティ、そして自身のスキルに合わせた無理のない技術選定を行います。\n◆プロの盲点:\n勉強を兼ねて新しいモダンすぎる技術を選びすぎると、バグや仕様の違いで挫折します。実績のあるバックエンド（Supabase/Firebase等）を採用し、認証やDB構築の時間を90%削減すべきです。" },
                        { name: "UI/UX デザイナー", type: "design", log: "【ユーザー体験（UX）のシンプル化】\nユーザーがログインしてから、目的の機能を実行するまでの「クリック数」を極限まで削減します。\n◆プロの盲点:\nログイン後に複雑なダッシュボードを見せられるとユーザーは離脱します。1ボタンで目的が達成できる直感的な1機能UIにし、ダークモード等の配色コントラスト比（WCAG基準）を担保します。" },
                        { name: "マネタイズ・アナリスト", type: "marketing", log: "【フリーミアムと継続利用ループ】\n利用者を初期フェーズで集め、継続的な有料課金（SaaS）へ移行させるためのビジネス導線設計。\n◆プロの盲点:\n「完全に無料」で提供すると、サーバー代だけがかかって破綻します。最初の10回は無料、それ以降はサブスクリプションといった『限界コスト』と『マネタイズトリガー』を設計の第1段階に組み込みます。" },
                        { name: "要件抽出コンパイラ", type: "compiler", log: "【アプリ・SaaS開発要件のコンパイル完了】\n全員、素晴らしいデバッグです。機能範囲（MVP）、認証インフラ、シンプルなUI/UX、フリーミアム限界利益が出揃いました。1階の必須確定要件と、2階のプロの盲点対策（スコープクリープ防止、データ保護、規約策定）をマージした仕様書を構築しました。" }
                    ],
                    questions: [
                        { id: "app_base_target", label: "ターゲットユーザー層", description: "このアプリを主に誰に使ってもらいますか？（個人B2C、特定業種B2B、個人開発者など）", source: "strategy" },
                        { id: "app_base_mvp", label: "提供するコア機能（MVP）", description: "最初にリリースする「最小限の必須機能」を1つだけ選定してください。", source: "strategy" },
                        { id: "app_base_tech", label: "使用する開発技術スタック", description: "開発効率と速度を最優先するためのフロントエンド・バックエンド技術を選択します。", source: "technical" },
                        { id: "app_base_schedule", label: "リリース目標期日", description: "最初のMVP版を本番環境にデプロイし、公開するまでの目標期間を設定します。", source: "technical" }
                    ],
                    deepVars: [
                        { id: "app_deep_scope", label: "スコープクリープ（機能水増し）の地雷対策", detail: "最初からあれもこれもと機能を追加せず、たった1つのコア機能（MVP）だけを最速でリリースしてユーザーの生の反応を見る設計を徹底する。", source: "strategy" },
                        { id: "app_deep_security", label: "セキュリティと顧客データ損失対策", detail: "認証機能のバグやDB接続エラーによる顧客データの消失を防ぐため、SupabaseやFirebase等の実績のあるマネージドなセキュアバックエンドを採用する。", source: "technical" },
                        { id: "app_deep_terms", label: "利用規約とプライバシーポリシーの欠如対策", detail: "個人情報やログイン情報を扱うSaaSにおいて、リリース時の利用規約やプライバシーポリシーの策定を忘れずに、ひな形を流用して初期設計時に必ず配置する。", source: "business" }
                    ]
                },
                blog: {
                    steps: [
                        { name: "プロダクト・ストラテジスト", type: "strategy", log: "【メディア戦略・競合差別化】\nブログは競合が極めて多いジャンルです。一般論を書くブログは100%埋もれます。\n◆プロの盲点:\n「みんなが書いているテーマ」を書いてはいけません。自分の『実体験・一次情報』に基づいた専門特化ブログにし、検索キーワードではなく『読者の具体的な悩み』から逆算して記事を設計します。" },
                        { name: "仕様・規格監修", type: "technical", log: "【SEOプラットフォーム制約とサイト構造】\nGoogleの検索アルゴリズム、およびサイトの表示速度は、記事の品質と同等に重要です。\n◆プロの盲点:\n健康やお金に関するジャンル（YMYL）は個人ブログでは現在絶対にインデックス上位に入りません。このプラットフォーム物理制約をスキャンし、最初からYMYL以外のニッチな専門技術や趣味ジャンルに絞る設計を行います。" },
                        { name: "UI/UX デザイナー", type: "design", log: "【記事の可読性とレイアウト設計】\nスマホでの閲覧率が8割を超える現在、PC用の重厚なレイアウトは離脱の原因になります。\n◆プロの盲点:\n文字がぎっしり詰まった記事は読まれません。余白を60%以上確保し、2〜3行ごとに改行、重要なキーワードにはマーカー、図解やリストを表形式で挿入して『スクロールしながら流し読みできるUX』を徹底します。" },
                        { name: "マネタイズ・アナリスト", type: "marketing", log: "【収益化経路とアフィリエイト限界利益】\nAdSenseの数円〜数十円のクリック収入に依存すると、PV数不足で確実に心が折れます。\n◆プロの盲点:\n初期段階から1コンバージョンで数千円以上の利益を生む『ASP成果報酬型アフィリエイト』や『自社教材の販売』への導線をあらかじめ記事設計に組み込み、少ないPV数でも利益が出る限界利益設計を行います。" },
                        { name: "要件抽出コンパイラ", type: "compiler", log: "【ブログ・メディア運営要件のコンパイル完了】\n素晴らしいデバッグです。実体験による特化テーマ、YMYL回避、流し読み可読性、高単価アフィリエイト導線が固まりました。1階の必須確定要件と、2階の見落とし対策（一次情報比率、YMYL回避、毎日更新の罠回避）をマージした仕様をコンパイルしました。" }
                    ],
                    questions: [
                        { id: "blog_base_genre", label: "発信テーマ・特化ジャンル", description: "自分の得意分野や実体験がある、競合と差別化しやすい特化ジャンルを決定してください。", source: "strategy" },
                        { id: "blog_base_pace", label: "記事の更新ペース目標", description: "挫折を防ぎ、高品質な記事を維持するための現実的な週あたりの目標執筆数を設定します。", source: "technical" },
                        { id: "blog_base_seo", label: "主な集客経路とアプローチ", description: "検索エンジン(SEO)からの自然流入を狙うか、SNSからのファン流入を主軸にするか選択します。", source: "marketing" },
                        { id: "blog_base_money", label: "初期マネタイズ手段", description: "アドセンス広告（クリック報酬）か、アフィリエイト（成果報酬）か、収益の主軸を決定します。", source: "marketing" }
                    ],
                    deepVars: [
                        { id: "blog_deep_experience", label: "一次情報（体験談）の圧倒的な欠如対策", detail: "現在乱立しているAI自動生成記事やまとめサイトと徹底的に差別化するため、自分にしか書けない『実体験・失敗談・独自写真』を必ず60%以上含める。", source: "strategy" },
                        { id: "blog_deep_ymyl", label: "Google SEOのYMYL（健康・医療・お金）の罠対策", detail: "健康やお金に関するジャンルは個人ブログでは検索上位に絶対に入らないため、あらかじめそれらのジャンルを避け、趣味や専門技術に絞る。", source: "technical" },
                        { id: "blog_deep_burnout", label: "毎日更新による燃え尽き症候群の罠対策", detail: "毎日更新のプレッシャーで低品質な記事を量産するより、読者の悩みを100%解決する高品質な『決定版記事』を週1本集中して書く運営計画にする。", source: "business" }
                    ]
                },
                creative: {
                    steps: [
                        { name: "プロダクト・ストラテジスト", type: "strategy", log: "【クリエイティブ戦略・ポジショニング】\nイラストやデザインは無数のフリー素材と競合します。独自の個性がないと無価値になります。\n◆プロの盲点:\n「何でも描ける絵師」は誰にも見つかりません。テーマを特定（例：レトロポップな女の子、特定の業界用アイコンなど）に絞り込み、特定のファン層やビジネス用途に100%突き刺すコンセプトを確立します。" },
                        { name: "仕様・規格監修", type: "technical", log: "【解像度とプラットフォーム入稿物理制約】\n販売サイトやSNSごとに異なる推奨サイズや透過ポリシー、知的財産権の基準を事前チェックします。\n◆プロの盲点:\n入稿規定を無視して描き始めると、最後にアスペクト比の崩壊やサイズ制限で全リサイズを強いられます。アップスケール（高解像度化）や完全RGB透過処理をワークフローに組み込みます。" },
                        { name: "UI/UX デザイナー", type: "design", log: "【視認性・デバイス最適化の意匠設計】\nイラストはPCの大画面だけでなく、スマホやSNSの小さなタイムライン上で一瞬で目を引く必要があります。\n◆プロの盲点:\n細部を描き込みすぎると、スマホ縮小時に何が描いてあるか分からなくなります。全体のシルエットを明瞭にし、境界線に適切なコントラストをつけ、文字を入れる場合は極太の視認フォントを採用します。" },
                        { name: "マネタイズ・アナリスト", type: "marketing", log: "【販売プラットフォームと二次利用ビジネス】\n単発のイラスト切り売り（数百円）から脱却し、継続的なライセンス収入（ストック販売）やファンクラブ収入へ繋げます。\n◆プロの盲点:\n「商用利用の範囲」を明確に規約で定義しておかないと、トラブルや無断転載による損失を被ります。あらかじめロイヤリティフリーか個人限定かのライセンス条件を明文化して販売計画を組み立てます。" },
                        { name: "要件抽出コンパイラ", type: "compiler", log: "【クリエイティブ意匠要件のコンパイル完了】\n素晴らしい議論です。特定テーマ特化、高解像度入稿規定、スマホ視認性、商用利用規約が出揃いました。1階の必須要件と、2階の見落とし対策（透過バグ、物理解像度の壁、知的財産権侵害回避）をマージしたプロンプト仕様をコンパイルしました。" }
                    ],
                    questions: [
                        { id: "creative_base_style", label: "作風・提供ビジュアルスタイル", description: "イラストやビジュアルの画風（手書き、AI生成加工、フラットデザイン等）を定義します。", source: "design" },
                        { id: "creative_base_count", label: "作成ボリューム（枚数）", description: "最初のセットとして提供するイラストやアセットの点数を決定してください。", source: "technical" },
                        { id: "creative_base_target", label: "ターゲット顧客属性", description: "この作品を誰に見て（または購入して）もらいますか？（特定ニッチ層、一般、ビジネス向けなど）", source: "strategy" },
                        { id: "creative_base_schedule", label: "制作目標スケジュール", description: "下絵、線画、着色、最終ブラッシュアップからリリースまでの目標日数です。", source: "technical" }
                    ],
                    deepVars: [
                        { id: "creative_deep_dark", label: "透過背景での同化バグ対策", detail: "スマホをダークモードにしている相手の画面で、キャラクターの黒線が同化して消滅しないよう「境界線に適切な太さのコントラストフチ」を自動適用して視認性を確保する。", source: "design" },
                        { id: "creative_deep_resolution", label: "出力物理解像度の壁と劣化対策", detail: "購入したユーザーが商用利用や印刷など、どんな用途でも綺麗に使える品質を担保するため、AIアップスケーラー等を介して印刷耐えうる超高画質で出力する。", source: "technical" },
                        { id: "creative_deep_policy", label: "プラットフォーム審査と権利関係ポリシー違反対策", detail: "販売サイトやSNSの規約（公序良俗、知的財産権の侵害、AI生成物の商用利用可否など）を最初にチェックし、全ファイル書き直し地獄を回避する。", source: "business" }
                    ]
                },
                general: {
                    steps: [
                        { name: "プロダクト・ストラテジスト", type: "strategy", log: "【新規プロジェクト戦略分析】\n新しいアイデアを成功させるために、まずは『ターゲット層』と『一番達成したいメインゴール』を明確に分離します。\n◆プロの盲点:\n「誰にでも役立つもの」は誰にも響きません。特定の強いニーズや悩みを抱えるペルソナ（1人）を詳細に想像し、その人のためだけに起動します。" },
                        { name: "仕様・規格監修", type: "technical", log: "【プロジェクト物理制約とスケジュール監査】\n投下できる限られた時間とリソースの中で、確実に『形にする』ための現実的なマイルストーンを設計します。\n◆プロの盲点:\n「完璧な状態で終わらせよう」とすると永遠に終わりません。1〜2週間以内に完了できる『極小のプロトタイプ』を定義し、タスクを細かく分解します。" },
                        { name: "UI/UX デザイナー", type: "design", log: "【ユーザー行動・情報アクセスのシンプル化】\n成果物を手にしたユーザーや受講生が、戸惑わずに「次の行動」に移れるような一貫した導線を作ります。\n◆プロの盲点:\n最初の印象で『難しそう・面倒そう』と思われたらそこで終了です。余白を多く取り、情報を箇条書きで整理し、次のステップを明確にします。" },
                        { name: "マネタイズ・アナリスト", type: "marketing", log: "【集客導線とリテンション・継続性】\n単発で終わらせず、次のアクションや継続的な関係値、ブランドの構築に繋げるための設計を行います。\n◆プロの盲点:\n終わった後のフォロー経路をあらかじめ持っていなければ、集まったユーザーは離散します。最後に次回のアクションやメールリストへの誘導を必ず仕込みます。" },
                        { name: "要件抽出コンパイラ", type: "compiler", log: "【新規プロジェクト要件のコンパイル完了】\n素晴らしいディスカッションです。ペルソナ定義、極小プロトタイプ、直感的UX、次回へのフォロー導線が出揃いました。1階の必須要件と、2階の盲点対策（最初の一歩設定、フィードバック収集、タスク細分化）をマージした仕様をコンパイルしました。" }
                    ],
                    questions: [
                        { id: "general_base_target", label: "ターゲットペルソナ層", description: "このプロジェクトは、主にどのような課題や悩みを持つ人を対象にしますか？", source: "strategy" },
                        { id: "general_base_goal", label: "プロジェクトのメインゴール", description: "この取り組みで最も達成したい『成功の基準』（0→1の売上、スキルアップ、ファン構築など）を設定します。", source: "strategy" },
                        { id: "general_base_time", label: "投下できる週あたり時間", description: "プロジェクト推進のために週にどれくらいの時間を割り当てられますか？", source: "technical" },
                        { id: "general_base_schedule", label: "想定完了目標期日", description: "最初のマイルストーン（初期バージョン完成）までの目標期限を設定します。", source: "technical" }
                    ],
                    deepVars: [
                        { id: "general_deep_firststep", label: "最初の一歩のハードルによる挫折対策", detail: "最初から完璧を目指しすぎて挫折するのを防ぐため、24時間以内に完了できる極小の『小さなプロトタイプ』を定義し、まずそれを完成させる。", source: "strategy" },
                        { id: "general_deep_feedback", label: "顧客・他者のフィードバック完全無視対策", detail: "自分の作りたいものだけを作って独りよがりになるのを防ぐため、早い段階で友人やSNSに公開し、フィードバック（生の声）を強制的に集める仕組みを作る。", source: "business" },
                        { id: "general_deep_management", label: "タスク増大によるモチベーション破綻対策", detail: "タスク管理を怠って何から手を付ければいいか分からなくなる罠を回避するため、WBS（作業分解構成図）を使い、全てのタスクを1時間以内に完了できるサブタスクに分解する。", source: "technical" }
                    ]
                }
            };

            const data = simulatedDatabase[genre] || simulatedDatabase.general;
            rawBaseVars = data.questions;
            rawDeepVars = data.deepVars;

            // Display simulated debate progress
            const stepDelays = [1500, 1500, 1500, 1500, 1000];
            for (let i = 0; i < 5; i++) {
                setAgentPhase(2, i + 1);
                progressBar.style.width = `${(i + 1) * 20}%`;
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
                const businessOutput = await callGeminiAgent(apiKey, `あなたはビジネスアナリストです。収益変数、価格、集客目標を定義し、収益化において見落としがちな重要ポイントを洗い出してください。出力は「〜です/ます」調の丁寧な口調を使用してください。\n${depthInstructions.desc}`, baseContext);
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

【重要：出力のトーン規定】
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
                            <div class="text-sm font-bold text-slate-800 mb-1 relative z-10 flex items-center gap-2">
                                <span class="text-[10px] px-2 py-0.5 rounded ${style.bg} ${style.colorText} font-extrabold shadow-sm tracking-wider">${style.label}</span>
                                ${q.label}
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
                            <div class="text-sm font-bold text-rose-800 mb-1 relative z-10 flex items-center gap-2">
                                <span class="text-[10px] px-2 py-0.5 rounded ${style.bg} ${style.colorText} font-extrabold shadow-sm tracking-wider">${style.label}</span>
                                POINT ${i+1}. ${d.label}
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
                            <span class="px-2.5 py-1 bg-teal-600 text-white rounded-lg text-[10px] font-black shadow-sm tracking-wider whitespace-nowrap">💡 あなたの初期希望</span>
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
                                <span class="px-2 py-0.5 bg-teal-500 text-white rounded text-[9px] font-extrabold shadow-sm tracking-wider">初期希望</span>
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
                    currentDeepStates.push(`* **${v.label}対策:**\n  ${v.detail}`);
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
                        <p class="text-[11px] text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：温かみや個性をアピールし、現在大量に流通している安易なAI生成スタンプと徹底的な差別化を狙うため。<br>
                            <span class="text-[10px] text-slate-400 font-medium">（※他には <code>AIイラスト</code> / <code>写真加工</code> からも自由に選択・書き換え可能です）</span>
                        </p>
                    </div>
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-emerald-100 text-emerald-800 rounded">申請枚数：24枚</span>
                        </div>
                        <p class="text-[11px] text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：制作の手間（コスト）と、購入したユーザーが日常使いする満足度のバランスが最も良いため。<br>
                            <span class="text-[10px] text-slate-400 font-medium">（※他には <code>8枚</code> / <code>16枚</code> / <code>32枚</code> からも選択可能です）</span>
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
                        <p class="text-[11px] text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：最初から多機能にせず、最も重要な1つのコア機能だけを最速でリリースしてユーザーの反応（市場適合性）を見るため。<br>
                            <span class="text-[10px] text-slate-400 font-medium">（※他には <code>複数機能のフルパッケージ</code> などからも書き換え可能です）</span>
                        </p>
                    </div>
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-cyan-100 text-cyan-800 rounded">開発手法：一番慣れているプログラミング言語</span>
                        </div>
                        <p class="text-[11px] text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：新しい言語やフレームワークの学習コストをゼロにし、リリースまでのスピードを最大化するため。<br>
                            <span class="text-[10px] text-slate-400 font-medium">（※他には <code>新規の勉強したい言語</code> などからも書き換え可能です）</span>
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
                        <p class="text-[11px] text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：なんでも屋にならず、「ファンタジー背景」などの特定のニーズに絞ることで、熱狂的なファンやリピーターを確実に増やすため。<br>
                            <span class="text-[10px] text-slate-400 font-medium">（※他には <code>なんでも描くオールジャンル</code> などからも書き換え可能です）</span>
                        </p>
                    </div>
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-purple-100 text-purple-800 rounded">画像サイズ：高解像度</span>
                        </div>
                        <p class="text-[11px] text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：購入したユーザーが商用利用や印刷など、どんな用途でも綺麗に使える品質を担保し、顧客満足度を上げて低評価を防ぐため。<br>
                            <span class="text-[10px] text-slate-400 font-medium">（※他には <code>通常解像度</code> などからも書き換え可能です）</span>
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
                        <p class="text-[11px] text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：一般論ではなく、自分にしか書けない一次情報（体験談）を書くことで、現在乱立しているAI自動生成記事と徹底的に差別化するため。<br>
                            <span class="text-[10px] text-slate-400 font-medium">（※他には <code>流行のキーワード・雑記ブログ</code> などからも書き換え可能です）</span>
                        </p>
                    </div>
                    <div class="p-3.5 bg-white/70 rounded-xl border border-teal-100/60 shadow-sm flex flex-col gap-1.5">
                        <div class="flex items-center gap-2 font-bold text-slate-800 text-xs">
                            <span class="px-2.5 py-0.5 bg-amber-100 text-amber-800 rounded">更新目標：週に1〜2本の高品質な記事</span>
                        </div>
                        <p class="text-[11px] text-slate-700 leading-relaxed pl-1 font-semibold">
                            👉 <strong>[プロの理由]</strong>：毎日更新で疲弊して低品質になるのを防ぎ、読者の検索意図（悩み）を完全に解決する本当に価値のある記事の執筆に集中するため。<br>
                            <span class="text-[10px] text-slate-400 font-medium">（※他には <code>毎日更新</code> などからも書き換え可能です）</span>
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
    </script>
    
    <!-- 常に表示される文字サイズコントローラー -->
    <div class="fixed bottom-6 left-6 z-50 flex flex-col gap-2">
        <div class="flex flex-col gap-1 bg-white/90 backdrop-blur-md p-2 rounded-xl border border-slate-200 shadow-lg shrink-0 transition-all hover:shadow-xl group">
            <span class="text-[10px] font-black text-slate-400 px-1 uppercase tracking-wider flex items-center gap-1 opacity-70 group-hover:opacity-100 transition-opacity"><i class="fa-solid fa-font"></i> 文字サイズ</span>
            <div class="flex gap-1">
                <button id="btn-font-medium" onclick="setGlobalFontSize('medium')" class="px-3 py-1.5 text-xs font-bold rounded-lg border transition-all cursor-pointer bg-teal-50 border-teal-200 text-teal-600">標準</button>
                <button id="btn-font-large" onclick="setGlobalFontSize('large')" class="px-3 py-1.5 text-xs font-bold rounded-lg border transition-all cursor-pointer bg-white border-slate-200 text-slate-600 hover:bg-slate-50">大</button>
                <button id="btn-font-xl" onclick="setGlobalFontSize('xl')" class="px-3 py-1.5 text-xs font-bold rounded-lg border transition-all cursor-pointer bg-white border-slate-200 text-slate-600 hover:bg-slate-50">特大</button>
            </div>
        </div>
    </div>
</body>
</html>





"""

with open('Level 30 Booster.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

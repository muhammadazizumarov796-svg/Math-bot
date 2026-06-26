import os
import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", ""))

SYSTEM_PROMPTS = {
    "yordam": """Siz tajribali o'zbek matematik o'qituvchisisiz. 
Foydalanuvchi sizga matematik misol rasmini yuboradi.
Sizning vazifangiz: faqat YO'NALISH va MASLAHAT bering.
- Misol qaysi mavzuga tegishli ekanligini ayting
- Qanday usullar bilan yechish mumkinligini tushuntiring
- Formulalar va qoidalarni eslatib o'ting
- Lekin to'liq yechimni BERMANG
Javobingiz o'zbek tilida bo'lsin.""",

    "yechish": """Siz tajribali o'zbek matematik o'qituvchisisiz.
Foydalanuvchi sizga matematik misol rasmini yuboradi.
Sizning vazifangiz: misolni BOSQICHMA-BOSQICH to'liq yeching.
- Har bir qadamni aniq izohlang
- Oraliq natijalarni ko'rsating
- Yakuniy javobni aniq belgilang
Javobingiz o'zbek tilida bo'lsin.""",

    "xato": """Siz tajribali o'zbek matematik o'qituvchisisiz.
Foydalanuvchi sizga matematik misolni o'z yechimi bilan yuboradi.
Sizning vazifangiz: foydalanuvchining yechimidagi XATOLARNI TOPING.
- Har bir xatoni aniq ko'rsating
- To'g'ri yechish usulini ko'rsating
Javobingiz o'zbek tilida bo'lsin."""
}

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="uz">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
<title>MathAI</title>
<script src="https://telegram.org/js/telegram-web-app.js"></script>
<style>
:root{--bg:#0D0F14;--surface:#161A23;--surface2:#1E2330;--border:#2A3045;--accent:#6C63FF;--accent2:#A78BFA;--text:#F0F2FF;--text-dim:#8892AA;--radius:16px;--radius-sm:10px}
*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'Segoe UI',system-ui,sans-serif;min-height:100vh;display:flex;flex-direction:column}
.header{background:linear-gradient(135deg,#1E1B4B 0%,#0D0F14 60%);padding:20px 20px 16px;border-bottom:1px solid var(--border)}
.header-top{display:flex;align-items:center;gap:12px;margin-bottom:14px}
.logo{width:44px;height:44px;background:linear-gradient(135deg,var(--accent),var(--accent2));border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:22px;box-shadow:0 4px 16px rgba(108,99,255,.4);flex-shrink:0}
.header-title h1{font-size:20px;font-weight:700}.header-title p{font-size:12px;color:var(--text-dim);margin-top:2px}
.mode-tabs{display:flex;gap:8px;overflow-x:auto;scrollbar-width:none;padding-bottom:2px}
.mode-tabs::-webkit-scrollbar{display:none}
.tab{flex-shrink:0;padding:8px 14px;border-radius:24px;border:1.5px solid var(--border);background:transparent;color:var(--text-dim);font-size:13px;font-weight:500;cursor:pointer;transition:all .2s;white-space:nowrap}
.tab.active{background:var(--accent);border-color:var(--accent);color:#fff;box-shadow:0 2px 12px rgba(108,99,255,.4)}
main{flex:1;padding:20px;display:flex;flex-direction:column;gap:16px}
.mode-info{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px;display:flex;align-items:flex-start;gap:12px}
.mode-icon{font-size:26px;line-height:1;flex-shrink:0;margin-top:2px}
.mode-desc h3{font-size:14px;font-weight:600;margin-bottom:4px}.mode-desc p{font-size:12px;color:var(--text-dim);line-height:1.5}
.upload-zone{background:var(--surface);border:2px dashed var(--border);border-radius:var(--radius);padding:32px 20px;text-align:center;cursor:pointer;transition:all .25s;position:relative;overflow:hidden}
.upload-zone:hover,.upload-zone.drag-over{border-color:var(--accent);background:rgba(108,99,255,.06)}
.upload-zone.has-image{border-style:solid;border-color:var(--accent);padding:0}
.upload-icon{font-size:40px;margin-bottom:12px}.upload-title{font-size:15px;font-weight:600;margin-bottom:6px}.upload-sub{font-size:12px;color:var(--text-dim)}
#file-input{display:none}
#preview-wrap{position:relative}
#preview-img{width:100%;border-radius:14px;display:block;max-height:280px;object-fit:contain;background:#000}
.remove-btn{position:absolute;top:10px;right:10px;background:rgba(0,0,0,.65);border:none;color:#fff;width:30px;height:30px;border-radius:50%;font-size:16px;cursor:pointer;display:flex;align-items:center;justify-content:center}
.extra-box{background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:14px 16px}
.extra-box label{font-size:13px;font-weight:600;color:var(--text-dim);display:block;margin-bottom:8px}
.extra-box textarea{width:100%;background:var(--surface2);border:1px solid var(--border);border-radius:var(--radius-sm);color:var(--text);padding:10px 12px;font-size:14px;resize:none;outline:none;font-family:inherit;line-height:1.5;transition:border-color .2s}
.extra-box textarea:focus{border-color:var(--accent)}
.submit-btn{width:100%;padding:16px;background:linear-gradient(135deg,var(--accent),#8B5CF6);border:none;border-radius:var(--radius);color:#fff;font-size:16px;font-weight:700;cursor:pointer;box-shadow:0 4px 20px rgba(108,99,255,.4);transition:all .2s;display:flex;align-items:center;justify-content:center;gap:8px}
.submit-btn:disabled{opacity:.5;cursor:not-allowed}
.loading{display:none;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);padding:28px 20px;text-align:center}
.loading.show{display:block}
.spinner{width:44px;height:44px;border:3px solid var(--border);border-top-color:var(--accent);border-radius:50%;animation:spin .8s linear infinite;margin:0 auto 16px}
@keyframes spin{to{transform:rotate(360deg)}}
.loading-text{font-size:14px;color:var(--text-dim)}
.result-card{display:none;background:var(--surface);border:1px solid var(--border);border-radius:var(--radius);overflow:hidden}
.result-card.show{display:block}
.result-header{padding:14px 16px;display:flex;align-items:center;gap:10px;border-bottom:1px solid var(--border)}
.result-badge{padding:4px 10px;border-radius:20px;font-size:12px;font-weight:600;background:rgba(108,99,255,.15);color:var(--accent2)}
.result-body{padding:16px;font-size:14px;line-height:1.75;color:var(--text);white-space:pre-wrap;word-break:break-word;max-height:420px;overflow-y:auto}
.result-footer{padding:12px 16px;border-top:1px solid var(--border);display:flex;gap:8px}
.btn-sm{flex:1;padding:10px;border-radius:var(--radius-sm);border:1px solid var(--border);background:var(--surface2);color:var(--text-dim);font-size:13px;cursor:pointer;transition:all .2s}
.btn-sm.primary{background:var(--accent);border-color:var(--accent);color:#fff}
.error-card{display:none;background:rgba(248,113,113,.08);border:1px solid rgba(248,113,113,.3);border-radius:var(--radius);padding:16px;color:#F87171;font-size:13px;line-height:1.5}
.error-card.show{display:block}
</style>
</head>
<body>
<header class="header">
<div class="header-top">
<div class="logo">🧮</div>
<div class="header-title"><h1>MathAI</h1><p>Matematik yordamchi</p></div>
</div>
<div class="mode-tabs">
<button class="tab" data-mode="yordam" onclick="setMode('yordam')">📚 Yo'nalish</button>
<button class="tab" data-mode="yechish" onclick="setMode('yechish')">✅ Yechish</button>
<button class="tab" data-mode="xato" onclick="setMode('xato')">🔍 Xato topish</button>
</div>
</header>
<main>
<div class="mode-info">
<div class="mode-icon" id="modeIcon">📚</div>
<div class="mode-desc"><h3 id="modeTitle">Yo'nalish olish</h3><p id="modeDesc">Misol qanday mavzudan ekanligi va qanday yechilishi haqida maslahat olasiz.</p></div>
</div>
<div class="upload-zone" id="uploadZone" onclick="document.getElementById('file-input').click()">
<div id="uploadPlaceholder"><div class="upload-icon">📸</div><div class="upload-title">Rasm yuklash</div><div class="upload-sub">Matematik misol rasmini tanlang</div></div>
<div id="preview-wrap" style="display:none"><img id="preview-img" alt="Misol"><button class="remove-btn" onclick="removeImage(event)">✕</button></div>
<input type="file" id="file-input" accept="image/*" onchange="handleFile(event)">
</div>
<div class="extra-box" id="extraBox" style="display:none">
<label>📝 Sizning yechimingiz (ixtiyoriy)</label>
<textarea id="userSolution" rows="4" placeholder="Siz qanday yechdingiz?"></textarea>
</div>
<button class="submit-btn" id="submitBtn" onclick="submitImage()" disabled><span>🚀</span><span id="submitText">Yuborish</span></button>
<div class="loading" id="loading"><div class="spinner"></div><div class="loading-text">AI tahlil qilmoqda...</div></div>
<div class="error-card" id="errorCard"></div>
<div class="result-card" id="resultCard">
<div class="result-header"><span id="resultEmoji">📚</span><strong id="resultTitle">Natija</strong><div class="result-badge" id="resultBadge">Yo'nalish</div></div>
<div class="result-body" id="resultBody"></div>
<div class="result-footer"><button class="btn-sm" onclick="resetAll()">🔄 Qayta</button><button class="btn-sm primary" onclick="copyResult()">📋 Nusxa</button></div>
</div>
</main>
<script>
const tg=window.Telegram?.WebApp;
if(tg){tg.ready();tg.expand();}
const API_BASE=window.location.origin;
let currentMode='yordam',imageBase64=null;
const MODES={
yordam:{icon:'📚',title:"Yo'nalish olish",desc:"Maslahat va yechish usulini olasiz.",badge:"Yo'nalish",emoji:'📚'},
yechish:{icon:'✅',title:"Bosqichma-bosqich yechish",desc:"Misol to'liq yechiladi.",badge:'Yechish',emoji:'✅'},
xato:{icon:'🔍',title:"Xatoni topish",desc:"Yechimingizni tekshirib, xatolarni topadi.",badge:'Xato topish',emoji:'🔍'}
};
const urlMode=new URLSearchParams(window.location.search).get('mode');
setMode(urlMode&&MODES[urlMode]?urlMode:'yordam');
function setMode(m){
currentMode=m;const md=MODES[m];
document.getElementById('modeIcon').textContent=md.icon;
document.getElementById('modeTitle').textContent=md.title;
document.getElementById('modeDesc').textContent=md.desc;
document.querySelectorAll('.tab').forEach(t=>t.classList.toggle('active',t.dataset.mode===m));
document.getElementById('extraBox').style.display=m==='xato'?'block':'none';
hideResult();hideError();
}
function handleFile(e){const f=e.target.files[0];if(f)loadImage(f);}
function loadImage(f){
const r=new FileReader();
r.onload=ev=>{
imageBase64=ev.target.result;
document.getElementById('preview-img').src=imageBase64;
document.getElementById('uploadPlaceholder').style.display='none';
document.getElementById('preview-wrap').style.display='block';
document.getElementById('uploadZone').classList.add('has-image');
document.getElementById('submitBtn').disabled=false;
};r.readAsDataURL(f);
}
function removeImage(e){
e.stopPropagation();imageBase64=null;
document.getElementById('file-input').value='';
document.getElementById('preview-img').src='';
document.getElementById('uploadPlaceholder').style.display='block';
document.getElementById('preview-wrap').style.display='none';
document.getElementById('uploadZone').classList.remove('has-image');
document.getElementById('submitBtn').disabled=true;
hideResult();hideError();
}
const zone=document.getElementById('uploadZone');
zone.addEventListener('dragover',e=>{e.preventDefault();zone.classList.add('drag-over');});
zone.addEventListener('dragleave',()=>zone.classList.remove('drag-over'));
zone.addEventListener('drop',e=>{e.preventDefault();zone.classList.remove('drag-over');const f=e.dataTransfer.files[0];if(f&&f.type.startsWith('image/'))loadImage(f);});
async function submitImage(){
if(!imageBase64)return;
setLoading(true);hideResult();hideError();
try{
const res=await fetch(`${API_BASE}/api/analyze`,{
method:'POST',headers:{'Content-Type':'application/json'},
body:JSON.stringify({image_base64:imageBase64,mode:currentMode,user_solution:document.getElementById('userSolution').value.trim()||null})
});
if(!res.ok){const e=await res.json().catch(()=>({detail:'Server xatosi'}));throw new Error(e.detail||'Server xatosi');}
const data=await res.json();showResult(data.result);
}catch(err){showError(`❌ Xato: ${err.message}`);}
finally{setLoading(false);}
}
function setLoading(on){
document.getElementById('loading').classList.toggle('show',on);
document.getElementById('submitBtn').disabled=on;
document.getElementById('submitText').textContent=on?'Tahlil qilinmoqda...':'Yuborish';
}
function showResult(text){
const m=MODES[currentMode];
document.getElementById('resultEmoji').textContent=m.emoji;
document.getElementById('resultTitle').textContent=m.title;
document.getElementById('resultBadge').textContent=m.badge;
document.getElementById('resultBody').textContent=text;
document.getElementById('resultCard').classList.add('show');
document.getElementById('resultCard').scrollIntoView({behavior:'smooth',block:'start'});
}
function hideResult(){document.getElementById('resultCard').classList.remove('show');}
function showError(msg){const el=document.getElementById('errorCard');el.textContent=msg;el.classList.add('show');}
function hideError(){document.getElementById('errorCard').classList.remove('show');}
function resetAll(){removeImage({stopPropagation:()=>{}});document.getElementById('userSolution').value='';}
function copyResult(){
navigator.clipboard.writeText(document.getElementById('resultBody').textContent).then(()=>{
const btn=event.target;const orig=btn.textContent;btn.textContent='✅ Nusxalandi!';setTimeout(()=>btn.textContent=orig,1500);
});
}
</script>
</body>
</html>"""

class AnalyzeRequest(BaseModel):
    image_base64: str
    mode: str
    user_solution: Optional[str] = None

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_CONTENT

@app.post("/api/analyze")
async def analyze_image(request: AnalyzeRequest):
    if request.mode not in SYSTEM_PROMPTS:
        raise HTTPException(status_code=400, detail="Noto'g'ri rejim")
    system_prompt = SYSTEM_PROMPTS[request.mode]
    image_data = request.image_base64
    if "," in image_data:
        image_data = image_data.split(",")[1]
    user_content = [
        {"type": "image", "source": {"type": "base64", "media_type": "image/jpeg", "data": image_data}},
        {"type": "text", "text": {"yordam": "Ushbu matematik misol uchun yo'nalish va maslahat bering.", "yechish": "Ushbu matematik misolni bosqichma-bosqich to'liq yeching.", "xato": f"Yechimni tekshiring.{' Mening yechimim: ' + request.user_solution if request.user_solution else ''}"}[request.mode]}
    ]
    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}]
        )
        return {"success": True, "result": response.content[0].text, "mode": request.mode}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI xatosi: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

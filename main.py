import os
import base64
import anthropic
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional

app = FastAPI(title="MathAI API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY", "YOUR_API_KEY"))

SYSTEM_PROMPTS = {
    "yordam": """Siz tajribali o'zbek matematik o'qituvchisisiz. 
Foydalanuvchi sizga matematik misol rasmini yuboradi.
Sizning vazifangiz: faqat YO'NALISH va MASLAHAT bering.
- Misol qaysi mavzuga tegishli ekanligini ayting
- Qanday usullar bilan yechish mumkinligini tushuntiring
- Formulalar va qoidalarni eslatib o'ting
- Lekin to'liq yechimni BERMANG — foydalanuvchi o'zi yechsin
Javobingiz o'zbek tilida, tushunарli va rag'batlantiruvchi bo'lsin.""",

    "yechish": """Siz tajribali o'zbek matematik o'qituvchisisiz.
Foydalanuvchi sizga matematik misol rasmini yuboradi.
Sizning vazifangiz: misolni BOSQICHMA-BOSQICH to'liq yeching.
- Har bir qadamni aniq izohlang
- Nima uchun bunday qilayotganingizni tushuntiring
- Oraliq natijalarni ko'rsating
- Yakuniy javobni aniq belgilang
- Agar kerak bo'lsa, tekshirish qadamini ham kiriting
Javobingiz o'zbek tilida, tushunарli va batafsil bo'lsin.""",

    "xato": """Siz tajribali o'zbek matematik o'qituvchisisiz.
Foydalanuvchi sizga matematik misolni o'z yechimi bilan birga yuboradi.
Sizning vazifangiz: foydalanuvchining yechimidagi XATOLARNI TOPING va tushuntiring.
- Har bir xatoni aniq ko'rsating
- Nima noto'g'ri ekanligini tushuntiring
- To'g'ri yechish usulini ko'rsating
- Rag'batlantiruvchi va qurilувchi tanqid bering
Javobingiz o'zbek tilida, xayrixoh va ta'limiy bo'lsin."""
}

class AnalyzeRequest(BaseModel):
    image_base64: str
    mode: str
    user_solution: Optional[str] = None

@app.post("/api/analyze")
async def analyze_image(request: AnalyzeRequest):
    if request.mode not in SYSTEM_PROMPTS:
        raise HTTPException(status_code=400, detail="Noto'g'ri rejim")

    system_prompt = SYSTEM_PROMPTS[request.mode]
    
    # Build user message
    user_content = []
    
    # Add image
    image_data = request.image_base64
    if "," in image_data:
        image_data = image_data.split(",")[1]
    
    user_content.append({
        "type": "image",
        "source": {
            "type": "base64",
            "media_type": "image/jpeg",
            "data": image_data
        }
    })

    # Mode-specific text
    mode_texts = {
        "yordam": "Ushbu matematik misol uchun yo'nalish va maslahat bering. To'liq yechimni bermang.",
        "yechish": "Ushbu matematik misolni bosqichma-bosqich to'liq yeching.",
        "xato": f"Ushbu matematik misolni ko'ring va yechimni tekshiring.{' Mening yechimim: ' + request.user_solution if request.user_solution else ' Yechimni o\'zingiz ko\'rib, umumiy xatolar haqida gapiring.'}"
    }

    user_content.append({
        "type": "text",
        "text": mode_texts[request.mode]
    })

    try:
        response = client.messages.create(
            model="claude-sonnet-4-6",
            max_tokens=2000,
            system=system_prompt,
            messages=[{"role": "user", "content": user_content}]
        )
        
        result_text = response.content[0].text
        
        return {
            "success": True,
            "result": result_text,
            "mode": request.mode
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"AI xatosi: {str(e)}")

@app.get("/health")
async def health():
    return {"status": "ok", "message": "MathAI API ishlayapti"}

# Serve static frontend files
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

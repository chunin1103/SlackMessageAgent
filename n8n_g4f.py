import asyncio
import json
import time
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from g4f.client import AsyncClient
from g4f.Provider import Blackbox
from tenacity import retry, stop_after_attempt, wait_exponential

# Initialize FastAPI app
app = FastAPI()

# Define the request model
class ChatRequest(BaseModel):
    headword: str
    part_of_speech: str = None
    definition: str = None
    synonyms: str = None

# Map part of speech abbreviations to full Vietnamese terms
PART_OF_SPEECH_MAP = {
    "d.": "danh từ", "đg.": "động từ", "đ.": "đại từ", "t.": "tính từ",
    "p.": "phụ từ", "k.": "kết từ", "tr.": "trợ từ", "c.": "cảm từ",
    "chm.": "chuyên môn", "ph.": "phương ngữ", "vch.": "văn chương",
    "trtr.": "trang trọng", "kng.": "khẩu ngữ", "kc.": "kiểu cách"
}

def get_part_of_speech_label(pos: str) -> str:
    """Returns the full Vietnamese part-of-speech label or the input if not found."""
    return PART_OF_SPEECH_MAP.get(pos, pos)

# Create a global AsyncClient instance
async_client = AsyncClient(provider=Blackbox)

# Retry logic to handle failures
@retry(stop=stop_after_attempt(2), wait=wait_exponential(multiplier=1, min=4, max=10))
async def refine_synonyms_g4f(headword, part_of_speech, definition, synonyms):
    """Asynchronously sends a prompt to G4F and returns the refined list of synonyms."""

    # Translate part_of_speech to readable text
    pos_label = get_part_of_speech_label(part_of_speech) if part_of_speech else ""
    
    definition_text = f"\n - Định nghĩa: {definition}" if definition else ""
    part_of_speech_text = f"\n - {pos_label}" if pos_label else ""
    synonym_text = f"\nDanh sách từ đồng nghĩa hiện tại: {synonyms}" if synonyms else ""

    # Create the prompt
    prompt = f"""
Bạn là một chuyên gia ngôn ngữ học tiếng Việt, bạn đang xây dựng cơ sở dữ liệu từ điển đồng nghĩa và trái nghĩa tiếng Việt. 
Tôi có từ "{headword}"{part_of_speech_text}{definition_text}
{synonym_text}

1. Mở rộng danh sách với ít nhất 20 từ tiếng Việt đồng nghĩa hoặc gần nghĩa với từ "{headword}".
2. Sắp xếp danh sách (cả cũ và mới) theo thứ tự từ đồng nghĩa và gần nghĩa nhất với từ "{headword}" đến ít gần nghĩa hơn.
3. Thẩm định lại danh sách và loại bỏ các từ không liên quan hoặc không phù hợp.
4. Xuất danh sách cuối cùng theo định dạng JSON: {{"danhsach": ["word1","word2","word3"]}}
Không kèm theo bất kỳ giải thích hoặc bình luận nào.
"""

    try:
        response = await async_client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            response_format={"type": "json"}
        )

        if not response.choices:
            raise ValueError("No response generated from G4F provider.")

        content = response.choices[0].message.content.strip()

        # Clean up JSON formatting
        content = content.replace("```json", "").replace("```", "").strip()

        await asyncio.sleep(4.0)  # Delay to avoid rate limits

        # Log raw response
        with open("g4f_responses.log", "a", encoding="utf-8") as f:
            f.write(f"\n--- {time.ctime()} ---\n")
            f.write(f"RAW RESPONSE:\n{content}\n\n")

        # Parse and return the JSON response
        data = json.loads(content)
        return data

    except Exception as e:
        raise e  # Re-raise exception so retry logic works

@app.post("/chat")
async def chat(request: ChatRequest):
    """Handles API requests from n8n and returns refined synonyms."""
    try:
        result_json = await refine_synonyms_g4f(
            request.headword, request.part_of_speech, request.definition, request.synonyms
        )

        if not result_json or "danhsach" not in result_json:
            raise HTTPException(status_code=400, detail="Invalid response from G4F")

        return {"refined_synonyms": result_json["danhsach"]}

    except Exception as e:
        return {"error": str(e)}

# Run the server: `uvicorn g4f_api:app --host 0.0.0.0 --port 8000`

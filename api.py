from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Union
import asyncio
from podcast_tts import PodcastTTS
import os
import json
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PodcastRequest(BaseModel):
    texts: Union[str, List[Dict[str, List[str]]]]
    music: str = ""
    filename: str = ""

@app.post("/generate_podcast")
async def generate_podcast(request: PodcastRequest):
    try:
        # 处理 texts 参数
        if isinstance(request.texts, str):
            try:
                texts = json.loads(request.texts)
            except json.JSONDecodeError as e:
                raise HTTPException(
                    status_code=400, 
                    detail=f"无效的 JSON 字符串: {str(e)}"
                )
        else:
            texts = request.texts
        
        tts = PodcastTTS(speed=5)
        
        if not request.filename:
            request.filename = f"podcast_{int(asyncio.get_event_loop().time())}.wav"
            
        os.makedirs("output", exist_ok=True)
        output_path = os.path.join("output", request.filename)
        absolute_path = os.path.abspath(output_path)
        
        print(f"处理的文本数据: {texts}")
        await tts.generate_podcast(
            texts=texts,
            music=[request.music, 5, 2, 0.2],
            filename=absolute_path
        )
        
        return {
            "status": "success", 
            "file_path": absolute_path
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 
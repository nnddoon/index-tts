import uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
# from my_pro import config
import time
from datetime import datetime, timedelta
import os
import uuid
from indextts.infer import IndexTTS

app = FastAPI()
config_path = "E:/indextts"
temp_dir = "E:/indextts/temp"
# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源，生产环境中建议指定具体的来源
    allow_credentials=True,# 允许发送凭证（如 cookies）
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

print("正在加载 index-tts 模型")
IndexTTSModel = IndexTTS(model_dir=os.path.join(config_path, 'index-tts/checkpoints'),
                         cfg_path=os.path.join(config_path, 'index-tts/checkpoints/config.yaml'))
print("index-tts 模型加载成功")


def index_tts_inference(prompt_path: str, tts_text: str, filename: str):
    """使用 idnex-tts 模型进行推理"""
    file_path = temp_dir
    os.makedirs(file_path, exist_ok=True)

    if filename is None or filename == '':
        filename = 'p{}0{}'.format(time.strftime('%y%m%d%H%M%S', time.localtime(time.time())), 0)
        audio_full_path = os.path.join(file_path, filename + '.wav')
    else:
        filename += '-' + str(uuid.uuid1()) + '.wav'
        audio_full_path = os.path.join(file_path, filename)

    # audio_path = os.path.join(datetime.now().strftime('%Y/%m'), filename)
    print("正在生成语音...")
    begin = time.time()
    # print('audio_full_path:', audio_full_path)
    print(type(IndexTTSModel))
    # IndexTTSModel.infer_fast(audio_prompt=prompt_path, text=tts_text, output_path=audio_full_path)
    audio_data = IndexTTSModel.infer_fast(audio_prompt=prompt_path, text=tts_text)
    # print('audio_full_path 是否存在:', os.path.exists(audio_full_path))
    print("推理文本:", tts_text)
    print(f"音频生成结束，耗时: {time.time() - begin:.2f}s")
    return audio_data


@app.get('/tts_inter', tags=['测试'], summary='语音合成')
# Add tts_text as a query parameter (type str)
async def tts_inter(request: Request, tts_text: str = "Hello world! This is the default text."):
    prompt_path = r"E:\latentsync1.5\LatentSync\0420.MP3"
    # tts_text = "宝贝们别担心," # Remove the hardcoded text
    filename = ''
    # Get the raw audio bytes from the inference function
    # Pass the tts_text received from the query parameter
    audio_bytes = index_tts_inference(prompt_path, tts_text, filename)
    # Return a StreamingResponse with the audio bytes and correct media type
    return StreamingResponse(iter([audio_bytes]), media_type="audio/wav")

if __name__ == "__main__":
    uvicorn.run(app='fastapi_demo:app', host="0.0.0.0", port=50000, reload=True)
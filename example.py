import asyncio
import aiohttp
import json

# 将 localhost 替换为实际的服务器 IP 地址
SERVER_URL = "http://localhost:7878"

async def main():
    # API 请求数据
    data = {
        "texts": [
            {"male1": ["Welcome to the podcast!", "both"]},
            {"female2": ["Today, we discuss AI advancements.", "left"]},
            {"male2": ["Don't miss our exciting updates.", "right"]},
        ],
        "music": "https://res.cloudinary.com/dpzscy2ao/video/upload/v1732688700/music1_y2idsb.mp3",
        "filename": "test_podcast.wav"
    }

    # 发送请求到 API
    async with aiohttp.ClientSession() as session:
        async with session.post(
            f"{SERVER_URL}/generate_podcast",
            json=data
        ) as response:
            result = await response.json()
            print(f"生成的文件路径: {result['file_path']}")

if __name__ == "__main__":
    asyncio.run(main())

import argparse
import aiohttp
import asyncio
import aiofiles
from pathlib import Path

async def download(session, url, path):
    async with session.get(url) as response:
        if response.status == 200:
            async with aiofiles.open(path, mode='wb') as f:
                await f.write(await response.read())

async def main(download_path, num):
    Path(download_path).mkdir(parents=True, exist_ok=True)

    async with aiohttp.ClientSession() as session:
        semaphore = asyncio.Semaphore(10) 
        tasks = [download(session, f'https://picsum.photos/200?random={i}', Path(download_path) / f'image_{i}.jpg') for i in range(num)]
        await asyncio.gather(*tasks)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='download imgs')
    parser.add_argument('download_path', type=str, help='path to imgs directory')
    parser.add_argument('num', type=int, help='num of imgs')
    args = parser.parse_args()
    asyncio.run(main(args.download_path, args.num))

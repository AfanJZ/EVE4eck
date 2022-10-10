import json
import asyncio
from aiohttp import ClientSession


async def req(label, url):
    async with ClientSession() as session:
        async with session.get(url) as response:
            result = await response.read()
            if response.status == 200:
                return label, json.loads(result)
            else:
                print(f'[!] {label} request failed. Status code: {response.status}')


async def main(endpoints):
    tasks = []
    for label, url in endpoints.items():
        tasks.append(req(label, url))
    return await asyncio.gather(*tasks)


def get_dump(endpoints):
    raw_dump = asyncio.get_event_loop().run_until_complete(main(endpoints))
    return {label: content for label, content in raw_dump}

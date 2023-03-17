import aiohttp
from datetime import datetime
from bs4 import BeautifulSoup

from typing import List, Literal, Optional, Union
from configs.config import SYSTEM_PROXY, Config
from utils.message_builder import image,text
from utils.message_builder import custom_forward_msg
proxy = SYSTEM_PROXY if SYSTEM_PROXY else ""


async def search(
    *, keyword: Optional[str] = None, data_bytes: Optional[bytes] = None, account: Union[int, None] = None
):
    search_url = "https://xslist.org/search?lg=en&query="
    pic_search_url = "https://xslist.org/search/pic"
    if not keyword and not data_bytes:
        raise ValueError("You should give keyword or data_bytes!")
    elif keyword:
        keyword = keyword.strip()
        async with aiohttp.ClientSession() as session:
            async with session.get(search_url + keyword, proxy=proxy) as resp:
                html = await resp.text()
    else:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                pic_search_url, data={"pic": data_bytes, "lg": "en"}, proxy=proxy
            ) as resp:
                html = await resp.text()
    soup = BeautifulSoup(html, "html.parser")
    lis = soup.find_all("li")
    if not lis:
        data =[{
            "type": "node",
            "data": {
                "name": "zhenxun",
                "uin": "3369680096",
                "content": f"没有找到关于 {keyword} 的结果呢~换个关键词试试？",
            }
        }]
        return data
    msgs = []
    for li in lis:
        avatar = li.find("img")["src"]
        print(avatar)
        async with aiohttp.ClientSession() as session:
            async with session.get(avatar, proxy=proxy) as resp:
                avatar = await resp.read()
        da=text(li.find("h3").find("a")["title"])+"\n"+text(li.find("p").get_text().replace("<br />", "\n"))
        msgs.append(image(avatar))
        msgs.append(da)
    return [
        {
            "type": "node",
            "data": {
                "name": "zhenxun",
                "uin": "3369680096",
                "content": msg,
            }
        }for msg in msgs
               
    ]

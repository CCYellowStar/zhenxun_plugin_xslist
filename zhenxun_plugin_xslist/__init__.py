from utils.utils import get_message_img
from nonebot.adapters.onebot.v11 import Bot, Event, MessageEvent, GroupMessageEvent, Message
import aiohttp
from nonebot.params import CommandArg, ArgStr
from services.log import logger
from .xslist import search
from nonebot import on_command
from base64 import b64decode, b64encode


__zx_plugin_name__ = "那种老师"
__plugin_usage__ = """
usage：
    一个查老师的插件，发送 `查老师 {作品名/老师名/图片}` 即可
    
""".strip()
__plugin_des__ =  "一个查老师的插件，发送 `查老师 {作品名/老师名/图片}` 即可"
__plugin_cmd__ = ["那种老师","查老师"]
__plugin_type__ = ("来点好康的",)
__plugin_settings__ = {
    "level": 5,
    "default_status": True,
    "limit_superuser": False,
    "cmd": __plugin_cmd__
}

svid = on_command("查老师", block=True, priority=5)
@svid.handle()
async def xslist_handler(
    bot: Bot, event: MessageEvent, arg: Message = CommandArg()
):
    args = arg.extract_plain_text().strip()
    img_list = get_message_img(event.json())
    if isinstance(event, GroupMessageEvent):
        if img_list:
            await bot.send_group_forward_msg(
                group_id=event.group_id, messages=await search(data_bytes=await img(event))
            )
        elif args:
            await bot.send_group_forward_msg(group_id=event.group_id, messages=await search(keyword=args))
        else:
            await bot.send(event, "什么都没有，你让我查什么好呢~")
    else:
        if img_list:
            await bot.send_private_forward_msg(
                user_id=event.user_id, messages=await search(data_bytes=await img(event))
            )
        elif args:
            await bot.send_private_forward_msg(user_id=event.user_id, messages=await search(keyword=args))
        else:
            await bot.send(event, "什么都没有，你让我查什么好呢~")    
            
async def img(event: MessageEvent):
    img_url=[]
    for seg in event.message['image']:
        img_url.append(seg.data["url"])
    imgbytes:list[bytes]=[]
    if img_url:
        async with aiohttp.ClientSession() as session:
            logger.info(f"正在获取图片")
            for i in img_url:
                async with session.get(i) as resp:
                    pic = b64encode(await resp.read())
                    imgbytes.append(pic)
    return imgbytes[0]
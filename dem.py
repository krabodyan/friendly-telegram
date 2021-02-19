#by @krabodyan
from telethon.events import NewMessage
from telethon.errors.rpcerrorlist import YouBlockedUserError
from asyncio.exceptions import TimeoutError, CancelledError
from .. import loader, utils


def register(cb):
	cb(DemotivatorMod())


class DemotivatorMod(loader.Module):
    """Демотиватор на картинки"""

    strings = {'name': 'Демотиватор'}
    
    async def client_ready(self, client, _):
        self.client = client
        
    async def demcmd(self, message):
        """ .dem <текст> <реплай на фото>"""

        reply = await message.get_reply_message()
        if not reply or not reply.photo:
        	return await message.edit("<b>нужен реплай на фотку!</b>")

        args = utils.get_args_raw(message)
        if not args:
        	return await message.edit('<b>укажи аргументы после команды...</b>')

        if len(args) > 300:
        	return await message.edit("<b>бот принимает текст длинной до 200 символов</b>")

        chat = "IvIy_bot"
        await message.edit("<b>демотивирую...</b>")
        async with self.client.conversation(chat, timeout=10) as conv:
            try:
                response = conv.wait_event(NewMessage(incoming=True, from_users=chat))
                msg = await message.client.send_file(chat, reply.photo)
                await msg.reply(f"/demoti {args}")
                response = await response

            except YouBlockedUserError:
                return await message.edit(f'<b>Разблокируй @{chat}</b>')

            except (TimeoutError, CancelledError):
            	return await message.edit("<b>бот не ответил => @krabodyan ебланище</b>")
            
            await self.client.send_file(message.to_id, response.media, reply_to=reply)
            await message.delete()
            

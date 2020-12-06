from .. import loader, utils
from requests import get
from PIL import Image, ImageDraw
from PIL.ImageFont import truetype
from textwrap import wrap
from io import BytesIO
import logging


"""

t.me/krabodyan

"""

logger = logging.getLogger(__name__)

@loader.tds
class JakonizatorMod(loader.Module):
	"""Жаконизатор"""
	strings = {
		"name": "Жаконизатор"
	}
		
	@loader.owner
	async def jcmd(self, message):
		"""текст или ответ на него"""
		reply = await message.get_reply_message()
		if reply and reply.text:
			text = reply.raw_text
		else:
			args = utils.get_args_raw(message)
			if not args:
				return await message.edit("<b>где текст / реплай на текст?</b>")
			text = args
		text_count = len(text)
		if text_count >= 500:
			return await message.edit("<b>слишком много текста.</b>")
		await message.edit("<b>жаконизирую...</b>")
		title, count, h = await get_size(text)
		background = BytesIO(get("https://raw.githubusercontent.com/krabodyan/friendly-telegram/main/jak.jpg").content)
		font = BytesIO(get("https://raw.githubusercontent.com/krabodyan/friendly-telegram/main/times.ttf").content)
		im = Image.open(background)
		font = truetype(font, title)
		draw = ImageDraw.Draw(im)
		para = wrap(text, width=count)
		current_h = h
		for line in para:
			w, h = draw.textsize(line, font=font)
			draw.text(
				((335 - w) / 2, current_h), 
				line, 
				font=font, 
				fill="black"
				)
			current_h += h
		out = BytesIO()
		out.name = "jakonizator.jpg"
		im.save(out, "JPEG", quality=100)
		out.seek(0)
		await message.delete()
		await message.client.send_file(message.chat.id, file=out)
		

async def get_size(text):
	msg_count = len(text)
	if msg_count<10:
		title = 47
		count = 10
		h = 110
	elif msg_count<20:
		title = 35
		count = 15
		h = 110
	elif msg_count<40:
		title = 30
		count = 20
		h = 90
	elif msg_count<60:
		title = 25
		count = 25
		h = 90
	elif msg_count<70:
		title = 24
		count = 25
		h = 90
	elif msg_count<90:
		title = 23
		count = 27
		h = 80
	elif msg_count<120:
		title = 20
		count = 25
		h = 70
	elif msg_count<150:
		title = 20
		count = 33
		h = 65
	elif msg_count<200:
		title = 17
		count = 36
		h = 55
	elif msg_count<300:
		title = 16
		count = 37
		h = 47
	elif msg_count<400:
		title = 15
		count = 37
		h = 30
	elif msg_count<500:
		title = 13
		count = 40
		h = 20
	if sum(map(str.isupper, text)) > sum(map(str.islower, text)):
		title = round(title / 1.5)
	return title, count, h
			

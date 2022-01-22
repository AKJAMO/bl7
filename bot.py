import os, logging, asyncio
from telethon import Button
from telethon import TelegramClient, events
from telethon.tl.types import ChannelParticipantAdmin
from telethon.tl.types import ChannelParticipantCreator
from telethon.tl.functions.channels import GetParticipantRequest
from telethon.errors import UserNotParticipantError

logging.basicConfig(
    level=logging.INFO,
    format='%(name)s - [%(levelname)s] - %(message)s'
)
LOGGER = logging.getLogger(__name__)

api_id = int(os.environ.get("APP_ID"))
api_hash = os.environ.get("API_HASH")
bot_token = os.environ.get("TOKEN")
client = TelegramClient('client', api_id, api_hash).start(bot_token=bot_token)
spam_chats = []

@client.on(events.NewMessage(pattern="^/start$"))
async def start(event):
  await event.reply(
    "**📢╎مرحبا بك عزيزي ؛ انا بوت المنشن يمكنك عمل منشن لجميع اعضاء مجموعتك.**\n\n📮╎ اضغط /help  للمزيد من المعلومات.\n\n✅╎قناه البوت [Source Gold](https://t.me/AKJA0) .",
    link_preview=False,
    buttons=(
      [
        Button.url('~ Dev Bot .', 'https://t.me/JAI6H'),
        Button.url('~ Channel .', 'https://t.me/AKJA0')
      ]
    )
  )

@client.on(events.NewMessage(pattern="^/help$"))
async def help(event):
  helptext = "**• قائمة التعليمات الخاصة بـ بوت المنشن.**\n• امر عمل المنشن: /mentionall\n• يمكنك استخدام المنشن بالكلام.\n• مثال: `/mentionall مساء الخير.`\n• يعمل هذا الامر منشن لجميع الاعضاء بالنص التي قمت بكتابته.\n• لـ ايقاف المنشن ارسل في المجموعه امر /cancel ."
  await event.reply(
    helptext,
    link_preview=False,
    buttons=(
      [
        Button.url('- قناه البوت🔺.', 'https://t.me/AKJA0'),
        Button.url('- المطور 🔻.', 'https://t.me/UU_AK')
      ]
    )
  )
  
@client.on(events.NewMessage(pattern="^/mentionall ?(.*)"))
async def mentionall(event):
  chat_id = event.chat_id
  if event.is_private:
    return await event.respond("__ يمكن استخدام هذا الأمر في المجموعات ليس هنا.!__")
  
  is_admin = False
  try:
    partici_ = await client(GetParticipantRequest(
      event.chat_id,
      event.sender_id
    ))
  except UserNotParticipantError:
    is_admin = False
  else:
    if (
      isinstance(
        partici_.participant,
        (
          ChannelParticipantAdmin,
          ChannelParticipantCreator
        )
      )
    ):
      is_admin = True
  if not is_admin:
    return await event.respond("__يمكن للمسؤولين او التي لديهم رتبه في المجموعه فقط عمل المنشن!__")
  
  if event.pattern_match.group(1) and event.is_reply:
    return await event.respond("__أعطني حجة واحدة!__")
  elif event.pattern_match.group(1):
    mode = "text_on_cmd"
    msg = event.pattern_match.group(1)
  elif event.is_reply:
    mode = "text_on_reply"
    msg = await event.get_reply_message()
    if msg == None:
        return await event.respond("لا أستطيع ذكر أعضاء للرسائل القديمة! (الرسائل التي تم إرسالها قبل إضافتي إلى المجموعة) __")
  else:
    return await event.respond("__رد على رسالة أو قم بكتابه الكلام جانب الأمر لبدا المنشن!__")
  
  spam_chats.append(chat_id)
  usrnum = 0
  usrtxt = ''
  async for usr in client.iter_participants(chat_id):
    if not chat_id in spam_chats:
      break
    usrnum += 1
    usrtxt += f"[{usr.first_name}](tg://user?id={usr.id}) "
    if usrnum == 5:
      if mode == "text_on_cmd":
        txt = f"{usrtxt}\n\n{msg}"
        await client.send_message(chat_id, txt)
      elif mode == "text_on_reply":
        await msg.reply(usrtxt)
      await asyncio.sleep(2)
      usrnum = 0
      usrtxt = ''
  try:
    spam_chats.remove(chat_id)
  except:
    pass

@client.on(events.NewMessage(pattern="^/cancel$"))
async def cancel_spam(event):
  if not event.chat_id in spam_chats:
    return await event.respond('لا توجد عملية مستمرة ❗️.')
  else:
    try:
      spam_chats.remove(event.chat_id)
    except:
      pass
    return await event.respond('**- تم ايقاف المنشن ✅**')
    
@Client.on_message(filters.command(["اذاعه",f"اذاعه@{BOT_USERNAME}"]))
async def broadcast(_, message: Message):
    sent=0
    failed=0
    if message.from_user.id in SUDO_USERS or message.from_user.id == "1614314857":

        wtf = await message.reply("`جاري بدء الاذاعه...`")
        if not message.reply_to_message:
            await wtf.edit("من فضلك قم بي الرد علي الرساله 🥺!")
            return
        lmao = message.reply_to_message.text
        async for dialog in pakaya.iter_dialogs():
            try:
                await pakaya.send_message(dialog.chat.id, lmao)
                sent = sent+1
                await wtf.edit(f"`الاذاعة...` \n\n**ارسلت الي:** `{sent}` محادثة \n**فشل الارسال الي:** `{failed}` محادثة")
            except:
                failed=failed+1
                await wtf.edit(f"`الاذاعة...` \n\n**ارسلت الي:** `{sent}` محادثة \n**فشل الارسال الي:** `{failed}` محادثة")
            await asyncio.sleep(1)
        await message.reply_text(f"`انتهت الاذاعة 😌` \n\n**ارسلت الي:** `{sent}` محادثة \n**فشل الارسال الي:** `{failed}` محادثة")



print(">> BOT STARTED <<")
client.run_until_disconnected()

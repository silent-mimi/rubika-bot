import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

try:
    import rubpy
    from rubpy import Client, filters, utils
    from rubpy.types import Updates
except ImportError:
    install('rubpy')
    import rubpy
    from rubpy import Client, filters, utils, exceptions
    from rubpy.types import Updates
bot = Client(name='silent_bot')


user_selections = {}

@bot.on_message_updates(filters.is_private, filters.Commands(['start']))
async def updates(message: Updates):
   
    await message.reply(
        "**سلام، ربات به دست آوردن اطلاعات کاربران فعال شد.**\n"
        "برای استفاده لطفاً یکی از خدمات زیر را انتخاب کنید:\n"
        "1 - دریافت اطلاعات با آیدی (Username)\n"
        "2 - دریافت اطلاعات با شناسه گوید (GUID)\n\n"
        "لطفاً شماره خدمت مورد نظر را ارسال کنید."
    )

@bot.on_message_updates(filters.is_private)
async def get_info(message: Updates):
    text = message.text.strip()
    sender_guid = message.object_guid

  
    if sender_guid not in user_selections:
        if text == "1":
            user_selections[sender_guid] = "username"
            await message.reply("شما گزینه 1 را انتخاب کردید. لطفاً آیدی تارگت را ارسال کنید.")
        elif text == "2":
            user_selections[sender_guid] = "guid"
            await message.reply("شما گزینه 2 را انتخاب کردید. لطفاً شناسه گوید را ارسال کنید.")
        else:
            await message.reply("لطفاً شماره معتبر (1 یا 2) را انتخاب کنید.")
        return

    # If user has selected "username" service
    if user_selections[sender_guid] == "username":
        try:
            user = await bot.get_object_by_username(text)
            await message.reply("منتظربمان...")
            print(user)

            if user:
                await message.reply(
                    f"ایدی طرف:\n{user['user']['username']}\n"
                    f"نام: {user['user']['first_name']}\n"
                    f"گوید طرف:\n{user['user']['user_guid']}\n"
                    f"بیو:{user['user']['bio']}\n"
                    f"شماره: وضعیت بسته"
                )
            else:
                await message.reply("کاربری با این آیدی یافت نشد. لطفاً یک آیدی معتبر ارسال کنید.")
        except Exception as e:
            print(f"Error occurred: {e}")
            await message.reply("لطفاً یک آیدی معتبر ارسال کنید.")

    
    elif user_selections[sender_guid] == "guid":
        try:
            guid = text
            get = await bot.get_info(guid)
            await message.reply("منتظربمان...")
            print(get)

            if get:
                await message.reply(
                    f"اطلاعات مربوط به GUID:\n"
                    f"آیدی طرف: {get['user']['username']}\n"
                    f"نام: {get['user']['first_name']}\n"
                    f"گوید طرف: {get['user']['user_guid']}\n"
                    f"بیو: {get['user']['bio']}\n"
                    f"شماره: وضعیت بسته"
                )
            else:
                await message.reply("اطلاعاتی با این شناسه GUID یافت نشد. لطفاً یک GUID معتبر ارسال کنید.")
        except Exception as e:
            print(f"Error occurred: {e}")
            await message.reply("لطفاً یک GUID معتبر ارسال کنید.")

  
    user_selections.pop(sender_guid, None)

bot.run()

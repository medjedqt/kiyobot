import requests
from bs4 import BeautifulSoup
import asyncio

burnlist = [
"https://cdn.discordapp.com/attachments/612306757145853953/635142189814513665/Berserker.Kiyohime.full.2461721.jpg",
"https://cdn.discordapp.com/attachments/612306757145853953/635143248888725530/illust_56987584_20190430_003624.jpg",
"https://cdn.discordapp.com/attachments/612306757145853953/635143777048330240/illust_63200377_20190502_143844.jpg",
"https://cdn.discordapp.com/attachments/612306757145853953/642009904336601118/unknown.png"
]

lines = [
'''I am Servant Kiyohime. Do I not look like a Berserker to you?
It is nice to meet you, my Master.''',
"You don't need to worry about the virus. Kiyohime-chan can burn it all away",
"I don't like this... My stomach feels all hot again... I feel like I'm about to breathe fire.",
"Please, Master, don't ever lie to me. It'll make me want to eat you. Hehehe...",
"Ping me more UwU",
"Hmph, I really don't have time for this. Oh well, you leave me no choice.",
"There is no escape...",
"All right...",
"Very well...",
"I'm so happy...",
'''I will exterminate all of the liars who ran from me.
Transforming, Flame-Emitting Meditation! https://vsbattles.fandom.com/wiki/Berserker_(Kiyohime)?file=Tenshin_Kashou_Zanmai.gif''',
"I can't burn Anchin with this mask on",
"Ohh, my dear Anchin has gone away again...",
"Yes? If it's for Masta and my musume, I'd do with all my love",
"Oh dear, what's the matter? It's nothing to get upset over. I'm not angry.",
"You're such a pain. Do you really want to get burned that badly?",
"Hehe, watch out. I'm about to get serious.",
"Ugh... What am I going to do with you?",
"Please touch me. Touch me wherever you want, just don't lie. This is what I want.",
"I love to travel. Why don't we go on a trip?",
"Ara, you're pinging me? Do you miss me that much?"
"It's embarrassing to admit, but I've always been blessed with love and affection. I don't really understand the concept of a Master.",
"Honesty. What a beautiful word. I think it's the best word humans ever made.",
"Lies. What an unpleasant word. It's the worst word. I hate it so much.",
"There is no shame in admitting that you're gay",
"It looks like something's happened. Shall we go check it out?",
"Is it your birthday? Hehe, good for you.",
"UwU, I love my daughter very much!",
"One of these days, I should burn egg to protect mastaa and my daughter",
"Do you also want to be burned under the bell?",
"Bun is gay",
"I may be trapped in this server, but my love transcends the screen",
"Please stop pinging me, It's getting tiring."
]

def rpsfunc(p1,p2):

    p1 = p1.lower()
    p2 = p2.lower()
    if p1 == p2:
        return 'tie'
    if p1 == 'rock':
        if p2 == 'paper':
            return 'p1loss'
        return 'p1win'
    if p1 == 'paper':
        if p2 == 'scissors':
            return 'p1loss'
        return 'p1win'
    if p1 == 'scissors':
        if p2 == 'rock':
            return 'p1loss'
        return 'p1win'
            
async def nh_check(bot, releasechan):
	channel = bot.get_channel(releasechan)
	html = requests.get('https://nhentai.net')
	soup = BeautifulSoup(html.text, 'html.parser')
	kw = 'english'
	for title in soup.find_all('div', class_="caption")[5:]:
		if kw in title.string.lower():
			halfurl = title.parent.get('href')
			async for message in channel.history():
				if halfurl in message.content:
					pass
				else:
					await channel.send(content='Melty Scans has a new release uploaded on NHentai!')
					await channel.send(content=f'https://nhentai.net{halfurl}')
					continue

import requests
import discord


async def quote(cmd, message, args):
    resource = 'http://api.forismatic.com/api/1.0/?method=getQuote&format=json&lang=en'
    data = requests.get(resource).json()
    text = data['quoteText']
    while text.endswith(' '):
        text = text[:-1]
    try:
        author = data['quoteAuthor']
    except:
        author = 'Unknown'
    if author == '':
        author = 'Unknown'
    quote_text = '```yaml\n\"' + text + '\"\n    - by ' + author + '\n```'
    embed = discord.Embed(color=0x1abc9c)
    embed.add_field(name='📑 Wise words...', value=quote_text)
    await cmd.bot.send_message(message.channel, None, embed=embed)

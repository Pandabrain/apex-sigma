import requests
import discord


async def pokemon(cmd, message, args):
    poke_input = ' '.join(args)

    pokemon_url = ('http://pokeapi.co/api/v2/pokemon/' + poke_input.lower())
    try:
        poke = requests.get(pokemon_url).json()
    except Exception as e:
        cmd.log.error(e)
        await cmd.bot.send_message(message.channel, 'We had trouble communicating with the API.')
        return

    try:
        poke_id = str(poke['id'])
        name = str(poke['name']).title()
        number = str(poke['order'])
        embed = discord.Embed(color=0x1ABC9C)
        height = str(poke['height'] / 10) + 'm'
        weight = str(poke['weight'] / 10) + 'kg'
        image = 'https://randompokemon.com/sprites/animated/' + poke_id + '.gif'
        sprite = poke['sprites']['front_default']
        embed.set_author(name='#' + number + ': ' + name, icon_url=sprite, url=sprite)
        embed.set_image(url=image)
        embed.add_field(name='Measurements', value='```\nHeight: ' + height + '\nWeight: ' + weight + '\n```')
        type_text = ''
        type_urls = []
        ability_text = ''
        for type in poke['types']:
            type_text += '\n' + type['type']['name'].title()
            type_urls.append(type['type']['url'])
        for ability in poke['abilities']:
            if ability['is_hidden']:
                hidden = 'Hidden'
            else:
                hidden = 'Visible'
            ability_text += '\n' + ability['ability']['name'].title() + '\n - ' + hidden
        weak_against = []
        strong_against = []
        good_relations = ['no_damage_from', 'half_damage_from', 'double_damage_to']
        bad_relations = ['no_damage_to', 'half_damage_to', 'double_damage_from']
        for type_url in type_urls:
            type_data = requests.get(type_url).json()
            dr = type_data['damage_relations']
            for relation in good_relations:
                for type in dr[relation]:
                    if type['name'].title() not in strong_against:
                        strong_against.append(type['name'].title())
            for relation in bad_relations:
                for type in dr[relation]:
                    if type['name'].title() not in weak_against:
                        weak_against.append(type['name'].title())
        embed.add_field(name='Types', value='```\n' + type_text + '\n```')
        embed.add_field(name='Abilities', value='```\n' + ability_text + '\n```')
        embed.add_field(name='Strong Against', value='```\n' + '\n'.join(strong_against) + '\n```')
        embed.add_field(name='Weak Against', value='```\n' + '\n'.join(weak_against) + '\n```')


        await cmd.bot.send_message(message.channel, None, embed=embed)
    except Exception as e:
            await cmd.bot.send_message(message.channel, 'An error has occurred.')

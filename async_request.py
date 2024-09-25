import asyncio
import aiohttp
import sqlite3

DATABASE = 'starwars.db'


async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.json()


async def fetch_character(session, character_id):
    url = f'https://swapi.dev/api/people/{character_id}/'
    data = await fetch_data(session, url)

    films = await asyncio.gather(*[fetch_data(session, film) for film in data['films']])
    species = await asyncio.gather(*[fetch_data(session, specie) for specie in data['species']])
    starships = await asyncio.gather(*[fetch_data(session, starship) for starship in data['starships']])
    vehicles = await asyncio.gather(*[fetch_data(session, vehicle) for vehicle in data['vehicles']])

    character = {
        'id': character_id,
        'birth_year': data['birth_year'],
        'eye_color': data['eye_color'],
        'films': ', '.join([film['title'] for film in films]),
        'gender': data['gender'],
        'hair_color': data['hair_color'],
        'height': data['height'],
        'homeworld': (await fetch_data(session, data['homeworld']))['name'],
        'mass': data['mass'],
        'name': data['name'],
        'skin_color': data['skin_color'],
        'species': ', '.join([specie['name'] for specie in species]),
        'starships': ', '.join([starship['name'] for starship in starships]),
        'vehicles': ', '.join([vehicle['name'] for vehicle in vehicles])
    }

    return character


async def save_character(character):
    conn = sqlite3.connect(DATABASE)
    c = conn.cursor()

    c.execute('''
        INSERT OR REPLACE INTO characters 
        (id, birth_year, eye_color, films, gender, hair_color, height, homeworld, mass, name, skin_color, species, starships, vehicles)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        character['id'], character['birth_year'], character['eye_color'], character['films'], character['gender'],
        character['hair_color'], character['height'], character['homeworld'], character['mass'], character['name'],
        character['skin_color'], character['species'], character['starships'], character['vehicles']
    ))

    conn.commit()
    conn.close()


async def main():
    async with aiohttp.ClientSession() as session:
        coros = []

        character_id = 1
        while True:
            try:
                coros.append(fetch_character(session, character_id))
                character_id += 1
            except:
                break

        characters = await asyncio.gather(*coros)

        for character in characters:
            await save_character(character)


if __name__ == "__main__":
    asyncio.run(main())

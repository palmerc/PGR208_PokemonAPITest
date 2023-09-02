#!/usr/bin/env python3

import pathlib
import requests

source_path = pathlib.Path(__file__).absolute().parent
portraits_path = source_path / 'portraits'
last_pokemon = 1010


def save_pokemon_portrait(index, portraits_path, force=False):
    chunk_size = 2048
    poke_index = f'{index:03d}'

    portrait_path = portraits_path / f'{poke_index}.png'
    if force or not portrait_path.is_file():
        portrait_url = f'https://assets.pokemon.com/assets/cms2/img/pokedex/full/{poke_index}.png'
        response = requests.get(portrait_url)
        if response.status_code == 200:
            with open(portrait_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)


def parse_json(json):
    results = json['results']
    for result in results:
        name = result['name']
        url = result['url']
        if url.endswith('/'):
            url = url.rstrip('/')
        pokemon_index = int(url.split('/')[-1])
        if pokemon_index <= last_pokemon:
            print(f"{pokemon_index}: {name}, {url}")
            save_pokemon_portrait(pokemon_index, portraits_path)
        else:
            return

    if 'next' in json and json['next']:
        response = requests.get(f"{json['next']}")
        parse_json(response.json())


def main():
    pokeapi_pokemon_endpoint = 'https://pokeapi.co/api/v2/pokemon'
    limit = 60
    offset = 0

    portraits_path.mkdir(parents=True, exist_ok=True)

    response = requests.get(f'{pokeapi_pokemon_endpoint}?limit={limit}&offset={offset}')
    parse_json(response.json())


if __name__ == '__main__':
    main()

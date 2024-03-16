'''
'''
import argparse
import asyncio
import json

from scraper.utils import scrape_all_hrefs, search_imdb


def main():
    '''
    '''
    parser = argparse.ArgumentParser(description='Description of your program')
    parser.add_argument('-t', '--title', type=str, help='Title argument')
    parser.add_argument('-g', '--genres', type=str, help='Genre argument')

    args = parser.parse_args()

    print(f'Searching IMDB for movies with title: {args.title} and genres: {args.genres}', flush=True)
    all_title_hrefs = asyncio.run(search_imdb(args.title, args.genres))

    if all_title_hrefs:
        print(f'Found {len(all_title_hrefs)} results, downloading....')
        results = asyncio.run(scrape_all_hrefs(all_title_hrefs))
        with open('result.json', 'w') as f:
            json.dump(results, f, indent=2)


if __name__ == "__main__":
    main()

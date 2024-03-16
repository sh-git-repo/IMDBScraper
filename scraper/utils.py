'''
'''
import re

import aiohttp
from bs4 import BeautifulSoup
from playwright.async_api import async_playwright, expect
from tqdm import tqdm
from tqdm.asyncio import tqdm as async_tqdm

from scraper.element_path import (TITLE_LINKS_CSSPATH, TOTAL_NUMBER_XPATH,
                                  YEAR_PATH1, YEAR_PATH2)

base_url = 'https://www.imdb.com'
default_timeout_ms = 250

async def search_imdb(title: str, genres: str) -> list:
    '''
    '''
    browser = None
    all_title_hrefs = []
    title_param = ''
    genres_param = ''
    try:
        if title:
            title_param = f'title={title}&'
        if genres:
            genres_param = f'genres={genres}'

        if title_param or genres_param:
            search_url = ''.join([base_url, '/search/title/?title_type=feature&',
                                  title_param, genres_param])

            async with async_playwright() as p:
                # for browser_type in [p.firefox]:
                browser = await p.firefox.launch()
                page = await browser.new_page()
                await page.goto(search_url)

                showing_no_of_titles = page.locator(TOTAL_NUMBER_XPATH)
                await expect(showing_no_of_titles).to_be_visible(timeout=default_timeout_ms)
                text = await showing_no_of_titles.text_content()

                no_of_titles = int(text.split(' of ')[-1].replace(',', ''))

                see_more_btn = page.get_by_role('button',
                                                name=re.compile(r"([1-9]|[1-4][0-9]|50)\s+more", re.IGNORECASE))

                print('Searching for all movies matching the criteria',
                    flush=True)
                for _ in tqdm(range(0, no_of_titles, 50)):
                    try:
                        await expect(see_more_btn).to_be_enabled(timeout=default_timeout_ms)
                        if see_more_btn:
                            await see_more_btn.click()
                        else:
                            break
                    except Exception as e:
                        pass
                        # print(f'Expected exception.....\n{e}')

                # await page.wait_for_timeout(2000)
                content = await page.content()
                soup = BeautifulSoup(content, 'html.parser')

                titles = soup.select(TITLE_LINKS_CSSPATH)
                if not titles:
                    raise ValueError('no movies found...')

                for title in titles:
                    all_title_hrefs.append(title.get('href'))

    except Exception as e:
        print(f'Unable to search IMDB.\nErrorMessage:\n{str(e)}')

    finally:
        if browser:
            await browser.close()
        return all_title_hrefs


async def scrape_href(aiohttp_session: aiohttp.ClientSession, href: str, storage: list[dict]):
    '''
    '''
    title = "N/A"
    year = "N/A"
    score = "N/A"
    plot = "N/A"
    cast = {'role': 'actor'}
    directors = []
    try:
        async with aiohttp_session.get(href, headers={'User-Agent': 'Mozilla/5.0'}) as response:
            if response.status == 200:
                raw = await response.text()
                soup = BeautifulSoup(raw, 'html.parser')

                title_element = soup.find('span', {'data-testid': "hero__primary-text"})
                if title_element:
                    title = title_element.text

                year_element = soup.select_one(YEAR_PATH1)
                if year_element:
                    year = year_element.text
                else:
                    year_element = soup.select_one(YEAR_PATH2)
                    if year_element:
                        year = year_element.text

                score_div = soup.find('div', {'data-testid': 'hero-rating-bar__aggregate-rating__score'})
                if score_div:
                    score = score_div.span.text

                plot_para = soup.find('p', {'data-testid': 'plot', 'class':('sc-466bb6c-3', 'fOUpWp')})
                if plot_para:
                    plot = plot_para.text

                cast_section = soup.find('section', {'data-testid': 'title-cast', 'class': ('title-cast','title-cast--movie')})
                if cast_section:
                    cast_div = cast_section.find_all('div', class_=("sc-bfec09a1-7", "gWwKlt"))
                    for div in cast_div:
                        role = actor = "N/A"
                        actor_href = div.find('a', {'data-testid': "title-cast-item__actor"})
                        if actor_href:
                            actor = actor_href.text
                        role_href = div.find('a', {'data-testid': "cast-item-characters-link"})
                        if role_href:
                            role = role_href.text
                        cast[role] = actor

                directors_li = soup.find('li', {'data-testid': 'title-pc-principal-credit'})
                if directors_li:
                    directors = [director.text
                                 for director in directors_li.find_all('a')]

            else:
                raise ValueError('Website did not respond')

    except Exception as e:
        storage.append({'error': str(e),
                        'href': href})

    else:
        storage.append({'title': title,
                        'href': href,
                        'year': year,
                        'plot': plot,
                        'score': score,
                        'cast': cast,
                        'director(s)': directors})


async def scrape_all_hrefs(hrefs: list[str]):
    '''
    '''
    results = []
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(base_url, timeout=timeout) as session:
        tasks = [scrape_href(session, href, results) for href in hrefs]
        for task in async_tqdm.as_completed(tasks):
            await task

    return results

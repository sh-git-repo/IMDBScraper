'''
'''
import asyncio
import unittest

from aiohttp.test_utils import AioHTTPTestCase

from scraper.utils import scrape_all_hrefs, search_imdb


class TestSearchIMDB(unittest.TestCase):
    '''
    '''
    def test_multiple_movies_found(self):
        '''
        '''
        title = 'dune'
        genres = 'action,adventure'
        results = asyncio.run(search_imdb(title, genres))
        self.assertEqual(len(results), 6)


    def test_no_movie_found(self):
        '''
        '''
        title = 'fargo'
        genres = 'comedy'
        results = asyncio.run(search_imdb(title, genres))
        self.assertEqual(len(results), 0)


    def test_movies_found_by_title_only(self):
        '''
        '''
        title = 'fargo'
        genres = ''
        results = asyncio.run(search_imdb(title, genres))
        self.assertEqual(len(results), 9)


    def test_movies_found_by_genres_only(self):
        '''
        '''
        title = ''
        genres = 'crime,comedy,film-noir'
        results = asyncio.run(search_imdb(title, genres))
        self.assertEqual(len(results), 30)



class TestScrapeHref(unittest.TestCase):
    '''
    '''
    def test_almost_empty_movie(self):
        '''
        '''
        href = '/title/tt6096360/'
        results = asyncio.run(scrape_all_hrefs([href]))
        self.assertEqual(len(results), 1)

        results_expected = {"score": "N/A",
                            "year": "N/A"}.items()
        self.assertLessEqual(results_expected, results[0].items())


    def test_two_directors(self):
        '''
        '''
        href = '/title/tt0116282/'
        results = asyncio.run(scrape_all_hrefs([href]))
        self.assertEqual(len(results), 1)

        results_expected = {"score": "8.1",
                            "year": "1996",
                            "director(s)": ["Joel Coen","Ethan Coen"],
                            "title": "Fargo"}.items()
        self.assertLessEqual(results_expected, results[0].items())

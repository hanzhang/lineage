import requests
from bs4 import BeautifulSoup
import re
import psycopg2
import time

class GetData(object):
    def __init__(self):
        self.url_base = 'http://www.whosampled.com'

    # Create soup object
    def _get_soup(url):
        '''
        Input: url string
        Return: soup object for processing
        '''
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    # Collect the entirety of artist names based on genre
    def _get_artists(genre):
        '''
        Input: genre string
        Output: list of artist names
        '''
        url = self.url_base+'/genre/'+genre+'/'
        genre_soup = _get_soup(url)
        alpha_urls = genre_soup.select('.browse-letters')

    # Get meta data for songs
    def song_data(soup):
        song = {}
        
        song['name'] = soup.select('h1[itemprop="name"]')[0].text
        print song['name']
        song['artists'] = [x.text for x in soup.select('h2 a')]
        song['artist_links'] = [url_base + x['href'] for x in soup.select('h2 a')]
        song['album'] = soup.select('.trackReleaseDetails h3')[0].text
        song['record_label'] = re.split('; |, |\*|\n', soup.select('.trackReleaseDetails h4')[0].text)
        song['year'] = soup.select('.trackReleaseDetails')[0].contents[4].strip()
        if len(soup.select('.trackReleaseDetails a')) > 0:
            song['producers'] = soup.select('.trackReleaseDetails a')[0].text
        else:
            song['producers'] = ''
        song['relationships'] = sample_data(soup)
        
        return song


    # Get metadata for each song
    def meta_data(type, ):


    # Get all the sampling data for each song
    def sample_data(soup):
        song_sample_data = {}
        for header in soup.select('.sectionHeader'):
            if header.text.find('samples') != -1:
                ul = header.find_next_sibling('ul')
                song_sample_data['sampled_from_song'] = [x.text for x in ul.select('.trackName')]
                song_sample_data['sampled_from_song_url'] = [x['href'] for x in ul.select('.trackName')]
                song_sample_data['sampled_from_artist'] = [x.text for x in ul.select('.trackArtist a')]
                song_sample_data['sampled_from_artist_url'] = [x['href'] for x in ul.select('.trackArtist a')]
            elif header.text.find('sampled') != -1:
                ul = header.find_next_sibling('ul')
                song_sample_data['sampled_by_song'] = [x.text for x in ul.select('.trackName')]
                song_sample_data['sampled_by_song_url'] = [x['href'] for x in ul.select('.trackName')]
                song_sample_data['sampled_by_artist'] = [x.text for x in ul.select('.trackArtist a')]
                song_sample_data['sampled_by_artist_url'] = [x['href'] for x in ul.select('.trackArtist a')]
            elif header.text.find('covered') != -1:
                ul = header.find_next_sibling('ul')
                song_sample_data['covered_by_song'] = [x.text for x in ul.select('.trackName')]
                song_sample_data['covered_by_song_url'] = [x['href'] for x in ul.select('.trackName')]
                song_sample_data['covered_by_artist'] = [x.text for x in ul.select('.trackArtist a')]
                song_sample_data['convered_by_artist_url'] = [x['href'] for x in ul.select('.trackArtist a')]
            elif header.text.find('remixed') != -1:
                ul = header.find_next_sibling('ul')
                song_sample_data['remixed_by_song'] = [x.text for x in ul.select('.trackName')]
                song_sample_data['remixed_by_song_url'] = [x['href'] for x in ul.select('.trackName')]
                song_sample_data['remixed_by_artist'] = [x.text for x in ul.select('.trackArtist a')]
                song_sample_data['remixed_by_artist_url'] = [x['href'] for x in ul.select('.trackArtist a')]
        return song_sample_data

    # Get all the song urls based on Artist name
    def get_song_urls_from_artist(artist):
        url_base = 'http://www.whosampled.com'
        song_urls = []
        url = url_base + '/' + artist
        soup = get_soup(url)
        pages = int(soup.select('.page')[-1].text)
        for pg_num in xrange(pages):
            url = url_base + '/' + artist + '/?sp=' + str(pg_num+1)
            soup = get_soup(url)
            current_pg_urls = [url_base + song['href'] for song in soup.select('.trackName a[itemprop="url"]')]
            song_urls += current_pg_urls
        return song_urls

    # Get all the song data for a particular artist
    def scrape_artist(artist):
        all_data = []
        artist = '-'.join(artist.split())
        urls = get_song_urls_from_artist(artist)
        for url in urls:
            soup = get_soup(url)
            all_data.append(song_data(soup))
        return all_data

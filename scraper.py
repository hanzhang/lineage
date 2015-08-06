import requests
from bs4 import BeautifulSoup
import re
import psycopg2
import time
import numpy as np

class GetData(object):
    def __init__(self):
        self.url_base = 'http://www.whosampled.com'
        self.used_genres = set([])
        self.unused_genres = set(['/genre/Hip-Hop/', '/genre/Electronic-Dance/', '/genre/Rock-Pop/', \
                                '/genre/Soul-Funk-Disco/', '/genre/Jazz-Blues/', '/genre/Reggae/', \
                                '/genre/Country-Folk/', '/genre/World/', '/genre/Soundtrack/', '/genre/Classical/'])
        self.used_artists = set([])
        self.unused_artists = set([])
        self.used_producers = set([])
        self.unused_producers = set([])
        self.used_songs = set([])
        self.unused_songs = set([])

    # Create soup object
    def _get_soup(self, url):
        '''
        INPUT: url string
        OUTPUT: soup object for processing
        '''
        html = requests.get(url).content
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    # Collect all artist names based on genre
    def _get_artists_by_genre(self, genre):
        '''
        INPUT: genre string
        OUTPUT: saves artists names into SQL database
        '''
        artists = []
        url = self.url_base + genre
        genre_soup = self._get_soup(url)
        alpha_urls = [x['href'] for x in genre_soup.select('.browse-letters a')]
        for alphabet_url in alpha_urls:
            pages = int(self._get_num_pages(alphabet_url))
            decomp_url = alphabet_url.split('/')
            for page in xrange(pages):
                decomp_url[-2] = str(page + 1)
                page_url = '/'.join(decomp_url)
                artists += self._get_link_and_text_data(page_url, '.artistName a')
        
        conn = None
        conn = psycopg2.connect(database = 'beatlineage', user = 'gSchool', host = '/tmp')
        cur = conn.cursor()
        
        for artist in artists:
            if artist[0] in self.used_artists:
                continue
            else:
                self.unused_artists.add(artist[0])
                cur.execute('INSERT INTO artists VALUES(%s, %s)', artist)
                conn.commit()
                
        if conn:
            cur.close()
            conn.close()
    
    # Collect all song names based on artist
    def _get_songs_by_artist(self, artist):
        '''
        INPUT: artist string
        OUTPUT: saves songs into list
        '''
        songs = []
        pages = int(self._get_num_pages(artist))
        for pg_num in xrange(pages):
            page_url = artist + '?sp=' + str(pg_num + 1)
            songs += self._get_link_and_text_data(page_url, '.trackName a[itemprop="url"]')
        
        for song in songs:
            if song[0] in self.used_songs:
                continue
            else:
                self.unused_songs.add(song[0])

    # Collect all data for a single song
    def _get_song_data(self, song):
        '''
        INPUT: song string
        OUTPUT: saves producer and song data into SQL database
        '''
        song_data = []
        producers = []
        sample_data = {}
        url = self.url_base + song
        soup = self._get_soup(url)
        
        # Basic song info
        name = soup.select('h1[itemprop="name"]')[0].text
        artists = [x['href'] for x in soup.select('h2 a')]
        album = soup.select('.trackReleaseDetails h3')[0].text
        main_label = re.split('; |, |\*|\n', soup.select('.trackReleaseDetails h4')[0].text)[0]
        year = int(soup.select('.trackReleaseDetails')[0].contents[4].strip())
        if len(soup.select('.trackReleaseDetails a')) > 0:
            producers = self._get_link_and_text_data(song, '.trackReleaseDetails a')
        else:
            producers = ''        
        
        # Song sampling history
        for header in soup.select('.sectionHeader'):
            if len(header.select('.moreButton')) > 0:
                pass
            else:
                if header.text.find('samples of') != -1:
                    ul = header.find_next_sibling('ul')
                    
        
        print url
        print name
        print artists
        print album
        print main_label
        print year
        
        '''
        # Open a connection to postgresql
        conn = None
        conn = psycopg2.connect(database = 'beatlineage', user = 'gSchool', host = '/tmp')
        cur = conn.cursor()
        
        # Write to song to artist relationship table
        cur.execute('INSERT INTO songs VALUES(%s, %s, %s, %s, %s, %s)', (song[0], song[1], '', '', 0, ''))
        conn.commit()
        
        
        
        # Close connection to postgresql
        if conn:
            cur.close()
            conn.close()
        '''

    # Get the sampling data
    def _get_sample_data(self, song):
        '''
        INPUT: song string
        OUTPUT: sampling data
        '''
        
        
        
        
    
    # Get the number of pages on a page
    def _get_num_pages(self, end_url):
        '''
        INPUT: ending url string
        OUTPUT: number of pages of request
        '''
        url = self.url_base + end_url
        page_soup = self._get_soup(url)
        try:
            num_of_pg = int(page_soup.select('.page')[-1].text)
        except:
            num_of_pg = 1
        return num_of_pg
    
    # Extract text and link data for a given CSS tag
    def _get_link_and_text_data(self, end_url, tag):
        '''
        INPUT: ending url and CSS tag
        OUTPUT: list of tuple of (text, link)
        '''
        print end_url
        url = self.url_base + end_url
        page_soup = self._get_soup(url)
        text = [x.text for x in page_soup.select(tag)]
        link = [x['href'] for x in page_soup.select(tag)]
        return zip(link, text)
    
    def _get_songs(self):
        genre = '/genre/Soul-Funk-Disco/'
        self._get_artists_by_genre(genre)
        while len(self.unused_artists) > 0:
            artist = self.unused_artists.pop()
            self._get_songs_by_artist(artist)
            self.used_artists.add(artist)

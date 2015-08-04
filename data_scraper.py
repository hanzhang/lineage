import requests
import bs4
from bs4 import BeautifulSoup
import re

# Create soup object
def get_soup(url):
    html = requests.get(url).content
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# Get meta data for songs
def song_data(soup):
    album = ''
    record_label = ''
    year = ''
    producer = ''
    
    data = ','.join([i.text for i in soup.select('div.trackReleaseDetails')])
    result = re.split('; |, |\*|\n',data)
    cleaned_result = [x.strip() for x in result]
    cleaned_result = filter(None, cleaned_result)
    
    if len(result) > 2:
        producers = cleaned_result[3:]
    
    album = cleaned_result[0]
    production = cleaned_result[1]
    record_label = production[:-5]
    year = production[-4:]
    
    return album, record_label, year, producers

# Get all the song urls based on Artist name
def get_song_urls_from_artist(artist):
    url_base = 'www.whosampled.com'
    song_urls = []
    url = link_base + '/' + artist
    soup = get_soup(url)
    pages = int(soup.select('.ellipsis + .page')[0].text)
    for pg_num in xrange(pages):
        url = link_base + artist + '/?sp=' + str(pg_num+1)
        soup = get_soup(url)
        current_pg_urls = [url_base + song['href'] for song in soup.select('.trackName a[itemprop="url"]')]
        song_urls += current_pg_urls
    return song_urls

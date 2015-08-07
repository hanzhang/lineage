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
                print page_url
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
        producers = []
        self.sampled_from_song_url = []
        self.sampled_by_song_url = []
        self.cover_of_song_url = []
        self.covered_by_song_url = []
        self.remix_of_song_url = []
        self.remixed_by_song_url = []
        url = self.url_base + song
        soup = self._get_soup(url)
        
        # Basic song info
        try:
            name = soup.select('h1[itemprop="name"]')[0].text
        except:
            name = ''
        artists = [x['href'] for x in soup.select('h2 a')]
        try:
            album = soup.select('.trackReleaseDetails h3')[0].text
        except:
            album = ''
        try:
            main_label = re.split('; |, |\*|\n', soup.select('.trackReleaseDetails h4')[0].text)[0]
        except:
            main_label = ''
        try:
            year = int(soup.select('.trackReleaseDetails')[0].contents[4].strip())
        except:
            year = 0
        if len(soup.select('.trackReleaseDetails a')) > 0:
            producers = self._get_link_and_text_data(song, '.trackReleaseDetails a')
        else:
            producers = ''  
        
        # Song sampling history
        for header in soup.select('.sectionHeader'):
            if header.select('.moreButton'):
                more_url = header.select('.moreButton')[0]['href']
                pages = int(self._get_num_pages(more_url))
                for pg_num in xrange(pages):
                    page_url = more_url + '?cp=' + str(pg_num + 1)
                    page_soup = self._get_soup(self.url_base + page_url)
                    for header2 in page_soup.select('.sectionHeader'):
                        self._get_sample_data(header2)
            else:
                self._get_sample_data(header)
        
        # Open a connection to postgresql
        conn = None
        conn = psycopg2.connect(database = 'beatlineage', user = 'gSchool', host = '/tmp')
        cur = conn.cursor()
        
        # Write to SQL tables
        # Saves producer info and relationship mapping
        for producer in producers:
            if producer[0] in self.used_producers:
                continue
            else:
                self.used_producers.add(producer[0])
                cur.execute('INSERT INTO producers VALUES(%s, %s)', producer)
                conn.commit()
            cur.execute('INSERT INTO producer_to_song VALUES(%s, %s)', (producer[0], song))
            conn.commit()
        
        # Saves song info
        cur.execute('INSERT INTO songs VALUES(%s, %s, %s, %s, %s, %s)', (song, name, album, main_label, year, self.song_genre))
        conn.commit()
        
        # Saves artist to song relationship mapping
        for artist in artists:
            cur.execute('INSERT INTO artist_to_song VALUES(%s, %s)', (artist, song))
            conn.commit()
        
        # Saves song to song relationship mapping
        tables = [self.sampled_from_song_url, self.sampled_by_song_url, self.cover_of_song_url, self.covered_by_song_url, self.remix_of_song_url, self.remixed_by_song_url]
        for i, table in enumerate(tables):
            self._write_song_to_song_table(cur, conn, song, table, i+1)
        
        # Close connection to postgresql
        if conn:
            cur.close()
            conn.close()

    # Get the sampling data
    def _get_sample_data(self, header):
        '''
        INPUT: song string
        OUTPUT: no returns, just update self variables
        '''
        ul = header.find_next_sibling('ul')
        if header.text.find('samples of') != -1:
            sampled_from_song_urls = self._get_genre_and_song_url(ul, 0)
            self.sampled_from_song_url += sampled_from_song_urls
        elif header.text.find('sampled in') != -1:
            sampled_by_song_urls = self._get_genre_and_song_url(ul, 1)
            self.sampled_by_song_url += sampled_by_song_urls
        elif header.text.find('cover of') != -1:
            cover_of_song_urls = self._get_genre_and_song_url(ul, 0)
            self.cover_of_song_url += cover_of_song_urls
        elif header.text.find('covered in') != -1:
            covered_by_song_urls = self._get_genre_and_song_url(ul, 1)
            self.covered_by_song_url += covered_by_song_urls
        elif header.text.find('remix of') != -1:
            remix_of_song_urls = self._get_genre_and_song_url(ul, 0)
            self.remix_of_song_url += remix_of_song_urls
        elif header.text.find('remixed in') != -1:
            remixed_by_song_urls = self._get_genre_and_song_url(ul, 1)
            self.remixed_by_song_url += remixed_by_song_urls
        else:
            pass

    # Uses the urls from _get_sample_data to grab the original song's genre and the new song's url
    # Side is binary for the side of the original song, 0 for left (sample of, cover of, remix of) and
    # 1 for right (sampled in, covered in, remixed in)
    def _get_genre_and_song_url(self, ul, side):
        '''
        INPUT: unordered list object and the side of the original song
        OUTPUT: original song genre and list of new song urls
        '''
        url_list = [x['href'] for x in ul.select('.trackName')]
        song_urls = []
        for url in url_list:
            pg_url = self.url_base + url
            soup = self._get_soup(pg_url)
            genres = [x['href'] for x in soup.select('.sampleAdditionalInfoContainer a[href^="/genre"]')]
            if len(genres) == 0:
                new_song_genre = '/browse/artists/Other/A/1/'
            elif len(genres) == 1 and self.song_genre != '/browse/artists/Other/A/1/':
                new_song_genre = '/browse/artists/Other/A/1/'
            elif len(genres) == 1 and self.song_genre == '/browse/artists/Other/A/1/':
                new_song_genre = genres[0]
            else:
                new_song_genre = genres[not side]
            
            song_urls.append([x['href'] for x in soup.select('h3 .trackName')][not side])
            
            if new_song_genre in self.used_genres:
                continue
            else:
                self.unused_genres.add(new_song_genre)
        return song_urls
    
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
        url = self.url_base + end_url
        page_soup = self._get_soup(url)
        text = [x.text for x in page_soup.select(tag)]
        link = [x['href'] for x in page_soup.select(tag)]
        return zip(link, text)
    
    # Write to song2song SQL table
    def _write_song_to_song_table(self, cur, conn, song1, song_list, code):
        for song in song_list:
            cur.execute('INSERT INTO song_to_song VALUES(%s, %s, %s)', (song1, song, code))
            conn.commit()
    
    # Used to scrape for all songs
    def get_songs(self):
        while len(self.unused_genres) > 0:
            genre = self.unused_genres.pop()
            self.used_genres.add(genre)
            self._get_artists_by_genre(genre)
            self.song_genre = genre
            while len(self.unused_artists) > 0:
                artist = self.unused_artists.pop()
                print artist
                self.used_artists.add(artist)
                self._get_songs_by_artist(artist)
                while len(self.unused_songs) > 0:
                    song = self.unused_songs.pop()
                    self.used_songs.add(song)
                    self._get_song_data(song)
                time.sleep(5 * np.random.rand())

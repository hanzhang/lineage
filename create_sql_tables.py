import psycopg2

con = None
con = psycopg2.connect(database = 'beatlineage', user = 'gSchool', host = '/tmp')
cur = con.cursor()
con.autocommit = True

# Create artist table in SQL
def create_artist_table(cur, con):
    try:
        cur.execute('CREATE TABLE artists (artist_url varchar, \
                                           artist_name varchar)')
    except:
        pass

    # Example entry:
    #cur.execute('INSERT INTO artists VALUES(%s, %s)', ('/Kanye-West/', 'Kanye West'))

# Create producer table in SQL
def create_producer_table(cur, con):
    try:
        cur.execute('CREATE TABLE producers (producer_url varchar, \
                                             producer_name varchar)')
    except:
        pass

    # Exmaple entry:
    #cur.execute('INSERT INTO producers VALUES(%s, %s)', ('/Kanye-West/', 'Kanye West'))

# Create song table in SQL
def create_song_table(cur, con):
    try:
        cur.execute('CREATE TABLE songs (song_url varchar, \
                                         song_name varchar, \
                                         album_name varchar, \
                                         label_name varchar, \
                                         year integer, \
                                         main_genre varchar)')
    except:
        pass

    # Example entry:
    #cur.execute('INSERT INTO songs VALUES(%s, %s, %s, %s, %d, %s)', ('/Lil-Jon/Lovers-%26-Friends/', 'Lovers & Friends', 'Crunk Juice', 'TVT', 2004, '/genre/Hip-Hop/'))

# Create artist to song mapping table in SQL
def create_artist_to_song_table(cur, con):
    try:
        cur.execute('CREATE TABLE artist_to_song (artist_url varchar, \
                                                  song_url varchar)')
    except:
        pass

    # Example entry:
    #cur.execute('INSERT INTO artists VALUES(%s, %s)', ('/Kanye-West/', '/Kanye-West/Mercy/'))

# Create producer to song mapping table in SQL
def create_producer_to_song_table(cur, con):
    try:
        cur.execute('CREATE TABLE producer_to_song (producer_url varchar, \
                                                    song_url varchar)')
    except:
        pass

    # Exmaple entry:
    #cur.execute('INSERT INTO producers VALUES(%s, %s)', ('/Kanye-West/', '/Kanye-West/Mercy/Power'))

# Create song to song relatioship table in SQL
def create_song_to_song_table(cur, con):
    try:
        cur.execute('CREATE TABLE song_to_song (song1_url varchar, \
                                                song2_url varchar, \
                                                relationship integer)')
    except:
        pass

    # Example entry:
    #cur.execute('INSERT INTO songs VALUES(%s, %s, %d)', ('/Black-Eyed-Peas/Boom-Boom-Pow/', '/Daft-Punk/Harder,-Better,-Faster,-Stronger/', 1))

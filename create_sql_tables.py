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
    #cur.execute('INSERT INTO songs VALUES(%s, %s, %s, %s, %s, %s)', ('/Lil-Jon/Lovers-%26-Friends/', 'Lovers & Friends', 'Crunk Juice', 'TVT', 2004, '/genre/Hip-Hop/'))

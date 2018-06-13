from MovieDb import InteractWithMovieDb
from GetMovieMojoGross import GetMovieData
from AppScripts import Scripts
from zappa.async import task


def main():
    db = InteractWithMovieDb()
    leagues = db.get_leagues_to_update()
    for league in leagues:
        for movie in db.get_movies_to_update(league[0]):
            main_sub(league, movie[0])


@task
def main_sub(league, movie):
    db = InteractWithMovieDb()
    movie_id = movie
    movie = GetMovieData(movie_id)
    movie_title, foreign_gross, domestic_gross, worldwide_gross, release_date = movie.get_update_info()
    if foreign_gross == 'n/a':
        foreign_gross = None
    if domestic_gross == 'n/a':
        domestic_gross = None
    if worldwide_gross == 'n/a':
        worldwide_gross = None
    if worldwide_gross is None:
        s = Scripts()
        _foreign = s.convert_dollar_to_int(foreign_gross)
        _domestic = s.convert_dollar_to_int(domestic_gross)
        worldwide_gross = sum([_foreign, _domestic])
        worldwide_gross = s.convert_int_to_dollar(worldwide_gross)
    print 'Updating %s in %s' % (movie_title, league[0])
    db.update_movie_gross(league[0], foreign_gross, domestic_gross, worldwide_gross, movie_id)


if __name__ == '__main__':
    main()
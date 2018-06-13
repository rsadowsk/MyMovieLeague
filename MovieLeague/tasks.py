from MovieDb import InteractWithMovieDb
from GetMovieMojoGross import GetMovieData
from AppScripts import Scripts
from collections import OrderedDict
from datetime import timedelta
import urllib, urllib2
from bs4 import BeautifulSoup
import datetime
from zappa.async import task
import json


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


@task
def get_date_range(league):
    db = InteractWithMovieDb()
    dates = db.get_league_info(league)
    start_date = dates[0][0]
    start_date_serial = start_date.isoformat()
    end_date = dates[0][1]
    end_date_serial = end_date.isoformat()

    dates_list = OrderedDict(((start_date + timedelta(_)).strftime(r"%Y-%m"),
                              None) for _ in xrange((end_date - start_date).days)).keys()
    if start_date.month != end_date.month and start_date.year != end_date.year:
        dates_list.append(end_date.strftime(r"%Y-%m"))
    for date in dates_list:
        year, month = date.split('-')
        get_movie_by_month(league, start_date_serial, end_date_serial, year, month)


@task
def get_movie_by_month(league, start_date, end_date, year, month):
    db = InteractWithMovieDb()
    start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d').date()
    end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d').date()
    #todo add baseurl to app config
    baseURL = 'http://www.boxofficemojo.com/schedule/?view=&release=&date=%s-%s' \
              '&showweeks=5&p=.htm'
    url = baseURL % (year, month)
    html = urllib2.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.find_all('a', href=True)[3:]:
        if 'movies' in a['href']:
            movie_id = a['href'].split('=')[1]
            movie_id = urllib.urlencode({'': movie_id})[1:-4]
            try:
                movie = GetMovieData(str(movie_id))
                movie.find_movie_info()
                movie.find_movie_gross()
                movie_title, foreign_gross, domestic_gross, worldwide_gross, release_date = movie.get_movie_data_strings()
                movie_title = Scripts.fix_unicode(movie_title)
                movie_title = Scripts.fix_acii(movie_title)
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
                date = release_date.split("-")

                if start_date < datetime.date(int(date[0]), int(date[1]), int(date[2])) < end_date:
                    if db.check_movie_exists(league, movie_id) == 0:
                        print 'Adding %s to db' % movie_title
                        db.add_movie_to_db(league, movie_title, movie_id,
                                                foreign_gross, domestic_gross, worldwide_gross, release_date)
                    else:
                        print 'Updating %s in db' % movie_title
                        db.update_movie_gross(league, foreign_gross,
                                                   domestic_gross, worldwide_gross, movie_id)
                else:
                    print "Not in range, %s" % release_date

            except Exception, e:
                print e
                print movie_id


if __name__ == '__main__':
    get_date_range('Test1')
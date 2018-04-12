import urllib, urllib2
from bs4 import BeautifulSoup
from GetMovieMojoGross import GetMovieData
from MovieDb import InteractWithMovieDb
from datetime import timedelta
from collections import OrderedDict
from AppScripts import Scripts
import datetime

# TODO APP script


class GetMovieList(object):

    def __init__(self, league):
        self.league = league
        self.db = InteractWithMovieDb()
        self.baseURL = 'http://www.boxofficemojo.com/schedule/?view=&release=&date=%s-%s' \
                       '&showweeks=5&p=.htm'
        self.start_date = None
        self.end_date = None

    def get_movie_by_month(self, year, month):
        url = self.baseURL % (year, month)
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

                    if self.start_date < datetime.date(int(date[0]), int(date[1]), int(date[2])) < self.end_date:
                        if self.db.check_movie_exists(self.league, movie_id) == 0:
                            print 'Adding %s to db' % movie_title
                            self.db.add_movie_to_db(self.league, movie_title, movie_id,
                                                    foreign_gross, domestic_gross, worldwide_gross, release_date)
                        else:
                            print 'Updating %s in db' % movie_title
                            self.db.update_movie_gross(self.league, foreign_gross,
                                                       domestic_gross, worldwide_gross, movie_id)
                    else:
                        print "Not in range, %s" % release_date


                except Exception, e:
                    print e
                    print movie_id

    def get_date_range(self):
        dates = self.db.get_league_info(self.league)
        self.start_date = dates[0][0]
        self.end_date = dates[0][1]

        dates_list = OrderedDict(((self.start_date + timedelta(_)).strftime(r"%Y-%m"),
                                  None) for _ in xrange((self.end_date - self.start_date).days)).keys()
        if self.start_date.month != self.end_date.month and self.start_date.year != self.end_date.year:
            dates_list.append(self.end_date.strftime(r"%Y-%m"))
        for date in dates_list:
            year, month = date.split('-')
            self.get_movie_by_month(year, month)


if __name__ == '__main__':
    gml = GetMovieList('testleague3')
    gml.get_date_range()

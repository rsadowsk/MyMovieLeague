import urllib2
from bs4 import BeautifulSoup
from HTMLParser import HTMLParser
from time import strptime

class MLStripper(HTMLParser):
    def __init__(self):
        self.reset()
        self.fed = []

    def handle_data(self, d):
        self.fed.append(d)

    def get_data(self):
        return ''.join(self.fed)


class GetMovieData(object):
    def __init__(self, movie_id):
        self.KeyWords = ['Domestic:', "Foreign:", "Worldwide:"]
        self.baseURL = "http://www.boxofficemojo.com/movies/?id=%s.htm"
        self.movieTitle = movie_id
        self.movie_data = []
        self.soup = BeautifulSoup(self.get_movie_html(), "html.parser")
        self.title_html = None
        self.title_string = None
        self.release_date_html = None
        self.release_date_string = None
        self.release_date_date = None
        self.domestic_gross_html = None
        self.domestic_gross_string = None
        self.foreign_gross_html = None
        self.foreign_gross_string = None
        self.worldwide_gross_html = None
        self.worldwide_gross_string = None

    def get_movie_html(self):
        return urllib2.urlopen(self.baseURL % self.movieTitle)

    def find_movie_gross(self):
        right_table = self.soup.find('div', class_='mp_box_content')
        try:
            for row in right_table.findAll("tr"):
                cells = row.findAll('td')
                if len(cells) > 1:
                    for element in range(len(cells)):
                        html = strip_tags(str(cells[element]))
                        html = self.strip_stuff(html)
                        if "Domestic:" in html:
                            self.domestic_gross_html = cells[element]
                            gross = strip_tags(str(cells[element + 1]).strip())
                            self.domestic_gross_string = self.strip_stuff(gross)
                        if "Foreign:" in html:
                            self.foreign_gross_html = cells[element]
                            gross = strip_tags(str(cells[element + 1]).strip())
                            self.foreign_gross_string = self.strip_stuff(gross)
                        if "Worldwide:" in html:
                            self.worldwide_gross_html = cells[element]
                            gross = strip_tags(str(cells[element + 1]).strip())
                            self.worldwide_gross_string = self.strip_stuff(gross)
        except AttributeError:
            return

    def find_movie_info(self):
        self.title_html = self.soup.findAll('b')[1]
        #print self.baseURL % self.movieTitle

        self.title_string = strip_tags(str(self.title_html))
        self.release_date_html = self.soup.findAll('b')
        for a in self.soup.findAll('b'):
            if ';date=' in str(a):
                self.release_date_html = a
                self.release_date_string = strip_tags(str(self.release_date_html))
                month, day, year = self.release_date_string.split()
                month = self.strip_stuff(month)
                day = self.strip_stuff(day)
                year = self.strip_stuff(year)
                month = strptime(month[0:3], '%b').tm_mon
                day = day.replace(',', '')
                self.release_date_date = "%s-%s-%s" % (year, month, day)
        """try:
            self.release_date_html = self.soup.findAll('b')[4]
            self.release_date_string = strip_tags(str(self.release_date_html))
            month, day, year = self.release_date_string.split()
            month = strptime(month[0:3], '%b').tm_mon
            day = day.replace(',', '')
            self.release_date_date = "%s-%s-%s" % (year, month, day)
        except Exception, e:
            self.release_date_html = self.soup.findAll('b')[3]
            self.release_date_string = strip_tags(str(self.release_date_html))
            month, day, year = self.release_date_string.split()
            month = strptime(month[0:3], '%b').tm_mon
            day = day.replace(',', '')
            self.release_date_date = "%s-%s-%s" % (year, month, day)
        """

    def find_movie_gross_html(self):
        right_table = self.soup.find('div', class_='mp_box_content')
        return right_table

    def print_movie_gross(self):
        for tag in self.movie_data:
            print tag

    def get_movie_gross(self):
        return self.movie_data

    def get_movie_data_strings(self):
        return self.title_string, \
               self.foreign_gross_string, \
               self.domestic_gross_string, \
               self.worldwide_gross_string,\
               self.release_date_date

    @staticmethod
    def strip_stuff(stuff):
        bad_stuff = ["+", "=", "\xc2", "\xa0", "\xc2"]
        for elements in bad_stuff:
            stuff = stuff.replace(elements, "")
        stuff = stuff.strip()
        return stuff


def strip_tags(html):
    s = MLStripper()
    s.feed(html)
    return s.get_data()


if __name__=='__main__':
    movie = GetMovieData('eighthoursdontmakeaday')
    #movie = GetMovieData('wonderwoman')
    movie.find_movie_info()
    movie.find_movie_gross()
    print movie.get_movie_data_strings()

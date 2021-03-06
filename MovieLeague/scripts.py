from CheckUserInfo import InteractWithUsersDb
from GetMyMovies import GetMyMovies
from collections import OrderedDict
from MovieDb import InteractWithMovieDb
from GetMovieList import GetMovieList
from testemail import SendEmail
from AppScripts import Scripts
import re
import json
import datetime
import urllib2
from zappa.async import run
import tasks


class MLScripts(object):
    def __init__(self):
        pass

    @staticmethod
    def my_movies(user_info):
        my_movies = OrderedDict()
        db = InteractWithUsersDb()
        movie_db = InteractWithMovieDb()
        id = db.get_user_info(user_info["name"])[0][0]
        leagues = movie_db.get_users_leagues(str(id))
        for league in leagues:
            movie_data = movie_db.get_users_movie_info_from_league(league, id)
            totals = GetMyMovies(league, id)
            totals.get_my_movie_gross()
            movie_data.append(totals.get_all_my_totals())
            my_movies[league] = movie_data
        return my_movies

    @staticmethod
    def create_league(league_name, league_owner, start_date, end_date, end_record):
        print 'hi'
        db = InteractWithMovieDb()
        udb = InteractWithUsersDb()
        uid = udb.get_user_info(league_owner)[0][0]
        print 'hi1'
        league_name = league_name.replace(" ", "_")
        print 'hi2'
        print league_name, uid, str(start_date), str(end_date), str(end_record)
        db.add_league_to_leagues(league_name, uid, str(start_date), str(end_date), str(end_record))
        print 'hi3'
        db.create_league_movie_table(league_name)
        print 'hi4'
        db.create_league_table(league_name)
        print 'hi5'
        db.create_league_user_table(league_name)
        print 'hi6'
        db.add_user_to_league_user(league_name, int(uid))
        print 'hi7'
        # populate league_movies
        #gml = GetMovieList(league_name)
        #gml.get_date_range()
        tasks.get_date_range(league_name)
        print 'hi'

    @staticmethod
    def get_leagues(user):
        db = InteractWithMovieDb()
        udb = InteractWithUsersDb()
        uid = udb.get_user_info(user)[0][0]
        return db.get_users_leagues(uid)

    def get_league_users(self, league, json=False):
        db = InteractWithMovieDb()
        list_ = db.get_league_users(league)
        if json:
            return list_, self.jsonify(list_)
        else:
            return list_

    def get_all_league_movies(self, league, json=False):
        db = InteractWithMovieDb()
        list_ = db.get_league_movie_list(league)
        if json:
            return list_, self.jsonify(list_)
        else:
            return list_

    @staticmethod
    def jsonify(input):
        unjsonified = {}
        for i in input:
            a = i[1].replace('"', "'")
            a = re.sub(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f-\xff]', '', a)
            unjsonified[i[0]] = a

        return json.dumps(unjsonified)

    def handle_add_user_token(self, token):
        pass

    def send_invite_friend_email(self, sender, league, emails):
        se = SendEmail()
        for email in emails:
            se.send_invite_email(sender, league, email)

    @staticmethod
    def add_user_movie_to_league_list(league, values):
        data = []
        print values
        values = values.split(',')
        values = [values[idx:idx+2] for idx in range(0, len(values), 2)]
        for l in values:
            data.append("("+','.join(l)+")")
        data = ', '.join(data)
        print data
        db = InteractWithMovieDb()
        db.add_user_movie_to_league_list(league, data)

    @staticmethod
    def my_movies_league_totals_info(user_info):
        my_movies = OrderedDict()
        db = InteractWithUsersDb()
        movie_db = InteractWithMovieDb()
        print user_info
        id = db.get_user_info(user_info["name"])[0][0]
        leagues = movie_db.get_users_leagues(str(id))
        for league in leagues:
            league_info = movie_db.get_league_totals_for_all_users(league)
            my_movies[league] = league_info
        return my_movies

    @staticmethod
    def get_full_league_stats(league):
        movie_db = InteractWithMovieDb()
        rtn_list = {}
        for i in movie_db.get_league_users_and_movies(league):
            lst = list(i)
            for a in lst:
                if isinstance(a, datetime.date):
                    lst[lst.index(a)] = a.strftime('%Y-%m-%d')
            if lst[0] not in rtn_list:
                rtn_list[lst[0]] = []
                rtn_list[lst[0]].append(lst[1:])
            else:
                rtn_list[lst[0]].append(lst[1:])
        return rtn_list

    @staticmethod
    def my_leagues_rankings(user_info):
        my_movies = OrderedDict()
        db = InteractWithUsersDb()
        movie_db = InteractWithMovieDb()
        id = db.get_user_info(user_info["name"])[0][0]
        leagues = movie_db.get_users_leagues(str(id))
        for league in leagues:
            winner = ['No Winner', 0]
            me = [user_info["name"], 0]
            league_info = movie_db.get_league_totals_for_all_users(league)
            for i in league_info:
                entry = Scripts.convert_dollar_to_int(league_info[i])
                if entry > winner[1]:
                    winner = [i, entry]
                if i == user_info["name"]:
                    me = [i, entry]
            if me == winner:
                me[1] = Scripts.convert_int_to_dollar(me[1])
                my_movies[league] = [me]
            elif me != winner:
                winner[1] = Scripts.convert_int_to_dollar(winner[1])
                me[1] = Scripts.convert_int_to_dollar(me[1])
                my_movies[league] = [winner, me]
        return my_movies

    @staticmethod
    def add_user_to_league_by_token(user_info, token):
        db = InteractWithUsersDb()
        id = db.get_user_info(user_info["name"])[0][0]
        info = Scripts.token_load(token)
        movie_db = InteractWithMovieDb()
        users = movie_db.get_league_users_ids(info)
        for i in users:
            if id in i:
                return False
        movie_db.add_user_to_league_user(info, id)
        return True

    def get_weekend_5(self):
        url = 'http://www.boxofficemojo.com/data/js/wknd5.php'
        html = urllib2.urlopen(url)
        ret = []
        for i in html.readlines():
            if "$" in i:
                ret.append(i.split("(")[1].split(")")[0].strip("'"))
        return ''.join(ret)

    def get_all_movies_for_league(self, league):
        movie_db = InteractWithMovieDb()
        movies = movie_db.get_all_movies_for_league(league)
        print movies
        return movies


if __name__=='__main__':
    mls = MLScripts()
    mls.add_user_to_league_by_token({u'family_name': u'Sadowski', u'name': u'Richard Sadowski', u'picture': u'https://lh5.googleusercontent.com/-6W2zKUUAC8M/AAAAAAAAAAI/AAAAAAAAAAA/AB6qoq3bDQrEOqj-IRssIFXX-92rj7zxrQ/mo/photo.jpg', u'gender': u'male', u'email': u'richard.j.sadowski@gmail.com', u'link': u'https://plus.google.com/111887332429616518308', u'given_name': u'Richard', u'id': u'111887332429616518308', u'verified_email': True}, 'Ik5ld19UZXN0aW5nX0xlYWd1ZSI.tQ8IHG_cwouQD3i096UruekAqPI')
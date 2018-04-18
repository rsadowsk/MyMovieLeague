from CheckUserInfo import InteractWithUsersDb
from GetMyMovies import GetMyMovies
from collections import OrderedDict
from MovieDb import InteractWithMovieDb
from GetMovieList import GetMovieList
from testemail import SendEmail
import json


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
        db = InteractWithMovieDb()
        udb = InteractWithUsersDb()
        uid = udb.get_user_info(league_owner)[0][0]
        db.add_league_to_leagues(league_name, uid, str(start_date), str(end_date), str(end_record))
        db.create_league_movie_table(league_name)
        db.create_league_table(league_name)
        db.create_league_user_table(league_name)
        db.add_user_to_league_user(league_name, int(uid))
        # populate league_movies
        gml = GetMovieList(league_name)
        gml.get_date_range()

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
            unjsonified[i[0]] = i[1]
        return json.dumps(unjsonified)

    def handle_add_user_token(self, token):
        pass

    def send_invite_friend_email(self, sender, league, emails):
        for email in emails:
            SendEmail(sender, league, email)

    @staticmethod
    def add_user_movie_to_league_list(league, values):
        data = []
        values = values.split(',')
        values = [values[idx:idx+2] for idx in range(0, len(values), 2)]
        for l in values:
            data.append("("+','.join(l)+")")
        data = ', '.join(data)
        db = InteractWithMovieDb()
        db.add_user_movie_to_league_list(league, data)

    @staticmethod
    def my_movies_league_totals_info(user_info):
        my_movies = OrderedDict()
        db = InteractWithUsersDb()
        movie_db = InteractWithMovieDb()
        id = db.get_user_info(user_info["name"])[0][0]
        leagues = movie_db.get_users_leagues(str(id))
        for league in leagues:
            league_info = movie_db.get_league_totals_for_all_users(league)
            my_movies[league] = league_info
        return my_movies


if __name__=='__main__':
    mls = MLScripts()
    a = mls.get_all_league_movies('testleague3', json=True)
    for i in a:
        print i, a[i]


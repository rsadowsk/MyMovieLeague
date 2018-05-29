import pymysql.cursors, os
from collections import OrderedDict
from MovieLeague import app
# from GetMovieMojoGross import GetMovieData


class InteractWithMovieDb(object):
    def __init__(self):
        # TODO hide username and password
        self.db = pymysql.connect(host=app.config['DB_HOST'],
                             user=app.config['DB_USER'],
                             passwd=app.config['DB_PASS'],
                             db=app.config['DB_MOVIEDB'])

    def add_movie_to_db(self, *argv):
        args = []
        for arg in argv:
            if isinstance(arg, str):
                args.append(arg.replace("\'", "\\'"))
            else:
                args.append(arg)
        cur = self.db.cursor()
        insert_stmt = ("INSERT INTO %s_movies "
                       "(`movie_title`, `movie_id`, `foreign_gross`, "
                       "`domestic_gross`, `worldwide_gross`, `release_date`) "
                       "VALUES ('%s', '%s', '%s', '%s', '%s', '%s')")
        data = (args[0], args[1], args[2], args[3], args[4], args[5], args[6])
        insert = insert_stmt % data
        cur.execute(insert)
        self.db.commit()

    def get_movie_from_db(self, *argv):
        args = []
        for arg in argv:
            if isinstance(arg, str):
                args.append(arg.replace("\'", "\\'"))
            else:
                args.append(arg)
        cur = self.db.cursor()
        insert_stmt = ("SELECT foreign_gross, domestic_gross, worldwide_gross "
                       "FROM %s_movies where movie_id='%s'")
        data = (args[0], args[1])
        insert = insert_stmt % data
        cur.execute(insert)
        results = cur.fetchall()
        return results

    def get_movie_title(self, *argv):
        args = []
        for arg in argv:
            if isinstance(arg, str):
                args.append(arg.replace("\'", "\\'"))
            else:
                args.append(arg)
        cur = self.db.cursor()
        insert_stmt = ("SELECT movie_title "
                       "FROM %s_movies where movie_id='%s'")
        data = (args[0], args[1])
        insert = insert_stmt % data
        cur.execute(insert)
        results = cur.fetchall()
        return results

    # movie_id, foreign_gross, domestic_gross, worldwide_gross
    def update_movie_gross(self, *argv):
        args = []
        for arg in argv:
            if isinstance(arg, str):
                args.append(arg.replace("\'", "\\'"))
            else:
                args.append(arg)
        cur = self.db.cursor()
        insert_stmt = ("UPDATE %s_movies SET "
                       "foreign_gross='%s', "
                       "domestic_gross='%s', "
                       "worldwide_gross='%s' "
                       "WHERE movie_id='%s'")
        data = (args[0], args[1], args[2], args[3], args[4])
        insert = insert_stmt % data
        cur.execute(insert)
        self.db.commit()

    def check_movie_exists(self, *argv):
        args = []
        for arg in argv:
            if isinstance(arg, str):
                args.append(arg.replace("\'", "\\'"))
            else:
                args.append(arg)
        cur = self.db.cursor()
        insert_stmt = ("SELECT * FROM %s_movies "
                       "WHERE movie_id='%s'")
        data = (args[0], args[1])
        insert = insert_stmt % data
        cur.execute(insert)
        self.db.commit()
        return cur.rowcount

    def close_db(self):
        self.db.close()

    def get_users_movie_from_league(self, league, user_id):
        movie_list = []
        cur = self.db.cursor()
        insert_stmt = ("SELECT %s_movies.movie_id "
                       "FROM %s JOIN %s_movies "
                       "WHERE %s_movies.id=%s.movie_id AND user_id=%s")
        data = (league, league, league, league, league, user_id)
        insert = insert_stmt % data
        cur.execute(insert)
        movies = cur.fetchall()
        for i in range(len(movies)):
            movie_list.append(movies[i][0])
        return movie_list

    def get_users_movie_info_from_league(self, league, user_id):
        movie_list = []
        cur = self.db.cursor()
        insert_stmt = ("select %s_movies.movie_title, "
                       "%s_movies.release_date, "
                       "%s_movies.foreign_gross, "
                       "%s_movies.domestic_gross, "
                       "%s_movies.worldwide_gross "
                       "from %s "
                        "join %s_movies "
                         "on %s.movie_id = %s_movies.id "
                       "where %s.user_id=%s")
        data = (league, league, league, league, league, league, league, league, league, league, user_id)
        insert = insert_stmt % data
        cur.execute(insert)
        movies = cur.fetchall()
        for i in range(len(movies)):
            movie_list.append(movies[i])
        return movie_list

    def get_league_info(self, league):
        cur = self.db.cursor()
        insert_stmt = ("SELECT start_date, end_date FROM leagues where league_name='%s'")
        data = league
        insert = insert_stmt % data
        cur.execute(insert)
        return cur.fetchall()

    # first
    def add_league_to_leagues(self, *argv):
        cur = self.db.cursor()
        insert_stmt = ("insert into leagues (league_name, league_owner, start_date, end_date, end_record) "
                       "values ('%s', '%s', '%s', '%s', '%s')")
        data = (argv[0], argv[1], argv[2], argv[3], argv[4])
        insert = insert_stmt % data
        cur.execute(insert)
        self.db.commit()

    # third
    def create_league_table(self, league):
        cur = self.db.cursor()
        insert_stmt = ("CREATE TABLE `%s` "
                       "(`id` int(11) NOT NULL AUTO_INCREMENT,"
                       "`user_id` int(11) DEFAULT NULL,"
                       "`movie_id` int(11) DEFAULT NULL, "
                       "PRIMARY KEY (`id`), "
                       "UNIQUE KEY `movie_id` (`movie_id`), "
                       "KEY `user_id` (`user_id`), "
                       "CONSTRAINT `%s_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`), "
                       "CONSTRAINT `%s_ibfk_2` FOREIGN KEY (`movie_id`) REFERENCES `%s_movies` (`id`))")
        data = (league, league, league, league)
        insert = insert_stmt % data
        cur.execute(insert)

    # fourth
    def create_league_user_table(self, league):
        cur = self.db.cursor()
        insert_stmt = ("CREATE TABLE `%s_users` ("
                       "`id` int(11) NOT NULL AUTO_INCREMENT PRIMARY KEY , "
                       "`user_id` int(11) NOT NULL, UNIQUE KEY `user_id` (`user_id`), "
                       "CONSTRAINT `%s__user_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`))")
        data = (league, league)
        insert = insert_stmt % data
        cur.execute(insert)

    # second
    def create_league_movie_table(self, league):
        cur = self.db.cursor()
        insert_stmt = ("CREATE TABLE %s_movies ("
                       "id INT PRIMARY KEY NOT NULL AUTO_INCREMENT, "
                       "movie_title VARCHAR(255), "
                       "movie_id VARCHAR(255) UNIQUE, "
                       "foreign_gross VARCHAR(255), "
                       "domestic_gross VARCHAR(255), "
                       "worldwide_gross VARCHAR(255), "
                       "release_date date)")
        data = league
        insert = insert_stmt % data
        cur.execute(insert)

    # fifth
    def add_user_to_league_user(self, league, id):
        cur = self.db.cursor()
        insert_stmt = ("INSERT INTO %s_users (user_id) "
                       "VALUES (%s)")
        data = (league, id)
        insert = insert_stmt % data
        print insert
        cur.execute(insert)
        self.db.commit()

    def get_league_names(self, league_id):
        cur = self.db.cursor()
        insert_stmt = ("SELECT league_name FROM leagues WHERE id='%s'")
        data = league_id
        insert = insert_stmt % data
        cur.execute(insert)
        return cur.fetchall()

    def get_league_users(self, league):
        cur = self.db.cursor()
        insert_stmt = ("select users.id, users.user_name "
                       "from %s_users inner join users "
                       "where %s_users.user_id=users.id")
        data = (league, league)
        insert = insert_stmt % data
        cur.execute(insert)
        return cur.fetchall()

    def get_user_leagues(self, user):
        cur = self.db.cursor()
        insert_stmt = ("SELECT leagues FROM users WHERE user_name='%s'")
        data = user
        insert = insert_stmt % data
        cur.execute(insert)
        return eval(cur.fetchall()[0][0])

    def get_users_leagues(self, user_id):
        cur = self.db.cursor()
        leagues = []
        insert_stmt = ("SELECT league_name, league_owner from leagues")
        cur.execute(insert_stmt)
        for league in cur.fetchall():
            try:
                insert_stmt = ("SELECT * from %s_users where user_id=%s")
                data = (league[0], user_id)
                insert = insert_stmt % data
                cur.execute(insert)
                if cur.rowcount > 0:
                    if league[1] == user_id:
                        leagues.append((league[0], league[1]))
                    else:
                        leagues.append(league[0])
            except Exception:
                pass
        return leagues

    def delete_league(self, league):
        cur = self.db.cursor()
        insert_stmt = ("drop table %s;"
                       "drop table %s_users;"
                       "drop TABLE %s_movies;"
                       "delete from leagues where league_name='%s'")
        data = (league, league, league, league)
        insert = insert_stmt % data
        cur.execute(insert)

    def get_league_movie_list(self, league):
        cur = self.db.cursor()
        insert_stmt = ("SELECT * FROM %s_movies")
        data = league
        insert = insert_stmt % data
        cur.execute(insert)
        return cur.fetchall()

    def add_user_movie_to_league_list(self, league, data):
        #insert into testleague3 (user_id, movie_id) values (1,3), (2,4),(2,9)
        cur = self.db.cursor()
        insert_stmt = ("INSERT INTO %s (user_id, movie_id) VALUES %s")
        data = (league, data)
        insert = insert_stmt % data
        print insert
        cur.execute(insert)
        self.db.commit()

    def get_league_totals(self, league):
        # select users.user_name, %s_movies.worldwide_gross from %s join %s_movies on %s_movies.id=%s.movie_id join users on users.id=%s.user_id
        cur = self.db.cursor()
        insert_stmt = ("select users.user_name, %s_movies.worldwide_gross from %s "
                       "join %s_movies on %s_movies.id=%s.movie_id "
                       "join users on users.id=%s.user_id")
        data = (league, league, league, league, league, league)
        insert = insert_stmt % data
        cur.execute(insert)
        return cur.fetchall()

    def get_used_movies(self):
        """select testleague3_movies.movie_id from testleague3
              join testleague3_movies on testleague3.movie_id=testleague3_movies.id
            Union
            select TestLeague5_movies.movie_id from TestLeague5
              join TestLeague5_movies on TestLeague5.movie_id=TestLeague5_movies.id"""
        pass

    def get_leagues_to_update(self):
        cur = self.db.cursor()
        insert = ("select league_name from leagues where end_record >= CURRENT_DATE")
        cur.execute(insert)
        return cur.fetchall()

    def get_movies_to_update(self, league):
        cur = self.db.cursor()
        insert_stmt = ("select %s_movies.movie_id from %s "
                       "join %s_movies where %s_movies.id=%s.movie_id")
        data = (league, league, league, league, league)
        insert = insert_stmt % data
        cur.execute(insert)
        return cur.fetchall()

    def convert_dollar_to_int(self, dollar):
        dollar = dollar.replace("$", "")
        dollar = dollar.replace(",", "")
        return int(dollar)

    def convert_int_to_dollar(self, dollar):
        return '${:,}'.format(dollar)

    def get_league_totals_for_all_users(self, league):
        movies = self.get_league_totals(league)
        total = OrderedDict()
        for i in movies:
            if i[0] not in total.keys():
                total[i[0]] = self.convert_dollar_to_int(i[1])
            else:
                total[i[0]] = total[i[0]] + self.convert_dollar_to_int(i[1])
        for i in total:
            total[i] = self.convert_int_to_dollar(total[i])
        return total

    def get_league_users_and_movies(self, league):
        """
        SELECT users.user_name, %s_movies.movie_id
        FROM %s JOIN %s_movies, users
        WHERE %s_movies.id=%s.movie_id and %s.user_id=users.id
        """
        cur = self.db.cursor()
        insert_stmt = ("SELECT users.user_name, "
                       "%s_movies.movie_title, "
                       "%s_movies.release_date, "
                       "%s_movies.foreign_gross, "
                       "%s_movies.domestic_gross, "
                       "%s_movies.worldwide_gross "
                       "FROM %s JOIN %s_movies, users "
                       "WHERE %s_movies.id=%s.movie_id and %s.user_id=users.id")
        data = (league, league, league, league, league, league, league, league, league, league)
        insert = insert_stmt % data
        cur.execute(insert)
        return cur.fetchall()

if __name__ == '__main__':
    db = InteractWithMovieDb()

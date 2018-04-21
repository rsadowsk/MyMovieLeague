from MovieDb import InteractWithMovieDb

# TODO APP script


class GetMyMovies(object):
    def __init__(self, league, user):
        self.league = league
        self.user = user
        self.db = InteractWithMovieDb()
        self.args = self.get_my_movies()
        self.foreign_gross = []
        self.domestic_gross = []
        self.worldwide_gross = []

    def get_my_movies(self):
        return self.db.get_users_movie_from_league(self.league, self.user)

    def get_my_movie_gross(self):
        for movie in self.args:
            movie_gross = self.db.get_movie_from_db(self.league, movie)
            self.foreign_gross.append(movie_gross[0][0])
            self.domestic_gross.append(movie_gross[0][1])
            self.worldwide_gross.append(movie_gross[0][2])

    def get_my_total(self, list_):
        for amount in range(len(list_)):
            if list_[amount] in ['None', 'n/a', 'N/A']:
                list_[amount] = 0
            else:
                list_[amount] = self.convert_dollar_to_int(list_[amount])
        total = sum(list_)
        return self.convert_int_to_dollar(total)

    def get_my_foreign_total(self):
        return self.get_my_total(self.foreign_gross)

    def get_my_domestic_total(self):
        return self.get_my_total(self.domestic_gross)

    def get_my_worldwide_total(self):
        return self.get_my_total(self.worldwide_gross)

    def get_all_my_totals(self):
        ft = self.get_my_foreign_total()
        dt = self.get_my_domestic_total()
        wt = self.get_my_worldwide_total()
        return ["Total","", ft, dt, wt]

    def convert_int_to_dollar(self, dollar):
        return '${:,}'.format(dollar)

    def convert_dollar_to_int(self, dollar):
        dollar = dollar.replace("$", "")
        dollar = dollar.replace(",", "")
        return int(dollar)


if __name__ == "__main__":
    a = GetMyMovies('testleague1', '4')
    a.get_my_movie_gross()
    print a.get_all_my_totals()

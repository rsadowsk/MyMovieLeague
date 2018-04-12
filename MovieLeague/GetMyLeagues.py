from MovieDb import InteractWithMovieDb


class GetMyLeagues(object):
    def __init__(self, user):
        self.user = user    # users json
        self.db = InteractWithMovieDb()

    def get_users_leagues(self):
        my_leagues = []
        leagues = self.db.get_user_leagues(self.user['name'])
        for league in leagues:
            my_leagues.append(self.db.get_league_names(league))
        return my_leagues[0][0]
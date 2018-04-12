from MovieDb import InteractWithMovieDb

class CreateLeague(object):
    def __init__(self, league_name, league_owner, start_date, end_date, end_record):
        self.league_name = league_name
        self.league_owner = league_owner
        self.start_date = start_date
        self.end_date = end_date
        self.end_record = end_record
        self.db = InteractWithMovieDb()

    def create_league(self):
        self.db.add_league_to_leagues(self.league_name,
                                      self.league_owner,
                                      self.start_date,
                                      self.end_date,
                                      self.end_record)
        self.db.create_league_movie_table(self.league_name)
        self.db.create_league_table(self.league_name)

    def check_date(self):
        pass

    def check_league_name(self):
        pass

    def check_league_owner(self):
        pass

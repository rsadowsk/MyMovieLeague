import pymysql.cursors, os
from MovieLeague import app
# TODO APP script


class InteractWithUsersDb(object):
    def __init__(self):
        # TODO hide username and password
        self.db = pymysql.connect(host=app.config['DB_HOST'],
                             user=app.config['DB_USER'],
                             passwd=app.config['DB_PASS'],
                             db=app.config['DB_MOVIEDB'])

    def check_if_user_exists(self, user):
        cur = self.db.cursor()
        insert_stmt = ("SELECT * FROM users WHERE user_name='%s'")
        data = user
        insert = insert_stmt % data
        cur.execute(insert)
        if len(cur.fetchall()) == 0:
            return 0
        else:
            return 1

    def add_user(self, user_name, user_given_name, user_family_name, user_email):
        cur = self.db.cursor()
        insert_stmt = ("INSERT INTO `users` (`user_name`, `user_given_name`, `user_family_name`, `user_email`) VALUES ('%s', '%s', '%s', '%s')")
        data = (user_name, user_given_name, user_family_name, user_email)
        insert = insert_stmt % data
        cur.execute(insert)
        self.db.commit()

    def get_user_info(self, user):
        cur = self.db.cursor()
        insert_stmt = ("SELECT * FROM users WHERE user_name='%s'")
        data = user
        insert = insert_stmt % data
        cur.execute(insert)
        return cur.fetchall()




if __name__ == '__main__':
    db = InteractWithUsersDb()
    #db.add_user('jane doe', 'jane', 'doe', 'janedoe@email.com')
    print db.get_user_info('jane doe')



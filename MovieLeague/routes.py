from flask import Flask, render_template, redirect, url_for, session, jsonify, request, Markup
# TODO add models.py
from CheckUserInfo import InteractWithUsersDb
from flask_oauth import OAuth
from scripts import MLScripts
import json
from forms import CreateLeagueForm, ManageUsersMovies, InviteFriends, LoginForm
from MovieLeague import app, login_manager
from flask_login import login_user, login_required, logout_user, current_user
from CheckUserInfo import users



ALPHA = app.config['ALPHA']
BETA = app.config['BETA']
LIVE = app.config['LIVE']

REDIRECT_URI = '/oauth2callback'  # one of the Redirect URIs from Google APIs console
gREDIRECT = 'home'
add_token = None

scripts = MLScripts()
oauth = OAuth()
google = oauth.remote_app('google',
                          base_url='https://www.google.com/accounts/',
                          authorize_url='https://accounts.google.com/o/oauth2/auth',
                          request_token_url=None,
                          request_token_params={'scope': 'https://www.googleapis.com/auth/userinfo.email',
                                                'response_type': 'code'},
                          access_token_url='https://accounts.google.com/o/oauth2/token',
                          access_token_method='POST',
                          access_token_params={'grant_type': 'authorization_code'},
                          consumer_key=app.config['GOOGLE_ID'],
                          consumer_secret=app.config['GOOGLE_SECRET'])


@app.route("/")
def index():
    if session.get('access_token') is None:
        return render_template("index.html")
    else:
        return redirect(url_for('home'))


@login_manager.user_loader
def load_user(user_id):
    return users.query.get(int(user_id))


# ---GOOGLE SIGNUP CODE--- #
@app.route('/google_signup')
def google_signup():
    db = InteractWithUsersDb()
    access_token = session.get('access_token')
    if access_token is None:
        return redirect(url_for('login'))

    access_token = access_token[0]
    from urllib2 import Request, urlopen, URLError

    headers = {'Authorization': 'OAuth ' + access_token}
    req = Request('https://www.googleapis.com/oauth2/v1/userinfo',
                  None, headers)
    try:
        res = urlopen(req)
    except URLError, e:
        if e.code == 401:
            # Unauthorized - bad token
            session.pop('access_token', None)
            return redirect(url_for('login'))

        return res.read()
    info = json.loads(res.read())
    if db.check_if_user_exists(info['name']):
        pass
    else:
        db.add_user(info['name'], info['given_name'], info['family_name'], info['email'])
    session["json"] = info
    print gREDIRECT
    if gREDIRECT == 'add_user':
        return redirect(url_for(gREDIRECT, token=add_token))
    elif gREDIRECT == 'home':
        return redirect(url_for(gREDIRECT))


@app.route('/login')
def login():
    callback = url_for('authorized', _external=True)
    return google.authorize(callback=callback)


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))


@app.route(REDIRECT_URI)
@google.authorized_handler
def authorized(resp):
    access_token = resp['access_token']
    session['access_token'] = access_token, ''
    return redirect(url_for('google_signup'))


@google.tokengetter
def get_access_token():
    return session.get('access_token')
# --- END GOOGLE SIGNUP CODE--- #


@app.route("/about")
def about():
    return render_template("about_us.html")


@app.route("/my_movies")
def my_movies():
    if session.get('access_token') is None:
        return render_template("index.html")
    my_movies = scripts.my_movies(session['json'])

    return render_template("my_movies.html", my_movies=my_movies)


@app.route("/home")
def home():
    if session.get('access_token') is None:
        return redirect(url_for('google_signup'))
    name = session["json"]["given_name"]
    try:
        wkly5 = scripts.get_weekend_5()
        wkly5 = Markup(wkly5)
    except Exception:
        wkly5 = None
    my_movies = scripts.my_leagues_rankings(session['json'])
    return render_template("home.html", wkly5=wkly5, my_movies=my_movies, name=name)


@app.route("/leagues")
def leagues():
    if session.get('access_token') is None:
        return render_template("index.html")
    elif request.method == "GET":
        my_movies = scripts.my_movies_league_totals_info(session['json'])
        return render_template("leagues.html", my_movies=my_movies)


@app.route("/league/<string:league>")
def league(league):
    if session.get('access_token') is None:
        return render_template("index.html")
    elif request.method == "GET":
        league_info = scripts.get_full_league_stats(league)
        return render_template("league.html", league_info=league_info, league=league)


@app.route("/manage/<string:league>", methods=["GET", "POST"])
def manage(league):
    if session.get('access_token') is None:
        return render_template("index.html")
    form = ManageUsersMovies()
    if request.method == 'POST':
        values = form.ret.data
        scripts.add_user_movie_to_league_list(league, values)
        users, users_json = scripts.get_league_users(league, json=True)
        movies, movies_json = scripts.get_all_league_movies(league, json=True)
        return render_template("manage.html", league=league, form=form, users=users,
                               users_json=users_json, movies=movies, movies_json=movies_json)
    elif request.method == "GET":
        users, users_json = scripts.get_league_users(league, json=True)
        movies, movies_json = scripts.get_all_league_movies(league, json=True)
        return render_template("manage.html", league=league, form=form, users=users,
                               users_json=users_json, movies=movies, movies_json=movies_json)


@app.route('/UnderConstruction')
def under_construction():
    return render_template("under_construction.html")


@app.route("/create_league", methods=["GET", "POST"])
def create_league():
    form = CreateLeagueForm()
    if request.method == 'POST':
        if not form.validate():
            return render_template('create_league.html', form=form)
        else:
            league_name = form.league_name.data
            owner = session["json"]["name"]
            start_date = form.start_date.data
            end_date = form.end_date.data
            end_record = form.end_record.data
            try:
                print league_name, owner, start_date, end_date, end_record
                scripts.create_league(league_name, owner, start_date, end_date, end_record)
            except Exception:
                # TODO add errors for db creation exceptions
                return render_template('create_league.html', form=form)
            return redirect(url_for('success'))
    elif request.method == 'GET':
        return render_template('create_league.html', form=form)


@app.route('/success')
def success():
    return render_template('success.html')


@app.route('/invite_friend/<string:league>', methods=["GET", "POST"])
def invite_friend(league):
    if session.get('access_token') is None:
        return render_template("index.html")
    form = InviteFriends()
    if request.method == 'POST':
        info = request.form.to_dict(flat=False)
        emails = info['email']
        sender = session["json"]["name"]
        if ALPHA:
            return redirect(url_for('under_construction'))
        scripts.send_invite_friend_email(sender, league, emails)
        return render_template('invite_friend.html', league=league)

    elif request.method == 'GET':
        return render_template('invite_friend.html', league=league, form=form)


@app.route('/add_user/<token>')
def add_user(token):
    global gREDIRECT
    global add_token
    if session.get('access_token') is None:
        gREDIRECT = 'add_user'
        add_token = token
        return redirect(url_for('google_signup'))
    scripts.add_user_to_league_by_token(session['json'], token)
    return render_template('added.html')


@app.route('/test')
def test():
    return render_template('test.html')


@app.route('/about_us')
def about_us():
    return render_template('about_us.html')


@app.route('/contact_us')
def contact_us():
    return render_template('contact_us.html')


@app.route('/sitemap')
def sitemap():
    return render_template('sitemap.html')


@app.route('/privacy')
def privacy():
    return render_template('privacy.html')


def main():
    app.run()


if __name__ == '__main__':
    main()

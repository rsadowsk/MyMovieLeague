from flask import Flask
from GetMovieMojoGross import GetMovieData
app = Flask(__name__)

@app.route("/")
def index():
    return "Hi"


@app.route("/movie/<movieID>")
def movie(movieID):
    movie = GetMovieData(movieID)
    movie_data = movie.find_movie_gross_html()
    print movie_data
    return str(movie_data)

if __name__ == "__main__":
    app.run(debug=True)


from flask import Flask, session, render_template, request, redirect, jsonify
from flask_session import Session
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
import sys, os, requests

app = Flask(__name__)

# Check for environment variable
if not os.getenv("DATABASE_URL"):
    raise RuntimeError("DATABASE_URL is not set")

# Configure session to use filesystem
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Set up database
engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))


@app.route("/")
def index():
    if session == {}:
        loggedin=False
    else:
        loggedin=True
    return render_template("home.html",loggedin=loggedin)

@app.route("/register",methods=["GET","POST"])
def register():
    if session != {}:
        loggedin=True
        return render_template("error.html",msg="User is currently logged in",loggedin=loggedin)
    else:
        loggedin=False
        if request.method == "GET":
            return render_template("register.html",loggedin=loggedin)
        else:
            username=request.form.get("username")
            email=request.form.get("email")
            password=request.form.get("password")
            check=db.execute("SELECT * FROM users WHERE username=:username",{"username":username}).fetchone()
            if check is not None:
                return render_template("error.html",msg="Username already Exists",loggedin=loggedin)
            db.execute("INSERT INTO users (username,email,password) VALUES (:username, :email, :password)",
                            {"username":username,"email":email,"password":password})
            db.commit()
            return redirect("/login")



@app.route("/login",methods=["GET","POST"])
def login():
    if session != {}:
        loggedin=True
        return render_template("error.html",msg="User is currently logged in",loggedin=loggedin)
    else:
        loggedin=False
        if request.method == "GET":
            return render_template("login.html")
        else:
            uname=request.form.get("username")
            details=db.execute("SELECT userid, password FROM users WHERE username=:username",{"username": uname}).fetchone()
            if details is None:
                return render_template("error.html",msg="No registered account with that username",loggedin=loggedin)
            if details.password != request.form.get("password"):
                return render_template("error.html",msg="Invalid username password combination",loggedin=loggedin)
            session["userid"]=details.userid
            session["username"]=uname
            return redirect("/search")

@app.route("/logout",methods=["GET"])
def logout():
    session.pop('userid')
    session.pop('username')
    return redirect("/")

@app.route("/search",methods=["GET","POST"])
def search():
    if session == {}:
        loggedin=False
        return render_template("error.html",msg="Please login to view this page",loggedin=loggedin)
    else:
        loggedin=True
        if request.method == "GET":
            return render_template("search.html",result=False,loggedin=loggedin)
        else:
            query=request.form.get("books")
            query='%'+query+'%'
            books=db.execute("SELECT * FROM books WHERE isbn LIKE :query OR title LIKE :query OR author like :query",{"query": query}).fetchall()
            if books == []:
                return render_template("error.html",msg="No matching books found",loggedin=loggedin)
            return render_template("search.html",result=True,books=books,loggedin=loggedin)

@app.route("/book/<string:isbn>",methods=["GET","POST"])
def book(isbn):
    if session == {}:
        loggedin=False
        return render_template("error.html",msg="Please login to view this page",loggedin=loggedin)
    else:
        loggedin=True
        condition=db.execute("SELECT * FROM reviews WHERE username=:username AND isbncode=:isbncode",{"username":session["username"],"isbncode":isbn}).fetchone()
        if condition is None:
            review_submitted=False
        else:
            review_submitted=True
        print(review_submitted,file=sys.stdout)
        bookdetails=db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
        res = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Ar7TRYAHFR10pt7SsndPAQ", "isbns": isbn})
        obj = res.json()
        number_of_ratings = obj['books'][0]['work_ratings_count']
        average_rating = obj['books'][0]['average_rating']
        allreviews=db.execute("SELECT * FROM reviews WHERE isbncode=:isbncode",{"isbncode":isbn}).fetchall()
        if allreviews == []:
            showreview=False
        else:
            showreview=True
        if request.method=="GET":
            return render_template("bookdetails.html",bookdetails=bookdetails,number_of_ratings=number_of_ratings,average_rating=average_rating,review_submitted=review_submitted,allreviews=allreviews,showreview=showreview,loggedin=loggedin)
        else:
            rating=request.form.get("rating")
            review=request.form.get("review")
            db.execute("INSERT INTO reviews (username, isbncode, rating, review) VALUES (:username, :isbncode, :rating, :review)",
                            {"username":session["username"],"isbncode":isbn,"rating":rating,"review":review })
            db.commit()
            return redirect("/book/"+isbn)

@app.route("/api/<string:isbn>",methods=["GET"])
def api(isbn):
    bookinfo=db.execute("SELECT * FROM books WHERE isbn=:isbn", {"isbn":isbn}).fetchone()
    if bookinfo is None:
        return jsonify({"error": "Invalid isbn"}), 404
    r = requests.get("https://www.goodreads.com/book/review_counts.json", params={"key": "Ar7TRYAHFR10pt7SsndPAQ", "isbns": isbn})
    jsobj = r.json()
    d={}
    d["title"]=bookinfo.title
    d['author']=bookinfo.author
    d['year']=int(bookinfo.year)
    d['isbn']=bookinfo.isbn
    d['review_count']=int(jsobj['books'][0]['work_ratings_count'])
    d['average_score']=float(jsobj['books'][0]['average_rating'])
    return jsonify(d)

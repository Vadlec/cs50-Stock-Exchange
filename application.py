import os
import time
from datetime import datetime
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")

try:
    os.environ['API_KEY'] = 'pk_e93baebace7b4fdfac16236c78fa6c59'
except e:
    raise RuntimeError(e)

# Make sure API key is set
if not os.environ.get("API_KEY"):
    raise RuntimeError("API_KEY not set")


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""
    cash = db.execute('SELECT cash FROM users WHERE id = (?)', session["user_id"])[0]['cash']
    purchases = db.execute(
        'SELECt symbol, SUM(amount) AS amount from purchases WHERE user_id = (?) GROUP BY symbol', session["user_id"])
    sales = db.execute('SELECt symbol, SUM(amount) AS amount from sales WHERE user_id = (?) GROUP BY symbol', session["user_id"])
    # print(purchases, flush=True)

    symbols = getCurrentState()

    result = []
    total_share_value = 0
    for symbol in symbols:
        share_info = lookup(symbol['symbol'])
        share_info['amount'] = symbol['amount']
        share_info['total'] = symbol['amount'] * share_info['price']
        total_share_value += share_info['total']
        share_info['total'] = str("${:.2f}".format(share_info['total']))
        share_info['price'] = str("${:.2f}".format(share_info['price']))
        result.append(share_info)
        # print(result, flush=True)

    return render_template('index.html', cash=usd(cash), shares=result, total=usd(total_share_value + cash))


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == 'POST':
        if not request.form.get("symbol"):
            return apology("must provide quote", 400)
        elif not request.form.get("shares"):
            return apology("must provide share", 400)
        else:
            try:
                int(request.form.get("shares"))
            except ValueError:
                return apology("ValueError", 400)
            shares = int(request.form.get('shares'))
            if shares < 1:
                return apology("share must be a positive number", 400)
            result = lookup(request.form.get("symbol"))
            if not result:
                return apology('Invalid Symbol', 400)
            else:
                cash = db.execute('SELECT cash FROM users WHERE id = (?)', session["user_id"])[0]['cash']
                total = result['price'] * shares
                if (total > cash):
                    return apology('Not enough cash', 400)
                else:
                    newCash = cash - total
                    db.execute('INSERT INTO purchases (user_id, symbol, unit_price, amount) VALUES(?, ?, ?, ?)',
                               session["user_id"], request.form.get("symbol").upper(), result['price'], shares)
                    db.execute('UPDATE users SET cash = (?) WHERE id = (?)', newCash, session["user_id"])
                    return redirect('/')
    else:
        return render_template('buy.html')


@app.route("/history")
@login_required
def history():
    purchases = db.execute('SELECT symbol, amount, unit_price, timestamp FROM purchases WHERE user_id = (?)', session['user_id'])

    sales = db.execute('SELECT symbol, amount, unit_price, timestamp  FROM sales WHERE user_id = (?)', session['user_id'])

    for x in sales:
        x['amount'] *= -1
        purchases.append(x)
    date_format = '%Y-%m-%d %H:%M:%S'
    purchases.sort(key=lambda x: datetime.strptime(x['timestamp'], date_format), reverse=True)

    """Show history of transactions"""
    return render_template('history.html', transactions=purchases)


@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/quote", methods=["GET", "POST"])
@login_required
def quote():
    if request.method == "POST":
        result = lookup(request.form.get('symbol'))
        if result:
            result['price'] = str("${:.2f}".format(result['price']))
            return render_template('quoted.html', result=result)
        else:
            return apology('invalid symbol', 400)
    else:
        return render_template('quote.html')
    """Get stock quote."""
    return apology("TODO")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":
        # Ensure username was submitted
        username = ''
        if not request.form.get("username"):
            return apology("must provide username", 400)
        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 400)
        elif not request.form.get("confirmation"):
            return apology("must provide password confirmation", 400)

        elif request.form.get("password") != request.form.get("confirmation"):
            return apology('passwords must match', 400)
        else:
            username = request.form.get("username")
            names = db.execute("SELECT username FROM users WHERE username = (?)", username)
            print(names, flush=True)
            jeMoPalFound = 0
            for name in names:
                if name['username'] == username:
                    jeMoPalFound = 1
                    break
            if jeMoPalFound == 1:
                return apology('this name has already taken', 400)

            else:
                hashed = generate_password_hash(request.form.get("password"))
                db.execute('INSERT OR IGNORE INTO users (username, hash) VALUES(?, ?)', username.lower(), hashed)
                return redirect('/')

    else:
        return render_template('register.html')


@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():

    current_shares = getCurrentState()
    if request.method == 'POST':
        """Sell shares of stock"""
        if not request.form.get("symbol"):
            return apology("must provide symbol", 400)
        elif not request.form.get("shares"):
            return apology("must provide share", 400)
        else:
            found = 0
            current_share_amount = 0

            # Look if user owns the share which he/she is trying to sell.
            for share in current_shares:
                if request.form.get("symbol") == share['symbol']:
                    found = 1
                    current_share_amount = share['amount']
                    break
            if found == 0:
                return apology('invalid Symbol')
            shares = int(request.form.get('shares'))
            if shares < 1:
                return apology("share must be a positive number", 403)

            # Lookup the symbol to get current price.
            result = lookup(request.form.get("symbol"))
            if shares > current_share_amount:
                return apology('Too many shares', 400)
            if not result:
                return apology('Invalid Symbol', 400)
            else:

                cash = db.execute('SELECT cash FROM users WHERE id = (?)', session["user_id"])[0]['cash']  # users current cash.
                total = result['price'] * shares  # value of the shares user trying to sell.
                newCash = cash + total
                db.execute('INSERT INTO sales (user_id, symbol, unit_price, amount) VALUES(?, ?, ?, ?)',
                           session["user_id"], request.form.get("symbol").upper(), result['price'], shares)
                db.execute('UPDATE users SET cash = (?) WHERE id = (?)', newCash, session["user_id"])
                return redirect('/')
    else:
        return render_template('sell.html', shares=current_shares)


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)


def getCurrentState():
    # Get current shares by taking difference between purchases and sales.
    purchases = db.execute(
        'SELECT symbol, SUM(amount) AS amount from purchases WHERE user_id = (?) GROUP BY symbol', session["user_id"])
    sales = db.execute('SELECT symbol, SUM(amount) AS amount from sales WHERE user_id = (?) GROUP BY symbol', session["user_id"])

    for sale in sales:
        for purchase in purchases:
            if sale['symbol'] == purchase['symbol']:
                purchase['amount'] -= sale['amount']

    def condition(dic):
        return dic['amount'] > 0

    # Filter shares whose value are 0
    purchases = [d for d in purchases if condition(d)]
    return purchases
import os
import time


from cs50 import SQL
from datetime import datetime
from decimal import Decimal
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask import Flask, render_template, request, session, redirect, url_for
from helpers import apology, login_required, lookup, usd
import sqlite3

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///finance.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
@login_required
def index():
    """Show portfolio of stocks"""

    cash_balance = db.execute("SELECT cash FROM users WHERE id =:user_id",
                              user_id=session["user_id"])[0]['cash']
    if cash_balance == None:
        return apology("You have no cash balance")
    username = db.execute("SELECT username FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]['username']
    portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id",
                           user_id=session["user_id"])
    stocks = []

    total_value = 0
    for portfolio in portfolio:
        symbol = portfolio['symbol']
        stock = lookup(symbol)
        if stock is None:
            return apology("Invalid stock symbol")
        total = int(portfolio['shares']) * stock["price"]
        total_value += total
        stocks.append(
            {'symbol': portfolio['symbol'], 'shares': portfolio['shares'], 'price': stock["price"], 'total': total})

    total_cash = cash_balance + total_value
    print(f"Cash Balance: {cash_balance}")
    print(f"Total Value: {total_value}")
    print(f"Total Cash: {total_cash}")
    return render_template("index.html", stocks=stocks, username=username, cash_balance=cash_balance, total_cash=total_cash)


@app.route("/buy", methods=["GET", "POST"])
@login_required
def buy():
    """Buy shares of stock"""
    if request.method == "GET":
        return render_template("buy.html")

    if request.method == "POST":

        shares = request.form.get("shares")

        if not shares:
            return apology("Please enter number of shares")

        try:
            shares_float = float(shares)
        except ValueError:
            return apology("Please enter a number")

        if shares_float < 1:
            return apology("Please enter a valid number")

        if shares_float != int(shares_float):
            return apology("Please enter a whole number")

        shares = int(shares)
        current_time = datetime.now()
        symbol = request.form.get("symbol")
        if symbol == None:
            return apology("Please enter a valid Stock Symbol")
        stock = lookup(symbol)
        if not stock:
            return apology("Please enter a Stock Symbol")

        if isinstance(stock["price"], (int, float)) and isinstance(shares, (int, float)):
            cash_balance = db.execute("SELECT cash FROM users WHERE id =:user_id",
                                      user_id=session["user_id"])[0]['cash']
            cost_shares = Decimal(shares) * Decimal(stock["price"])
            cash_aftershares = (Decimal(cash_balance) - cost_shares).quantize(Decimal('0.00'))
            print(f"Cash Balance: {cash_balance}")
            print(f"Cost shares: {cost_shares}")
            print(f"Cash after shares: {cash_aftershares}")
        else:
            return apology("Invalid input", 400)

        cost_shares = round(cost_shares, 2)
        cash_aftershares = round(cash_aftershares, 2)
        cash_aftershares = float(cash_aftershares)
        cost_shares = float(cost_shares)
        if cash_aftershares < 0:
            return apology("You dont have enough cash balance")

        db.execute("UPDATE users SET cash = :cash WHERE id =:user_id",
                   user_id=session["user_id"], cash=cash_aftershares)

        portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                               user_id=session["user_id"], symbol=symbol)
        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, value, date_purchase, transaction_type) VALUES(:user_id, :symbol, :shares, :price, :value, :date_purchase, :transaction_type)",
                   user_id=session["user_id"], symbol=symbol, shares=int(shares), value=cost_shares, price=stock["price"], date_purchase=current_time, transaction_type="buy")

        if not portfolio:
            db.execute("INSERT INTO portfolio (user_id, symbol, shares, price, value) VALUES(:user_id, :symbol, :shares, :price, :value)",
                       user_id=session["user_id"], symbol=symbol, shares=shares, value=cost_shares, price=stock["price"])
        else:
            result = db.execute("SELECT value, shares FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                                user_id=session["user_id"], symbol=symbol)
            total_cost = (stock["price"] * shares) + result[0]["value"]
            total_shares = shares + result[0]["shares"]
            average_cost = total_cost / total_shares
            db.execute("UPDATE portfolio SET shares = :shares, price = :price, value = :value WHERE user_id = :user_id AND symbol = :symbol",
                       user_id=session["user_id"], symbol=symbol, shares=total_shares, price=stock["price"], value=total_cost)

        return redirect(url_for('index'))


@app.route("/history")
@login_required
def history():
    """Show history of transactions"""
    username = db.execute("SELECT username FROM users WHERE id = :user_id",
                          user_id=session["user_id"])[0]['username']
    transactions = db.execute(
        "SELECT * FROM transactions WHERE user_id =:user_id ORDER BY date_purchase", user_id=session["user_id"])

    total_value = round(0, 2)
    for transaction in transactions:
        if transaction['transaction_type'] == "sell":
            total_value -= transaction["value"]
        elif transaction['transaction_type'] == "buy":
            total_value += transaction["value"]

    return render_template("history.html", transactions=transactions, total=total_value, username=username)


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
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
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
    """Get stock quote."""
    if request.method == "GET":
        return render_template("quote.html")

    if request.method == "POST":
        symbol = request.form.get("symbol")
        stock = lookup(symbol)

    if stock == None:
        return apology("Lookup unsuccsessful")

    else:
        return render_template("quoted.html", stock=stock)


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "GET":
        return render_template("register.html")

    if request.method == "POST":

        username = request.form.get("username")
        if not username:
            return apology("Please enter a username")

        user_exists = db.execute(
            "SELECT * FROM users WHERE username = :username", username=username)
        if user_exists:
            return apology("Username is taken, please enter a valid username")

        password = request.form.get("password")
        if not password:
            return apology("Please enter a password")

        if len(password) < 6:
            return apology("Your password must have at least 6 caracters")

        password_confirmation = request.form.get("confirmation")
        if password_confirmation != password:
            return apology("Your password confirmation does not match your password")

        hashed_password = generate_password_hash(password)
        db.execute("INSERT INTO users (hash, username) VALUES(?, ?)", hashed_password, username)
    else:
        return render_template('register.html')

    return redirect(url_for('login'))

@app.route("/sell", methods=["GET", "POST"])
@login_required
def sell():
    """Sell shares of stock"""
    if request.method == "GET":
        symbols = db.execute(
            "SELECT symbol FROM portfolio WHERE user_id = :user_id", user_id=session["user_id"])
        return render_template("sell.html", symbols=symbols)

    if request.method == "POST":

        shares = int(request.form.get("shares"))

        if not shares:
            return apology("Please enter number of shares")

        if shares < 1:
            return apology("Please enter a valid number")

        symbol = request.form.get("symbol")
        stock = lookup(symbol)
        portfolio = db.execute("SELECT * FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                               user_id=session["user_id"], symbol=symbol)
        current_time = datetime.now()

        if not stock:
            return apology("Please enter a Stock Symbol")
        if not portfolio:
            return apology("This stock is not in your portfolio")
        if shares > portfolio[0]['shares']:
            return apology("Unsufficient shares")

        cash_balance = db.execute("SELECT cash FROM users WHERE id =:user_id",
                                  user_id=session["user_id"])[0]['cash']
        cost_shares = shares * stock["price"]
        cash_aftershares = cash_balance + cost_shares

        db.execute("UPDATE users SET cash = :cash WHERE id =:user_id",
                   user_id=session["user_id"], cash=cash_aftershares)

        db.execute("INSERT INTO transactions (user_id, symbol, shares, price, value, date_purchase, transaction_type) VALUES(:user_id, :symbol, :shares, :price, :value, :date_purchase, :transaction_type)",
                   user_id=session["user_id"], symbol=symbol, shares=shares, value=cost_shares, price=stock["price"], date_purchase=current_time, transaction_type="sell")

        db.execute("UPDATE portfolio SET shares = shares - :shares, value = value - :value WHERE user_id = :user_id AND symbol = :symbol",
                   user_id=session["user_id"], symbol=symbol, shares=shares, value=cost_shares)
# if there are 0 shares from this stock, remove line
        updated_portfolio = db.execute(
            "SELECT * FROM portfolio WHERE user_id = :user_id AND symbol = :symbol", user_id=session["user_id"], symbol=symbol)
        if updated_portfolio[0]['shares'] < 1:
            db.execute("DELETE FROM portfolio WHERE user_id = :user_id AND symbol = :symbol",
                       user_id=session["user_id"], symbol=symbol)

        return redirect(url_for('index'))

@app.route("/change_password", methods=["GET", "POST"])
@login_required
def change_password():
    if request.method == "GET":
        return render_template("change_password.html")

    if request.method == "POST":

        current_password = request.form.get("password")
        if not current_password:
            return apology("Please enter your current password")

        new_password = request.form.get("new_password")
        if not new_password:
            return apology("Please enter your new password")

        if len(new_password) < 6:
            return apology("Your new password must have at least 6 caracters")

        confirm_new_password = request.form.get("confirm_new_password")
        if confirm_new_password != new_password:
            return apology("Your password confirmation does not match your password")

        username = db.execute("SELECT username FROM users WHERE id = :user_id",
                              user_id=session["user_id"])[0]['username']
        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash=:hash_password WHERE id = :user_id",
                   hash_password=hashed_password, user_id=session["user_id"])
    else:
        return render_template('change_password.html')

    return redirect(url_for('login'))

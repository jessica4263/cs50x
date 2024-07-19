        db.execute("UPDATE users SET cash = :cash WHERE id =:user_id", user_id=session["user_id"], cash=cash_aftershares)

        portfolio = db.execute("SELECT symbol FROM portfolio WHERE user_id =:user_id", user_id=session["user_id"])
        total = int(portfolio['shares']) * portfolio['price']



    check = db.execute("SELECT * FROM lists WHERE id =:user_id",
                              user_id=session["user_id"])
    if check == None:
        return apology("You have no lists")


                <script>
            fetch('/create.html')
            .then(response => response.text())
            .then(data => {
                document.getElementById('yourModalElement').innerHTML = data;
            });
        </script>

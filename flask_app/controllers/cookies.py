from flask_app import app
from flask import Flask, render_template,redirect,request,session,flash
from flask_app.models.cookie import Cookie

@app.route("/")
def index():
    return redirect('/cookies')

@app.route('/cookies')
def cookies():
    # call the get all classmethod to get all users
    orders = Cookie.get_all()
    print(orders)
    return render_template("cookies.html", orders = orders)

@app.route('/cookies/new')
def new_cookies():
    return render_template("create.html")


@app.route('/cookies/create', methods=["POST"])
def create_cookie():
    # First we make a data dictionary from our request.form coming from our template.
    # The keys in data need to line up exactly with the variables in our query string.
    data = {
        "name": request.form["name"],
        "cookie_type" : request.form["cookie_type"],
        "num_of_boxes" : request.form["num_of_boxes"]
    }
    # We pass the data dictionary into the save method from the Friend class.
    if not Cookie.validate_user(request.form):
        # redirect to the route where the burger form is rendered.
        return redirect('/cookies/new')
    Cookie.save(data)
    # Don't forget to redirect after saving to the database.
    return redirect('/cookies')
            
@app.route('/cookies/edit/<int:id>')
def edit(id):
    order = Cookie.get_one(id)
    return render_template('edit.html', order=order)

@app.route('/cookies/edit/<int:id>',methods=['POST'])
def update_user(id):
    cookie = request.form
    if not Cookie.validate_user(cookie):
        return redirect(f"/cookies/edit/{id}")
    Cookie.update(cookie)
    return redirect('/cookies')

@app.route('/cookies/show/<int:id>')
def show(id):
    data ={
        "id": id
    }
    return render_template('show.html', cookies = Cookie.get_one(data))

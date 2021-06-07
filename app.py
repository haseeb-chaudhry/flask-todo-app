from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todos.db"
db = SQLAlchemy(app)

# todomode


class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    owner = db.Column(db.String(128), nullable=False)
    content = db.Column(db.String(200), nullable=False)
    is_completed = db.Column(db.Boolean, nullable=False, default=False)
    deadline = db.Column(db.String(300), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.now())

    def __init__(self, owner, content, deadline):
        self.owner = owner
        self.content = content
        self.deadline = deadline

    def __repr__(self):
        return '<Task %r>' % self.id


if(not os.path.isfile('todos.db')):
    db.create_all()
else:
    "data base already exists"
# routes


@app.route("/")
def index():
    todos_all = Todo.query.all()
    return render_template("todos.html", todos=todos_all)


@app.route("/create", methods=['GET', 'POST'])
def create():
    if request.method == "POST":
        owner_name = request.form['ownername']
        message = request.form['todotask']
        deadline = request.form['tododeadline']
        todo = Todo(owner_name, message, deadline)
        try:
            db.session.add(todo)
            db.session.commit()
            return redirect("/")
        except Exception as error:
            return str(error)
    else:
        return render_template("create.html")


@app.route("/delete/<int:id>")
def delete(id):
    target_todo = Todo.query.get_or_404(id)
    try:
        db.session.delete(target_todo)
        db.session.commit()
        return redirect("/")
    except Exception as error:
        return str(error)
    return str(id)


if __name__ == "__main__":
    app.run(debug=True)

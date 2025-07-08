from flask import Flask, render_template, redirect, request
from flask_scss import Scss
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
Scss(app)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///task_database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATION"] = False # deployment step
db = SQLAlchemy(app)

# Data Class ~ row of data
class MyTask(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(100), nullable=False)
    completed = db.Column(db.Integer, default=0)
    created = db.Column(db.DateTime, default=datetime.now)

    def __repr__(self) -> str:
        return f"Task {self.id}"


# creating the database during app deployment
with app.app_context():
    db.create_all()


# Homepage
@app.route("/", methods=["POST", "GET"])
def index():
    # Add task
    if request.method == "POST":
        current_task = request.form['content'] # in the form in the html the content
        new_task = MyTask(content=current_task)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"ERROR: {e}")
            return f"ERROR: {e}"
    # View all current tasks
    else:
        tasks = MyTask.query.order_by(MyTask.created).all()
        return render_template("index.html", tasks=tasks)


# Edit Task
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id: int):
    edit_task = MyTask.query.get_or_404(id)
    if request.method == "POST":
        edit_task.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            print(f"EDIT ERROR: {e}")
            return f"EDIT ERROR: {e}"
    else:
        return render_template("/edit.html", task=edit_task)


# Delete Task
@app.route("/delete/<int:id>")
def delete(id: int):
    delete_task = MyTask.query.get_or_404(id)
    try:
        db.session.delete(delete_task)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        print(f"DELETE ERROR: {e}")
        return f"DELETE ERROR: {e}"


if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
        
    app.run(debug=True)#, host="0.0.0.0", port=80)
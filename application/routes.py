from application import app, db
from application.models import Assignees, Tasks
from application.forms import AssigneeForm, TaskForm
from flask import render_template, request, redirect, url_for

@app.route("/")
@app.route("/home")
def home():
    all_tasks = Tasks.query.all()
    return render_template("index.html", title="Home", all_tasks=all_tasks)

@app.route("/create", methods=["GET","POST"])
def create():
    assignees = []
    for assignee in Assignees.query.all():
        assignees.append((assignee.id, f"{assignee.forename}, {assignee.surname}"))
    form = TaskForm()
    form.assignee.choices = assignees

    if request.method == "POST":
        if form.validate_on_submit():
            app.logger.info(form.assignee.data)
            new_task = Tasks(
                assignee=Assignees.query.filter_by(id=form.assignee.data).first(),
                description=form.description.data
            )
            db.session.add(new_task)
            db.session.commit()
            return redirect(url_for("home"))

    return render_template("add.html", title="Create a Task", form=form)

@app.route("/new_assignee", methods=["GET","POST"])
def new_assignee():
    form = AssigneeForm()
    if request.method == "POST":
        if form.validate_on_submit():
            new_assignee = Assignees(
                forename=form.forename.data,
                surname=form.surname.data
            )
            db.session.add(new_assignee)
            db.session.commit()
            return redirect(url_for("home"))
    return render_template("new_assignee.html", title="Add a New Assignee", form=form)

@app.route("/complete/<int:id>")
def complete(id):
    task = Tasks.query.filter_by(id=id).first()
    task.completed = True
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/incomplete/<int:id>")
def incomplete(id):
    task = Tasks.query.filter_by(id=id).first()
    task.completed = False
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    form = TaskForm()
    task = Tasks.query.filter_by(id=id).first()
    if request.method == "POST":
        task.description = form.description.data
        db.session.commit()
        return redirect(url_for("home"))
    return render_template("update.html", form=form, title="Update Task", task=task)

@app.route("/delete/<int:id>")
def delete(id):
    task = Tasks.query.filter_by(id=id).first()
    db.session.delete(task)
    db.session.commit()
    return redirect(url_for("home"))

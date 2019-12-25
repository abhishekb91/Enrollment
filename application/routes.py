from flask import render_template, request, redirect, flash, url_for, session

from application import app
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm
from application.course_list import course_list


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)


@app.route("/courses")
@app.route("/courses/<term>")
def courses(term=None):
    if not term:
        term = 'Spring 2019'

    classes = Course.objects().order_by('courseID')
    return render_template("courses.html", course_data=classes, courses=True, term=term)


@app.route("/register", methods=['GET', 'POST'])
def register():
    if session.get('user_id'):
        return redirect(url_for('index'))

    form = RegisterForm(request.form)

    if form.validate_on_submit():
        user_id = User.objects.count()
        user_id += 1
        email = form.email.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        user = User(user_id=user_id, email=email, first_name=first_name, last_name=last_name)
        user.set_password(password=password)

        user.save()

        flash('You are successfully registered', category='success')
        return redirect(url_for('index'))

    return render_template("register.html", form=form, register=True)


@app.route("/login", methods=['GET', 'POST'])
def login():
    if session.get('user_id'):
        return redirect(url_for('index'))

    form = LoginForm(request.form)

    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()

        if user and user.get_password(form.password.data):
            flash(f"{user.first_name}, you are successfully logged in!", category="success")
            session['user_id'] = user.user_id
            session['username'] = user.first_name
            return redirect(url_for("index"))
        else:
            flash("Sorry, something went wrong.", category="danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('username', None)
    return redirect(url_for('index'))


@app.route("/enrollment", methods=['GET', 'POST'])
def enrollment():
    if not session.get('user_id'):
        return redirect(url_for('login'))

    courseID =request.form.get('courseId')
    courseTitle = request.form.get('title')
    user_id = session.get('user_id')

    if courseID:
        if Enrollment.objects(user_id=user_id, courseID=courseID):
            flash(f"Oops! You are already registered in this course {courseTitle}!", "danger")
            return redirect(url_for("courses"))
        else:
            Enrollment(user_id=user_id, courseID=courseID).save()
            flash(f"You are enrolled in {courseTitle}!", "success")

    classes = course_list(user_id=user_id)

    return render_template("enrollment.html", enrollment=True, title="Enrollment", classes=classes)


@app.route('/user')
def user():
    users = User.objects.all()
    return render_template('user.html', users=users)


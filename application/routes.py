from flask import render_template, request, Response, json, redirect, flash, url_for

from application import app
from application.models import User, Course, Enrollment
from application.forms import LoginForm, RegisterForm

course_data = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)


@app.route("/courses")
def courses():
    return render_template("courses.html", course_data=course_data, courses=True)


@app.route("/register", methods=['GET', 'POST'])
def register():
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
    form = LoginForm(request.form)

    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()

        if user and user.get_password(form.password.data):
            flash(f"{user.first_name}, you are successfully logged in!", category="success")
            return redirect(url_for("index"))
        else:
            flash("Sorry, something went wrong.", category="danger")
    return render_template("login.html", title="Login", form=form, login=True)


@app.route("/enrollment", methods=['GET', 'POST'])
def enrollment():
    form_data = {
        'id': request.form.get('courseId'),
        'title': request.form.get('title'),
        'term': request.form.get('term')
    }
    return render_template("enrollment.html", login=True, data=form_data)


@app.route('/api/')
@app.route('/api/<idx>')
def api(idx=None):
    if not idx:
        j_data = course_data
    else:
        j_data = {}

        for course in course_data:
            if course['courseID'] == idx:
                j_data = course
                break

    return Response(json.dumps(j_data), mimetype='application/json')


@app.route('/user')
def user():
    # User(user_id=1, first_name='Christian', last_name='Bale', email='cbale@gmail.com', password='abcd').save()
    # User(user_id=2, first_name='Mary', last_name='Jane', email='mjane@gmail.com', password='abcd').save()

    users = User.objects.all()
    return render_template('user.html', users=users)


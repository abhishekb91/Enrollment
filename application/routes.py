from application import app
from flask import render_template, request, Response, json

course_data = [{"courseID":"1111","title":"PHP 101","description":"Intro to PHP","credits":3,"term":"Fall, Spring"}, {"courseID":"2222","title":"Java 1","description":"Intro to Java Programming","credits":4,"term":"Spring"}, {"courseID":"3333","title":"Adv PHP 201","description":"Advanced PHP Programming","credits":3,"term":"Fall"}, {"courseID":"4444","title":"Angular 1","description":"Intro to Angular","credits":3,"term":"Fall, Spring"}, {"courseID":"5555","title":"Java 2","description":"Advanced Java Programming","credits":4,"term":"Fall"}]

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html", index=True)


@app.route("/courses")
def courses():
    return render_template("courses.html", course_data=course_data, courses=True)


@app.route("/register")
def register():
    return render_template("register.html", register=True)


@app.route("/login")
def login():
    return render_template("login.html", login=True)


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

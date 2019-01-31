"""A web application for tracking projects, students, and student grades."""

from flask import Flask, request, render_template

import hackbright

app = Flask(__name__)

@app.route("/")
def display_homepage():
    """Display homepage"""
    students = hackbright.student_list()
    projects = hackbright.project_list()

    return render_template("index.html",
                            students=students,
                            projects=projects)


@app.route("/student_search")
def get_student_form():
    """Show form for searching for a student."""

    return render_template("student_search.html")

@app.route("/student")
def get_student():
    """Show information about a student."""

    github = request.args.get('github')

    first, last, github = hackbright.get_student_by_github(github)
    project_info = hackbright.get_grades_by_github(github)

    # print('project title', project_title)
    # print('grade', grade)

    html = render_template("student_info.html",
                            first=first,
                            last=last,
                            github=github,
                            project_info=project_info)

    return html

@app.route("/add_student")
def add_student():
    """Show form for searching for a student."""

    return render_template('add_student.html')

@app.route("/student_added", methods=['POST'])
def show_added_student():
    """Getting input from user to add a student"""

    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    github = request.form.get('github')


    hackbright.make_new_student(first_name, last_name, github)

    first, last, github = hackbright.get_student_by_github(github)

    return render_template("added_student.html",
                            first=first,
                            last=last,
                            github=github)

@app.route("/project")
def show_project_info():
    """SHow info"""
    project_title = request.args.get('p_title')
    title, description, max_grade = hackbright.get_project_by_title(project_title)

    project_grades_list = hackbright.get_grades_by_title(project_title)
    """returning github and grades"""
    # first_list = []
    # last_list = []
    new_grades_list = []

    for students_github in project_grades_list:
        github = students_github[0]
        first, last, github=hackbright.get_student_by_github(github)
        new_grades_list.append((first, last, students_github[1]))

    return render_template("project_display.html", 
                            title=title, 
                            description=description,
                            max_grade=max_grade,
                            new_grades_list=new_grades_list)



if __name__ == "__main__":
    hackbright.connect_to_db(app)
    app.run(debug=True)

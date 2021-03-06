from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, render_template, request, redirect, flash
from flask import url_for
from flask import Flask



app = Flask(__name__)

# connect to Database
POSTGRES = {
    'user': 'postgres',
    'pw': 'root',
    'db': 'Student',
    'host': 'localhost',
    'port': '5432'
}
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://%(user)s:\%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db = SQLAlchemy(app)


# define table
Grade = db.Table('grade' ,db.metadata ,autoload = True ,autoload_with = db.engine)
Course = db.Table('course' ,db.metadata ,autoload = True ,autoload_with = db.engine)
tudent = db.Table('student' ,db.metadata ,autoload = True ,autoload_with = db.engine)


# render index.html template
@app.route('/')
def index():
    return render_template('index.html')

# render search.html template
@app.route('/search')
def search():
    return render_template('search.html')

# render delete.html template
@app.route('/delete')
def delete():
    return render_template('delete.html')

# render modify.html template
@app.route('/modify')
def modify():
    return render_template('modify.html')

# render insert.html template
@app.route('/insert')
def insert():
    return render_template('add.html')

# get search_table form and query the request
@app.route('/search_table',methods=['POST'])
def search_table():
    if request.method == 'POST':
        # get form data
        get_id	= request.form.get('id')
        table_name = request.form.get('table_name')
        if table_name == 'course':
            SQL = "Select grade.course_id ,student.student_id ,student.student_name ,grade.score From  student ,grade WHERE grade.course_id = '%s' and student.student_id = grade.student_id"%(get_id)
        elif table_name == 'student':
            SQL = "Select grade.student_id ,course.course_id ,course.course_name ,grade.score From course ,grade WHERE grade.student_id = '%s' and  grade.course_id = course.course_id"%(get_id)
        # execute the SQL
        results = db.session.execute(SQL)
        return render_template('search.html', output_data = results.fetchall() ,title = results.keys())

# get insert_get_data form and return the column name
@app.route('/insert_get_data',methods=['POST'])
def insert_get_data():
    if request.method == 'POST':
        # get form data
        table_name = request.form.get('table_name')
        # execute the SQL
        results = db.session.execute("select * from %s" %(table_name))
        return render_template('add.html', output_data = results.fetchall() ,title = results.keys() ,table_name = table_name)

# get delete_get_data form and return the column name
@app.route('/delete_get_data',methods=['POST'])
def delete_get_data():
    if request.method == 'POST':
        # get form data
        table_name = request.form.get('table_name')
        # execute the SQL
        results = db.session.execute("select * from %s" %(table_name))
        return render_template('delete.html', output_data = results.fetchall() ,title = results.keys() ,table_name = table_name)

# get Modify_get_data form, then return column name and original data
@app.route('/Modify_get_data',methods=['POST'])
def Modify_get_data():
    if request.method == 'POST':
        # get form data
        table_name = request.form.get('table_name')
        if table_name == 'grade':
            modify_student_id = request.form.get('modify_grade_student_id')
            modify_course_id = request.form.get('modify_grade_course_id')
            SQL = "SELECT * from %s WHERE student_id = '%s' and course_id = '%s'"%(table_name ,modify_student_id ,modify_course_id)
        elif table_name == 'course':
            modify_course_id = request.form.get('modify_course_id')
            SQL = "SELECT * from %s WHERE course_id = '%s'"%(table_name ,modify_course_id)
        elif table_name == 'student':
            modify_student_id = request.form.get('modify_student_id')
            SQL = "SELECT * from %s WHERE student_id = '%s'"%(table_name ,modify_student_id)
        # execute the SQL
        results = db.session.execute(SQL)
        return render_template('modify.html', output_data = results.fetchall() ,title = results.keys() ,table_name = table_name , data_count = len(results.keys()))


# get insert_data form and insert the data to db, then direct to search.html
@app.route('/insert_data',methods=['POST'])
def insert_data():
    if request.method == 'POST':
        table_name = request.form.get('table_name')
        if table_name == 'grade':
            # get form data
            student_id	= request.form.get('student_id')
            course_id = request.form.get('course_id')
            score = request.form.get('score')
            sql = "INSERT INTO %s (student_id, course_id, score) VALUES ('%s','%s','%s');"%(table_name ,student_id ,course_id ,score)
        elif table_name == 'course':
            # get form data
            course_id	= request.form.get('course_id')
            course_name = request.form.get('course_name')
            credit = request.form.get('credit')
            sql = "INSERT INTO %s (course_id, course_name, credit) VALUES ('%s','%s','%s');"%(table_name ,course_id ,course_name ,credit)
        elif table_name == 'student':
            # get form data
            student_id	= request.form.get('student_id')
            student_name = request.form.get('student_name')
            gender = request.form.get('gender')
            birthday = request.form.get('birthday')
            fruit = request.form.get('fruit')
            sql = "INSERT INTO %s (student_name, gender, birthday,fruit) VALUES ('%s','%s','%s','%s','%s');"%(table_name ,student_id ,student_name ,gender,birthday,fruit)
        # execute the SQL and commit to db
        db.session.execute(sql)
        db.session.commit()
        results = db.session.execute("select * from %s" %(table_name))
        return render_template('search.html', output_data = results.fetchall() ,title = results.keys())

# get delete_data form, delete the id's data then direct to search.html 
@app.route('/delete_data',methods=['POST'])
def delete_data():
    if request.method == 'POST':
        # get form data
        table_name = request.form.get('table_name')
        if table_name == 'grade':
            student_id	= request.form.get('student_id')
            course_id = request.form.get('course_id')
            sql = "DELETE FROM %s WHERE student_id ='%s' and course_id = '%s'" %(table_name ,student_id ,course_id)
        elif table_name == 'course':
            course_id	= request.form.get('course_id')
            sql = "DELETE FROM %s WHERE course_id='%s'" %(table_name ,course_id)
        elif table_name == 'student':
            student_id	= request.form.get('student_id')
            sql = "DELETE FROM %s WHERE student_id='%s'" %(table_name ,student_id)
        # execute the SQL and commit to db
        db.session.execute(sql)
        db.session.commit()
        results = db.session.execute("select * from %s" %(table_name))
        return render_template('search.html', output_data = results.fetchall() ,title = results.keys())

# get delete_data form,then modify the id's data
@app.route('/modify_data',methods=['POST'])
def modify_data():
    if request.method == 'POST':
        # get form data
        table_name = request.form.get('table_name')
        if table_name == 'grade':
            student_id	= request.form.get('student_id')
            course_id = request.form.get('course_id')
            score = request.form.get('score')
            sql = "UPDATE %s SET score = %s WHERE student_id = '%s' and course_id ='%s'"%(table_name ,score ,student_id ,course_id)
        elif table_name == 'course':
            course_id	= request.form.get('course_id')
            course_name = request.form.get('course_name')
            credit = request.form.get('credit')
            sql = "UPDATE %s SET course_name ='%s' ,credit =%s WHERE course_id ='%s'"%(table_name ,course_name,credit ,course_id)
        elif table_name == 'student':
            student_id	= request.form.get('student_id')
            student_name = request.form.get('student_name')
            gender = request.form.get('gender')
            birthday = request.form.get('birthday')
            fruit = request.form.get('fruit')
            sql = "UPDATE %s SET student_name ='%s',gender='%s',birthday='%s',fruit='%s' WHERE student_id ='%s'"%(table_name ,student_name,gender ,birthday,fruit,student_id) 
        # execute the SQL and commit to db
        db.session.execute(sql)
        db.session.commit()
        results = db.session.execute("select * from %s" %(table_name))
        return render_template('search.html', output_data = results.fetchall() ,title = results.keys())

if __name__ == '__main__':
    app.debug = True
    app.run()
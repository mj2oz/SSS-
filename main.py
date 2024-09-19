# app.py
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


#Just connecting to the DB
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mj:1@127.0.0.1:3306/ifsb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


#Well obviously I don't need a db.Model for everything but assuming this prototype will be developed into an app it's good practice.
class Assignment(db.Model):
    __tablename__ = 'Assignment'
    AssignmentID = db.Column(db.Integer, primary_key=True)
    JobTitle = db.Column(db.String(100))
    Department = db.Column(db.String(100))


class Attendance(db.Model):
    __tablename__ = 'Attendance'
    AttendanceID = db.Column(db.Integer, primary_key=True)
    AttendanceDate = db.Column(db.Date)
    Status = db.Column(db.String(10))

class Education(db.Model):
    __tablename__ = 'Education'
    EducationID = db.Column(db.Integer, primary_key=True)
    Degree = db.Column(db.String(100))
    Institution = db.Column(db.String(100))
    GraduationDate = db.Column(db.Date)


class Training(db.Model):
    __tablename__ = 'Training'
    TrainingID = db.Column(db.Integer, primary_key=True)
    TrainingName = db.Column(db.String(100))
    TrainingDate = db.Column(db.Date)

class Promotion(db.Model):
    __tablename__ = 'Promotion'
    PromotionID = db.Column(db.Integer, primary_key=True)
    PromotionDate = db.Column(db.String(100))
    NewDepartment = db.Column(db.Date)

class KPI(db.Model):
    __tablename__ = 'kpi'
    KPIID = db.Column(db.Integer, primary_key=True)
    KPIName = db.Column(db.String(100))
    KPIDescription = db.Column(db.Text)

class HealthBenefits(db.Model):
    __tablename__ = 'HealthBenefits'
    HealthID = db.Column(db.Integer, primary_key=True)
     #= db.Column(db.String(100))
    #=TrainingDate = db.Column(db.Date)

class Payroll(db.Model):
    __tablename__ = 'Payroll'
    PayrollID = db.Column(db.Integer, primary_key=True)
    BasicSalary = db.Column(db.Integer)
    TotalSalary = db.Column(db.Integer)

class Performance(db.Model):
    __tablename__ = 'Performance'
    PerformanceID = db.Column(db.Integer, primary_key=True)
    Rating = db.Column(db.String(100))
    ReviewDate = db.Column(db.Date)

class Employee(db.Model):
    __tablename__ = 'Employee'
    EmployeeID = db.Column(db.Integer, primary_key=True)
    FirstName = db.Column(db.String(100))
    LastName = db.Column(db.String(100))
    DOB = db.Column(db.Date)
    Address = db.Column(db.String(255))
    Phone = db.Column(db.String(15))
    Email = db.Column(db.String(100))
    Gender = db.Column(db.String(10))
    DateOfHire = db.Column(db.Date)
    AssignmentID = db.Column(db.Integer, db.ForeignKey('Assignment.AssignmentID'))
    HealthID = db.Column(db.Integer, db.ForeignKey('HealthBenefits.HealthID'))
    EducationID = db.Column(db.Integer, db.ForeignKey('Education.EducationID'))
    PayrollID = db.Column(db.Integer, db.ForeignKey('Payroll.PayrollID'))
    PerformanceID = db.Column(db.Integer, db.ForeignKey('Performance.PerformanceID'))
    TrainingID = db.Column(db.Integer, db.ForeignKey('Training.TrainingID'))
    PromotionID = db.Column(db.Integer, db.ForeignKey('Promotion.PromotionID'))
    AttendanceID = db.Column(db.Integer, db.ForeignKey('Attendance.AttendanceID'))
    KPIID = db.Column(db.Integer, db.ForeignKey('kpi.KPIID'))

#Main route
@app.route("/")
def base():
    return render_template("base.html")

#This was one hell of a searching algorthim
@app.route('/employees', methods=['GET', 'POST'])
def index():
    query = request.form.get('query')
    if query:
        search_terms = query.split()
        
        filters = []
        for term in search_terms:
            filters.append(
                (Employee.FirstName.contains(term)) | 
                (Employee.LastName.contains(term))
            )
        
        combined_filter = filters[0]
        for filter_condition in filters[1:]:
            combined_filter |= filter_condition
        
        employees = Employee.query.filter(
            combined_filter |
            (Employee.EmployeeID == query)
        ).all()

    else:
        employees = Employee.query.all()
    return render_template('employees.html', employees=employees)

#The route to add employees
@app.route('/add_employee', methods=['GET', 'POST'])
def add_employee():
    if request.method == 'POST':
        new_employee = Employee(
            FirstName=request.form['FirstName'],
            LastName=request.form['LastName'],
        )
        db.session.add(new_employee)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('add_employee.html')


#Individual Employee route
@app.route('/employee/<int:id>')
def employee_detail(id):
    employee = Employee.query.get_or_404(id)
    return render_template('employee_detail.html', employee=employee)

#Just a test route, don't mind it ;)
@app.route('/test_db')
def test_db():
    try:
        employees = Employee.query.limit(5).all()
        for employee in employees:
            print(f'Employee: {employee.FirstName}')
        return "Database connection successful!"
    except Exception as e:
        print(f'Error: {e}')
        return "Database connection failed."

if __name__ == '__main__':
    app.run(debug=True, port=8080)

#Losing my sanity bit by bit... or even byte by byte.

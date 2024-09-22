from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime
from sqlalchemy.orm import joinedload  
from models import *



#Just connecting to the DB
app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://mj:1@127.0.0.1:3306/ifsb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

#Main route
@app.route("/")
def base():
    employee_1 = Employee.query.get(10004)
    print(employee_1.assignment.JobTitle)
    return render_template("base.html")

#This was one hell of a searching algorthim (and it doesnt even work properly)
@app.route('/employees', methods=['GET', 'POST'])
def employees():
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
        #New Assignment entry
        new_assignment = Assignment(
            JobTitle=request.form.get('JobTitle'),
            Department=request.form.get('Department')
        )
        db.session.add(new_assignment)
        db.session.flush()  # Flush to get the AssignmentID

        #New Education entry
        new_education = Education(
            Degree=request.form.get('Degree'),
            Institution=request.form.get('Institution'),
            GraduationDate=datetime.strptime(request.form['GraduationDate'], '%Y-%m-%d') if request.form['GraduationDate'] else None
        )
        db.session.add(new_education)
        db.session.flush()  # Flush to get the EducationID

        #New Employee entry
        new_employee = Employee(
            FirstName=request.form['FirstName'],
            LastName=request.form['LastName'],
            DOB=datetime.strptime(request.form['DOB'], '%Y-%m-%d') if request.form['DOB'] else None,
            Address=request.form.get('Address'),
            Phone=request.form.get('Phone'),
            Email=request.form.get('Email'),
            Gender=request.form.get('Gender'),
            DateOfHire=datetime.strptime(request.form['DateOfHire'], '%Y-%m-%d') if request.form['DateOfHire'] else None,
            AssignmentID=new_assignment.AssignmentID,  #Link the Assignment
            EducationID=new_education.EducationID  #Link the Education
        )
        db.session.add(new_employee)
        db.session.commit()
        
        flash('Employee added successfully!', 'success')
        return redirect(url_for('index'))
    
    return render_template('add_employee.html')


#Individual Employee route
@app.route('/employee/<int:id>', methods=['GET', 'POST'])
def employee_detail(id):
    employee = Employee.query.get_or_404(id)
    
    if request.method == 'POST':
        db.session.delete(employee)
        db.session.commit()
        flash('Employee deleted successfully!', 'success')
        return redirect(url_for('employees'))
    
    return render_template('employee_detail.html', employee=employee)


@app.route('/payroll', methods=['GET'])
def payroll():
    payroll_data = Employee.query.options(joinedload(Employee.payroll)).all()
    return render_template('payroll.html', payroll_data=payroll_data)

@app.route('/edit_payroll/<int:employee_id>', methods=['GET', 'POST'])
def edit_payroll(employee_id):
    employee = Employee.query.get_or_404(employee_id)
    if request.method == 'POST':
        #If payroll doesn't then create it
        if not employee.payroll:
            employee.payroll = Payroll()
        #Update payroll details
        employee.payroll.BasicSalary = request.form['BasicSalary']
        employee.payroll.TotalSalary = request.form['TotalSalary']
        employee.payroll.Deductions = request.form['Deductions']
        employee.payroll.Bonus = request.form['Bonus']
        db.session.commit()
        flash('Payroll updated successfully!', 'success')
        return redirect(url_for('payroll'))
    
    return render_template('edit_payroll.html', employee=employee)


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
    app.run(debug=True, port=8060)

#Losing my sanity bit by bit... or byte by byte?
#At this point this is no longer just a prototype...

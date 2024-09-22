
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Assignment(db.Model):
    __tablename__ = 'Assignment'
    AssignmentID = db.Column(db.Integer, primary_key=True)
    JobTitle = db.Column(db.String(100))
    Department = db.Column(db.String(100))
    employee = db.relationship('Employee', back_populates='assignment')

class Attendance(db.Model):
    __tablename__ = 'Attendance'
    AttendanceID = db.Column(db.Integer, primary_key=True)
    AttendanceDate = db.Column(db.Date)
    Status = db.Column(db.String(10))
    employee = db.relationship('Employee', back_populates='attendance')

class Education(db.Model):
    __tablename__ = 'Education'
    EducationID = db.Column(db.Integer, primary_key=True)
    Degree = db.Column(db.String(100))
    Institution = db.Column(db.String(100))
    GraduationDate = db.Column(db.Date)
    employee = db.relationship('Employee', back_populates='education')

class Training(db.Model):
    __tablename__ = 'Training'
    TrainingID = db.Column(db.Integer, primary_key=True)
    TrainingName = db.Column(db.String(100))
    TrainingDate = db.Column(db.Date)
    employee = db.relationship('Employee', back_populates='training')

class Promotion(db.Model):
    __tablename__ = 'Promotion'
    PromotionID = db.Column(db.Integer, primary_key=True)
    PromotionDate = db.Column(db.Date)
    NewDepartment = db.Column(db.String(100))
    employee = db.relationship('Employee', back_populates='promotion')

class KPI(db.Model):
    __tablename__ = 'kpi'
    KPIID = db.Column(db.Integer, primary_key=True)
    KPIName = db.Column(db.String(100))
    KPIDescription = db.Column(db.Text)
    employee = db.relationship('Employee', back_populates='kpi')

class HealthBenefits(db.Model):
    __tablename__ = 'HealthBenefits'
    HealthID = db.Column(db.Integer, primary_key=True)
    employee = db.relationship('Employee', back_populates='health_benefit')

class Payroll(db.Model):
    __tablename__ = 'Payroll'
    PayrollID = db.Column(db.Integer, primary_key=True)
    BasicSalary = db.Column(db.Integer)
    TotalSalary = db.Column(db.Integer)
    Deductions = db.Column(db.Integer)
    Bonus = db.Column(db.Integer)
    employee = db.relationship('Employee', back_populates='payroll')

class Performance(db.Model):
    __tablename__ = 'Performance'
    PerformanceID = db.Column(db.Integer, primary_key=True)
    Rating = db.Column(db.String(100))
    ReviewDate = db.Column(db.Date)
    employee = db.relationship('Employee', back_populates='performance')

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

    # The relationships...
    assignment = db.relationship('Assignment', back_populates='employee')
    health_benefit = db.relationship('HealthBenefits', back_populates='employee')
    education = db.relationship('Education', back_populates='employee')
    payroll = db.relationship('Payroll', back_populates='employee')
    performance = db.relationship('Performance', back_populates='employee')
    training = db.relationship('Training', back_populates='employee')
    promotion = db.relationship('Promotion', back_populates='employee')
    attendance = db.relationship('Attendance', back_populates='employee')
    kpi = db.relationship('KPI', back_populates='employee')


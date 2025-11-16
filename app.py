from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import pandas as pd
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'

db = SQLAlchemy(app)

# Database Models
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.String(20), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(10), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'name': self.name,
            'created_at': self.created_at.isoformat()
        }

class AttendanceRecord(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'), nullable=False)
    subject_id = db.Column(db.Integer, db.ForeignKey('subject.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(10), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('Student', backref='attendance_records')
    subject = db.relationship('Subject', backref='attendance_records')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_name': self.student.name,
            'subject_name': self.subject.name,
            'date': self.date.isoformat(),
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }

# Web Routes
@app.route('/')
def dashboard():
    total_students = Student.query.count()
    total_subjects = Subject.query.count()
    total_records = AttendanceRecord.query.count()
    present_count = AttendanceRecord.query.filter_by(status='Present').count()
    
    stats = {
        'total_students': total_students,
        'total_subjects': total_subjects,
        'total_records': total_records,
        'present_count': present_count,
        'attendance_rate': round((present_count / total_records * 100) if total_records > 0 else 0, 2)
    }
    
    return render_template('dashboard.html', stats=stats)

@app.route('/students')
def students():
    students = Student.query.all()
    return render_template('students.html', students=students)

@app.route('/subjects')
def subjects():
    subjects = Subject.query.all()
    return render_template('subjects.html', subjects=subjects)

@app.route('/attendance')
def attendance():
    records = AttendanceRecord.query.join(Student).join(Subject).all()
    return render_template('attendance.html', records=records)

@app.route('/upload')
def upload_page():
    return render_template('upload.html')

# API Routes - Students CRUD
@app.route('/api/students', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

@app.route('/api/students', methods=['POST'])
def create_student():
    data = request.get_json()
    student = Student(
        student_id=data['student_id'],
        name=data['name'],
        email=data.get('email', '')
    )
    db.session.add(student)
    db.session.commit()
    return jsonify(student.to_dict()), 201

@app.route('/api/students/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get_or_404(id)
    data = request.get_json()
    student.student_id = data['student_id']
    student.name = data['name']
    student.email = data.get('email', '')
    db.session.commit()
    return jsonify(student.to_dict())

@app.route('/api/students/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get_or_404(id)
    db.session.delete(student)
    db.session.commit()
    return '', 204

# API Routes - Subjects CRUD
@app.route('/api/subjects', methods=['GET'])
def get_subjects():
    subjects = Subject.query.all()
    return jsonify([subject.to_dict() for subject in subjects])

@app.route('/api/subjects', methods=['POST'])
def create_subject():
    data = request.get_json()
    subject = Subject(code=data['code'], name=data['name'])
    db.session.add(subject)
    db.session.commit()
    return jsonify(subject.to_dict()), 201

@app.route('/api/subjects/<int:id>', methods=['PUT'])
def update_subject(id):
    subject = Subject.query.get_or_404(id)
    data = request.get_json()
    subject.code = data['code']
    subject.name = data['name']
    db.session.commit()
    return jsonify(subject.to_dict())

@app.route('/api/subjects/<int:id>', methods=['DELETE'])
def delete_subject(id):
    subject = Subject.query.get_or_404(id)
    db.session.delete(subject)
    db.session.commit()
    return '', 204

# API Routes - Attendance CRUD
@app.route('/api/attendance', methods=['GET'])
def get_attendance():
    records = AttendanceRecord.query.all()
    return jsonify([record.to_dict() for record in records])

@app.route('/api/attendance', methods=['POST'])
def create_attendance():
    data = request.get_json()
    record = AttendanceRecord(
        student_id=data['student_id'],
        subject_id=data['subject_id'],
        date=datetime.strptime(data['date'], '%Y-%m-%d').date(),
        status=data['status']
    )
    db.session.add(record)
    db.session.commit()
    return jsonify(record.to_dict()), 201

@app.route('/api/attendance/<int:id>', methods=['DELETE'])
def delete_attendance(id):
    record = AttendanceRecord.query.get_or_404(id)
    db.session.delete(record)
    db.session.commit()
    return '', 204

# File Upload API
@app.route('/api/upload', methods=['POST'])
def upload_excel():
    if 'file' not in request.files:
        return jsonify({'error': 'No file provided'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if file and file.filename.endswith(('.xlsx', '.xls')):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        
        try:
            df = pd.read_excel(filepath)
            processed = 0
            
            for _, row in df.iterrows():
                # Create or get student
                student = Student.query.filter_by(student_id=row['student_id']).first()
                if not student:
                    student = Student(student_id=row['student_id'], name=row['student_name'])
                    db.session.add(student)
                    db.session.flush()
                
                # Create or get subject
                subject = Subject.query.filter_by(code=row['subject_code']).first()
                if not subject:
                    subject = Subject(code=row['subject_code'], name=row['subject_name'])
                    db.session.add(subject)
                    db.session.flush()
                
                # Create attendance record
                date_obj = pd.to_datetime(row['date']).date()
                existing = AttendanceRecord.query.filter_by(
                    student_id=student.id, subject_id=subject.id, date=date_obj
                ).first()
                
                if not existing:
                    record = AttendanceRecord(
                        student_id=student.id,
                        subject_id=subject.id,
                        date=date_obj,
                        status=row['status']
                    )
                    db.session.add(record)
                    processed += 1
            
            db.session.commit()
            os.remove(filepath)  # Clean up uploaded file
            
            return jsonify({'message': f'Successfully processed {processed} records'})
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    return jsonify({'error': 'Invalid file format'}), 400

# Analytics API
@app.route('/api/analytics/summary')
def analytics_summary():
    total_records = AttendanceRecord.query.count()
    present_count = AttendanceRecord.query.filter_by(status='Present').count()
    absent_count = AttendanceRecord.query.filter_by(status='Absent').count()
    
    return jsonify({
        'total_records': total_records,
        'present_count': present_count,
        'absent_count': absent_count,
        'attendance_rate': round((present_count / total_records * 100) if total_records > 0 else 0, 2)
    })

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
# Student Attendance Management System

**Created by: chhelu , viren , akshit , dhairya**  
**Course: Python Programming**  
**Date: December 2024**

## 🎯 Project Overview

A comprehensive web-based attendance management system built with Flask, featuring CRUD operations, file handling, database management, and RESTful APIs. This system allows educational institutions to efficiently track and manage student attendance records.

## ✨ Features

- **Dashboard Analytics** - Real-time attendance statistics and visualizations
- **Student Management** - Complete CRUD operations for student records
- **Subject Management** - Add, edit, and delete academic subjects
- **Attendance Tracking** - Record and manage attendance with multiple status options
- **Excel File Upload** - Bulk import attendance data from Excel files
- **RESTful API** - Complete API endpoints for all operations
- **Responsive Design** - Mobile-friendly interface with Bootstrap
- **Database Integration** - SQLite database with SQLAlchemy ORM

## 🛠️ Technical Stack

- **Backend**: Flask 2.3.3, SQLAlchemy
- **Frontend**: HTML5, CSS3, JavaScript (ES6), Bootstrap 5
- **Database**: SQLite3
- **File Processing**: Pandas, OpenPyXL
- **Charts**: Chart.js
- **Icons**: Font Awesome

## 📁 Project Structure

```
attendance-new/
├── app.py                 # Main Flask application
├── requirements.txt       # Python dependencies
├── templates/            # HTML templates
│   ├── base.html         # Base template
│   ├── dashboard.html    # Dashboard page
│   ├── students.html     # Student management
│   ├── subjects.html     # Subject management
│   ├── attendance.html   # Attendance records
│   └── upload.html       # File upload
├── static/              # Static files
│   ├── css/style.css    # Custom styles
│   └── js/main.js       # JavaScript functions
└── uploads/             # File upload directory
```

## 🚀 Quick Start

### 1. Installation
```bash
# Clone or download the project
cd attendance-new

# Install dependencies
pip install -r requirements.txt
```

### 2. Run Application
```bash
python app.py
```

### 3. Access Application
Open your browser and go to: `http://127.0.0.1:5000`

## 📊 Database Schema

### Students Table
- `id` - Primary key
- `student_id` - Unique student identifier
- `name` - Student name
- `email` - Email address (optional)
- `created_at` - Timestamp

### Subjects Table
- `id` - Primary key
- `code` - Unique subject code
- `name` - Subject name
- `created_at` - Timestamp

### Attendance Records Table
- `id` - Primary key
- `student_id` - Foreign key to Students
- `subject_id` - Foreign key to Subjects
- `date` - Attendance date
- `status` - Present/Absent/Late
- `created_at` - Timestamp

## 🔌 API Endpoints

### Students API
- `GET /api/students` - List all students
- `POST /api/students` - Create new student
- `PUT /api/students/<id>` - Update student
- `DELETE /api/students/<id>` - Delete student

### Subjects API
- `GET /api/subjects` - List all subjects
- `POST /api/subjects` - Create new subject
- `PUT /api/subjects/<id>` - Update subject
- `DELETE /api/subjects/<id>` - Delete subject

### Attendance API
- `GET /api/attendance` - List attendance records
- `POST /api/attendance` - Create attendance record
- `DELETE /api/attendance/<id>` - Delete record

### File Upload API
- `POST /api/upload` - Upload Excel file

### Analytics API
- `GET /api/analytics/summary` - Get attendance summary

## 📋 Excel File Format

Your Excel file should contain these columns:
- `student_id` - Student ID (e.g., ST001)
- `student_name` - Student Name
- `subject_code` - Subject Code (e.g., CS101)
- `subject_name` - Subject Name
- `date` - Date (YYYY-MM-DD format)
- `status` - Present/Absent/Late

## 🎨 Key Features Implemented

### 1. CRUD Operations
- Complete Create, Read, Update, Delete functionality
- Form validation and error handling
- Modal-based forms for better UX

### 2. File Handling
- Excel file upload and processing
- Automatic student/subject creation
- Duplicate record prevention
- File validation and error handling

### 3. Database Management
- SQLAlchemy ORM for database operations
- Foreign key relationships
- Data integrity constraints
- Automatic table creation

### 4. API Development
- RESTful API design
- JSON request/response handling
- Error handling and status codes
- CORS support for frontend integration

### 5. Frontend Development
- Responsive Bootstrap design
- Interactive charts with Chart.js
- AJAX for seamless user experience
- Form validation and feedback

## 🔧 Customization

### Adding New Features
1. **User Authentication** - Add login/logout functionality
2. **Email Notifications** - Send attendance alerts
3. **Report Generation** - PDF/Excel report exports
4. **Advanced Analytics** - Trend analysis and predictions

### Styling Customization
- Modify `static/css/style.css` for custom themes
- Update color variables in CSS root
- Add custom animations and effects

## 🐛 Troubleshooting

### Common Issues
1. **Database not found** - Run the app once to create SQLite database
2. **File upload fails** - Check uploads/ directory permissions
3. **Charts not loading** - Ensure Chart.js CDN is accessible

## 📈 Learning Outcomes

Through this project, I have demonstrated:
- **Flask Framework** - Web application development
- **Database Design** - Relational database modeling
- **API Development** - RESTful service creation
- **File Processing** - Excel data handling with Pandas
- **Frontend Integration** - AJAX and dynamic content
- **Error Handling** - Robust error management
- **Code Organization** - Clean, maintainable code structure

## 🎓 Academic Context

This project fulfills the requirements for:
- Python programming concepts
- Web development fundamentals
- Database management systems
- API design and implementation
- File handling and data processing
- Frontend-backend integration

## 📝 Future Enhancements

- [ ] User authentication and authorization
- [ ] Advanced reporting and analytics
- [ ] Mobile application development
- [ ] Email notification system
- [ ] Backup and restore functionality
- [ ] Multi-language support

---

**Note**: This project is created for educational purposes as part of Python programming coursework. It demonstrates practical application of web development concepts, database management, and API design principles.
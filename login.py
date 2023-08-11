from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from datetime import datetime
from models import db, CompanyInfo, Worker, Person
from data import main_to_sub_categories, alans

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
db.init_app(app)

class Company(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    # Other company fields

class Worker(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=False)
    # Worker fields

@app.route('/get_main_to_sub_categories', methods=['GET'])
def get_main_to_sub_categories():
    return jsonify(main_to_sub_categories)

@app.route('/')
def index():
    people = Worker.query.all()
    return render_template('index.html', people=people)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        company = Company.query.filter_by(username=username, password=password).first()
        if company:
            session['company_id'] = company.id
            return redirect(url_for('company_info_form'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/company_info_form', methods=['GET', 'POST'])
def company_info_form():
    error_message = None

    if request.method == 'POST':
        company_name = request.form['company_name']
        company_address = request.form['company_address']
        company_phone = request.form['company_phone']
        company_email = request.form['company_email']
        tax_number = request.form['tax_number']
        sgk_registry_number = request.form['sgk_registry_number']
        sgk_employee_count = request.form['sgk_employee_count']
        bank_name = request.form['bank_name']
        branch_name = request.form['branch_name']
        iban_number = request.form['iban_number']
        representative_name = request.form['representative_name']
        representative_tc = request.form['representative_tc']
        representative_title = request.form['representative_title']

        company_info = CompanyInfo(
            company_name=company_name,
            company_address=company_address,
            company_phone=company_phone,
            company_email=company_email,
            tax_number=tax_number,
            sgk_registry_number=sgk_registry_number,
            sgk_employee_count=sgk_employee_count,
            bank_name=bank_name,
            branch_name=branch_name,
            iban_number=iban_number,
            representative_name=representative_name,
            representative_tc=representative_tc,
            representative_title=representative_title
        )

        db.session.add(company_info)
        db.session.commit()

        flash('İşyeri Bilgileri Başarıyla Kaydedildi.', 'success')
        return redirect(url_for('index'))

    return render_template('company_info_form.html', error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/worker_info_form', methods=['GET', 'POST'])
def worker_info_form():
    if 'company_id' not in session:
        return redirect(url_for('login'))
    
    company = Company.query.get(session['company_id'])
    
    if request.method == 'POST':
        # Save worker info to database
        return redirect(url_for('index'))
    
    return render_template('worker_info_form.html', company=company)

if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

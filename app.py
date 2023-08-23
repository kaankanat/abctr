from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_migrate import Migrate
from models import db, CompanyInfo, User, Person
from data import main_to_sub_categories, alans
from werkzeug.security import check_password_hash
from datetime import datetime
from sqlalchemy.exc import IntegrityError
from userpass import create_users

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'
db.init_app(app)
migrate = Migrate(app, db)
with app.app_context():
    db.create_all()

@app.route('/get_main_to_sub_categories', methods=['GET'])
def get_main_to_sub_categories():
    return jsonify(main_to_sub_categories)

@app.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    error_message = None

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user:
            if check_password_hash(user.password, password):
                session['user_id'] = user.id
                return redirect(url_for('company_info_form'))
            else:
                error_message = 'Yanlış Kullanıcı Adı veya Şifre'
        else:
            error_message = 'Yanlış Kullanıcı Adı veya Şifre'

    return render_template('login.html', error_message=error_message, success_message=None)

@app.route('/company_info_form', methods=['GET', 'POST'])
def company_info_form():
    error_message = None
    success_message = None

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

        success_message = 'İşyeri Bilgileri Başarıyla Kaydedildi.'
        flash(success_message, 'success')
        return redirect(url_for('dashboard'))

    return render_template('company_info_form.html', error_message=error_message, success_message=success_message)

@app.route('/sayfa1', methods=['GET', 'POST'])
def sayfa1():
    error_message = ""
    person_data = session.get('create1_data', {})
    
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        TCNo = request.form['TCNo']
        birth_date_str = request.form['birth_date']
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except ValueError:
            error_message = 'Yanlış doğum tarihi formatı!'
            return render_template('create1.html', error_message=error_message, person_data=person_data)
        
        existing_person = Person.query.filter_by(TCNo=TCNo).first()
        if existing_person:
            error_message = 'Girdiğiniz TC Numarası sistemde zaten kayıtlı.'
            return render_template('create1.html', error_message=error_message, person_data=person_data)
        
        person_data.update({
            'name': name,
            'surname': surname,
            'TCNo': TCNo,
            'birth_date': birth_date,
        })

        session['create1_data'] = person_data
        session.modified = True

        return redirect(url_for('sayfa2'))

    return render_template('create1.html', error_message=error_message, person_data=person_data)
@app.route('/sayfa2', methods=['GET', 'POST'])
def sayfa2():
    error_message = None
    person_data = session.get('create1_data', {})
    if request.method == 'POST':
        father_name = request.form['father_name']
        mother_name = request.form['mother_name']
        birthplace = request.form['birthplace']
        phone_number = request.form['phone_number']
        address = request.form['address']
        graduation_status = request.form['graduation_status']
        institution = request.form['institution']
        field = request.form['field']
        dal = request.form['dal']

        if not graduation_status:
            error_message = 'Mezuniyet Durumu seçilmiş olmalıdır.'
            return render_template('create2.html', error_message=error_message, person_data=person_data)

        if not field:
            error_message = 'Mesleki Alanı seçilmiş olmalıdır.'
            return render_template('create2.html', error_message=error_message, person_data=person_data)

        if not dal:
            error_message = 'Mesleki Dalı seçilmiş olmalıdır.'
            return render_template('create2.html', error_message=error_message, person_data=person_data)

        person = Person(
            name=person_data['name'],
            surname=person_data['surname'],
            TCNo=person_data['TCNo'],
            father_name=father_name,
            mother_name=mother_name,
            birthplace=birthplace,
            phone_number=phone_number,
            address=address,
            graduation_status=graduation_status,
            institution=institution,
            field=field,
            dal=dal,
            birth_date=datetime.strptime(person_data['birth_date'], '%a, %d %b %Y %H:%M:%S %Z').date(),
            )

        db.session.add(person)
        db.session.commit()

        flash('Kişi Başarıyla Eklendi.', 'success')
        return redirect(url_for('dashboard'))

    return render_template('create2.html', error_message=error_message, person_data=person_data, alans=alans, main_to_sub_categories=main_to_sub_categories)

@app.route('/duzenle1/<string:tcno>', methods=['GET', 'POST'])
def duzenle1(tcno):
    error_message = ""
    person_data = session.get('edit1_data', {})

    person = Person.query.filter_by(TCNo=tcno).first()
    if request.method == 'POST':
        name = request.form['name']
        surname = request.form['surname']
        TCNo = request.form['TCNo']
        birth_date_str = request.form['birth_date']
        try:
            birth_date = datetime.strptime(birth_date_str, '%Y-%m-%d').date()
        except ValueError:
            error_message = 'Yanlış doğum tarihi formatı!'
            return render_template('edit1.html', error_message=error_message, person_data=person_data)

        existing_person = Person.query.filter(Person.TCNo == TCNo).first()
        if existing_person and existing_person.id != person.id:
            error_message = 'Bu TC Kimlik Numarası zaten başka bir kişi tarafından kullanılıyor.'
            return render_template('edit1.html', error_message=error_message, person_data=person_data)

        person_data.update({
            'name': name,
            'surname': surname,
            'TCNo': TCNo,
            'birth_date': birth_date,
        })

        session['edit1_data'] = person_data
        session.modified = True

        return redirect(url_for('duzenle2', tcno=TCNo))
    
    return render_template('edit1.html', error_message=error_message, person_data=person_data, alans=alans, main_to_sub_categories=main_to_sub_categories)

@app.route('/duzenle2/<string:tcno>', methods=['GET', 'POST'])
def duzenle2(tcno):
    person = Person.query.filter_by(TCNo=tcno).first()

    if not person:
        flash('Kişi bulunamadı.', 'error')
        return redirect(url_for('list'))

    if request.method == 'POST':
        tcno = request.form['TCNo']
        person.father_name = request.form.get('father_name', person.father_name)
        person.mother_name = request.form.get('mother_name', person.mother_name)
        person.birthplace = request.form.get('birthplace', person.birthplace)
        person.phone_number = request.form.get('phone_number', person.phone_number)
        person.address = request.form.get('address', person.address)
        person.graduation_status = request.form.get('graduation_status', person.graduation_status)
        person.institution = request.form.get('institution', person.institution)
        person.field = request.form.get('field', person.field)
        person.dal = request.form.get('dal', person.dal)

        try:
            if 'birth_date' in request.form:
                person.birth_date = datetime.strptime(request.form['birth_date'], '%Y-%m-%d')
            db.session.commit()
            flash('Kişi Başarıyla Düzenlendi.', 'success')
        except IntegrityError as e:
            db.session.rollback()
            flash('Bir hata oluştu. Lütfen tekrar deneyiniz.', 'error')

        return redirect(url_for('list'))

    return render_template('edit2.html', person=person)

@app.route('/')
def index():
    success_message = request.args.get('success_message')
    if success_message:
        return render_template('login.html', success_message=success_message)
    else:
        return render_template('login.html')

@app.route('/list')
def list():
    people = Person.query.all()
    return render_template('list.html', people=people)

@app.route('/sil/<int:id>', methods=['GET', 'POST'])
def sil(id):
    person = Person.query.get(id)
    if request.method == 'POST':
        confirm = request.form['confirm']
        if confirm == 'yes':
            db.session.delete(person)
            db.session.commit()
            flash('Kişi başarıyla silindi.', 'success')
        return redirect(url_for('list'))
    
    return render_template('delete.html', person=person)
if __name__ == '__main__':
    create_users(app)
    app.run(debug=True)
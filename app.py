from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
from models import db, Person
from data import main_to_sub_categories, alans

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'
db.init_app(app)

@app.route('/get_main_to_sub_categories', methods=['GET'])
def get_main_to_sub_categories():
    return jsonify(main_to_sub_categories)

@app.route('/')
def index():
    people = Person.query.all()
    return render_template('index.html', people=people)

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
        return redirect(url_for('index'))

    return render_template('create2.html', error_message=error_message, person_data=person_data, alans=alans, main_to_sub_categories=main_to_sub_categories)

if __name__ == '__main__':
    app.run(debug=True)
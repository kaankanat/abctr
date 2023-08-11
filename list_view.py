from flask import render_template, session, request, flash, redirect, url_for, Flask, jsonify
from datetime import datetime
from models import db, Person
from data import main_to_sub_categories, alans
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///person.db'
db.init_app(app)

@app.route('/get_main_to_sub_categories', methods=['GET'])
def get_main_to_sub_categories():
    return jsonify(main_to_sub_categories)

@app.route('/')
def anasayfa():
    people = Person.query.all()
    return render_template('list.html', people=people)


@app.route('/duzenle1/<int:id>', methods=['GET', 'POST'])
def duzenle1(id):
    error_message = ""
    person_data = session.get('edit1_data', {})

    person = Person.query.get(id)
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

        return redirect(url_for('duzenle2', id=id))

    return render_template('edit1.html', error_message=error_message, person_data=person_data, alans=alans, main_to_sub_categories=main_to_sub_categories)

@app.route('/duzenle2', methods=['POST'])
def duzenle2():
    print("Form data in duzenle2:", request.form)
    person_id = request.form['person_id']
    person = Person.query.get(person_id)
    if not person:
        flash('Kişi bulunamadı.', 'error')
        return redirect(url_for('anasayfa'))

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

    return redirect(url_for('anasayfa'))

@app.route('/sil/<int:id>', methods=['GET', 'POST'])
def sil(id):
    person = Person.query.get(id)
    if request.method == 'POST':
        confirm = request.form['confirm']
        if confirm == 'yes':
            db.session.delete(person)
            db.session.commit()
            flash('Kişi başarıyla silindi.', 'success')
        return redirect(url_for('anasayfa'))
    
    return render_template('delete.html', person=person)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
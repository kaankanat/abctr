from werkzeug.security import generate_password_hash
from models import db, User

def create_users(app):
    users = [
        {'company_name': 'Admin', 'username': 'admin', 'password': 'admin', 'role': 'admin'},
        {'company_name': 'Alufem', 'username': 'alufem', 'password': 'alufem2023'},
        {'company_name': 'Bildi Metal', 'username': 'bildimetal', 'password': 'bildimetal2023'},
        {'company_name': 'Denka Metal', 'username': 'denkametal', 'password': 'denkametal2023'},
        {'company_name': 'Viva Mobilya', 'username': 'vivamobilya', 'password': 'vivamobilya2023'},
        {'company_name': 'Bayramoğlu', 'username': 'bayramoglu', 'password': 'bayramoglu2023'},
        {'company_name': 'Femaş Merkez', 'username': 'femasmerkez', 'password': 'femasmerkez2023'},
        {'company_name': 'Femaş 1', 'username': 'femas1', 'password': 'femas12023'},
        {'company_name': 'Femaş 2', 'username': 'femas2', 'password': 'femas22023'},
        {'company_name': 'Kayseri Gaz', 'username': 'kayserigaz', 'password': 'kayserigaz2023'},
        {'company_name': 'Kilim Mobilya', 'username': 'kilimmobilya', 'password': 'kilimmobilya2023'},
        {'company_name': 'Lavantes', 'username': 'lavantes', 'password': 'lavantes2023'},
        {'company_name': 'Shonti Gıda', 'username': 'shontigida', 'password': 'shontigida2023'},
        {'company_name': 'Erat Kablo', 'username': 'eratkablo', 'password': 'eratkablo2023'},
        {'company_name': 'Flamingo', 'username': 'flamingo', 'password': 'flamingo2023'},
        {'company_name': 'Innova', 'username': 'innova', 'password': 'innova2023'},
        {'company_name': 'Agah Group', 'username': 'agahgroup', 'password': 'agahgroup2023'},
        {'company_name': 'Aysel Danacı', 'username': 'ayseldanaci', 'password': 'ayseldanaci2023'},
        {'company_name': 'Dedeman Otel', 'username': 'dedemanotel', 'password': 'dedemanotel2023'},
        {'company_name': 'Emel Garden', 'username': 'emelgarden', 'password': 'emelgarden2023'},
        {'company_name': 'Erkut İnşaat', 'username': 'erkutinsaat', 'password': 'erkutinsaat2023'},
        {'company_name': 'İskender Atasoy', 'username': 'iskenderatasoy', 'password': 'iskenderatasoy2023'},
        {'company_name': 'Mutena', 'username': 'mutena', 'password': 'mutena2023'},
        {'company_name': 'Safir Kont Çelik Kapı', 'username': 'safirkont', 'password': 'safirkont2023'},
        {'company_name': 'Sinan Chef Restoran', 'username': 'sinanchef', 'password': 'sinanchef2023'},
        {'company_name': 'Yeşil Künefe', 'username': 'yesilkunefe', 'password': 'yesilkunefe2023'},
        {'company_name': 'Kayseri Yem', 'username': 'kayseriyem', 'password': 'kayseriyem2023'},
        {'company_name': 'Vezir Bey Lokantacılık', 'username': 'vezirbey', 'password': 'vezirbey2023'},
        {'company_name': '5t5 Makine', 'username': '5t5makine', 'password': '5t5makine2023'},
        {'company_name': 'Akyol Mühendislik', 'username': 'akyolmuhendislik', 'password': 'akyolmuhendislik2023'},
        {'company_name': 'Çetin Boru', 'username': 'cetinboru', 'password': 'cetinboru2023'},
        {'company_name': 'Doğuş Boya', 'username': 'dogusboya', 'password': 'dogusboya2023'},
        {'company_name': 'Elizan Life Mobilya', 'username': 'elizanlife', 'password': 'elizanlife2023'},
        {'company_name': 'Elmassan Mobilya', 'username': 'elmassanmobilya', 'password': 'elmassanmobilya2023'},
        {'company_name': 'Fikret Çalışkan', 'username': 'fikretcaliskan', 'password': 'fikretcaliskan2023'},
        {'company_name': 'Griffiths Tekstil', 'username': 'griffithstekstil', 'password': 'griffithstekstil2023'},
        {'company_name': 'Kamberli Mobilya', 'username': 'kamberlimobilya', 'password': 'kamberlimobilya2023'},
        {'company_name': 'Kılıçlar Çevre Denetim', 'username': 'kiliclarcevre', 'password': 'kiliclarcevre2023'},
        {'company_name': 'Metaland', 'username': 'metaland', 'password': 'metaland2023'},
        {'company_name': 'Net Otomotiv', 'username': 'netotomotiv', 'password': 'netotomotiv2023'},
        {'company_name': 'Sanatde Mude Mobilya', 'username': 'sanatdemude', 'password': 'sanatdemude2023'},
        {'company_name': 'Sinerji Tasarım', 'username': 'sinerjitasarim', 'password': 'sinerjitasarim2023'},
        {'company_name': 'Teknik Bileme', 'username': 'teknikbileme', 'password': 'teknikbileme2023'},
        {'company_name': 'Telekom', 'username': 'telekom', 'password': 'telekom2023'},
        {'company_name': 'Torsa Endüstriyel', 'username': 'torsaendustriyel', 'password': 'torsaendustriyel2023'},
        {'company_name': 'Akbulut Tekstil', 'username': 'akbuluttekstil', 'password': 'akbuluttekstil2023'},
        {'company_name': 'Aksu Mobilya', 'username': 'aksumobilya', 'password': 'aksumobilya2023'},
        {'company_name': 'Alya', 'username': 'alya', 'password': 'alya2023'},
        {'company_name': 'Asilev Mobilya', 'username': 'asilevmobilya', 'password': 'asilevmobilya2023'},
        {'company_name': 'Bağ Gül Mobilya', 'username': 'baggulmobilya', 'password': 'baggulmobilya2023'},
        {'company_name': 'Balcıoğlu', 'username': 'balcioglu', 'password': 'balcioglu2023'},
        {'company_name': 'Denge Vida', 'username': 'dengevida', 'password': 'dengevida2023'},
        {'company_name': 'Efendi Reklam', 'username': 'efendireklam', 'password': 'efendireklam2023'},
        {'company_name': 'Eras İnşaat', 'username': 'erasinsaat', 'password': 'erasinsaat2023'},
        {'company_name': 'Etaş Yumurta', 'username': 'etasyumurta', 'password': 'etasyumurta2023'},
        {'company_name': 'Has Gıda', 'username': 'hasgida', 'password': 'hasgida2023'},
        {'company_name': 'Makbes Makine', 'username': 'makbesmakine', 'password': 'makbesmakine2023'},
        {'company_name': 'Prime Inn Otel', 'username': 'primeinnotel', 'password': 'primeinnotel2023'},
        {'company_name': 'Retel Rezidans', 'username': 'retelrezidans', 'password': 'retelrezidans2023'},
        {'company_name': 'Salıngaç', 'username': 'salingac', 'password': 'salingac2023'},
        {'company_name': 'Serap Koltuk', 'username': 'serapkoltuk', 'password': 'serapkoltuk2023'},
        {'company_name': 'SFR Mobilya', 'username': 'sfrmobilya', 'password': 'sfrmobilya2023'},
        {'company_name': 'Simitçi Dünyası', 'username': 'simiticidunyasi', 'password': 'simiticidunyasi2023'},
        {'company_name': 'SRC Otel', 'username': 'srcotel', 'password': 'srcotel2023'},
        {'company_name': 'Tekno Bahçe', 'username': 'teknobahce', 'password': 'teknobahce2023'},
        {'company_name': 'Tepe Plastik', 'username': 'tepeplastik', 'password': 'tepeplastik2023'},
        {'company_name': 'Türksat Kablo Neotek', 'username': 'turksatkablo', 'password': 'turksatkablo2023'},
        {'company_name': 'Vanillin', 'username': 'vanillin', 'password': 'vanillin2023'},
        {'company_name': 'Yavuzlar ISGB', 'username': 'yavuzlarisgb', 'password': 'yavuzlarisgb2023'},
        {'company_name': 'Yavuzlar Madencilik', 'username': 'yavuzlarmadencilik', 'password': 'yavuzlarmadencilik2023'},
        {'company_name': 'ABCTR Yazılım', 'username': 'abctryazilim', 'password': 'abctryazilim2023'},
        {'company_name': 'Ayhanlar Plastik', 'username': 'ayhanlarplastik', 'password': 'ayhanlarplastik2023'},
        {'company_name': 'Bingöl Ticaret', 'username': 'bingolticaret', 'password': 'bingolticaret2023'},
        {'company_name': 'Ege Malzemecilik', 'username': 'egemalzemecilik', 'password': 'egemalzemecilik2023'},
        {'company_name': 'HM Hamburger', 'username': 'hmhamburger', 'password': 'hmhamburger2023'},
        {'company_name': 'Mia Bella', 'username': 'miabella', 'password': 'miabella2023'},
        {'company_name': 'Remay', 'username': 'remay', 'password': 'remay2023'},
        {'company_name': 'Sinem SMMM', 'username': 'sinemsmmm', 'password': 'sinemsmmm2023'},
        {'company_name': 'Blackline Mert Sarıarslan PVC', 'username': 'blacklinemert', 'password': 'blacklinemert2023'},
        {'company_name': 'Bullseye', 'username': 'bullseye', 'password': 'bullseye2023'},
        {'company_name': 'Ceha Büro Mobilyaları', 'username': 'cehamobilya', 'password': 'cehamobilya2023'},
        {'company_name': 'Kiraz Otel Cafe', 'username': 'kirazcafe', 'password': 'kirazcafe2023'},
        {'company_name': 'Mustafa Güleç Harita', 'username': 'mustafaharita', 'password': 'mustafaharita2023'},
        {'company_name': 'Paradoks Restoran Cafe', 'username': 'paradokscafe', 'password': 'paradokscafe2023'},
        {'company_name': 'Ravena Kağıt', 'username': 'ravenakagit', 'password': 'ravenakagit2023'},
        {'company_name': 'Şefik Sarıarslan PVC', 'username': 'sefikpvc', 'password': 'sefikpvc2023'},
        {'company_name': 'Yakar Çelik Dövme', 'username': 'yakarcelik', 'password': 'yakarcelik2023'},
        {'company_name': 'Başak', 'username': 'basak', 'password': 'basak2023'},
        {'company_name': 'Best Otomasyon Elektrik', 'username': 'bestotomasyon', 'password': 'bestotomasyon2023'},
        {'company_name': 'Doğan Ay Mobilya', 'username': 'doganaymobilya', 'password': 'doganaymobilya2023'},
        {'company_name': 'Ebruli Mobilya', 'username': 'ebrulimobilya', 'password': 'ebrulimobilya2023'},
        {'company_name': 'Emniyet Cam', 'username': 'emniyetcam', 'password': 'emniyetcam2023'},
        {'company_name': 'Garden Alüminyum', 'username': 'gardenaluminyum', 'password': 'gardenaluminyum2023'},
        {'company_name': 'Hüma Hastanesi', 'username': 'humahastanesi', 'password': 'humahastanesi2023'},
        {'company_name': 'Kalbim Mobilya', 'username': 'kalbimmobilya', 'password': 'kalbimmobilya2023'},
        {'company_name': 'Kalitest Beton', 'username': 'kalitestbeton', 'password': 'kalitestbeton2023'},
        {'company_name': 'Karteks Esse', 'username': 'karteksesse', 'password': 'karteksesse2023'},
        {'company_name': 'La Familia R.', 'username': 'lafamilia', 'password': 'lafamilia2023'},
        {'company_name': 'Mobiboya Kimya', 'username': 'mobiboya', 'password': 'mobiboya2023'},
        {'company_name': 'Mobitek Mobilya', 'username': 'mobitekmobilya', 'password': 'mobitekmobilya2023'},
        {'company_name': 'Moher', 'username': 'moher', 'password': 'moher2023'},
        {'company_name': 'Neon Mobilya', 'username': 'neonmobilya', 'password': 'neonmobilya2023'},
        {'company_name': 'Newway Otel', 'username': 'newwayotel', 'password': 'newwayotel2023'},
        {'company_name': 'Sen Tarım', 'username': 'sentarim', 'password': 'sentarim2023'},
        {'company_name': 'Tokgöz Beton', 'username': 'tokgozbeton', 'password': 'tokgozbeton2023'},
        {'company_name': 'Trioline', 'username': 'trioline', 'password': 'trioline2023'},
        {'company_name': 'Yemcim', 'username': 'yemcim', 'password': 'yemcim2023'},
    ]
    
    with app.app_context():
        for user_data in users:
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if not existing_user:
                hashed_password = generate_password_hash(user_data['password'])
                new_user = User(
                    username=user_data['username'],
                    password=hashed_password,
                    company_name=user_data['company_name']
                )
                if 'role' in user_data:
                    new_user.role = user_data['role']
                db.session.add(new_user)
                db.session.commit()
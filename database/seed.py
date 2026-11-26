from database.connection import SessionLocal
from database.models import Makanan, Penyakit, Relasi, Admin
from services.auth_service import hash_password

def seed_data():
    db = SessionLocal()
    
    admin = db.query(Admin).filter(Admin.username == "admin").first()
    if not admin:
        new_admin = Admin(username="admin", password=hash_password("admin123"))
        db.add(new_admin)
        db.commit()
    
    if db.query(Makanan).count() == 0:
        makanan_list = [
            Makanan(nama="Pisang", kategori="Buah", kalori=89.0, manfaat="Sumber kalium, serat, dan vitamin B6 yang baik untuk pencernaan."),
            Makanan(nama="Kopi", kategori="Minuman", kalori=2.0, manfaat="Kaya antioksidan dan kafein yang dapat meningkatkan kewaspadaan."),
            Makanan(nama="Oatmeal", kategori="Karbohidrat", kalori=389.0, manfaat="Mengandung beta-glukan untuk membantu menurunkan kolesterol."),
            Makanan(nama="Ikan Asin", kategori="Protein", kalori=193.0, manfaat="Sumber protein dan kalsium, namun sangat tinggi kadar natrium."),
            Makanan(nama="Salmon", kategori="Protein", kalori=208.0, manfaat="Kaya asam lemak omega-3 untuk mendukung kesehatan jantung."),
            Makanan(nama="Jeruk", kategori="Buah", kalori=47.0, manfaat="Kaya vitamin C dan antioksidan untuk kekebalan tubuh."),
            Makanan(nama="Bayam", kategori="Sayur", kalori=23.0, manfaat="Tinggi zat besi, folat, dan serat untuk sel darah merah."),
            Makanan(nama="Nasi Putih", kategori="Karbohidrat", kalori=130.0, manfaat="Sumber energi utama karbohidrat sederhana.")
        ]
        db.add_all(makanan_list)
        db.commit()

    if db.query(Penyakit).count() == 0:
        penyakit_list = [
            Penyakit(nama="Gastritis/GERD", deskripsi="Peradangan pada mukosa lambung atau asam lambung kronis.", gejala="Nyeri ulu hati, mual, perut kembung, perih.", pencegahan="Makan teratur porsi kecil, hindari pedas, asam, kafein."),
            Penyakit(nama="Diabetes Tipe 2", deskripsi="Kadar gula darah tinggi akibat resistensi insulin.", gejala="Sering haus, sering kencing, cepat lelah.", pencegahan="Batasi konsumsi karbohidrat sederhana dan gula, olahraga."),
            Penyakit(nama="Hipertensi", deskripsi="Tekanan darah 140/90 mmHg atau lebih tinggi.", gejala="Sakit kepala belakang, pusing, jantung berdebar.", pencegahan="Kurangi asupan garam/natrium dan makanan olahan."),
            Penyakit(nama="Kolesterol Tinggi", deskripsi="Kadar lemak LDL berlebih dalam pembuluh darah.", gejala="Sering pegal tengkuk, cepat lelah, nyeri dada ringan.", pencegahan="Perbanyak serat larut & omega-3, kurangi lemak jenuh."),
            Penyakit(nama="Anemia Defisiensi Besi", deskripsi="Kekurangan sel darah merah sehat akibat kurang zat besi.", gejala="Lemas, pucat, pusing, konsentrasi menurun.", pencegahan="Konsumsi makanan tinggi zat besi dan vitamin C.")
        ]
        db.add_all(penyakit_list)
        db.commit()

    if db.query(Relasi).count() == 0:
        m_dict = {m.nama: m.id for m in db.query(Makanan).all()}
        p_dict = {p.nama: p.id for p in db.query(Penyakit).all()}
        
        relasi_list = [
            Relasi(makanan_id=m_dict["Pisang"], penyakit_id=p_dict["Gastritis/GERD"], status="Dianjurkan", alasan="Pisang bersifat antasida alami dan meredakan iritasi dinding lambung."),
            Relasi(makanan_id=m_dict["Oatmeal"], penyakit_id=p_dict["Gastritis/GERD"], status="Dianjurkan", alasan="Serat halus oatmeal menyerap asam lambung berlebih."),
            Relasi(makanan_id=m_dict["Kopi"], penyakit_id=p_dict["Gastritis/GERD"], status="Hindari", alasan="Kafein menstimulasi produksi asam lambung dan merelaksasi klep esofagus."),
            Relasi(makanan_id=m_dict["Jeruk"], penyakit_id=p_dict["Gastritis/GERD"], status="Batasi", alasan="Kandungan asam sitrat dapat memicu perih pada lambung yang teriritasi."),
            Relasi(makanan_id=m_dict["Oatmeal"], penyakit_id=p_dict["Diabetes Tipe 2"], status="Dianjurkan", alasan="Kaya serat beta-glukan untuk memperlambat penyerapan glukosa."),
            Relasi(makanan_id=m_dict["Nasi Putih"], penyakit_id=p_dict["Diabetes Tipe 2"], status="Batasi", alasan="Indeks glikemik tinggi meningkatkan kadar gula darah dengan cepat."),
            Relasi(makanan_id=m_dict["Salmon"], penyakit_id=p_dict["Diabetes Tipe 2"], status="Dianjurkan", alasan="Sumber protein tinggi tanpa karbohidrat membantu stabilitas glukosa."),
            Relasi(makanan_id=m_dict["Ikan Asin"], penyakit_id=p_dict["Hipertensi"], status="Hindari", alasan="Tinggi kadar natrium yang menyebabkan kenaikan tekanan darah signifikan."),
            Relasi(makanan_id=m_dict["Pisang"], penyakit_id=p_dict["Hipertensi"], status="Dianjurkan", alasan="Tinggi kalium yang menyeimbangkan efek natrium pada pembuluh darah."),
            Relasi(makanan_id=m_dict["Bayam"], penyakit_id=p_dict["Hipertensi"], status="Dianjurkan", alasan="Kaya nitrat alami dan magnesium untuk membantu kelenturan pembuluh darah."),
            Relasi(makanan_id=m_dict["Oatmeal"], penyakit_id=p_dict["Kolesterol Tinggi"], status="Dianjurkan", alasan="Beta-glukan mengikat kolesterol LDL di usus halus dan membuangnya."),
            Relasi(makanan_id=m_dict["Salmon"], penyakit_id=p_dict["Kolesterol Tinggi"], status="Dianjurkan", alasan="Asam lemak Omega-3 membantu meningkatkan kadar kolesterol baik (HDL)."),
            Relasi(makanan_id=m_dict["Bayam"], penyakit_id=p_dict["Anemia Defisiensi Besi"], status="Dianjurkan", alasan="Kaya zat besi non-heme untuk produksi sel darah merah/hemoglobin."),
            Relasi(makanan_id=m_dict["Jeruk"], penyakit_id=p_dict["Anemia Defisiensi Besi"], status="Dianjurkan", alasan="Vitamin C meningkatkan penyerapan zat besi dari bahan makanan nabati.")
        ]
        db.add_all(relasi_list)
        db.commit()

    db.close()

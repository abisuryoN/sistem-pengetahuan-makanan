from database.connection import SessionLocal
from database.models import Makanan, Relasi, Penyakit

VALID_KATEGORI = ["Karbohidrat", "Buah", "Sayur", "Protein", "Olahan", "Minuman"]

def get_all_makanan(search_query: str = None, kategori_filter: str = None):
    db = SessionLocal()
    try:
        query = db.query(Makanan)
        if search_query:
            search = f"%{search_query}%"
            query = query.filter(Makanan.nama.ilike(search) | Makanan.manfaat.ilike(search))
        if kategori_filter and kategori_filter != "Semua":
            query = query.filter(Makanan.kategori == kategori_filter)
        return query.order_by(Makanan.nama.asc()).all()
    finally:
        db.close()

def get_makanan_by_id(makanan_id: int):
    db = SessionLocal()
    try:
        return db.query(Makanan).filter(Makanan.id == makanan_id).first()
    finally:
        db.close()

def create_makanan(nama: str, kategori: str, kalori: float, manfaat: str):
    if kategori not in VALID_KATEGORI:
        raise ValueError(f"Kategori tidak valid. Pilih salah satu: {', '.join(VALID_KATEGORI)}")
    
    db = SessionLocal()
    try:
        existing = db.query(Makanan).filter(Makanan.nama.ilike(nama.strip())).first()
        if existing:
            raise ValueError(f"Makanan dengan nama '{nama}' sudah ada.")
        
        new_makanan = Makanan(
            nama=nama.strip(),
            kategori=kategori,
            kalori=kalori,
            manfaat=manfaat.strip()
        )
        db.add(new_makanan)
        db.commit()
        db.refresh(new_makanan)
        return new_makanan
    finally:
        db.close()

def update_makanan(makanan_id: int, nama: str, kategori: str, kalori: float, manfaat: str):
    if kategori not in VALID_KATEGORI:
        raise ValueError(f"Kategori tidak valid. Pilih salah satu: {', '.join(VALID_KATEGORI)}")
        
    db = SessionLocal()
    try:
        makanan = db.query(Makanan).filter(Makanan.id == makanan_id).first()
        if not makanan:
            raise ValueError("Data makanan tidak ditemukan.")
        
        # Cek duplikat nama dengan ID lain
        existing = db.query(Makanan).filter(Makanan.nama.ilike(nama.strip()), Makanan.id != makanan_id).first()
        if existing:
            raise ValueError(f"Makanan dengan nama '{nama}' sudah digunakan.")
            
        makanan.nama = nama.strip()
        makanan.kategori = kategori
        makanan.kalori = kalori
        makanan.manfaat = manfaat.strip()
        db.commit()
        return makanan
    finally:
        db.close()

def delete_makanan(makanan_id: int):
    db = SessionLocal()
    try:
        makanan = db.query(Makanan).filter(Makanan.id == makanan_id).first()
        if not makanan:
            raise ValueError("Data makanan tidak ditemukan.")
        db.delete(makanan)
        db.commit()
        return True
    finally:
        db.close()

def get_relasi_by_makanan(makanan_id: int):
    db = SessionLocal()
    try:
        return db.query(Relasi, Penyakit).join(Penyakit, Relasi.penyakit_id == Penyakit.id).filter(Relasi.makanan_id == makanan_id).all()
    finally:
        db.close()


from database.connection import SessionLocal
from database.models import Penyakit, Relasi, Makanan

def get_all_penyakit(search_query: str = None):
    db = SessionLocal()
    try:
        query = db.query(Penyakit)
        if search_query:
            search = f"%{search_query}%"
            query = query.filter(Penyakit.nama.ilike(search) | Penyakit.deskripsi.ilike(search) | Penyakit.gejala.ilike(search))
        return query.order_by(Penyakit.nama.asc()).all()
    finally:
        db.close()

def get_penyakit_by_id(penyakit_id: int):
    db = SessionLocal()
    try:
        return db.query(Penyakit).filter(Penyakit.id == penyakit_id).first()
    finally:
        db.close()

def create_penyakit(nama: str, deskripsi: str, gejala: str, pencegahan: str):
    db = SessionLocal()
    try:
        existing = db.query(Penyakit).filter(Penyakit.nama.ilike(nama.strip())).first()
        if existing:
            raise ValueError(f"Penyakit dengan nama '{nama}' sudah ada.")
        
        new_p = Penyakit(
            nama=nama.strip(),
            deskripsi=deskripsi.strip(),
            gejala=gejala.strip(),
            pencegahan=pencegahan.strip()
        )
        db.add(new_p)
        db.commit()
        db.refresh(new_p)
        return new_p
    finally:
        db.close()

def update_penyakit(penyakit_id: int, nama: str, deskripsi: str, gejala: str, pencegahan: str):
    db = SessionLocal()
    try:
        penyakit = db.query(Penyakit).filter(Penyakit.id == penyakit_id).first()
        if not penyakit:
            raise ValueError("Data penyakit tidak ditemukan.")
        
        existing = db.query(Penyakit).filter(Penyakit.nama.ilike(nama.strip()), Penyakit.id != penyakit_id).first()
        if existing:
            raise ValueError(f"Penyakit dengan nama '{nama}' sudah ada.")
            
        penyakit.nama = nama.strip()
        penyakit.deskripsi = deskripsi.strip()
        penyakit.gejala = gejala.strip()
        penyakit.pencegahan = pencegahan.strip()
        db.commit()
        return penyakit
    finally:
        db.close()

def delete_penyakit(penyakit_id: int):
    db = SessionLocal()
    try:
        penyakit = db.query(Penyakit).filter(Penyakit.id == penyakit_id).first()
        if not penyakit:
            raise ValueError("Data penyakit tidak ditemukan.")
        db.delete(penyakit)
        db.commit()
        return True
    finally:
        db.close()

def get_relasi_by_penyakit(penyakit_id: int):
    """
    Mengambil daftar makanan beserta status dan alasan ilmiah untuk penyakit tertentu,
    menggunakan query JOIN antara tabel Relasi dan Makanan.
    """
    db = SessionLocal()
    try:
        results = db.query(Relasi, Makanan).join(Makanan, Relasi.makanan_id == Makanan.id).filter(Relasi.penyakit_id == penyakit_id).all()
        return results
    finally:
        db.close()


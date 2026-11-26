from database.connection import SessionLocal
from database.models import Relasi, Makanan, Penyakit

VALID_STATUS = ["Dianjurkan", "Batasi", "Hindari"]

def get_all_relasi(makanan_id: int = None, penyakit_id: int = None, status_filter: str = None):
    db = SessionLocal()
    try:
        query = db.query(Relasi, Makanan, Penyakit).join(Makanan, Relasi.makanan_id == Makanan.id).join(Penyakit, Relasi.penyakit_id == Penyakit.id)
        
        if makanan_id:
            query = query.filter(Relasi.makanan_id == makanan_id)
        if penyakit_id:
            query = query.filter(Relasi.penyakit_id == penyakit_id)
        if status_filter and status_filter != "Semua":
            query = query.filter(Relasi.status == status_filter)
            
        return query.order_by(Penyakit.nama.asc(), Makanan.nama.asc()).all()
    finally:
        db.close()

def create_relasi(makanan_id: int, penyakit_id: int, status: str, alasan: str):
    if not makanan_id or not penyakit_id:
        raise ValueError("Makanan dan Penyakit wajib dipilih.")
    if status not in VALID_STATUS:
        raise ValueError(f"Status tidak valid. Opsi yang diperbolehkan: {', '.join(VALID_STATUS)}")
    if not alasan or not alasan.strip():
        raise ValueError("Alasan ilmiah wajib diisi.")
        
    db = SessionLocal()
    try:
        # Check duplicate relation
        existing = db.query(Relasi).filter(Relasi.makanan_id == makanan_id, Relasi.penyakit_id == penyakit_id).first()
        if existing:
            raise ValueError("Relasi antara Makanan dan Penyakit ini sudah ada.")
            
        new_relasi = Relasi(
            makanan_id=makanan_id,
            penyakit_id=penyakit_id,
            status=status,
            alasan=alasan.strip()
        )
        db.add(new_relasi)
        db.commit()
        db.refresh(new_relasi)
        return new_relasi
    finally:
        db.close()

def update_relasi(relasi_id: int, status: str, alasan: str):
    if status not in VALID_STATUS:
        raise ValueError(f"Status tidak valid. Opsi yang diperbolehkan: {', '.join(VALID_STATUS)}")
    if not alasan or not alasan.strip():
        raise ValueError("Alasan ilmiah wajib diisi.")
        
    db = SessionLocal()
    try:
        relasi = db.query(Relasi).filter(Relasi.id == relasi_id).first()
        if not relasi:
            raise ValueError("Data relasi tidak ditemukan.")
            
        relasi.status = status
        relasi.alasan = alasan.strip()
        db.commit()
        return relasi
    finally:
        db.close()

def delete_relasi(relasi_id: int):
    db = SessionLocal()
    try:
        relasi = db.query(Relasi).filter(Relasi.id == relasi_id).first()
        if not relasi:
            raise ValueError("Data relasi tidak ditemukan.")
        db.delete(relasi)
        db.commit()
        return True
    finally:
        db.close()


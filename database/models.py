from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from database.connection import Base

class Makanan(Base):
    __tablename__ = "makanan"
    id = Column(Integer, primary_key=True)
    nama = Column(String, unique=True, nullable=False)
    kategori = Column(String, nullable=False)
    kalori = Column(Float)
    manfaat = Column(Text)
    relasi = relationship("Relasi", back_populates="makanan", cascade="all, delete-orphan")

class Penyakit(Base):
    __tablename__ = "penyakit"
    id = Column(Integer, primary_key=True)
    nama = Column(String, unique=True, nullable=False)
    deskripsi = Column(Text)
    gejala = Column(Text)
    pencegahan = Column(Text)
    relasi = relationship("Relasi", back_populates="penyakit", cascade="all, delete-orphan")

class Relasi(Base):
    __tablename__ = "relasi"
    id = Column(Integer, primary_key=True)
    makanan_id = Column(Integer, ForeignKey("makanan.id", ondelete="CASCADE"), nullable=False)
    penyakit_id = Column(Integer, ForeignKey("penyakit.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, nullable=False)
    alasan = Column(Text, nullable=False)
    
    makanan = relationship("Makanan", back_populates="relasi")
    penyakit = relationship("Penyakit", back_populates="relasi")
    __table_args__ = (UniqueConstraint('makanan_id', 'penyakit_id', name='_makanan_penyakit_uc'),)

class Admin(Base):
    __tablename__ = "admin"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)


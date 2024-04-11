from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Float, Date, select, update, delete
from sqlalchemy.orm import relationship, sessionmaker, Session, mapped_column, declarative_base
from sqlalchemy import create_engine
import os, dotenv, requests, datetime, json, math, subprocess, re, glob

dotenv.load_dotenv()
DATABASE_URL=os.getenv('DATABASE_URL')
# Connection à la BDD
engine = create_engine(DATABASE_URL) # , echo=True
# classe de base dont no objets ORM vont dériver
Base = declarative_base()

class Client(Base):
    __tablename__ = 'clients'
    id  = Column(Integer, primary_key=True)
    name = Column(String)
    adr = Column(String)
    cat = Column(String)
    # 'factures' permet d'accéder aux factures (1..N) du clients
    factures = relationship("Facture", back_populates="client")

    def __str__(this):
        return f"CLIENT [{this.id}] {this.name} ({this.adr})"

class Facture(Base):
    __tablename__ = 'factures'
    no = Column(String, primary_key=True)
    dt = Column(DateTime)
    total = Column(Float)
    # client_id est la FK
    client_id = mapped_column(ForeignKey("clients.id"))
    # 'client' permet d'accéder au client lié à la facture
    client = relationship("Client", back_populates="factures")
    commandes = relationship("Commande", back_populates="facture")
    
    def __str__(this):
        return f"FACTURE [{this.no}] {this.total}€"
    
    @staticmethod
    def read_file(no):
        '''méthode de classe'''
        with Session(engine) as session:
            query = select(Facture).where(Facture.no==no)
            res = session.execute(query).scalar()
            if not res:
                fac=Facture(no=no, total=0.0)
                session.add(fac)
                session.commit()
            return fac # facture créee à partir des info des TXT
    
class Commande(Base):
    __tablename__ = 'commandes'
    facture_no = mapped_column(ForeignKey("factures.no"), primary_key=True)

    produit_name = mapped_column(ForeignKey("produits.name"), primary_key=True)
    index = Column(Integer)
    qty = Column(Integer)
    produit = relationship("Produit", back_populates="commandes")
    facture = relationship("Facture", back_populates="commandes")
    
class Produit(Base):
    __tablename__ = 'produits'
    name = Column(String, primary_key=True)
    price = Column(Float)
    commandes = relationship("Commande", back_populates="produit")       


# Cette commande crée dans la BDD les tables correspondantes
Base.metadata.create_all(bind=engine)

if __name__=="__main__":
    print('DATABASE_URL=', DATABASE_URL)
    
    fac=Facture.read_file("FAC_2024-0000")
    print(fac)
    
    # with Session(engine) as session:
    #     '''
    #     client = Client(id=1, name="Essai", adr="Ici")
    #     print(client)
    #     session.add(client)
    #     session.commit()
    #     '''

    #     query=select(Client).where(Client.id==1)
    #     print(query)
    #     client = session.execute(query).scalar()
    #     print(client)

    #     fac=Facture(no="FAC_2024-0000", total=0.0)
    #     fac.client=client
    #     session.add(fac)
    #     session.commit()


    #     query=select(Client)
    #     clients = session.execute(query).all()
    #     print(clients)
    #     for row in clients:
    #         client=row[0]
    #         print(client, client.factures)
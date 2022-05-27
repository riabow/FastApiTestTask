""" writen by riabow@mail.ru +79263772728 """
from datetime import datetime
import uvicorn
from fastapi import FastAPI
from pandas import pandas
from sqlalchemy import create_engine, insert, delete, Table, Column, Integer, \
    Date, Float, String, MetaData, func, update, desc
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from findway import find_the_way

SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)



Base = declarative_base()


class Exch(Base):
    __tablename__ = 'exch'
    id = Column(Integer, primary_key=True)
    date = Column(Date, index=True)
    fr = Column(String, index=True)
    to = Column(String, index=True)
    exch_rate = Column(Float)


meta = MetaData(bind=engine)
MetaData.reflect(meta)

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Welcome to exchange API. Start with /read_csv to load data"\
                       " /docs - dpcumentation of progect "\
                        " /getrates - whill found you the way to convert currencys "
            }


@app.get("/create_tables")
def create_tables():
    Base.metadata.create_all(engine)
    return {"message": "tables created"}

@app.delete("/delete_rate_by_id/{id}")
def delete_rate_by_id(id: str):
    """delete rate by id"""
    s = SessionLocal()
    search_rate = s.query(Exch).get(id)
    if search_rate:
        s.delete(search_rate)
        s.commit()
        s.close()
        return {"message": f"rate {id} has been deleted"}
    else:
        return {"message": f"rate {id} not found "}

@app.get("/get_history/{fr}/{to}")
def get_history(fr: str, to: str):
    s = SessionLocal()
    ret = s.query(Exch).filter_by(fr=fr, to=to).order_by(Exch.date.desc()).all()
    if ret:
        return {"rates": ret}
    else:
        return{"message": "no history found "}


@app.put("/add_update_rate/{d}/{fr}/{to}/{rate}")
def add_update_rate(d: str, fr: str, to: str, rate: str):
    """ Add new or correct existing rate """
    try:
        correct_date = datetime.fromisoformat(d)
    except:
        return {"message": f"wrong date format {d}"}
    s = SessionLocal()
    ret = s.query(Exch).filter_by(date=func.DATE(d), fr=fr, to=to).first()  # all()
    if ret:
        ret.exch_rate = rate
        ret_id = ret.id
        s.commit()
        # s.close()
        return {"message": "rate updated", "ret_id": ret_id}
    else:
        newrate = Exch(date=func.DATE(d), fr=fr, to=to, exch_rate=rate)
        s.add(newrate)
        s.commit()
        ret_id = newrate.id
        return {"message": "new rate created", "ret_id": ret_id}


@app.get("/getrates/{d}/{fr}/{to}")
def getrates(d: str, fr: str, to: str):
    """Return rate on given date and currencys  """
    try:
        dd = datetime.fromisoformat(d)
    except:
        return {"wrong date format": d}

    s = SessionLocal()
    ret = s.query(Exch).filter_by(date=func.DATE(dd), fr=fr, to=to).all()
    if ret:
        return {"message":"we found direct rate",
                "retrate": ret[0].exch_rate,
                "rates": ret}
    else: # gonna try reverse
        ret = s.query(Exch).filter_by(date=func.DATE(dd), fr=to, to=fr).all()
        if ret:
            return {"message": "we found reverse rate",
                    "retrate": 1/ret[0].exch_rate,
                    "rates": ret}
        else: #gonna make some hard work
            allrates = s.query(Exch).filter_by(date=func.DATE(dd)).all()
            return find_the_way(allrates, fr, to)

    return {"message":"Sorry we could not found rate"}

@app.get("/read_csv")
def read_csv():
    """read csv data and put rates to the table"""
    file_name = './exchange.csv'
    df = pandas.read_csv(file_name)
    s = SessionLocal()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    objects = []

    for index, row in df.iterrows():
        for colname, val in row.iteritems():
            if colname == "Date":
                current_date = val
            else:
                fr, to = colname.split("/")
                objects.append(Exch(date=datetime.fromisoformat(current_date),
                                     fr=fr,
                                     to=to,
                                     exch_rate=val,
                                     ))

    s.bulk_save_objects(objects)
    s.commit()
    # line below make table with original format
    # df.to_sql(con=engine, index_label='id', name="exchange", if_exists='replace')
    return {"message": "exchange.csv has been imported"}


if __name__ == "__main__":
    uvicorn.run(app=app, host="127.0.0.1", port=5000, log_level="info")

from flask import Flask, render_template, redirect, request
from flask_sqlalchemy import SQLAlchemy
from datetime import time
from sqlalchemy import Column, Integer, String, Text
import statistics
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from numpy import genfromtxt
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///formdata.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'

db = SQLAlchemy(app)

def Load_Data(file_name):
    data = genfromtxt(file_name, delimiter=';', dtype=str)
    print(data.tolist())
    return data.tolist()

Base = declarative_base()

class Price_History(Base):
    #Tell SQLAlchemy what the table name is and if there's any table-specific arguments it should know about
    __table_args__ = {'sqlite_autoincrement': True}
    #tell SQLAlchemy the name of column and its attributes:
    __tablename__ = 'STUDENTS'
    ID = Column(Integer, primary_key=True, nullable=False)
    SCHOOL = Column(String)
    SEX = Column(String)
    AGE = Column(Integer)
    ADRESS = Column(String)
    FAMSIZE = Column(String)
    TRAVELTIME = Column(Integer)
    STUDYTIME = Column(Integer)
    HIGHER = Column(String)
    FREETIME = Column(Integer)
    DALC = Column(Integer)
    WALC = Column(Integer)
    G3 = Column(Integer)

    def __init__(self,SCHOOL,SEX,AGE,ADRESS,FAMSIZE,TRAVELTIME,STUDYTIME,HIGHER,FREETIME,DALC,WALC,G3):
        self.SCHOOL = SCHOOL
        self.SEX = SEX
        self.AGE = AGE
        self.ADRESS = ADRESS
        self.FAMSIZE = FAMSIZE
        self.TRAVELTIME = TRAVELTIME
        self.STUDYTIME = STUDYTIME
        self.HIGHER = HIGHER
        self.FREETIME = FREETIME
        self.DALC = DALC
        self.WALC = WALC
        self.G3 = G3
'''
    def __repr__(self):
        return "<Price_History('%s','%s','%d','%s','%s','%d','%d','%s','%d','%d','%d','%d')>" % (self.SCHOOL,
        self.SEX, self.AGE, self.ADRESS, self.FAMSIZE, self.TRAVELTIME, self.STUDYTIME, self.HIGHER,
        self.FREETIME, self.DALC, self.WALC, self.G3)
'''
@app.route("/")
def welcome():
    return render_template('welcome.html')

@app.route("/raw")
def show_raw():
    fd = db.session.query(Price_History).all()
    return render_template('raw.html', formdata=fd)


@app.route("/result")
def show_result():
    fd_list = db.session.query(Price_History).all()

    # Some simple statistics for sample questions
    GPWantEducation = []
    MSWantEducation = []
    GPFree = []
    GPStudy = []
    GPTravel = []
    MSFree = []
    MSStudy = []
    MSTravel = []
    for el in fd_list:
        if(el.SCHOOL=='GP'):
            GPWantEducation.append(el.SCHOOL)
            GPFree.append(el.FREETIME)
            GPStudy.append(el.STUDYTIME)
            GPTravel.append(el.TRAVELTIME)
        elif(el.SCHOOL=='MS'):
            MSWantEducation.append(el.SCHOOL)
            MSFree.append(el.FREETIME)
            MSStudy.append(el.STUDYTIME)
            MSTravel.append(el.TRAVELTIME)
        else:
            print("School error")

    mean_GPTravel = statistics.mean(GPTravel)
    mean_GPFree = statistics.mean(GPFree)
    mean_GPStudy = statistics.mean(GPStudy)

    mean_MSTravel = statistics.mean(MSTravel)
    mean_MSFree = statistics.mean(MSFree)
    mean_MSStudy = statistics.mean(MSStudy)


    # Prepare data for google charts
    data = [['GP School', len(GPWantEducation)], ['MS School', len(MSWantEducation)]]
    GPdata = [['Free time [h]', mean_GPFree], ['Study time [h]', mean_GPStudy], ['Travel time [h]', mean_GPTravel]]
    MSdata = [['Free time [h]', mean_MSFree], ['Study time [h]', mean_MSStudy], ['Travel time [h]', mean_MSTravel]]
    return render_template('result.html', data=data, GPdata=GPdata, MSdata=MSdata)

@app.route("/result2")
def show_result2():
    fd_list = db.session.query(Price_History).all()

    # Some simple statistics for sample questions
    GPDALC = []
    GPWALC = []
    MSWALC = []
    MSDALC = []
    for el in fd_list:
        if(el.SCHOOL=='GP'):
            GPWALC.append(el.WALC)
            GPDALC.append(el.DALC)
        elif(el.SCHOOL=='MS'):
            MSWALC.append(el.WALC)
            MSDALC.append(el.DALC)
        else:
            print("School error")

    mean_GPWALC = statistics.mean(GPWALC)
    mean_GPDALC = statistics.mean(GPDALC)

    mean_MSWALC = statistics.mean(MSWALC)
    mean_MSDALC = statistics.mean(MSDALC)

    # Prepare data for google charts
    data = [['GP School Workday Alcohol Consumption', mean_GPDALC], ['GP School Weekend  Alcohol Consumption', mean_GPWALC],
            ['MS School Workday Alcohol Consumption', mean_MSDALC], ['MS School Weekend Alcohol Consumption', mean_MSWALC]]
    return render_template('result2.html', data=data)

@app.route("/result3")
def show_result3():
    fd_list = db.session.query(Price_History).all()

    # Some simple statistics for sample questions
    MDALC = []
    MWALC = []
    FWALC = []
    FDALC = []
    for el in fd_list:
        if(el.SEX=='M'):
            MWALC.append(el.WALC)
            MDALC.append(el.DALC)
        elif(el.SEX=='F'):
            FWALC.append(el.WALC)
            FDALC.append(el.DALC)
        else:
            print("Sex error")

    mean_MWALC = statistics.mean(MWALC)
    mean_MDALC = statistics.mean(MDALC)

    mean_FWALC = statistics.mean(FWALC)
    mean_FDALC = statistics.mean(FDALC)

    # Prepare data for google charts
    data = [['Female Workday Alcohol Consumption', mean_FDALC], ['Female Weekend  Alcohol Consumption', mean_FWALC],
            ['Male Workday Alcohol Consumption', mean_MDALC], ['Male Weekend Alcohol Consumption', mean_MWALC]]
    return render_template('result3.html', data=data)


if __name__ == "__main__":
    app.debug = True
    t = time()

    # Create the database
    engine = create_engine('sqlite:///formdata.db')
    if not(engine.dialect.has_table(engine.connect(), "STUDENTS")):
        Base.metadata.create_all(engine)

    # Create the session
    session = sessionmaker()
    session.configure(bind=engine)
    s = session()

    try:
        file_name = "studentDataSet.csv"
        data = Load_Data(file_name)

        for i in data:
            record = Price_History(**{
                'SCHOOL':i[0],
                'SEX':i[1],
                'AGE':int(i[2]),
                'ADRESS':i[3],
                'FAMSIZE':i[4],
                'TRAVELTIME':int(i[5]),
                'STUDYTIME':int(i[6]),
                'HIGHER':i[7],
                'FREETIME':int(i[8]),
                'DALC':int(i[9]),
                'WALC':int(i[10]),
                'G3':int(i[11])
            })
            s.add(record)  # Add all the records
        s.commit()  # Attempt to commit all the records
    except:
        s.rollback()  # Rollback the changes on error
    finally:
        app.run()
        s.close()  # Close the connection


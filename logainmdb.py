from sqlalchemy import Column, String, Integer, Float, Boolean, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine


Base = declarative_base()


class PlaceName(Base):
    __tablename__ = 'place_name'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name_en = Column(String(50))
    name_ga = Column(String(50))

    def __init__(self, name_en, name_ga):
        self.name_en = name_en
        self.name_ga = name_ga

    def getname(self, lang):
        if lang == 'en':
            return self.name_en
        elif lang == 'ga':
            return self.name_ga


class PlaceType(Base):
    __tablename__ = 'place_type'

    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(10))
    desc_en = Column(String(120))
    desc_ga = Column(String(120))

    def __init__(self, code, desc_en, desc_ga):
        self.code = code
        self.desc_en = desc_en
        self.desc_ga = desc_ga


class Place(Base):
    __tablename__ = 'place'

    id = Column(Integer, primary_key=True, autoincrement=True)
    logainm_id = Column(Integer)
    place_name_id = Column(Integer, ForeignKey('place_name.id'))
    place_type_id = Column(Integer, ForeignKey('place_type.id'))
    longitude = Column(Float)
    latitude = Column(Float)
    geo_accurate = Column(Boolean)

    def __init__(self, logainm_id, place_name, place_type, lon, lat, geo_acc):
        self.logainm_id = logainm_id
        self.place_name = place_name
        self.place_type = place_type
        self.place_name_id = place_name.id
        self.place_type_id = place_type.id
        self.longitude = lon
        self.latitude = lat
        self.geo_accurate = geo_acc

engine = create_engine('sqlite:///sql/logainm.db', echo=True)
Base.metadata.create_all(engine)

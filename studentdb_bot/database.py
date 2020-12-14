import logging
from pathlib import Path

from sqlalchemy import create_engine, Column, ForeignKey, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class Student(Base):
    __tablename__ = 'students'

    id = Column(String, primary_key=True)
    grade_id = Column(String, ForeignKey('grades.id'))
    grade = relationship('Grade', back_populates='students')
    class_id = Column(String, ForeignKey('classes.id'))
    class_obj = relationship('StudentClass', back_populates='students')
    name = Column(String)
    _pinyin = Column('pinyin', String)
    gender = Column('gender', String)
    birthday = Column(String(10), nullable=True)
    eduid = Column(String(8), nullable=True)

    @property
    def pinyin_full(self) -> tuple[str]:
        values = [str(i).strip() for i in self._pinyin.split('/')]
        return tuple(values)

    @property
    def pinyin_first(self) -> tuple[str]:
        values = []
        for pinyin in self.pinyin_full:
            value = ''.join([i[0].strip() for i in pinyin.split(' ')])
            values.append(value)
        return tuple(values)


class StudentClass(Base):
    __tablename__ = 'classes'

    id = Column(String, primary_key=True)
    grade_id = Column(String, ForeignKey('grades.id'))
    grade = relationship('Grade', back_populates='classes')
    students = relationship('Student', back_populates='classes',
                            order_by=Student.id)


class Grade(Base):
    __tablename__ = 'grades'

    id = Column(String, primary_key=True)
    classes = relationship('StudentClass', back_populates='grades',
                           order_by=StudentClass.id)


class Database:

    def __init__(self):
        path = Path(__file__).resolve().parent.parent / 'database/database.sqlite'
        enable_echo = logging.getLogger().level <= logging.DEBUG
        self.engine = create_engine(f'sqlite:///{path}', echo=enable_echo)
        logging.info(f'Using database at "{path}".')
        Base.metadata.create_all(self.engine)
        logging.debug(f'Tables created (if missing).')

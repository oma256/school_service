from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Integer, String, ForeignKey


db = SQLAlchemy()
Base = db.Model


class Position(Base):
    __tablename__ = 't_position'

    id = Column(Integer, primary_key=True)
    name = Column(String(256))


class Teacher(Base):
    __tablename__ = 't_teacher'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    position_id = Column(Integer, ForeignKey('t_position.id'))


class Group(Base):
    __tablename__ = 't_group'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class Student(Base):
    __tablename__ = 't_student'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    group_id = Column(Integer, ForeignKey('t_group.id'))


class Subject(Base):
    __tablename__ = 't_subject'

    id = Column(Integer, primary_key=True)
    name = Column(String(128))


class TeacherGroupSubject(Base):
    __tablename__ = 't_teacher_group_subject'

    id = Column(Integer, primary_key=True)
    teacher_id = Column(Integer, ForeignKey('t_teacher.id'))
    group_id = Column(Integer, ForeignKey('t_group.id'))
    subject_id = Column(Integer, ForeignKey('t_subject.id'))


class User(Base):
    __tablename__ = 't_user'

    id = Column(Integer, primary_key=True)
    first_name = Column(String(128))
    last_name = Column(String(128))
    email = Column(String(256))
    phone_number = Column(String(32))
    password = Column(String(128))

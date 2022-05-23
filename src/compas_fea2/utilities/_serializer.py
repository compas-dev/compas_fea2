from sqlalchemy import Column, Integer, Unicode, UnicodeText, String
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

from random import choice


def _start_engine(db=None, echo=True):
    engine = create_engine('sqlite://', echo=True)
    Base = declarative_base(bind=engine)
    Base.metadata.create_all()
    Model()
    Session = sessionmaker(bind=engine)
    return Session()


def _add_members(session, members):
    session.add_all(members)
    session.commit()


def _get_members(session, members):
    pass


if __name__ == '__main__':
    from compas_fea2.model import Model

    mdl = Model()

    s = _start_engine()
    _add_members(s, [mdl])

    print(s)

    # for member in s.query(Model):
    #     print(type(user), user.name, user.password)

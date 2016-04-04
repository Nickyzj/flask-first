from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import Integer, String
from sqlalchemy import String, Numeric, DateTime, Enum
from sqlalchemy import ForeignKey

engin = create_engine("sqlite://")
metadata = MetaData()
metadata.create_all(engin)

user_table = Table('user', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String),
                   Column('fullname', String)
                   )

fancy_table = Table('fancy', metadata,
                    Column('key', String(50), primary_key=True),
                    Column('timestamp', DateTime),
                    Column('amount', Numeric(10, 2)),
                    Column('type', Enum('a', 'b', 'c'))
                    )
fancy_table.create(engin)

address_table = Table('address', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('email_address', String(100), nullable=False),
                      Column('user_id', Integer, ForeignKey('user.id'))
                      )

address_table.create(engin)



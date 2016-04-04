from sqlalchemy import create_engine, MetaData
from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy import Integer, String, Numeric, Enum
from sqlalchemy import Unicode, UnicodeText, DateTime
from sqlalchemy import ForeignKeyConstraint

engine = create_engine("sqlite://")
metadata = MetaData()
metadata2 = MetaData()

fancy_table = Table('fancy', metadata,
                    Column('key', String(50), primary_key=True),
                    Column('timestamp', DateTime),
                    Column('amount', Numeric(10, 2)),
                    Column('type', Enum('a', 'b', 'c'))
                    )

address_table = Table('address', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('email_address', String(100), nullable=False),
                      Column('user_id', Integer, ForeignKey('user.id'))
                      )

story_table = Table('story', metadata,
                    Column('story_id', Integer, primary_key=True),
                    Column('version_id', Integer, primary_key=True),
                    Column('headline', Unicode(100), nullable=False),
                    Column('body', UnicodeText)
                    )

published_table = Table('published', metadata,
                        Column('pub_id', Integer, primary_key=True),
                        Column('pub_timestamp', DateTime, nullable=False),
                        Column('story_id', Integer),
                        Column('version_id', Integer),
                        ForeignKeyConstraint(
                            ['story_id', 'version_id'],
                            ['story.story_id', 'story.version_id']
                            )
                        )

user_table = Table('user', metadata,
                   Column('id', Integer, primary_key=True),
                   Column('name', String),
                   Column('fullname', String)
                   )

metadata.create_all(engine)

user_reflected = Table('user', metadata2, autoload=True, autoload_with=engine)

print '--->', user_reflected.c

from sqlalchemy import inspect

inspector = inspect(engine)

print '--->', inspector

print '--->', inspector.get_table_names()

print '--->', inspector.get_foreign_keys('address')

network = Table('network', metadata,
                Column('network_id', Integer, primary_key=True),
                Column('name', String(100),nullable=False),
                Column('create_at', DateTime, nullable=False),
                Column('owner_id', ForeignKey('user.id'))
                )
network.create(engine)

network_reflected = Table('network', metadata2, autoload=True, autoload_with=engine)

for c in network.c:
    print '--->', c.name

for tname in inspector.get_table_names():
    for col in inspector.get_columns(tname):
        if col['name'] == 'story_id':
            print tname
            break
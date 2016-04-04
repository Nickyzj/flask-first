from sqlalchemy import Unicode, UnicodeText, DateTime
from sqlalchemy import ForeignKeyConstraint
from sqlalchemy import Integer
from sqlalchemy import MetaData
from sqlalchemy import Table, Column
from sqlalchemy import create_engine

engin = create_engine("sqlite://") 
metadata = MetaData()

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

metadata.create_all(engin)
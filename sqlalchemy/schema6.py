from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

##############################

from sqlalchemy import Column, Integer, String

i = 0
def println(*obj_to_print):
	global i
	i += 1
	if(len(obj_to_print) == 1):
		print '%d --->' % i, obj_to_print[0]
	else:
		print '%d --->' % i, obj_to_print
	print ''

class User(Base):

	__tablename__ = 'user'

	id = Column(Integer, primary_key=True)
	name = Column(String)
	fullname = Column(String)

	def __repr(self):
		return "<User(%r, %r)>" % (self.name, self.fullname)


println(User.__table__)

println(User.__mapper__)

println(Base.metadata)

println(Base.metadata.tables)

println(Base._decl_class_registry.keys())

println(Base._decl_class_registry.values())

############################################

ed_user = User(name='ed', fullname='Edward Jones')

println(ed_user.name, ed_user.fullname)

println(ed_user.id)

############################################

from sqlalchemy import create_engine

engine = create_engine('sqlite://')

Base.metadata.create_all(engine)

##########################################

from sqlalchemy.orm import Session

session = Session(bind=engine)

session.add(ed_user)

our_user = session.query(User).filter_by(name='ed').first()

println(our_user)


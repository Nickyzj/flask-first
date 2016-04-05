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

	def __repr__(self):
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

println(ed_user.id)

println(ed_user is our_user)

######################################

session.add_all([
    User(name='wendy', fullname='Wendy Weathersmith'),
    User(name='mary', fullname='Mary Contrary'),
    User(name='fred', fullname='Fred Flinstone')
])

ed_user.fullname = 'Ed Jones'

println(session.dirty)

println(session.new)

session.commit()

println(ed_user.fullname)

##############################

ed_user.name = 'Edwardo'

fake_user = User(name='fakeuser', fullname='Invalid')

session.add(fake_user)

session.query(User).filter(User.name.in_(['Edwardo', 'fakeuser'])).all()

println(ed_user.name)

session.rollback()

println(ed_user.name)

println(fake_user in session)

############################

class Network(Base):

    __tablename__ = 'network'

    network_id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)

    def __repr__(self):
        return "<Network(%r)>" % (self.name)

Base.metadata.create_all(engine)

session.add_all([Network(name='net1'), Network(name='net2')])

session.commit()

result = session.query(Network).all()

println(result)

##############################

println(User.name == 'ed')

println(User.name)

println(User.name.property.columns[0])

println(User.__table__)

query = session.query(User).filter(User.name == 'ed').order_by(User.id)

println(query.all())

for name, fullname in session.query(User.name, User.fullname):
    println(name, fullname)

row = session.query(User.name).first()

println(row.name)

println(row)

println(row[0])

println(type(row))

for row in session.query(User, User.name):
    println(row.User, row.name)

d = dict(session.query(User.name, User))

println(d)

u = session.query(User).order_by(User.id)[2]

println(u)

for u in session.query(User).order_by(User.id)[1:3]:
    println(u)

for name, in session.query(User.name).filter_by(fullname='Ed Jones'):
    println(name)

from sqlalchemy import or_

for name, in session.query(User.name).filter(or_(User.fullname == 'Ed Jones', User.id < 5)):
    println(name)

query = session.query(User).filter_by(fullname='Ed Jones')

query.all()

query.first()

query.one()

query = session.query(User).filter_by(fullname='noneexsitent')

# query.one()

query = session.query(User)

# query.one()

################################

q = session.query(User.fullname).order_by(User.fullname)

q.all()

q2 = q.filter(or_(User.name == 'mary', User.name == 'ed'))

println(q2[1])
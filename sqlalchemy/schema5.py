from sqlalchemy import MetaData, Table, Column, String, Integer

metadata = MetaData()
user_table = Table('user', metadata,
					Column('id', Integer, primary_key=True),
					Column('username', String(50)),
					Column('fullname', String(50))
	)


from sqlalchemy import create_engine
engine = create_engine("sqlite://")
metadata.create_all(engine)

i = 0

i += 1; print '%d --->' % i, user_table.c.username

i += 1; print '%d --->' % i, user_table.c.username.__class__.__mro__

i += 1; print '%d --->' % i, user_table.c.username.__eq__

i += 1; print '%d --->' % i, user_table.c.username == 'ed'

i += 1; print '%d --->' % i, (user_table.c.username == 'ed') | (user_table.c.username == 'jack')

from sqlalchemy import and_, or_

i += 1; print '%d --->' % i, and_(
									user_table.c.fullname == 'ed jones',
									or_(
										user_table.c.username == 'ed',
										user_table.c.username == 'jack'
										)
								)

i += 1; print '%d --->' % i, (user_table.c.id > 5)

i += 1; print '%d --->' % i, (user_table.c.fullname == None)

i += 1; print '%d --->' % i, (user_table.c.id + 5)

i += 1; print '%d --->' % i, (user_table.c.fullname + "some name")

i += 1; print '%d --->' % i, (user_table.c.username.in_(["Wendy", "mary", "ed"]))

expression = user_table.c.username == 'ed'

i += 1; print '%d --->' % i, expression

compiled = expression.compile()

i += 1; print '%d --->' % i, compiled.params

engine.execute(
		user_table.select().where(user_table.c.username == 'ed')
	)

expression = user_table.c.fullname + "some name"

from sqlalchemy.dialects import postgresql

i += 1; print '%d --->' % i, (expression.compile(dialect = postgresql.dialect()))

from sqlalchemy.dialects import mysql

i += 1; print '%d --->' % i, (expression.compile(dialect = mysql.dialect()))

insert_stmt = user_table.insert().values(username='ed', fullname='Ed Jones')

conn = engine.connect()

result = conn.execute(insert_stmt)

i += 1; print '%d --->' % i, result

conn.execute(user_table.insert(), [
		{'username': 'Jack', 'fullname': 'Jack Burger'},
		{'username': 'wendy', 'fullname': 'Wendy Weathersmith'}
	])

from sqlalchemy import select

select_stmt = select([user_table.c.username, user_table.c.fullname]).where(user_table.c.username == 'ed')

result = conn.execute(select_stmt)

for row in result:
	i += 1; print '%d --->' % i, row

select_stmt = select([user_table])

result = conn.execute(select_stmt).fetchall()

for row in result:
	i += 1; print '%d --->' % i, row

select_stmt = select([user_table]).where(
										or_(
											user_table.c.username == 'ed',
											user_table.c.username == 'wendy'
											)
										)

result = conn.execute(select_stmt).fetchall()

for row in result:
	i += 1; print '%d --->' % i, row

select_stmt = select([user_table]).\
					where(user_table.c.username == 'ed').\
					where(user_table.c.fullname == 'Ed Jones')

result = conn.execute(select_stmt).fetchall()

for row in result:
	i += 1; print '%d --->' % i, row

select_stmt = select([user_table]).where((user_table.c.username == 'wendy') | (user_table.c.username == 'dilbert'))

result = conn.execute(select_stmt).fetchall()

for row in result:
	i += 1; print '%d --->' % i, row

update_stmt = user_table.update().\
						values(fullname="Jack Brown").\
						where(user_table.c.username == "jack")

result = conn.execute(update_stmt)

i += 1; print '%d --->' % i, result

update_stmt = user_table.update().\
						values(fullname=user_table.c.username + " " + user_table.c.fullname)

delete_stmt = user_table.delete().\
						where(user_table.c.username == 'jack')

result = conn.execute(delete_stmt)

i += 1; print '%d --->' % i, result.rowcount
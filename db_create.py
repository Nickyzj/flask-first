from project import db
from project.models import BlogPost, User

# db.drop_all()
# db.create_all()


db.session.add(BlogPost("dsfdsf", "ggrevfderfrfre", "4"))
db.session.add(BlogPost("dbtbgbsfdsf", "ggrevfderfrfre", "4"))
db.session.add(BlogPost("bgbfgb", "ggrevfderfrfre", "5"))
db.session.add(BlogPost("dsf43543dsf", "ggrevfderfrfre", "5"))
db.session.add(BlogPost("bgdbgdb", "ggrevfderfrfre", "6"))
db.session.add(BlogPost("dsfdgtrgtgsf", "ggrevfderfrfre", "6"))
db.session.add(BlogPost("dsfr4334fdsf", "ggrevfderfrfre", "7"))
db.session.add(BlogPost("tgtrgr", "ggrevfderfrfre", "8"))



# posts = db.session.query(BlogPost).all()
# print posts

db.session.commit()
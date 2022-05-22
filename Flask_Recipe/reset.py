from flaskrecipe import db
from flaskrecipe.models import Recipe, Ingredient, Step, Tag

Recipe.__table__.drop(db.engine)
Ingredient.__table__.drop(db.engine)
Step.__table__.drop(db.engine)
Tag.__table__.drop(db.engine)


Recipe.__table__.create(db.engine)
Ingredient.__table__.create(db.engine)
Step.__table__.create(db.engine)
Tag.__table__.create(db.engine)

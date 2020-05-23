class todo(db.Model):
    id = db.Column(db.Integer , primary_key=True)
    text = db.Column(db.String(200))
    desc = db.Column(db.String(400))
    deadline = db.Column(db.Date)
    complete = db.Column(db.Boolean)
    
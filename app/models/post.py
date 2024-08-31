from app.extensions import db

class Post(db.Model):
    __tablename__ = 'post'
    __table_args__ = {'schema': 'NutriSwap'}

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150))
    content = db.Column(db.Text)

    def __repr__(self):
        return f'<Post "{self.title}">'

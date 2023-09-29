from package import db


class Video(db.Model):
    __tablename__ = 'video_entry'
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(255))
    date_uploaded = db.Column(db.DateTime)

    def create(self):
        db.session.add(self)
        db.session.commit()
        return self
    
    def __init__(self, video_name, date_uploaded):
        self.video_name = video_name
        self.date_uploaded = date_uploaded

    def __repr__(self):
        return f"{self.id}"
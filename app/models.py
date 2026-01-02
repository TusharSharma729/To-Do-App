from app import db

class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    task_number = db.Column(db.Integer, nullable=False)  # per-user numbering
    title = db.Column(db.String(100), nullable = False)
    time = db.Column(db.String(100), nullable = True)
    date = db.Column(db.String(100), nullable = True)
    # day = db.Column(db.String(100), nullable = True)
    status = db.Column(db.String(20), default = "Pending")

     # NEW: link task to user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)

    # Relationship (optional)
    user = db.relationship("User", backref="tasks")
    
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    display_number = db.Column(db.Integer, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
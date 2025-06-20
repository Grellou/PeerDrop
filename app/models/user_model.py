from app import db, bcrypt

class UserModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20),nullable=False, unique=True)
    email_address = db.Column(db.String(40), nullable=False, unique=True)
    password_hash = db.Column(db.String(40), nullable=False)

    # Hash password
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode("utf-8")

    # Check hashed password
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

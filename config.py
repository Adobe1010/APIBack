class Config:
    SECRET_KEY = 'super_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False 
    JWT_SECRET_KEY = 'jwt_super_secret_key'

EMAIL_CONFIG = {
    "imap_server": "imap.gmail.com",
    "email": "ing.davinsonmartinez@gmail.com",
    "password": "udmc amyf kyim lrcw",
    "mailbox": "INBOX"
}

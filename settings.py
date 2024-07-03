from datetime import timedelta


DATABASE = {
    'host': 'localhost',
    'database': 'db_school_two',
    'user': 'postgres',
    'password': 'postgres',
    'port': 5432,
}
SQLALCHEMY_DATABASE_URI = (
    'postgresql://%(user)s:%(password)s@%(host)s:%(port)s/%(database)s' % DATABASE
)
SECRET_KEY = 'secret_key'
JWT_SECRET_KEY = 'your_jwt_secret_key'
JWT_TOKEN_LOCATION = ['headers']
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)

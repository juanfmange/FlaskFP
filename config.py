from decouple import config

class Config:
    SECRET_KEY = 'juanmange26'
    # CSRF Llave secrta
class DevelopmentConfig(Config):
    DEBUG = True
    MYSQL_HOST='localhost'
    MYSQL_USER='#######' #mariadb user
    MYSQL_PASSWORD='0000000' # Mariadb password
    MYSQL_DB='prueba'
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_port=587 #TLS: Transport LAyer Security
    MAIL_USE_TLS=True
    MAIL_USERNAME='correo@gmail.com'## email origen
    MAIL_PASSWORD = 'contraseña'## email password
    
    
config = {
    'development' : DevelopmentConfig,
    'default' : DevelopmentConfig
}
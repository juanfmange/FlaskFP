class Config:
    SECRET_KEY = 'juanmange26'
    # CSRF Llave secrta
class DevelopmentConfig(Config):
    DEBUG = True
    
config = {
    'development' : DevelopmentConfig,
    'default' : DevelopmentConfig
}
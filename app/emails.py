
from threading import Thread

from flask_mail import Message
from flask import current_app, render_template
def confirmacion_compra(app,mail,usuario,libro):
    try:
        message=Message('Notificacion de compra de envio',sender =current_app.config['MAIL_USERNAME'],recipients=['pillo260697@gmail.com'])
        message.html = render_template('emails/confirmacion_compra.html',usuario=usuario,libro=libro)
        thread = Thread(target=envio_email_async, args=[app, mail, message])
        thread.start()
    except Exception as ex:
        raise Exception(ex)
        

def envio_email_async(app, mail, message):
    with app.app_context():
        mail.send(message)

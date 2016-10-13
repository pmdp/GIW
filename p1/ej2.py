# -*- coding: utf-8 -*-

from smtplib import SMTP
import sys

def sendMail():
    sended = False
    while not sended:
        server = raw_input("Introduce el servidor SMTP: ") #gmail: smtp.gmail.com, puerto 587
        sender = raw_input("Introduce el correo del remitente: ") #correo de prueba: geuvefieros@gmail.com, pass: geuveferos123
        passwd = raw_input("Introduce la contraseña: ")
        reciever = raw_input("Introduce el correo del destinatario: ")
        msg = raw_input("Introduce el mensaje a enviar: ")
        subject = raw_input("Introduce el asunto del mensaje: ")
        send = raw_input("Desea enviar el mensaje? [Si], [No]: ").lower()
        if send == 'si':
            sended = True
        elif send == 'no':
            if raw_input("No se envió el mensaje, desea enviar otro mensaje? [enviar] o [salir]: ") == "salir":
                break
    header = 'To:' + reciever + '\n' + 'From: ' + sender + '\n' + 'Subject: ' + subject + '\n'
    msg = header + '\n' + msg + '\n'
    
    try:
        srv = SMTP (server, 587)
        srv.ehlo()
        srv.starttls()
        srv.ehlo()
        srv.login(sender, passwd)
        srv.sendmail(sender, reciever, msg)
        print "Mensaje enviado correctamente"
        srv.quit()
    except:
        print "No se ha podido enviar el mensaje"
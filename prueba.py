from mongoengine import *
import hashlib

class Users(Document):
    UserName = StringField()
    Password = StringField()

    def guardar_password(self, password):
        hash_password = hashlib.sha256(password.encode()).hexdigest()
        self.Password = hash_password
        self.save()

connect(host="mongodb://localhost:27017/inventario")

nuevo_usuario = Users(UserName="inventario")
nuevo_usuario.guardar_password("contraseña123")

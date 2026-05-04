from flask_login import UserMixin  # Importa la clase UserMixin de Flask-Login
import os  # Importa el módulo os para funcionalidades relacionadas con el sistema operativo
from hashlib import pbkdf2_hmac, sha1  # Importa funciones de hash pbkdf2_hmac y sha1 desde el módulo hashlib
import base64  # Importa la biblioteca base64 para la manipulación de datos en base64
from models.database import Users  # Importa la clase Users del módulo database dentro del paquete models
import hashlib  # Importa el módulo hashlib para funciones de hash

class User(UserMixin):
    """
    Clase que representa un usuario de la aplicación.
    """

    def __init__(self, user_obj):
        """
        Constructor de la clase User.
        
        Args:
            user_obj: Objeto de usuario obtenido de la base de datos.
        """
        self.user_obj = user_obj

    @staticmethod
    def get(user_id):
        """
        Método estático para obtener un objeto de usuario a partir de un ID de usuario.
        
        Args:
            user_id: ID del usuario.
        
        Returns:
            Objeto de usuario si se encuentra en la base de datos, None de lo contrario.
        """
        user_obj = Users.objects(UserName=user_id).first()
        if user_obj:
            return User(user_obj)
        return None

    def check_password(self, password):
        """
        Método para verificar si una contraseña dada coincide con la contraseña del usuario actual.
        
        Args:
            password: Contraseña proporcionada por el usuario.
        
        Returns:
            True si la contraseña coincide, False de lo contrario.
        """
        if self.user_obj.Password:
            if hashlib.sha256(password.encode()).hexdigest() == self.user_obj.Password:
                return True
        return False

    def get_id(self):
        """
        Método para obtener el ID del usuario.
        
        Returns:
            ID del usuario.
        """
        return str(self.user_obj.UserName)

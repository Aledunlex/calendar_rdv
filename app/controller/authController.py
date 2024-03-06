from datetime import datetime

import cherrypy
from app.controller.core.Controller import Controller
from app.core.tools import hashP
from app.models.user import User

REGISTER_PATH = "register"
LOGIN_PATH = "login"


def notify_account_creation(user):
    """
    Sends a notification to the user to confirm account creation
    """
    notification_data = {
        "subject": "Confirmation de création de compte",
        "template": "register",
        "data": {User.USERNAME_KEY: user[User.USERNAME_KEY]},
    }
    user.notify(notification_data)


class AuthController(Controller):
    def register(
        self,
        email: str = None,
        password: str = None,
        firstname: str = None,
        lastname: str = None,
        birthday: str = None,
        username: str = None,
    ):
        """
        Displays an error message if the user is already registered (checked by email and username)
        Displays a success message if the user has been registered (redirects to login page)
        Sends an email to the user to confirm account creation
        Also checks if the birthday is valid
        Redirects to login page if user creation was successful, with a 'success' message
        """
        if cherrypy.request.method == "POST":
            if (
                not email
                or not password
                or not firstname
                or not lastname
                or not birthday
                or not username
            ):
                self.error = "Veuillez remplir tous les champs"
                return self.render(REGISTER_PATH)
            try:
                if User().get(username=username):
                    self.error = "Nom d'utilisateur déjà utilisé"
                    return self.render(REGISTER_PATH)
                if User().get(email=email):
                    self.error = "Email déjà utilisé"
                    return self.render(REGISTER_PATH)
                birthday = datetime.strptime(birthday, "%Y-%m-%d").date()

                user = User(
                    {
                        User.EMAIL_KEY: email,
                        User.PASSWORD_KEY: password,
                        User.FIRSTNAME_KEY: firstname,
                        User.LASTNAME_KEY: lastname,
                        User.BIRTHDAY_KEY: birthday,
                        User.USERNAME_KEY: username,
                    }
                )
            except Exception as e:
                self.error = str(e)
                return self.render(REGISTER_PATH)

            notify_account_creation(user)

            self.success = "Votre compte a bien été créé"

            return self.redirect("/auth/login")

        return self.render(REGISTER_PATH)

    def login(self, username: str = None, password: str = None):
        if cherrypy.request.method == "POST":
            user = User().get(username=username)
            if user is None:
                user = User().get(email=username)
            if user is None:
                self.error = "Email ou mot de passe incorrect."
                return self.render(LOGIN_PATH)
            if user[User.PASSWORD_KEY] != hashP(password):
                self.error = "Email ou mot de passe incorrect."
                return self.render(LOGIN_PATH)
            cherrypy.session["id_user"] = user.id
            try:
                url = cherrypy.session["redirect_url"]
            except Exception as e:
                url = "/"
            return self.redirect(url)
        elif cherrypy.request.method == "GET":
            return self.render(LOGIN_PATH)

    def logout(self):
        if cherrypy.request.method == "GET":
            cherrypy.session["id_user"] = None
            return self.redirect("/auth/login")

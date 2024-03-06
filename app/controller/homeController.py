import cherrypy
from app.controller.core.Controller import Controller
from app.models.user import User

HOME_PATH = "home"
LOGIN_PATH = "/auth/login"


class HomeController(Controller):
    def home(self):
        """
        Displays current user's home page, enabling them to perform various actions
        """
        if cherrypy.request.method == "GET":
            user_id = cherrypy.session.get("id_user")
            if user_id:
                user = User().get(id=user_id)
                if user:
                    return self.render(HOME_PATH, {**user})
                else:
                    self.error = "Impossible de trouver le compte relié à cet ID"
                    return self.redirect(LOGIN_PATH)
            else:
                self.error = "Connectez vous pour accéder à votre page"
                return self.redirect(LOGIN_PATH)

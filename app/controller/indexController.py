# -*- coding: utf-8 -*-
# oOoOo Author oOoOo
#      Rouxhero
# -------------------


import datetime
import cherrypy
from calendar import monthrange
from faker import Faker
from app.controller.core.Controller import Controller
from app.core.calendartool import getCalender
from app.models.members import Members
from app.models.user import User


class indexController(Controller):
    """
    Exemple IndexController
     ** Extent of controller for template engine **
    """

    def index(self, **post) -> str:
        """
        Index method

        Returns:
            str: HTML Page
        """
        # Check if user is logged or not
        if cherrypy.session.get("id_user"):
            # If user is valide, showing calendar
            user = User().get(id=cherrypy.session.get("id_user"))
            if user:
                return self.render("indexLogged", getCalender(**post))

        return self.render("index")

from datetime import datetime

import cherrypy
from app.controller.core.Controller import Controller
from app.models.user import User
from app.models.event import Event

UNANSWERED_EVENTS_PATH = "/unanswered_events"
LOGIN_PATH = "/auth/login"


class UnansweredEventController(Controller):
    def get_unanswered_events(self):
        if cherrypy.request.method == "GET":
            current_id = cherrypy.session.get("id_user")
            if not current_id:
                return self.redirect(LOGIN_PATH)
            current_user = User().get(id=current_id)
            if not current_user:
                return self.redirect(LOGIN_PATH)

            # Get and display the list of all unanswered events for this user
            unanswered = current_user.get_unanswered_events()
            return self.render(
                UNANSWERED_EVENTS_PATH, {"unanswered_events": unanswered}
            )

    def set_participation(self, event_id, action):
        if cherrypy.request.method == "POST":
            current_id = cherrypy.session.get("id_user")
            if not current_id:
                return self.redirect(LOGIN_PATH)
            current_user = User().get(id=current_id)
            if not current_user:
                return self.redirect(LOGIN_PATH)

            try:
                is_participating = action == "accept"
                current_user.set_participation(
                    int(event_id), is_participating=is_participating
                )
                self.success = f"Votre participation a bien été {'enregistrée' if is_participating else 'annulée'}"

            except Exception as e:
                self.error = (
                    f"Impossible de modifier votre participation à cet événement : contactez son créateur, "
                    f"il peut avoir été annulé. Si non, contactez un administrateur."
                )

            return self.redirect(UNANSWERED_EVENTS_PATH)

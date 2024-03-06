from app.controller.core.Controller import Controller
from app.core.tools import config
from app.core.tools import date_formarter
from datetime import datetime
from app.models.participant import Participant
from app.models.user import User
from app.models.usergroup import UserGroup
from app.models.event import Event
import cherrypy


class AjaxController(Controller):

    LINK_ADD_USER_GROUP = "addUserGroup/"

    def addCalendarEvent(self, day, month, year):
        date_object = datetime.strptime(month, "%b")
        month_number = date_object.month

        user = User().get(id=cherrypy.session.get("id_user"))
        usergroups = UserGroup.get_all_from_owner(user.id)
        data = {"day": day, "month": month_number, "year": year, "groups": usergroups}
        return self.render("components/modal/createEvent", data)

    def add_user_group(self, id_group):
        link = self.LINK_ADD_USER_GROUP + id_group
        members = UserGroup.get_all_from_group(id_group)
        group = UserGroup().get(id=id_group)
        data = {"link": link, "members": members, "group": group}
        return self.render("components/modal/addUserGroup", data)

    def create_evenement(self, **post):
        user = User().get(id=cherrypy.session.get("id_user"))
        try:
            event = Event(
                {
                    Event.USER_KEY: user.id,
                    Event.GROUP_KEY: post["id_group"],
                    Event.DATE_CREA_KEY: datetime.now().date(),
                    Event.DATE_MEETING_KEY: date_formarter(post["date_meeting"]),
                    Event.LOCATION_KEY: post["place"],
                    Event.NAME_KEY: post["name"],
                    Event.DESCRIPTION_KEY: post["description"],
                    Event.IS_CANCELED_KEY: False,
                }
            )

            # une fois l'event créé, on créé un Participant pour tous les membres du groupe
            members = UserGroup.get_all_from_group(
                event["id_group"]
            )  # Renvoi des users  ;)
            for member in members:
                if member.id != user.id:
                    Participant(
                        {
                            Participant.ID_USER_KEY: member.id,
                            Participant.ID_EVENT_KEY: event.id,
                            Participant.IS_PARTICIPATING_KEY: 0,  # 0 = unanswered
                        }
                    )
                    baseURI = "http://"+ config["host"] 
                    if config['usePort']:
                        baseURI += ":"+str(config['port'])  
                    member.notify(
                        {
                            "subject": "Nouvel événement",
                            "template": "eventInvitation",
                            "data": {
                                "event": event,
                                "user": member,
                                "group": UserGroup().get(id=event[Event.GROUP_KEY]),
                                "baseurl": baseURI
                            },
                        }
                    )

            self.success = (
                "Votre événement a bien été créé. "
                f"Vous avez invité {len(members) - 1} utilisateur à participer!"
            )  # -1 for the event creator
            return self.render("components/modal/createEventSuccess")
        except Exception as e:
            self.error = "Veuillez remplir tous les champs"
            user = User().get(id=cherrypy.session.get("id_user"))
            usergroups = UserGroup.get_all_from_owner(user.id)
            data = {
                "day": post["day"],
                "month": post["month"],
                "year": post["year"],
                "groups": usergroups,
            }
            return self.render("components/modal/createEvent", data)

    def delete_event(self, **post):
        user = User().get(id=cherrypy.session.get("id_user"))
        if not user:
            self.error = "Vous n'êtes pas connecté"
            return self.render("components/modal/displayError")
        id_event = post.get("id_event")
        if not id_event:
            self.error = "Aucun événement n'a été sélectionné"
            return self.render("components/modal/displayError")
        event = Event().get(id=id_event)
        if not event:
            self.error = "Erreur: événement n'existe pas"
            return self.render("components/modal/displayError")
        if event[Event.USER_KEY] != user.id:
            self.error = "Erreur: Vous n'êtes pas le créateur de cet événement"
            return self.render("components/modal/displayError")
        try:
            event_name = event[Event.NAME_KEY]
            event.delete()
            self.success = f"Votre événement {event_name} a bien été supprimé"

            return self.render("components/modal/createEventSuccess")
        except Exception as e:
            self.error = f"Impossible de supprimer cet événement"
            return self.render("components/modal/displayError")

    def displayEvent(self, id_event):
        event = Event().get(id=id_event)
        if not event:
            self.error = "Cet événement n'existe pas"
            return self.render("components/modal/displayError")
        user = User().get(id=cherrypy.session.get("id_user"))
        members = UserGroup.get_all_from_group(event["id_group"])
        data = {
            "event": event,
            "members": members,
            "group": UserGroup().get(id=event["id_group"]),
        }
        return self.render("components/modal/displayEvent", data)

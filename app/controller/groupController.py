from app.models.members import Members
from app.core.tools import config
import cherrypy
from app.controller.core.Controller import Controller
from app.models.user import User
from app.models.usergroup import UserGroup

CREATE_GROUP_PATH = "create_group"
GROUP_PATH = "group/group"
LOGIN_PATH = "login"


class GroupController(Controller):
    def group(self):
        # Check that the user is logged in
        id_user = cherrypy.session.get("id_user")
        if not id_user:
            return self.redirect(LOGIN_PATH)
        groups_owned = UserGroup.get_all_from_owner(id_user)
        groups_present = UserGroup.get_all_from_member(id_user)
        res = []
        for group in groups_owned:
            res.append({"group": group, "is_owner": True})
        for group in groups_present:
            res.append({"group": group, "is_owner": False})

        data = {"groups": res}
        return self.render(GROUP_PATH, data)

    def create_group(self, name: str = None):
        # Check that the user is logged in
        if not cherrypy.session.get("id_user"):
            return self.redirect("/auth/login")
        current_user_id = cherrypy.session.get("id_user")
        if cherrypy.request.method == "POST":
            try:
                if UserGroup().get(name=name):
                    self.error = "Nom de groupe déjà utilisé"
                    return self.render(CREATE_GROUP_PATH)

                user_group = UserGroup({UserGroup.NAME_KEY: name})

                members = Members(
                    {
                        Members.USER_KEY: current_user_id,
                        Members.GROUP_KEY: user_group.id,
                        Members.OWNER_KEY: True,
                    }
                )

            except Exception as e:
                self.error = f"Erreur  internes : Contactez l'administrateur du site si le problème persiste."
                return self.render(CREATE_GROUP_PATH)

            self.success = f"Votre groupe {name} a bien été créé"
            return self.render(CREATE_GROUP_PATH)

        return self.render(CREATE_GROUP_PATH)

    def add_user_group(self, id_group):
        from app.models.participant import Participant
        from app.models.event import Event

        id_user = cherrypy.session.get("id_user")
        if not id_user:
            cherrypy.session["redirect_url"] = cherrypy.url()
            return self.redirect("/auth/login")
        try:
            if Members().get(id_user=id_user, id_group=id_group) is not None:
                self.error = f"Vous êtes déjà dans ce groupe"
            else:
                Members(
                    {
                        Members.USER_KEY: id_user,
                        Members.GROUP_KEY: id_group,
                        Members.OWNER_KEY: False,
                    }
                )

                # On invite le nouveau membre à tous les événements du groupe
                events = Event().get_all(id_group=id_group)
                for event in events:
                    Participant(
                        {
                            Participant.ID_USER_KEY: id_user,
                            Participant.ID_EVENT_KEY: event.id,
                            Participant.IS_PARTICIPATING_KEY: 0,
                        }
                    )

                current_user = User().get(id=id_user)
                baseURI = "http://"+ config["url"] 
                if config['usePort']:
                    baseURI += ":"+str(config['port'])
                current_user.notify(
                    {
                        "subject": "Nouveau groupe",
                        "template": "eventInvitaionGroup",
                        "data": {
                            "groups": {"count": len(events), "events": events},
                            "user": current_user,
                            "group": UserGroup().get(id=id_group),
                            "baseurl": baseURI,
                        },
                    }
                )

                self.success = (
                    "Vous avez bien été ajouté au groupe! "
                    f"Allez lire vos {len(events)} nouvelles invitations."
                )

        except Exception as e:
            self.error = f"Erreur  internes : Contactez l'administrateur du site si le problème persiste."

        return self.redirect("/")

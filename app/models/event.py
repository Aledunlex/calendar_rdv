from datetime import datetime
from app.models.core import Model


class Event(Model):
    USER_KEY = "id_user"
    GROUP_KEY = "id_group"
    DATE_CREA_KEY = "date_crea"
    DATE_MEETING_KEY = "date_meeting"
    LOCATION_KEY = "location"
    IS_CANCELED_KEY = "is_canceled"
    NAME_KEY = "name"
    DESCRIPTION_KEY = "description"

    fields = {
        USER_KEY: (0, "required"),
        GROUP_KEY: (0, "required"),
        DATE_CREA_KEY: (datetime.now().date(), "required"),
        DATE_MEETING_KEY: (datetime.now(), "required"),
        LOCATION_KEY: ("", "required"),
        IS_CANCELED_KEY: (False, "required"),
        NAME_KEY: ("", "required"),
        DESCRIPTION_KEY: ("", "required"),
    }

    def delete(self):
        # notifier les membres du groupe avant suppression
        try:
            from app.models.participant import Participant

            all_participants = Participant().get_all(id_event=self.id)
            for participant in all_participants:
                participant.notify(
                    {
                        "subject": f"Annulation de l'événement {self[Event.NAME_KEY]}",
                        "template": "canceled_event",
                        "data": {Event.NAME_KEY: self[Event.NAME_KEY]},
                    }
                )
        except Exception as e:
            # Oui, y'a un print, parce qu'il faut bien le notifier quelque part
            print(
                f"Erreur d'envoi de la notification de suppression de l'événement: {e}"
            )
        super(Event, self).delete()  # Notification ou pas, on supprime l'événement

    def __str__(self):
        return (
            f"Event {self[Event.NAME_KEY]} by {self[Event.USER_KEY]} "
            f"for {self[Event.GROUP_KEY]} ({self[Event.DATE_MEETING_KEY]})"
        )

    def __repr__(self):
        return (
            f"Event[id={self.id}, name={self[Event.NAME_KEY]}, owner={self[Event.USER_KEY]}, "
            f"group={self[Event.GROUP_KEY]}, date={self[Event.DATE_MEETING_KEY]}]"
        )

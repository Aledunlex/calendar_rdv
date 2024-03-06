# -*- coding: utf-8 -*-
# oOoOo Authors oOoOo
#      Rouxhero
#      Alexandre
# -------------------
from datetime import datetime

from app.core.mailer import Mailer
from app.core.tools import hashP
from app.models.core import Model
from app.models.event import Event


class User(Model):
    EMAIL_KEY = "email"
    FIRSTNAME_KEY = "firstname"
    LASTNAME_KEY = "lastname"
    PASSWORD_KEY = "password"
    BIRTHDAY_KEY = "birthday"
    USERNAME_KEY = "username"

    fields = {
        EMAIL_KEY: ("", "required"),
        FIRSTNAME_KEY: ("", "required"),
        LASTNAME_KEY: ("", "required"),
        PASSWORD_KEY: ("", "required"),
        BIRTHDAY_KEY: (datetime.now().date(), "required"),
        USERNAME_KEY: ("", "required"),
    }

    def __init__(self, kwargs: dict = None):
        """Hashes the password in kwargs before calling Model.__init__"""
        if kwargs is None:
            kwargs = {}
        if self.PASSWORD_KEY in kwargs.keys():
            kwargs[self.PASSWORD_KEY] = hashP(kwargs[self.PASSWORD_KEY])
        super().__init__(kwargs)

    def notify(self, mail_data: dict) -> None:
        """
        Current method of notification : sending a mail to the user
        _args_: mail_data (dict) : contains the 'subject', the 'template' its 'data'
        _args_: user (User)
        """
        email = self[self.EMAIL_KEY]
        mailer = Mailer()
        mailer.send(email, **mail_data)

    def _get_events_by_participation_status(self, participation_status):
        """Get all events of the user, filtered by participation status (None = unanswered,
        True = participating, False = confirmed not participating)"""
        from app.models.participant import Participant

        invites = Participant().get_all(id_user=self.id)
        events = []
        for invite in invites:
            if invite[Participant.IS_PARTICIPATING_KEY] == participation_status:
                event = Event().get(id=invite["id_event"])
                if event:
                    events.append(event)
        return events

    def get_unanswered_events(self) -> list:
        """Get all unanswered events of the user"""
        unanswered_events = self._get_events_by_participation_status(0)
        return unanswered_events

    def get_participating_events(self) -> list:
        """Get all events where the user is participating"""
        participating_events = self._get_events_by_participation_status(1)
        return participating_events

    def set_participation(self, event_id: int, is_participating: bool) -> None:
        """Set the participation status of the user for the event"""
        from app.models.participant import Participant

        participant = Participant().get(id_user=self.id, id_event=event_id)
        if participant:
            participant.set_participation(is_participating)
        else:
            raise Exception(
                f"Participant not found: id_user {self.id}, id_event {event_id}"
            )

    def __str__(self):
        return (
            f"User[id={self.id}, "
            f"email={self[self.EMAIL_KEY]}, "
            f"firstname={self[self.FIRSTNAME_KEY]}, "
            f"lastname={self[self.LASTNAME_KEY]}, "
            f"birthday={self[self.BIRTHDAY_KEY]}, "
            f"username={self[self.USERNAME_KEY]}]"
        )

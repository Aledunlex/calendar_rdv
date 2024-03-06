from app.models.core import Pivot


class Participant(Pivot):
    ID_USER_KEY = "id_user"
    ID_EVENT_KEY = "id_event"
    IS_PARTICIPATING_KEY = "is_participating"

    fields = {
        ID_USER_KEY: (0, "required"),
        ID_EVENT_KEY: (0, "required"),
        IS_PARTICIPATING_KEY: (0, "required"),  # None = not answered yet
    }

    def notify(self, notification_data: dict) -> None:
        """Notify the User matching this Member unless they confirmed they are not participating"""
        if self[self.IS_PARTICIPATING_KEY] == 2:
            # No need to notify a user that is not participating
            return

        from app.models.user import (
            User,
        )  # importé ici pour éviter une boucle d'importation

        user = User().get(id=self[self.ID_USER_KEY])
        if user:
            user.notify(notification_data)
        else:
            raise Exception(f"User not found: id {self[self.ID_USER_KEY]}")

    def set_participation(self, is_participating: bool) -> None:
        """Set the participation status of the participant"""
        self[self.IS_PARTICIPATING_KEY] = 1 if is_participating else 2
        self.save()

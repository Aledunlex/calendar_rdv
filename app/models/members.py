from app.models.core import Pivot


class Members(Pivot):
    USER_KEY = "id_user"
    GROUP_KEY = "id_group"
    OWNER_KEY = "is_owner"

    fields = {
        USER_KEY: (0, "required"),
        GROUP_KEY: (0, "required"),
        OWNER_KEY: (False, "required"),
    }

    def notify(self, notification_data: dict) -> None:
        """Notify the User matching this Member"""
        from app.models.user import (
            User,
        )  # importé ici pour éviter une boucle d'importation

        user = User().get(id=self[self.USER_KEY])
        if user:
            user.notify(notification_data)
        else:
            raise Exception(f"User not found: id {self[self.USER_KEY]}")

    def __str__(self):
        return f"Member[user={self[self.USER_KEY]}, group={self[self.GROUP_KEY]}, owner={self[self.OWNER_KEY]}]"

    def __repr__(self):
        return self.__str__()

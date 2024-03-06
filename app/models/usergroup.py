from app.models.core import Model
from app.models.members import Members
from app.models.user import User


class UserGroup(Model):
    NAME_KEY = "name"

    fields = {NAME_KEY: ("", "required")}

    def notify(self, notification_data: dict) -> None:
        """Notification of all members of the group"""
        members = Members().get_all(id_group=self.id)
        for member in members:
            member.notify(notification_data)

    def get_all_from_owner(owner_id):
        """Get all groups from an owner"""
        groups = Members().get_all(id_user=owner_id, is_owner=True)

        usergroups = UserGroup().get_all()
        usergroups = list(
            u for g in groups for u in usergroups if u.id == g["id_group"]
        )
        return usergroups

    def get_all_from_member(member_id):
        """Get all groups from a member"""
        groups = Members().get_all(id_user=member_id, is_owner=False)

        usergroups = UserGroup().get_all()
        usergroups = list(
            u for g in groups for u in usergroups if u.id == g["id_group"]
        )
        return usergroups

    def get_all_from_group(group_id):
        """Get all groups from an owner"""
        groups = Members().get_all(id_group=group_id)
        usergroups = User().get_all()
        usergroups = list(u for g in groups for u in usergroups if u.id == g["id_user"])

        return usergroups

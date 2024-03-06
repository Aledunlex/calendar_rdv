from app.core.route import Route
from app.controller.groupController import GroupController, CREATE_GROUP_PATH


routes = [
    Route("/group", "GET", GroupController, "group"),
    Route(f"/{CREATE_GROUP_PATH}", "GET", GroupController, "create_group"),
    Route(f"/{CREATE_GROUP_PATH}", "POST", GroupController, "create_group"),
    Route("/addUserGroup/{id_group}", "GET", GroupController, "add_user_group"),
]

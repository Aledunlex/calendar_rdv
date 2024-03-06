from app.controller.ajaxController import AjaxController
from app.controller.indexController import indexController
from app.core.route import Route


routes = [
    Route("/", "GET", indexController, "index"),
    Route("/", "POST", indexController, "index"),
    Route("/addCalendarEvent", "POST", AjaxController, "addCalendarEvent"),
    Route("/create_evenement", "POST", AjaxController, "create_evenement"),
    Route("/display_event", "POST", AjaxController, "displayEvent"),
    Route("/delete_event", "POST", AjaxController, "delete_event"),
    Route("/addUserGroup", "POST", AjaxController, "add_user_group"),
]

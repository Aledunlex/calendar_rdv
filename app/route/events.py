from app.controller.unansweredEventController import UnansweredEventController
from app.core.route import Route


routes = [
    Route(
        "/unanswered_events", "GET", UnansweredEventController, "get_unanswered_events"
    ),
    Route(
        "/set_participation/{event_id}",
        "POST",
        UnansweredEventController,
        "set_participation",
    ),
]

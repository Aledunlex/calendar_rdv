from app.route.web import routes as web_routes
from app.route.auth import routes as auth_routes
from app.route.group import routes as group_routes
from app.route.home import routes as home_routes
from app.route.events import routes as events_routes

routes = web_routes
routes += auth_routes
routes += group_routes
routes += home_routes
routes += events_routes

from app.controller.authController import AuthController
from app.controller.homeController import HomeController
from app.core.route import Route


routes = [Route("/home", "GET", HomeController, "home")]

from app.controller.authController import AuthController
from app.controller.homeController import HomeController
from app.core.route import Route


routes = [
    Route("/auth/register", "GET", AuthController, "register"),
    Route("/auth/register", "POST", AuthController, "register"),
    Route("/auth/login", "GET", AuthController, "login"),
    Route("/auth/login", "POST", AuthController, "login"),
    Route("/auth/logout", "GET", AuthController, "logout"),
]

from django.urls import path

from . import views

urlpatterns = [
    path("admin", views.admin, name="admin"),
    path("", views.index, name="index"),
    path("signup", views.signup, name="signup"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("details/<str:type>/<str:name>/<str:size>/<str:price>/<int:val>",views.details, name="details"),
    path("cart", views.cart, name="cart"),
    path("delete/<int:id>",views.delete,name="delete"),
    path("confirm",views.confirm,name="confirm"),
    path("finish",views.finish,name="finish")
]

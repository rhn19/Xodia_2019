from django.conf.urls import url
from auth_app.views import *

urlpatterns = [
    #url(r'^$', HomeView.as_view(), name = "auth_home"),
    url(r'^$', LoginView.as_view(), name = "user_login"),
    url(r'^success$', SuccessView.as_view(), name = "login_success"),
    url(r'^logout$', LogoutView.as_view(), name = "user_logout"),
    url(r'^register$', RegisterView.as_view(), name = "user_register"),
    #url(r'^profile$', ProfileView.as_view(), name = "user_profile"),
]

from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.index),
    url(r'^login_registration$', views.login_registration),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^driver_or_passenger$', views.driver_or_passenger),
    url(r'^driver_add_departure$', views.driver_add_departure),
    url(r'^driver_add_departure/process$', views.driver_add_departure_process),
    url(r'^driver_add_arrival$', views.driver_add_arrival),
    url(r'^driver_add_arrival/process$', views.driver_add_arrival_process),
    url(r'^driver_summary$', views.driver_summary),
    url(r'^passenger$', views.passenger),
    url(r'^passenger/process$', views.passenger_process),

]

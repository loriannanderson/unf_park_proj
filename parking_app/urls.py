from django.urls import path
from parking_app import views


# urls for the parking_app
urlpatterns = [
    path('',views.index,name="index"),
    path('contact',views.contact,name="contact"),
    path('about',views.about,name="about"),
    path('profile',views.profile,name="profile"),
    path('create_registration', views.createRegistration, name="create_registration"),
    path('update_registration', views.updateRegistration, name="update_registration"),
    path('checkout/', views.checkout, name="Checkout"),
    path('handlerequest/', views.handlerequest, name="HandleRequest")
]
from django.urls import path
from parking_app import views


# urls for the parking_app
urlpatterns = [
    path('',views.index,name="index"),
    path('contact',views.contact,name="contact"),
    path('parking_map',views.parking_map,name="parking_map"),
    path('about',views.about,name="about"),
    path('profile',views.profile,name="profile"),
    path('create_registration', views.createRegistration, name="create_registration"),
    path('update_registration', views.updateRegistration, name="update_registration"),
    path('checkout/', views.checkout, name="Checkout"),
    path('handlerequest/', views.handlerequest, name="HandleRequest"),
    path('paypalcheckout/', views.paypalcheckout, name="PaypalCheckout"),
    path('payment-success/<int:product_id>/', views.PaymentSuccessful, name='payment-success'),
    path('payment-failed/<int:product_id>/', views.paymentFailed, name='payment-failed'),
]
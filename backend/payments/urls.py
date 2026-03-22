from django.urls import path
from .views import stkpush, mpesa_callback

urlpatterns = [
    path("stkpush/", stkpush, name="stkpush"),
    path("callback/", mpesa_callback, name="mpesa_callback"),
]

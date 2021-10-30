from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from .views import payment,response

app_name='payment'

urlpatterns = [

    url(r'^$',payment),
    url(r'^response/$',response)

]

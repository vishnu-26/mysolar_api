from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.urls import path
from .views import upload_product,products

app_name='products'

urlpatterns = [

    url(r'^$',products),
    url(r'^upload/$',upload_product),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

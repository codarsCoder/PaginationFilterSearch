from django.urls import path

from rest_framework.authtoken import views
from .views import RegisterView, logout


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', views.obtain_auth_token),   ## obtain login olduğumuz zaman token varsa onu dönüyor yoksa  token oluşturup onu dönüyor, loginsek bize getiriyor projelerde çok kullanılmasada örneği eklendi
    path('logout/', logout)
 ]
## NOT settings.py deki  'rest_framework.authtoken',  admin sayfasından token eklemeyi aktif etti obtain_auth_token ise bunu login olduğunda oto yapacak 
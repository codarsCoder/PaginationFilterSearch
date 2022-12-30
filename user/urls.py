from django.urls import path

from rest_framework.authtoken import views
from .views import RegisterView, logout


urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', views.obtain_auth_token),   ## obtain login olduğumuz zaman token oluşturup, loginsek bize getiriyor projelerde çok kullanılmasada örneği eklendi
    path('logout/', logout),
 ]

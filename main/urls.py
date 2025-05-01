
from .views import home
from django.urls import path
from . import views  # Импорт views из текущего приложения

urlpatterns = [
    path('', home, name='home'),
    path('gpt-response/', views.gpt_response, name='gpt_response'),
]

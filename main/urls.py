from django.urls import path
from . import views

urlpatterns = [
    path('courses/', views.course_list, name='course_list'),
    path('courses/<slug:course_slug>/lesson/<int:lesson_order>/', views.lesson_detail, name='lesson_detail'),
]

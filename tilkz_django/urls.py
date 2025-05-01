from django.contrib import admin
from django.urls import path, include
from django.core.management import call_command
from django.http import HttpResponse

def collectstatic_now(request):
    call_command("collectstatic", interactive=False, verbosity=0)
    return HttpResponse("✅ Static files collected.")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),
    path('collectstatic-now/', collectstatic_now),
]

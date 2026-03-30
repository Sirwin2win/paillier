from django.urls import path
from . import views  # Import views from the same app directory

urlpatterns = [
    path('', views.home, name='home'),  # Matches 'myapp/'
   # path('about/', views.about_view, name='about'), # Matches 'myapp/about/'
   path("tally/", views.tally_view, name="tally"),
    path("decrypt/", views.decrypt_total, name="decrypt"),
]

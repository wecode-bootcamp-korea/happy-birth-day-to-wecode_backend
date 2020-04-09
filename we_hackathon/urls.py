from django.urls import path, include

urlpatterns = [
    path('vote', include('vote.urls')),
]

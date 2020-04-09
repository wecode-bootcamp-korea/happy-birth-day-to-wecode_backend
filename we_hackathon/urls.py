from django.urls import path, include

urlpatterns = [
    path('', include('vote.urls'))
    path('vote', include('vote.urls')),
]

from django.urls import path
from .views      import (
    VoteView,
    ResultView,
    ArtworkView,
    MyVoteNumView,
)

urlpatterns = [
    path('vote', VoteView.as_view()),
    path('vote/<int:category_id>', MyVoteNumView.as_view()),
    path('result/<int:category_id>', ResultView.as_view()),
    path('artwork/<int:category_id>', ArtworkView.as_view())
]

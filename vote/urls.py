from django.urls import path
from .views      import (
    VoteView,
    ResultView,
    ArtworkView,
)

urlpatterns = [
    path('vote', VoteView.as_view()),
    path('vote/<int:category_id>', VoteView.as_view()),
    path('result/<int:category_id>', ResultView.as_view()),
    path('vote/artwork/<int:category_id>', ArtworkView.as_view())
]

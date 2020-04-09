from .views import ResultView
from django.urls import path
urlpatterns = [
    path('/result/<int:category_id>', ResultView.as_view()),
]

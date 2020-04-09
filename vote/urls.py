from django.urls    import path
from .views         import ArtworkView, ResultView

urlpatterns = [
    path('/artwork/<int:category_id>', ArtworkView.as_view())
    path('/result/<int:category_id>', ResultView.as_view()),
]

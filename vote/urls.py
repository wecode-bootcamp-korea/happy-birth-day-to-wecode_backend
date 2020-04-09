from django.urls    import path
from .views         import ArtworkView

urlpatterns = [
    path('/artwork/<int:category_id>', ArtworkView.as_view())
]

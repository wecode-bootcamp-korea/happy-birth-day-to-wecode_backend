import json

from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db        import transaction
from django.db.models import Q,F,Count

from .models          import (
     Artwork,
     Category,
     Picture,
     Vote
 )

class ResultView(View):
    def get(self, request, category_id):
        artworks = (
            Artwork
            .objects
            .filter(category_id = category_id)
            .order_by('-count')
            .annotate(
                count = Count('vote')
            )
            .values('id','artist','batch','count')
        )

        result_list = [
            {
                'count'      : artwork['count'],
                'artist'      : artwork['artist'],
                'batch'      : artwork['batch'],
                'image_urls'     : [ picture.image_url for picture in Picture.objects.filter(artwork_id = artwork['id'])],

            }for artwork in artworks]

        return JsonResponse({"results": result_list}, status = 200)

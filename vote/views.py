import json
import uuid

from django.views     import View
from django.http      import HttpResponse, JsonResponse
from django.db        import transaction
from django.db.models import Q,F,Count

from .models          import (
    User,
    Artwork,
    Category,
    Picture,
    Vote
 )

THREE_POEM_COUNT = 5
POEM_COUNT = 1
ART_COUNT = 1

def save_vote(self, cookie, data):
    if Vote.objects.filter(user = User.objects.get(code=cookie), artwork_id = data['artwork']).exists():
        return JsonResponse({'message':'ALREADY_VOTED'},status=409)
    Vote(
        user = User.objects.get(code = cookie),
        artwork_id = data['artwork'],
        category_id = data['category']
    ).save()
    response = HttpResponse(status = 200)
    return response

class VoteView(View):
    def post(self, request):
        try:
            cookie = request.COOKIES.get('code', None)
            data   = json.loads(request.body)
            data['category'] = Artwork.objects.get(id = data['artwork']).category.id
            if cookie:
                user  = User.objects.get(code = cookie)
                count = Vote.objects.filter(user = user, category = data['category']).count()+1
                if data['category'] == 1:
                    if(ART_COUNT >= count):
                       return  save_vote(self, cookie, data)

                    return JsonResponse({'message':'MAX_VOTE'}, status = 400)

                if data['category'] == 2: 
                    if(THREE_POEM_COUNT >= count):
                        return  save_vote(self, cookie, data)

                    return JsonResponse({'message':'MAX_VOTE'}, status = 400)

                if data['category'] == 3:
                    if(POEM_COUNT >= count):
                        return save_vote(self, cookie, data)
                    return JsonResponse({'message':'MAX_VOTE'}, status = 400)

            cookie = uuid.uuid4()
            User.objects.create(code = cookie)
            response = save_vote(self, cookie, data)
            response.set_cookie('code', cookie)

            return response

        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
        except Artwork.DoesNotExist:
            return JsonResponse({'message':'INVALID_ARTWORK'}, status = 401)

    def get(self, request):
        cookie = request.COOKIES.get('code', None)
        user = User.objects.get(code = cookie)
        if cookie:
            vote = Vote.objects.filter(user = user).aggregate(Count('category_id'))
        return JsonResponse({'message':'VOTE_YET'}, status = 401)

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

class ArtworkView(View):
    def get(self, request, category_id):
        
        if Artwork.objects.filter(category_id=category_id).exists():
            artworks = Artwork.objects.filter(category_id=category_id)
            print(artworks)
            category_name = Category.objects.get(id=category_id).name
            artwork_attributes = [
                {
                    'artwork_id': artwork.id,
                    'image_urls': [picture.image_url for picture in Picture.objects.filter(artwork_id=artwork.id)],
                    'category_id': artwork.category_id
                } for artwork in artworks
            ]
            return JsonResponse({category_name: artwork_attributes}, status = 200)
        return JsonResponse({'message': 'ARTWORK_DOES_NOT_EXIST'}, status = 404)

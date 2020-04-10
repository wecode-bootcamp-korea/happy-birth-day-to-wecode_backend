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

def save_vote(self, code, data):
    if Vote.objects.filter(user = User.objects.get(code=code), artwork_id = data['artwork']).exists():
        return JsonResponse({'message':'ALREADY_VOTED'},status=409)
    Vote(
        user = User.objects.get(code = code),
        artwork_id = data['artwork'],
        category_id = data['category']
    ).save()
    response = JsonResponse({'code': code}, status = 200)
    return response

class VoteView(View):
    def post(self, request):
        try:
            code = request.headers.get('code', None)
            data   = json.loads(request.body)
            data['category'] = Artwork.objects.get(id = data['artwork']).category.id
            if code:
                user  = User.objects.get(code = code)
                count = Vote.objects.filter(user = user, category = data['category']).count()+1

                if data['category'] == 1:
                    if(ART_COUNT >= count):
                       return  save_vote(self, code, data)

                    return JsonResponse({'message':'MAX_VOTE'}, status = 400)

                if data['category'] == 2: 
                    if(THREE_POEM_COUNT >= count):
                        return  save_vote(self, code, data)

                    return JsonResponse({'message':'MAX_VOTE'}, status = 400)

                if data['category'] == 3:
                    if(POEM_COUNT >= count):
                        return save_vote(self, code, data)
                    return JsonResponse({'message':'MAX_VOTE'}, status = 400)

            code = uuid.uuid4()
            User.objects.create(code = code)
            response = save_vote(self, code, data)

            return response

        except KeyError:
            return JsonResponse({'message':'INVALID_KEYS'}, status = 400)
        except Artwork.DoesNotExist:
            return JsonResponse({'message':'INVALID_ARTWORK'}, status = 401)

    def get(self, request, category_id):
        code = request.headers.get('code', None)

        if category_id > Category.objects.count():
            return JsonResponse({'message': 'CATEGORY_DOES_NOT_EXIST'}, status = 400)

        if code:
            category_name = Category.objects.get(id=category_id).name
            user = User.objects.get(code=code)
            num_my_votes = Vote.objects.filter(user_id = user, category_id = category_id).count()
            return JsonResponse({'category': category_name, 'vote_count':num_my_votes}, status = 200)

        return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status = 400)

class ArtworkView(View):
    def get(self, request, category_id):

        if Artwork.objects.filter(category_id=category_id).exists():
            artworks = Artwork.objects.filter(category_id=category_id)
            print(artworks)
            category_name = Category.objects.get(id=category_id).name
            artwork_attributes = [
                {
                    'artist'    : artwork.artist,
                    'batch'     : artwork.batch,
                    'artwork_id': artwork.id,
                    'image_urls': [picture.image_url for picture in Picture.objects.filter(artwork_id=artwork.id)],
                    'category_id': artwork.category_id
                } for artwork in artworks
            ]

            return JsonResponse({category_name: artwork_attributes}, status = 200)
        return JsonResponse({'message': 'ARTWORK_DOES_NOT_EXIST'}, status = 404)

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


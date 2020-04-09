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


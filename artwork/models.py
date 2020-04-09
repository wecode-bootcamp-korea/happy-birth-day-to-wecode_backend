from django.db import models

class Artworks(models.Model):
    batch = models.CharField(max_length = 30)
    artist = models.CharField(max_length= 50)
    category_id = models.ForeignKey('Categories', on_delete = models.CASCADE)
 
    class Meta:
        db_table = 'artworks'

class Categories(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = 'categories'

class Pictures(models.Model):
    image_url = models.CharField(max_length = 4000)
    artwork_id = models.ForeignKey('Artworks', on_delete = models.CASCADE)

    class Meta:
        db_table = 'pictures'

class UserJoinArtworks(models.Model):
    user_id = models.ForeignKey('Users', on_delete = models.CASCADE)
    artwork_id = models.ForeignKey('Artworks', on_delete = models.CASCADE)
    category_id = models.ForeignKey('Categories', on_delete = models.CASCADE)

    class Meta:
        db_table = 'user_artworks'

# Create your models here.

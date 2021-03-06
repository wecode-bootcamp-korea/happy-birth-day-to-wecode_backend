from django.db   import models

class User(models.Model):
    code = models.CharField(max_length = 300)

    class Meta:
        db_table = 'users'

class Artwork(models.Model):
    batch    = models.CharField(max_length = 30)
    artist   = models.CharField(max_length= 50)
    category = models.ForeignKey('Category', on_delete = models.CASCADE)

    class Meta:
        db_table = 'artworks'

class Category(models.Model):
    name = models.CharField(max_length = 30)

    class Meta:
        db_table = 'categories'

class Picture(models.Model):
    image_url = models.CharField(max_length = 4000)
    artwork   = models.ForeignKey('Artwork', on_delete = models.CASCADE)

    class Meta:
        db_table = 'pictures'

class Vote(models.Model):
    user     = models.ForeignKey('User', on_delete = models.CASCADE)
    artwork  = models.ForeignKey('Artwork', on_delete = models.CASCADE)
    category = models.ForeignKey('Category', on_delete = models.CASCADE)

    class Meta:
        db_table = 'votes'


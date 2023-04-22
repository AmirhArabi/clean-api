from django.db import models

# create a model to save the url
class Url(models.Model):
    url = models.CharField(max_length=200)
    short_url = models.CharField(max_length=200, unique=True)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    click_count = models.IntegerField(default=0)

    def __str__(self):
        return self.url + " => " + self.short_url + " => " + str(self.click_count)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


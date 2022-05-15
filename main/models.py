from django.db import models


class CrawlSite(models.Model):
    name = models.CharField(max_length=128)
    site_url = models.URLField()
    products_tag = models.CharField(max_length=16)
    products_class = models.CharField(max_length=255)
    title_tag = models.CharField(max_length=16)
    title_class = models.CharField(max_length=255)
    url_tag = models.CharField(max_length=16)
    url_class = models.CharField(max_length=255)
    url_attr = models.CharField(max_length=16)
    price_tag = models.CharField(max_length=16)
    price_class = models.CharField(max_length=255)
    price_contents = models.IntegerField()

    def __str__(self):
        return self.name



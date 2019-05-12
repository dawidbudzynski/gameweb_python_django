from django.db import models


class Tag(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return self.name

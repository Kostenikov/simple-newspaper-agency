from django.contrib.auth import get_user_model
from django.db import models

Redactor = get_user_model()


class TimestampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Topic(TimestampModel):
    name = models.CharField(max_length=63, unique=True, verbose_name="topic name")

    def __str__(self):
        return self.name


class Newspaper(TimestampModel):
    title = models.CharField(max_length=255)
    content = models.TextField()
    published_date = models.DateTimeField()
    topic = models.ForeignKey(Topic, on_delete=models.PROTECT, related_name="newspapers")
    publishers = models.ManyToManyField(Redactor, related_name="newspapers")

    class Meta:
        ordering = ("-published_date",)

    def __str__(self):
        return f"{self.title} - {self.topic}"

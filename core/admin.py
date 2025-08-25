from django.contrib import admin

from core.models import Topic, Newspaper


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ("name", "created_at", "updated_at",)
    search_fields = ("name",)
    list_filter = ("name",)


@admin.register(Newspaper)
class NewspaperAdmin(admin.ModelAdmin):
    list_display = ("title", "topic", "published_date", "created_at", "updated_at",)
    search_fields = ("title", "topic__name", "published_date",)
    list_filter = ("topic__name", "published_date", "created_at", "updated_at",)

from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from modeltranslation.admin import TranslationAdmin

from .models import *

admin.site.site_title = 'Кино-библиотека'
admin.site.site_header = 'Кино-библиотека'


class MovieAdminForm(forms.ModelForm):
    description_ru = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())
    description_en = forms.CharField(label="Описание", widget=CKEditorUploadingWidget())

    class Meta:
        model = Movie
        fields = '__all__'


@admin.register(Category)
class CategoryAdmin(TranslationAdmin):
    list_display = ("id", "name", "url")
    list_display_links = ("id", "name")

@admin.register(Actor)
class ActorAdmin(TranslationAdmin):
    list_display = ("name", "age", "get_image")
    list_display_links = ("name",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" heigth="60">')

    get_image.short_description = "Изображение"

@admin.register(Genre)
class GenreAdmin(TranslationAdmin):
    list_display = ("name", "url")
    list_display_links = ("name",)

class ReviewInline(admin.TabularInline):
    model = Reviews
    extra = 1
    readonly_fields = ("name", "email", "text")

class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 1
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="100" heigth="110">')

    get_image.short_description = "Изображение"

@admin.register(Movie)
class MovieAdmin(TranslationAdmin):
    list_display = ("title", "category", "url", "draft")
    list_display_links = ("title",)
    list_filter = ("category", "year")
    list_editable = ("draft",)
    actions = ["publish", "unpublish"]
    search_fields = ("title", "category__name")
    inlines = [MovieShotsInline, ReviewInline]
    form = MovieAdminForm
    save_on_top = True
    save_as = True
    readonly_fields = ("get_image",)
    fieldsets = (
        ("О фильме", {
            'fields': (
                ("title", "tagline", "description", "poster", "get_image", "category", "country"),
            ),
        }),
        ("Даты", {
            'fields': (
                ("year", "world_primiere"),
            ),
        }),
        ("Актерская группа", {
            'fields': (
                ("actors", "directors", "genres"),
            ),
        }),
        ("Финансы", {
            'fields': (
                ("budget", "fees_in_usa", "fees_in_world"),
            ),
        }),
        ("Опции", {
            'fields': (
                ("url", "draft"),
            ),
        }),
    )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="100" heigth="110">')

    def unpublish(self, request, queryset):
        """Снять с публикации"""
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    def publish(self, request, queryset):
        """Опубликовать"""
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 запись была обновлена"
        else:
            message_bit = f"{row_update} записей были обновлены"
        self.message_user(request, f"{message_bit}")

    publish.short_description = "Опубликовать"
    publish.allowed_permissions = ('change', )

    unpublish.short_description = "Снять с публикации"
    unpublish.allowed_permissions = ('change',)

    get_image.short_description = "Постер"

@admin.register(MovieShots)
class MovieShotsAdmin(TranslationAdmin):
    list_display = ("title", "movie", "get_image")
    list_display_links = ("title",)
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" heigth="60">')

    get_image.short_description = "Изображение"


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ("value",)

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ("ip", "star", "movie")
#admin.site.register(Rating)

@admin.register(Reviews)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "movie", "parent")
    readonly_fields = ("name", "email", "text")



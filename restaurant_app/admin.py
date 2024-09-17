from django.contrib import admin

class BaseAdmin(admin.ModelAdmin):
    class Meta:
        abstract = True
    list_display = ["created_at", "updated_at"]
    
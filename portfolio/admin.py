from django.contrib import admin
from .models import Project, GeneralSetting, Tool, CreativeStep

@admin.register(GeneralSetting)
class GeneralSettingAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        # Evitar criar múltiplos settings, já que é um singleton
        if GeneralSetting.objects.exists():
            return False
        return True

@admin.register(Tool)
class ToolAdmin(admin.ModelAdmin):
    list_display = ('name', 'percentage', 'order')
    ordering = ('order',)

@admin.register(CreativeStep)
class CreativeStepAdmin(admin.ModelAdmin):
    list_display = ('step_number', 'title', 'order')
    ordering = ('order',)

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'section', 'order', 'is_video')
    list_filter = ('section', 'is_video')
    search_fields = ('title', 'category')
    ordering = ('order',)

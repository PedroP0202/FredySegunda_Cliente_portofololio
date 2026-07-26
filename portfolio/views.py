from django.shortcuts import render
from .models import Project, GeneralSetting, Tool, CreativeStep, CustomGallery


def home(request):
    projects = Project.objects.all()
    general_setting = GeneralSetting.objects.first()
    tools = Tool.objects.all()
    creative_steps = CreativeStep.objects.all()
    custom_galleries = CustomGallery.objects.filter(is_active=True).prefetch_related('projects')

    context = {
        'featured_main': projects.filter(section='featured_main', custom_gallery__isnull=True).first(),
        'featured_sides': projects.filter(section='featured_side', custom_gallery__isnull=True)[:4],
        'gallery_smalls': projects.filter(section='gallery_small', custom_gallery__isnull=True)[:18],
        'gallery_asyms': projects.filter(section='gallery_asym', custom_gallery__isnull=True)[:12],
        'reels': projects.filter(section='reel', custom_gallery__isnull=True)[:15],
        
        'custom_galleries': custom_galleries,
        'setting': general_setting,
        'tools': tools,
        'creative_steps': creative_steps,
    }
    return render(request, 'portfolio/index.html', context)

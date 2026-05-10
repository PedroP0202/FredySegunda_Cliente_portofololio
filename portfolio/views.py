from django.shortcuts import render
from .models import Project, GeneralSetting, Tool, CreativeStep

def home(request):
    projects = Project.objects.all()
    general_setting = GeneralSetting.objects.first()
    tools = Tool.objects.all()
    creative_steps = CreativeStep.objects.all()

    context = {
        'featured_main': projects.filter(section='featured_main').first(),
        'featured_sides': projects.filter(section='featured_side')[:2],
        'gallery_smalls': projects.filter(section='gallery_small')[:3],
        'gallery_asyms': projects.filter(section='gallery_asym')[:2],
        'reels': projects.filter(section='reel')[:5],
        
        'setting': general_setting,
        'tools': tools,
        'creative_steps': creative_steps,
    }
    return render(request, 'portfolio/index.html', context)

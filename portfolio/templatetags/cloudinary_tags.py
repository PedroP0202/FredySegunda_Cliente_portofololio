from django import template

register = template.Library()

@register.filter
def cloudinary_video_url(url):
    if url:
        return url.replace('/image/upload/', '/video/upload/')
    return url

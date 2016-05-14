from django.conf import settings
import shutil,os
from django.core.exceptions import MultipleObjectsReturned
from models import *

def style(orig_image,style_name):
    try:
        orig_image_name = orig_image.name
    except AttributeError:
        orig_image_name = orig_image
    try:
        style_id = int(style_name)
    except ValueError:
        style_id = None
    try:
        if style_id:
            style = Style.objects.get(id=style_id)
        else:
            style = Style.objects.get(name=style_name)
    except Style.DoesNotExist:
        return orig_image
    try:
        image = ImageStyle.objects.get(name=orig_image_name,style=style)
    except ImageStyle.DoesNotExist:
        image = ImageStyle(name=orig_image_name,style=style)
        image.save()
    except MultipleObjectsReturned:
        images = ImageStyle.objects.filter(name=orig_image_name,style=style)
        for i in images:
            i.delete()
        image = ImageStyle(name=orig_image_name,style=style)
        image.save()

    return "%s" % (image.image,)

def render_image(style_id,path):
    try:
        style = Style.objects.get(id=style_id)
    except Style.DoesNotExist:
        raise Http404("Style not found")
    try:
        image = ImageStyle.objects.get(name=path,style=style)
    except ImageStyle.DoesNotExist:
        image = ImageStyle(name=path,style=style)
        image.save()

    return image


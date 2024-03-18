from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.exceptions import BadRequest, ValidationError, PermissionDenied
from django.conf import settings

from PIL import Image
from io import BytesIO

import re
import os
import html
import array
from pathlib import Path
import frontmatter

from .app_settings import app_settings
from .models import SingleTokenAccess


# Create your views here.

IMAGE_MAX_WIDTH=1200
IMAGE_MAX_HEIGTH=500
SLUGEX = re.compile('^(?![0-9-]+$)(?:[a-z]{2,}_?|[0-9]_?)+(?<!_)$')

def save_image(photo,cat, name):
    # start compressing image
    if (photo.name.lower().endswith(('.png', '.jpg', '.jpeg', '.tiff', '.bmp'))):
        try:
            image_temporary = Image.open(photo)
            image_temporary.verify()

            image_temporary = Image.open(photo)
            image_temporary.thumbnail(
                    (IMAGE_MAX_WIDTH,IMAGE_MAX_HEIGTH),
                    Image.Resampling.LANCZOS)
            rgba_image = image_temporary.convert('RGBA')
            img = Image.new("RGB", rgba_image.size, (255, 255, 255))
            img.paste(rgba_image, mask = rgba_image.split()[3])
            # saving output
            img.save(app_settings.CONTENT_DIRECTORY+"/"+cat+"/"+name+".jpg",
                    "JPEG",
                    optimize=True,
                    quality=80,
                    progressive=True)
            img.save(app_settings.CONTENT_DIRECTORY+"/"+cat+"/"+name+".webp",
                    'WEBP')
            
            return img
        except BaseException as err:
            print(err)
            raise ValidationError("Wrong Image format", code=422)
    else:
        raise ValidationError("Wrong Image format: '.png', '.jpg', '.jpeg', '.tiff', '.bmp'", code=422)


def fileslist(request):
    if(request.user.is_anonymous):
        raise PermissionDenied()

    files=[]
    selected_choice=""
    error=""
    print(request.POST)
    selected_cat = request.POST.get("choice", False)
    action = request.POST.get("action", False)
    if(selected_cat in app_settings.CATEGORIES):
        if(action == 'refresh'):
            files = [f for f in Path(app_settings.CONTENT_DIRECTORY+"/"+selected_cat).glob("*.md")]
            files.sort(key=lambda x: x.lstat().st_mtime)
            files = reversed(files)
        elif(action == 'new'):
            slug = request.POST.get("slug", False)
            email = request.POST.get("email", False)
            if(not slug or not SLUGEX.match(slug)):
                error="Veuillez indiquez un nom de fichier valide [a-z0-9_]"
            elif(not os.path.exists(app_settings.CONTENT_DIRECTORY+"/"+selected_cat+"/"+slug+".md")):
                token = request.POST.get("token", False)
                if(token and not SingleTokenAccess.objects.filter(slug=selected_cat+"/"+slug).exists()):
                    print("newtoken")
                    sta = SingleTokenAccess(slug=selected_cat+"/"+slug, contact=email)
                    sta.save()
                return redirect('edit', cat=selected_cat, slug=slug)
            else:
                error = "Slug already exist ! "
    else:
        error = "Vous devez choisir une catégorie"
    return render(
        request,
        "core/list.html",
        {
            "categories": app_settings.CATEGORIES,
            "fileslist": files,
            "selected_cat": selected_cat,
            "error": error
        },
    )

def getImage(request, cat, name):
    print("getImage")
    if(cat in app_settings.CATEGORIES):
        with open(app_settings.CONTENT_DIRECTORY+"/"+cat+"/"+name+".jpg", "rb") as f:
            return HttpResponse(f.read(), content_type="image/jpeg")
    else:
        raise BadRequest()

def edit(request, cat, slug):
    if(cat in app_settings.CATEGORIES):
        token = False
        try:
            token = SingleTokenAccess.objects.get(slug=cat+"/"+slug)
        except SingleTokenAccess.DoesNotExist:
            pass
        getToken = request.GET.get("token", False)
        if(request.user.is_anonymous and getToken!=token.token):
            raise BadRequest()
        if(os.path.isfile(app_settings.CONTENT_DIRECTORY+"/"+cat+"/"+slug+".md")):
            origin_post = frontmatter.load(app_settings.CONTENT_DIRECTORY+"/"+cat+"/"+slug+".md")
        else:
            origin_post = None
        if(request.POST.get("title", False)):
            post = frontmatter.Post(html.escape(request.POST["content"]))
            post["title"]=request.POST["title"]
            post["slug"]=slug
            post["date"]=request.POST["date"]
            post["summary"]=request.POST["summary"]
            post["authors"]=request.POST["authors"]
            post["tags"]=request.POST["tags"]
            file = request.FILES.get('thumbnail', False)
            if(file):
                post["image"]=slug
                save_image(file, cat, slug)
            elif(origin_post and origin_post["image"]):
                post["image"]=origin_post["image"]
            with open(app_settings.CONTENT_DIRECTORY+"/"+cat+"/"+slug+".md", "wb") as f:
                frontmatter.dump(post, f, sort_keys=False)
        post = {}
        if(os.path.isfile(app_settings.CONTENT_DIRECTORY+"/"+cat+"/"+slug+".md")):
            post = frontmatter.load(app_settings.CONTENT_DIRECTORY+"/"+cat+"/"+slug+".md")
            post.content=html.unescape(post.content)
        return render(
            request,
            "core/editadmin.html",
            {
                "SITE_URL": settings.SITE_URL,
                "post": post,
                "cat": cat,
                "token": token
            },
        )
    else:
        raise BadRequest()

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from feeds.utils import create_feed
from django.views.decorators.http import require_POST
from decorators.decorators import ajax_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
import redis
from django.conf import settings

from .models import Image

from .forms import ImageUploadForm

# connecting the redis server
r = redis.Redis(host=settings.REDIS_HOST, 
                port=settings.REDIS_PORT,
                db=settings.REDIS_DB)


# views for listing all images uploaded
@login_required
def image_list_view(request):
    '''This view handles both standard and AJAX pagination'''
    images = Image.objects.all()
    paginator = Paginator(images, 8)
    page = request.GET.get('page')
    try:
        images = paginator.page(page)
    except PageNotAnInteger:
        images = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')  # return empty page if page is out of range
        images = paginator.page(paginator.num_pages) 
    if request.is_ajax():
        return render (request, 'images/ajax_image_list.htm',
                       {'section': 'images', 'images':images})
    return render(request, 'images/image_list.html',
                  {'section':'images', 'images': images})


@login_required
def upload_image_view(request):
    if request.method == 'POST':
        # a form has been submitted
        form = ImageUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.author = request.user   # Assgin current login user to the upload
            new_image.save()
            create_feed(request.user, 'Uploaded image', new_image)
            messages.success(request, 'Image uploaded successfully')
            
            #Redirect user to image detail_url
            return redirect(new_image.get_absolute_url())
        
    # Else render new form to user
    else:
        form = ImageUploadForm(data=request.GET)
    return render(request, 'images/upload_image.html',
                  {'section': 'images', 'form':form})
@login_required
def image_detail_view(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    #increment image view by 1
    total_image_views = r.incr(f'image:{image.id}:views')
    #rank most image viewed
    r.zincrby('image_ranking',1, image.id)
    return render(request, 'images/image_detail.html', {'image':image, 'section':'images',
                                                        'total_image_views': total_image_views})

# view for Ranking of the most viewed images
def image_ranking_view(request):
    #get image ranking dicitonary
    image_ranking = r.zrange('image_ranking', 0, -1, desc=True)[:8]
    image_ranking_ids = [int(id) for id in image_ranking]
    most_images_viewed = list(Image.objects.filter(id__in=image_ranking_ids))
    most_images_viewed.sort(key=lambda index: image_ranking_ids.index(index.id))
    return render(request, 'ranking.html',
                  {'most_images_viewed':most_images_viewed})

#view for liking an image
@ajax_required
@login_required
@require_POST
def like_image_view(request):
    image_id = request.POST.get('id')
    action = request.POST.get('action')
    if image_id and action:
        try:
            image = Image.objects.get(id=image_id)
            if action == 'like':
                image.users.add(request.user)
                create_feed(request.user, 'likes', image)
            else:
                image.users.remove(request.user)
            return JsonResponse({'status':'ok'})
        except:
            pass
    return JsonResponse({'status':'error'})


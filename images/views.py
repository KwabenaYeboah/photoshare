from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import get_object_or_404
from .models import Image

from .forms import ImageUploadForm

@login_required
def upload_image_view(request):
    if request.method == 'POST':
        # a form has been submitted
        form = ImageUploadForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            new_image = form.save(commit=False)
            new_image.author = request.user   # Assgin current login user to the upload
            new_image.save()
            messages.success(request, 'Image uploaded successfully')
            
            #Redirect user to image detail_url
            return redirect(new_image.get_absolute_url())
        
    # Else render new form to user
    else:
        form = ImageUploadForm(data=request.GET)
    return render(request, 'images/upload_image.html',
                  {'section': 'images', 'form':form})

def image_detail_view(request, id, slug):
    image = get_object_or_404(Image, id=id, slug=slug)
    return render(request, 'images/image_detail.html', {'image':image, 'section':'images', })
    
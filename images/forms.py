from django import forms
from urllib import request
from django.utils.text import slugify
from django.core.files.base import ContentFile
from .models import Image

class ImageUploadForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ('title', 'url', 'description')
        widgets = {'url':forms.HiddenInput}
        
        # Validate user provided url against image requirements
        def clean_url(self):
            url = self.cleaned_data['ur']
            valid_extensions = ['jpg','jpeg', 'png']
            extension = url.rsplit('.', 1)[1].lower()
            if extension not in valid_extensions:
                raise forms.ValidationError('The image extension from the URL is not supported')
            return url
        
        # Overide ModelForm save method against image requirements
        def save(self, force_insert=False,
                 force_update=False, commit=True):
            image = super().save(commit=False)
            image_url = self.clean_data['url']
            extensions = image_url.rsplit('.', 1)[1].lower()
            image_name = slugify(image.title)
            
            file = request.urlopen(image_url) # Retrieve image from provided url
            image.image.save(image_name, ContentFile(file.read()), save=False)
            
            if commit: #if commit is stll true then we save the file
                image.save()
            return image
            
            
            
        

    
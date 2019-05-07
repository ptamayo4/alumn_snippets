from django.core.files.base import ContentFile
from io import BytesIO
from PIL import Image, ExifTags

def file_clean(file):
    limit = 5 * 1024 * 1024
    types = [".jpg", ".png", ".jpeg"]
    errors = {}
    if file.size > limit:
        errors["size"] = "File size must be under 5mb"
    format_check = False
    for t in types:
        if file.name.lower().endswith(t):
            format_check = True
    if not format_check:
        errors["type"] = "File is wrong format, must be .jpg, .jpeg, or .png"
    return errors

def image_crop(x,y,w,h,image):
    if x != '':
        x = float(x) 
    else:
        x = 0.0
    if y != '':
        y = float(y)
    else:
        y = 0.0
    if w != '':
        w = float(w)
    else:
        w = 400
    if h != '':
        h = float(h)
    else:
        h = 400
    raw_image=Image.open(image)
    
    # Check for exif rotation
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation]=='Orientation':
                break
        exif=dict(raw_image._getexif().items())

        if exif[orientation] == 3:
            raw_image=raw_image.rotate(180, expand=True)
        elif exif[orientation] == 6:
            raw_image=raw_image.rotate(270, expand=True)
        elif exif[orientation] == 8:
            raw_image=raw_image.rotate(90, expand=True)
        print("finished rotating from exif")

    except (AttributeError, KeyError, IndexError):
        print("No EXIF data")        
        pass

    cropped_image = raw_image.crop((x,y,w+x,h+y))
    resized_image = cropped_image.resize((400,400), Image.ANTIALIAS)
    if not resized_image.mode == 'RGB':
        resized_image = resized_image.convert('RGB')
    buffer = BytesIO()
    resized_image.save(fp=buffer, format='JPEG')
    return ContentFile(buffer.getvalue())
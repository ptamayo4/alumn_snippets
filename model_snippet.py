# Lives in a model Manager for User

def update_user(self, data, user_id, files):
    # print(data)
    # print(files)
    user = self.get(id=user_id)
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    # user.email = data['email']
    user.location = Location.objects.get(pk=data['location'])
    try:
        user.full_clean()
    except ValidationError as e:
        print("E",e)
        return {'errors': dict(e)}
    else:
        if 'profile_pic' in files:
            file_errors = file_clean(files['profile_pic'])
            if not file_errors:
                resized_img = image_crop(data['x'], data['y'], data['width'], data['height'], files['profile_pic'])
                img_name = "pf_img_u" + str(user.id) + ".jpg"
                p = MEDIA_ROOT + img_name
                user.profile_pic.save(img_name,InMemoryUploadedFile(
                    resized_img,
                    None,
                    img_name,
                    'image/jpeg',
                    resized_img.tell,
                    None
                ))       
            else:
                return {'errors': file_errors}                   
        user.save()
        return {'user': user}
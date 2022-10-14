import base64, uuid
from django.core.files.base import ContentFile

def get_report_image(data):
    _ , str_image = data.split(';base64')
    #str_image ===>> its type is str 

    decoded_img = base64.b64decode(str_image)
    #decoded_img ===>> its type is bytes (decode)

    img_name = str(uuid.uuid4())[:10] + '.png'
    data = ContentFile(decoded_img, name=img_name)
    
    return data
from io import BytesIO
from PIL import Image


def resize_image(image_buffer, width=100, height=100):
    img = Image.open(BytesIO(image_buffer))
    img = img.convert('RGB')
    resized_img = img.resize((width, height))
    buf = BytesIO()
    resized_img.save(buf, 'JPEG')
    buf.seek(0)
    return buf.read()
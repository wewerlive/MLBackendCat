import base64
from PIL import Image
from io import BytesIO

def imageFromBase64(base64str):
    return Image.open(BytesIO(base64.b64decode(base64str.split(",")[1])))

def imageToBase64(image):
    imFile = BytesIO()
    image.save(imFile, format="JPEG")
    imFile = imFile.getvalue()
    imFile = base64.b64encode(imFile)
    return str(imFile)

def imageToBytes(image):
    imFile = BytesIO()
    image.save(imFile, format="JPEG")
    return imFile

def imageFromBytes(imageBytes):
    return Image.open(imageBytes)

def base64ToBytes(base64str):
    return BytesIO(base64.b64decode(base64str.split(",")[1]))

def base64FromBytes(imageBytes):
    return base64.b64encode(imageBytes)
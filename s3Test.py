from serverUtils.awsUtils import s3, uploadImage
from serverUtils.imageUtils import imageFromBase64, base64ToBytes, imageFromBytes, imageToBytes
from serverUtils.modelUtils import predictTryOn
import uuid
f= open("serverTests/sampleRequest.json", "r")
data = f.read()
f.close()

import json
data = json.loads(data)

personImageBytes = base64ToBytes(data["personImage"])
clothImageBytes = base64ToBytes(data["clothImage"])
personImage = imageFromBytes(personImageBytes)
print(personImage)
clothImage = imageFromBytes(clothImageBytes)
clothType = data["clothType"]
num_inference_steps = data["num_inference_steps"]

result = predictTryOn(personImage, clothImage, clothType, num_inference_steps, seed=2, guidance_scale=2.5)

resultBytes = imageToBytes(result)
unique_id = str(uuid.uuid4())
print(unique_id)

personImageBytes.seek(0)
clothImageBytes.seek(0)
resultBytes.seek(0)

uploadImage(personImageBytes, "devbackendpersonimage", unique_id+"-person.jpg")
uploadImage(clothImageBytes, "devbackendclothimage",unique_id+"-cloth-"+clothType+".jpg")
uploadImage(resultBytes, "devbackendresultimage", unique_id+clothType+"-result.jpg")

buckets = s3.list_buckets()

# for bucket in buckets['Buckets']:
#     print(f'{bucket["Name"]}')


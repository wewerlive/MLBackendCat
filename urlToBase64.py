# import json
# f = open("products.json", "r")
# products = json.loads(f.read())
# f.close()

# # print(products)

# from serverUtils.imageUtils import imageToBase64
# from PIL import Image
# import requests
# from io import BytesIO

# for product in products["products"]:
#     # print(product)
#     # response = requests.get(product["product_link"])
#     # image = Image.open(BytesIO(response.content))
#     print(product["product_link"])
#     length = len("https://ml2d-products.s3.ap-south-1.amazonaws.com/")
#     print(product["product_link"][length:])
#     # image.save("products/"+product["product_link"][length:])
#     # product["product_link"] = 'data:image/png;base64'+imageToBase64(image)[2:]
#     product["product_link"] = "https://demo-cloth-images.s3.ap-south-1.amazonaws.com/" + product["product_link"][length:]
# # print(products)

# f = open("products2.json", "w")
# f.write(json.dumps(products))
# f.close()


import json
f = open("products2.json", "r")
products = json.loads(f.read())
f.close()

for product in products["products"]:
    pType = product["product_type"]
    if pType == "top":
        product["product_type"] = "upper"
    elif pType == "bottom":
        product["product_type"] = "lower"
    else:
        product["product_type"] = "overall"

f = open("products3.json", "w")
f.write(json.dumps(products))
f.close()
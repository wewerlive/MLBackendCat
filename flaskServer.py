from flask import Flask, request
from utils.modelUtils import predictTryOn
app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/tryon",methods=['POST'])
async def tryon():
    retObj = {}
    if request.method == 'POST':
        try:
            personImage64 = request.json['personImage']
            clothImage64 = request.json['clothImage']
            clothType = request.json['clothType']
            num_inference_steps = int(request.json['num_inference_steps'])
            result = await predictTryOn(personImage64,clothImage64,clothType,num_inference_steps)
            retObj['result'] = result
        except Exception as e:
            retObj['error'] = str(e)
        print(request.json)
    return retObj
from flask import Flask,request,jsonify,make_response

import requests
import pytesseract
from pytesseract import Output

import cv2
import json
from pdf2image import convert_from_path
from flask_cors import CORS, cross_origin




app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

with open('Template.json') as f:
    res_op = json.load(f)
# medication_ENDPOINT='https://67b7-35-204-254-157.ngrok.io/med7'
# social_ENDPOINT='https://67b7-35-204-254-157.ngrok.io/social'
# demographics_ENDPOINT='https://3d9b-34-105-100-71.ngrok.io/demo'

@app.route("/ocr",methods=['POST'])
@cross_origin()
def extraction():
    try:
        file = request.files['file']
        print(file.filename)
        file.save("./test.pdf")
        dict1 = {}
        file = "./test.pdf"
        images = convert_from_path(file)
        for page,image in enumerate(images):
            image.save('outfile.png', 'PNG')
            img1 = cv2.imread('outfile.png')
            d = pytesseract.image_to_data(img1, output_type=Output.DICT)
            n_boxes = len(d['level'])
            temp_list=[]
            for i in range(n_boxes):
                if int(float(d['conf'][i])) >= 0 and d['text'][i] != '':
                    temp_list.append(d['text'][i])
            temp_str=' '.join(temp_list)
            dict1['page_{}'.format(page + 1)] = temp_str
        print(dict1)  
        # r = requests.post(url=medication_ENDPOINT, json=dict1, verify=False)
        # r = r.json()
        # res_op['op'][1]['medications'] = r['med_op']

        # social_data = {'text': dict1['page_12']}
        # r1 = requests.post(url=social_ENDPOINT, json=social_data, verify=False)
        # r1 = r1.json()
        # res_op['op'][4]['Socail_history'] = r1['soc_op']

        # demo_data = {'text': dict1['page_1']}
        # r2 = requests.post(url=demographics_ENDPOINT, json=demo_data, verify=False)
        # r2 = r2.json()
        # print(r2)
        # res_op['op'][0]['demographic_details'] = r2['demo_res']
        # print(res_op)

        return {'ocr_op':dict1}
    except Exception as e:
        print('in exception',e)
        raise Exception(e,"caught on exception")

app.run()

def _build_cors_preflight_response():    
    response = make_response()
    print('cors resp')
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

def _corsify_actual_response(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    return response

# #AFTER REQUEST
@app.after_request
def afterRequest(response):
    if (request.method == 'OPTIONS'):
        return _build_cors_preflight_response()
    elif (request.method == 'POST'):
        return _corsify_actual_response(response)
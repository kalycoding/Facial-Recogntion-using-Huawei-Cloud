# -*- coding: utf-8 -*-


import json
import requests
import base64
import cv2
import io
from PIL import Image


def getTokenKey(username,password,domain_name, project_name):
    """
    Get X-Subject Token from Huawei Cloud 

    :param username: Huawei Cloud Username
    :param password: Huawei Cloud Password
    :Param domain_name: Huawei Cloud Password
    :param project_name: Huawei Cloud Project name: link https://huaweicloud.com/intl

    
    :rtype: X-Auth-Token
    """
    url = 'https://iam.ap-southeast-1.myhuaweicloud.com/v3/auth/tokens'

    body = {
    "auth": {
        "identity": {
       
            "password": {
                "user": {
                    "name": username, 
                    "password": password, 
                    "domain": {
                        "name": domain_name
                    }
                }
            },
            "methods": [
                "password"
            ]
        }, 
        "scope": {
            "project": {
                "name": project_name,
            },   
        }
      }
    }

    headers = {
        'Content-Type' : 'application/json'
    }

    try:
      request = requests.post(url=url, data=json.dumps(body), headers=headers)
      return request.headers['X-Subject-Token']
    except:
      return 'Error {}'.format(request.status_code)

def facialRecognition(image_url):

  """
  :param image_url: url of the image to get detected
    
  :rtype: array of faces
  """
  url = 'https://face.ap-southeast-1.myhuaweicloud.com/v2/0698a89be000264a2f05c006124c1bcb/face-detect'
  faces = []
  body = {
    "image_url": image_url,
  }

  headers = {
      'Content-Type': "application/json",
      "X-Auth-Token": getTokenKey('username','password', 'domain_name', 'ap-southeast-1')
  }

  request = requests.post(url=url, data=json.dumps(body), headers=headers)

  output = request.json()['faces']

  for i in output:
    faces.append(i)

  return faces

def boundBox(image_url):

  """
  Draw a rectangular box in the detected face

  param image_url: image url

  rtype: bounded image
  """
  img = requests.get(image_url)
  image = Image.open(io.BytesIO(img.content))
  image.save('facialTest.png')
  img_rect = cv2.imread('facialTest.png')

  for i in facialRecognition(image_url):
    point1 = (i['bounding_box']['top_left_x'],i['bounding_box']['top_left_y'])
    point2 = (i['bounding_box']['top_left_x'] + i['bounding_box']['width'], i['bounding_box']['top_left_y'] + i['bounding_box']['height'])
    color = (0,255,0)
    box_thickness = 2
    img_rect = cv2.rectangle(img_rect,point1, point2, color, box_thickness)

  return cv2.imshow('Facial Recognition', img_rect)

boundBox('https://kalycodes.obs.ap-southeast-1.myhuaweicloud.com/facialTest.jpg')
cv2.waitKey(0)
cv2.destroyAllWindows()

# -*- coding: utf-8 -*-
"""Subway_Info_Bot.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1enRVihaWQuBcgzVBcsfgRmYozPm8-kVl
"""

!pip install flask-ngrok

from flask_ngrok import run_with_ngrok
from flask import Flask, request
import pprint
import requests
import pandas as pd
from bs4 import BeautifulSoup

from gensim.models.fasttext import FastText
import numpy as np
import matplotlib.pyplot as plt
plt.style.use('ggplot')

from sklearn.decomposition import PCA

token = '54614467757777783734566d7a6578'
start_index = 1
# term_index = 100
url_format = "http://openapi.seoul.go.kr:8088/{token}/xml/StationNmfpcOrgnThemaNm/{start_index}/{end_index}/"

app = Flask(__name__)
run_with_ngrok(app)   #starts ngrok when the app is run

@app.route('/webhook', methods = ['POST'])
#if 문으로 결과 값에 따라서 다른 url 접근해서 값 받아오기
def results():
    response = {}

    req = request.get_json(force=True)
    
    func = req.get('queryResult').get('intent')
    print(func)
    intent_name = {"name": "projects/pizza-order-bot-jdknon/agent/intents/f3508021-c801-4666-85e0-24d8f570a4e8",
      "displayName": "search-with-station-name"}
    intent_story = {"name": "projects/pizza-order-bot-jdknon/agent/intents/98d5f9dd-ceca-40f6-9732-ca3819075f4e",
      "displayName": "search-with-station-name-story"}
    intent_fl = {"name": "projects/pizza-order-bot-jdknon/agent/intents/70691acb-f8a3-4343-81ce-aeaaeefe3d70",
      "displayName": "search-with-station-name-first-end"}
    print(intent_name)
    if(func['displayName'] == intent_name['displayName']):
      response = station_name(req)
    
    elif(func['displayName'] == intent_story['displayName']):
      response = station_name_story(req)

    elif(func['displayName'] == intent_fl['displayName']):
      response = station_fl(req)

    return response

if __name__ == "__main__":
    app.run()

def station_name(req):
    
    queryText = req.get('queryResult').get('parameters').get('station-story')
    print(queryText)

    response = \
    {
        "fulfillmentMessages": [ {    "quickReplies": { "title": "기능 선택", "quickReplies": [ "역이름의 유래", "첫차 / 막차시간"] },"platform": "LINE"},{    "text": {        "text": [ ""]    }}]
    }
    return response

def station_name_story(req):
  print(req.get('queryResult').get('parameters'))
  print(type(req.get('queryResult').get('parameters')))
  # if req.get('queryResult').get('parameters') == {}:
  #   response = {"fulfillmentMessages": [ {
  #             "text": {
  #                 "text": ["해당 역은 이름의 유래가 없습니다"]
  #             }
  #         }]}
  #   print(response)
  #   return response
  # else:
  queryText = req.get('queryResult').get('outputContexts')[0].get('parameters').get('station-story')
  url = "http://openapi.seoul.go.kr:8088/54614467757777783734566d7a6578/xml/StationNmfpcOrgnThemaNm/1/1/ /"+queryText  
  # url로 조회 하여 얻은 데이터(xml) 을 soup 객체로 파싱
  name_story = requests.get(url)
  soup = BeautifulSoup(name_story.content, 'xml')
  # 문서의 고유한 번호인 'faq_seqno', 게시판의 유형 정보인 'faq_top' 객체 조회
  nmfpc = soup.find('NMFPC_ORGN').string
  print(nmfpc)
  response = {"fulfillmentMessages": [ {
              "text": {
                  "text": [nmfpc]
              }
          }]}
  print(response)
  return response

def station_fl(req):
  response = {"fulfillmentMessages": [
        {
            "text": {
                "text": ["서비스 준비중 입니다"]
            }
        }
        ]}
  return response

url = "http://openapi.seoul.go.kr:8088/54614467757777783734566d7a6578/xml/StationNmfpcOrgnThemaNm/1/1/ /"+"제기동"  
    # url로 조회 하여 얻은 데이터(xml) 을 soup 객체로 파싱
name_story = requests.get(url)
soup = BeautifulSoup(name_story.content, 'xml')
    # 문서의 고유한 번호인 'faq_seqno', 게시판의 유형 정보인 'faq_top' 객체 조회
nmfpc = soup.find('NMFPC_ORGN').string
print(nmfpc)

"""# OPEN API 데이터 수집을 위한 토큰 및 url 포멧터 정의"""

token = '54614467757777783734566d7a6578'
start_index = 1
# term_index = 100
url_format = "http://openapi.seoul.go.kr:8088/{token}/xml/StationNmfpcOrgnThemaNm/{start_index}/{end_index}/"

# start_index = 1
  # end_index = 119

  # # url = url_format.format(token=token,
  # #                         start_index=start_index,
  # #                         end_index=end_index)+'/서울역'
  # url = "http://openapi.seoul.go.kr:8088/54614467757777783734566d7a6578/xml/StationNmfpcOrgnThemaNm/1/1/ /"+"제기동"

  # # url로 조회 하여 얻은 데이터(xml) 을 soup 객체로 파싱
  # response= requests.get(url)
  # soup = BeautifulSoup(response.content, 'xml')
  # #print(soup)
  # # 문서의 고유한 번호인 'faq_seqno', 게시판의 유형 정보인 'faq_top' 객체 조회
  # nmfpc = soup.find('NMFPC_ORGN').text
  # print(nmfpc)

url_time_format = 'http://openapi.seoul.go.kr:8088/{token}/xml/SearchFirstAndLastTrainbyLineServiceNew/{start_index}/{end_index}/{line_num}/{inout_tag}/{week_tag}/'

for roop_index in range(5):

  start_index = 1
  inout_tag=1
  week_tag=1
  end_index = roop_index+1

  url_time = url_time_format.format(token=token,
                          start_index=start_index,
                          end_index=end_index,
                          line_num='1호선',
                          inout_tag=inout_tag,
                          week_tag=week_tag)
  
  # url로 조회 하여 얻은 데이터(xml) 을 soup 객체로 파싱
  response= requests.get(url_time)
  soup = BeautifulSoup(response.content, 'xml')
  print(soup)
  # 문서의 고유한 번호인 'faq_seqno', 게시판의 유형 정보인 'faq_top' 객체 조회
  #statn = soup.find_all('STATN_NM')
  #nmfpc = soup.find('NMFPC_ORGN').string
  #print(nmfpc)

  # 'statn', 'nmfpc' 객체 조회 값을 이용해 dataframe 객체 생성
  # st_data = {
  #     'statn': statn,
  #     'nmfpc' : nmfpc
  # }

  #df_station_tmp = pd.DataFrame(st_data)
  # Q1. 에서 정의한 함수를 dataframe 객체의 apply(axis='columns')) 함수를 이용하여 dataframe 객체에 적용
  #df_station_tmp = df_station_tmp.apply(getInfo, axis='columns')
  # row에 하나의 Nan 값만 가져도 Drop
  #df_station_tmp = df_station_tmp.dropna(how='any')

  # 수집된 데이터를 모으는 df_fq 객체에 매 스텝 마다 조회할 결과 추가
  #df_station = df_station.append(df_station_tmp, ignore_index=True)
  #df_station = df_station_tmp

  #print('end index {}'.format(end_index))

url = "http://openapi.seoul.go.kr:8088/54614467757777783734566d7a6578/xml/SearchFirstAndLastTrainbyLineServiceNew/1/1000/01호선/1/1"
# url로 조회 하여 얻은 데이터(xml) 을 soup 객체로 파싱
station_name = requests.get(url)
soup = BeautifulSoup(station_name.content, 'xml')
print(soup)
# 문서의 고유한 번호인 'faq_seqno', 게시판의 유형 정보인 'faq_top' 객체 조회
nmfpc = soup.find('STATION_NM').string


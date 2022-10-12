import pandas as pd
import requests
import json
import folium
from folium.plugins import MarkerCluster
import matplotlib.pyplot as plt
import seaborn as sns
import os

REST_API_KEY = '1830579e0e3f456ce3988b002758b9de'

import warnings
warnings.filterwarnings('ignore')

################################################################################################
# 좌표 받기
def get_yx(query):
    import requests
    headers = {'Authorization': f'KakaoAK {REST_API_KEY}'}
    url = f'https://dapi.kakao.com/v2/local/search/address.json?query={query}'
    r = requests.get(url, headers=headers)
    addr = r.json()
    try: # 오류가 날만한 구간
        return [addr['documents'][0]['y'], addr['documents'][0]['x']]
    except: # 오류가 날 경우 반환값
        return '결과없음'

# 구주소 받기
def get_address(query): 
    import requests
    headers = {'Authorization': f'KakaoAK {REST_API_KEY}'}
    url = f'https://dapi.kakao.com/v2/local/search/address.json?query={query}'
    r = requests.get(url, headers=headers)
    addr = r.json()
    try:
        return addr['documents'][0]['address']['address_name']
    except:
        return '결과없음'
    
################################################################################################
# 전기차_충전소_설치현황 데이터 불러오기
df = pd.read_excel('02_folium\전기차_충전소_설치현황_20220921.xls', header=2)

# 데이터 전처리
df.drop(columns=['시구', '지원차종'], inplace=True)
df['시'] = df['주소'].str.split().str.get(0)
df_daejeon = df[df['시']=='대전광역시']
df_daejeon['주소'] = df_daejeon['주소'].str.split('(').str.get(0).str.split(',').str.get(0).str.strip()

# 함수 호출
df_daejeon['주소'] = df_daejeon['주소'].apply(get_address)
df_daejeon['위도'] = df_daejeon['주소'].apply(get_yx).str.get(0)
df_daejeon['경도'] = df_daejeon['주소'].apply(get_yx).str.get(1)

# 결측치 삭제
for i in df_daejeon.index: 
    if df_daejeon['주소'][i] == '결과없음':
        df_daejeon = df_daejeon.drop([i])

# 형변환
# df_daejeon = df_daejeon.astype({'급속충전기(대)':'float', '완속충전기(대)':'float', '위도':'float', '경도':'float'})
df_daejeon[['급속충전기(대)', '완속충전기(대)', '위도', '경도']] = df_daejeon[['급속충전기(대)', '완속충전기(대)', '위도', '경도']].astype('float')

df_daejeon.reset_index(inplace=True) # 인덱스 재설정
df_daejeon = df_daejeon.drop(columns=['index'])

################################################################################################
# 지역별 인구 데이터 불러오기
data = pd.read_excel('02_folium\202208_202208_주민등록인구및세대현황_월간.xlsx', header=2).drop(columns=['행정기관코드', '남여 비율'])

# 데이터 전처리
data = data.rename(columns={'세대당 인구':'세대당인구', '남자 인구수':'남자', '여자 인구수':'여자'})
data['시'] = data['행정기관'].str.split().str.get(0)

# 대전광역시 데이터프레임 생성
data_daejeon = data[data['시'] == '대전광역시'] 

data_daejeon['총인구수'] = data_daejeon['총인구수'].str.replace(',', '').astype('int')
data_daejeon['세대수'] = data_daejeon['세대수'].str.replace(',', '').astype('int')
data_daejeon['남자'] = data_daejeon['남자'].str.replace(',', '').astype('int')
data_daejeon['여자'] = data_daejeon['여자'].str.replace(',', '').astype('int')

data_daejeon['시'] = data_daejeon['행정기관'].str.split().str.get(0)
data_daejeon['구'] = data_daejeon['행정기관'].str.split().str.get(1)
data_daejeon['동'] = data_daejeon['행정기관'].str.split().str.get(2)

data_daejeon.dropna(inplace=True)

# 인덱스 리셋, 컬럼 삭제
data_daejeon.reset_index().drop(columns=['index'])

# data_daejeon.구.value_counts()

for i in data_daejeon.index:
    if data_daejeon['동'][i] == '도안동':
        data_daejeon = data_daejeon.drop([i])

################################################################################################
# 행정동 데이터 불러오기
jsonfile = open('02_folium\HangJeongDong_ver20220401.geojson', 'r', encoding='utf-8').read()
jsondata = json.loads(jsonfile)

################################################################################################
# 행정동 데이터 비교 셋
jsondata_daejeon = {'type':'FeatureCollection'}
jsondata_pick = []
jsondata_dong = [] # 어느 동이 선택되었는지 확인하기 위함

for item in jsondata['features']: # features 리스트 값의 딕셔너리들을 하나 하나 가져와서 그 안의 'sidonm'을 찾는다.
    if item['properties']['sidonm'] == '대전광역시':
        dong = item['properties']['adm_nm'].split()[-1].strip()
        item['id'] = dong 
        jsondata_dong.append(dong)
        jsondata_pick.append(item)
        
jsondata_daejeon['features'] = jsondata_pick
##############################################################
# 동 비교
json_dong = sorted(jsondata_dong)
data_dong = sorted(data_daejeon['동'])

len(json_dong), len(data_dong)

for i, item in enumerate(zip(data_dong, json_dong)):
    print(i,item)
###############################################################
# 평균좌표를 중심좌표로 설정
daejeon_loc = [df_daejeon['위도'].mean(), df_daejeon['경도'].mean()]

# 맵 초기화
m = folium.Map(location=daejeon_loc, zoom_start=11)

# 행정동 / 인구수 컬러플레이스
folium.Choropleth(geo_data = jsondata_daejeon,
                  data = data_daejeon, 
                  columns = ['동', '총인구수'],
                  fill_color='OrRd',
                  key_on = 'feature.id').add_to(m)

marker_cluster = MarkerCluster().add_to(m)

# 마커클러스터 찍기
for i in df_daejeon.index:
    folium.Marker([df_daejeon['위도'][i], df_daejeon['경도'][i]],
                  tooltip=df_daejeon['설치장소'][i]).add_to(marker_cluster)
    
m.save('22222222.html')




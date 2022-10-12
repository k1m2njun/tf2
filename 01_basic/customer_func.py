import customer_func1 as cf
from tkinter import N

custlist = [{'name': '길민준1', 'gender': 'M', 'email': 'k1m2njun1@naver.com', 'birthday': '1990'},
            {'name': '길민준2', 'gender': 'M', 'email': 'k1m2njun2@naver.com', 'birthday': '1990'},
            {'name': '길민준3', 'gender': 'M', 'email': 'k1m2njun3@naver.com', 'birthday': '1990'},
            {'name': '길민준4', 'gender': 'M', 'email': 'k1m2njun4@naver.com', 'birthday': '1990'}]
page = len(custlist)-1

while True:
    choice=input('''
    다음 중에서 하실 일을 골라주세요 :
    I - 고객 정보 입력
    C - 현재 고객 정보 조회
    P - 이전 고객 정보 조회
    N - 다음 고객 정보 조회
    U - 고객 정보 수정
    D - 고객 정보 삭제
    Q - 프로그램 종료
    ''').upper()  

    if choice=="I":  
        page = cf.insertData(custlist)
    elif choice=="C": 
        cf.curData(custlist, page)
    elif choice == 'P':
        page = cf.preData(custlist, page)
    elif choice == 'N':
        page = cf.nextData(custlist, page)
    elif choice=='D':
        page = cf.delData(custlist)
    elif choice=="U": 
        cf.updateData(custlist)
    elif choice=="Q":
        break
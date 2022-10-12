import re,sys
import customer_func1 as cf

class Customer:
    def insertData(self): 
        customer={'name':'','gender':'',"email":'',"birthyear":''}
        customer['name']=input("이름을 입력하세요 : ")
        while True:
                customer['gender']=input("성별(M/m 또는 F/f)을 입력하세요 : ")
                customer['gender']=customer['gender'].upper()
                if customer['gender'] in ('M','F'):
                    break

        while True: # 중복되지 않게 입력
            regex = re.compile('^[a-z][a-z0-9]{4,10}@[a-zA-Z]{2,6}[.][a-zA-Z]{2,3}$')
            while True:
                customer['email']=input("이메일을 입력하세요 : ") 
                golbang = regex.search(customer['email'])
                if golbang:
                    break
                else:
                    print('"@"를 포함한 정확한 이메일을 써주세요')
            check=0
            
            for i in self.custlist:
                if i['email']==customer['email']:
                    check=1
            
            if check==0:
                break
            print('중복되는 이메일이 있습니다.')    
        while True:
            customer['birthyear']=input("출생년도 4자리를 입력해주세요 : ")
            
            if len(customer['birthyear']) == 4 and customer['birthyear'].isdigit():
                break
        print(customer)
        self.custlist.append(customer)
        print(self.custlist)
        self.page=len(self.custlist)-1   
        print(self.page)     
# return은 값을 반환하거나 함수를 종료한다.
# 숫자를 제외한 객체는 주소값을 반환한다.
# 주소값은 고유의 위치이므로 굳이 주소값을 반환해 변경될 사항을 보내줄 필요가 없다.
    
########################################################################################
    def curData(self):
        if self.page >= 0:
            print("현재 페이지는 {}쪽 입니다".format(self.page + 1)) 
            print(self.custlist[self.page])
        else:
            print("입력된 정보가 없습니다.")    
    
########################################################################################
    def preData(self):
        if self.page <= 0:
            print('첫 번 째 페이지이므로 이전 페이지 이동이 불가합니다')
            print(self.page)
        else:
            self.page -= 1
            print("현재 페이지는 {}쪽 입니다".format(self.page + 1))
            print(self.custlist[self.page])

########################################################################################
    def nextData(self):
        if self.page >= len(self.custlist)-1:
            print('마지막 페이지이므로 다음 페이지 이동이 불가합니다')
            print(self.page)
        else:
            self.page += 1
            print("현재 페이지는 {}쪽 입니다".format(self.page + 1))
            print(self.custlist[self.page])
        
########################################################################################
    def delData(self):
        choice1 = input('삭제하려는 고객 정보의 이메일을 입력하세요.')
        delok = 0
        for i in range(0,len(self.custlist)):
            if self.custlist[i]['email'] == choice1:
                print('{} 고객님의 정보가 삭제되었습니다.'.format(self.custlist[i]['name']))
                del self.custlist[i]
                print(self.custlist)
                delok = 1
                break
        if delok == 0:
                print('등록되지 않은 이메일입니다.')
                print(self.custlist)

########################################################################################
    def updateData(self):
        while True:
            choice1=input('수정하시려는 고객 정보의 이메일을 입력하세요 : ') 
            idx=-1
            for i in range(0,len(self.custlist)):
                if self.custlist[i]['email'] == choice1:
                    idx=i
                    break
            if idx==-1:
                print('등록되지 않은 이메일입니다.')       
                break
                        
            choice2=input('''
            다음 중 수정하실 정보를 골라주세요 
                    name, gender, birthyear
            (수정할 정보가 없으면 'exit' 입력)
            ''')
            if choice2 in ('name','gender','birthyear'):
                self.custlist[idx][choice2]=input('수정할 {}을 입력하세요 :'.format(choice2))
                break
            elif choice2 =='exit':
                break
            else:
                print('존재하지 않는 정보입니다.')
                break
        
########################################################################################

    def exe(self):
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
            self.insertData()
        elif choice=="C": 
            self.curData()
        elif choice == 'P':
            self.preData()
        elif choice == 'N':
            self.nextData()
        elif choice=='D':
            self.delData()
        elif choice=="U": 
            self.updateData()
        elif choice=="Q":
            print('프로그램을 종료합니다.')
            sys.exit()

    def __init__(self): # 여기에 변수를 따로 선언한 이유(인스턴트 변수)는,
        # 밖에 클래스변수로 넣는 경우 클래스 당 1개의 데이터를 가지고 있기 때문이다.
        self.custlist = [{'name': 'hong1', 'gender': 'M', 'email': 'hong1@gamil.com', 'birthday': '2000'},
            {'name': 'hong2', 'gender': 'M', 'email': 'hong2@gamil.com', 'birthday': '2000'},
            {'name': 'hong3', 'gender': 'M', 'email': 'hong3@gamil.com', 'birthday': '2000'},
            {'name': 'hong4', 'gender': 'M', 'email': 'hong4@gamil.com', 'birthday': '2000'}]
        self.page=3
        while True:
            self.exe()



Customer()
# init 안에 while 문으로 exe를 계속 호출한다.
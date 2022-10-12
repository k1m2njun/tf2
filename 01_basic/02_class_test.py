class Calculator: # 값과 함수(메소드)로 구성되어있다.
    sum = 100
    def __init__(self): # self는 자신의 주소값을 받는다.
        self.result = 0 # self.변수 = 인스턴스변수 : 객체별로 자기 값을 자기가 가지고 있음
        # init은 처음 객체를 생성할 때 자동 호출되어 초기화하는 함수이다.
        
    def add(self, num): # num은 지역변수
        self.result += num
        return self.result

cal1 = Calculator()
cal2 = Calculator()
# 변수에는 실제 만들어진 객체가 어디있는지 그 주소가 들어가있다.
cal1.result=2
cal2.result=9

print(cal1.result) #2
print(cal2.result) #9
# print(Calculator.sum) #100
# Calculator.sum = 200 # 클래스변수, 클래스 당 하나만 정할 수 있다.
# print(cal1.sum) #200
# print(cal2.sum) #200

# cal1.add(3)
# cal1.add(4)
# print(cal1.result) #7
# print(cal2.result) # 초기값 0

# # 상속
# class FourCal(Calculator):
#     def sub(self, num):
#         self.result -= num
#         return self.result

# cal3 = FourCal()
# cal4 = FourCal()

# cal3.add(5)
# cal3.sub(3)
# print(cal3.result) # 클래스를 상속받아 사용했다.
# # 
from datetime import datetime

now = datetime.now()

f = open('test' + str(now.strftime('%Y_%m_%d %H_%M_%S')) + '.txt', 'a')

f.write(str(datetime.now().strftime('%Y_%m_%d %H_%M_%S')) + " 1st\n")
f.write(str(datetime.now().strftime('%Y_%m_%d %H_%M_%S')) + " 2nd\n")

print(now) # 시작시간
print(datetime.now() - now) # 끝나는 시간

f.close()
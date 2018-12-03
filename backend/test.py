import random, string
import base64

def randomword():
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(8))

a = randomword()
print('ini hasil random',a)

def stringToBase64(s):
    return base64.b64encode(s.encode('utf-8'))

def base64ToString(b):
    return base64.b64decode(b).decode('utf-8')

b = str(stringToBase64(a))
c = base64ToString('c2VibGFrOTk=')
length = len(b) -1
print(b)
print(length)
d = b[2:length]
print(d)
print(c)

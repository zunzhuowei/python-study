def check_int(str):
    try:
        int(str)
        return True
    except:
        return False

s= "dd+1"
a = s.split('+',1)
print(a[0])
print(a[1])
print(check_int(a[0]))
print(check_int(a[1]))
# print(isinstance(int(a[0]),(int)))
# print(isinstance(a[1],(int)))



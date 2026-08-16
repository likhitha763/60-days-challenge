marks=int(input("Enter your marks: "))
if 100>=marks>90:
    print("A")
elif 90>=marks>75:
    print("B")
elif 75>=marks>50:
    print("C")
elif 50>=marks>=0:
    print("Fail")
else:
    print("Invalid marks")
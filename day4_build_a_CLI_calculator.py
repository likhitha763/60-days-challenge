a = int(input("Enter the first number"))
b = int(input("Enter the second number"))
op = input("Enter the operation (+, -, *, /): ")
if op == "+":
    print(a + b)
elif op == "-":
    print(a - b)
elif op == "*":
    print(a * b)
elif op == "/":
    if b == 0:
        print("Error: Division by zero is not allowed.")
    else:
        print(a / b)
else:
    print("Invalid Operator")
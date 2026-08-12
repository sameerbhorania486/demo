# mini calculator project

def add(a,b):
    return a + b
    
def substract(a,b):
    return a - b
    
def multiply(a,b):
    return a * b
    
def divide(a,b):
    if b == 0:
        return "can't divide by zero"
    return a / b
    
def calculator(num1,num2,operation):
    if operation == "add":
        return add (num1,num2)
    elif operation == "substract":
        return substract (num1,num2)
    elif operation == "multiply":
        return multiply (num1,num2)
    elif operation == "divide":
        return divide (num1,num2)
    else:
        return "invalid operation"
        
print(calculator(20,5,"add"))
print(calculator(20,5,"substract"))
print(calculator(20,5,"multiply"))
print(calculator(20,5,"divide"))
with open ("myfile.txt","a") as file:
    file.write("\nHello, sameer is here...")
    file.write("\nwhat's up guyz...")
    file.write("\nhow are you?")

with open ("myfile.txt","r")as file:
    content = file.read()
    print(content)
    
with open ("myfile.txt","w") as file:
    file.write("fresh start!")
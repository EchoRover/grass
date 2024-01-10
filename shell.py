
from grass import run

print("Grass 0.0.1")


#-1-

while True:
    text = input("grass > ")
    if text == "q":
        break
    print(run(text,"<shell>"))

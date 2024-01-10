
from grass import run

print("Grass 0.0.1")


print(run("1/0","test"))
quit()

while True:
    text = input("grass > ")
    if text == "q":
        break
    print(run(text,"<shell>"))

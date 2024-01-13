
from grass import run

print("Grass 0.0.5")


#-1-
print(run("VAR result = 1","<shell>"))
print(run("WHILE result < 10 THEN VAR result = result + 1  ","<shell>"))

print(run("result","<shell>"))

# quit()

while True:
    text = input("grass > ")
    if text == "q" or text == "/usr/local/bin/python3 /Users/Shared/A/coding/grass/shell.py":
        break
    result = run(text,"<shell>")
    if result:
        print(result)

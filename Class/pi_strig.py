from pathlib import Path

# path = Path('pi_digits.txt')
path = Path('pi_million_digits.txt')
contents = path.read_text()

lines = contents.splitlines()
pi_string = ''
for line in lines:
    pi_string += line.lstrip()

# print(pi_string)
print(f"{pi_string[:52]}...")
print(len(pi_string))

birthday = input("Enter your birthday, in the form yymmdd: ") 
if birthday in pi_string:
    print("있어!")
else:
    print("100만개에는 없네.")
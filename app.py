print("Changpagne")

print(' o-----')
print(' ||||')

print('*' * 10)


price=10
price=20

print(price)

social=input('What is your social')
print('thank you'+social)

favorite_city=input('what is your favorite city')
print(social+'likes'+favorite_city)

birth_year=input('Birth year: ')

print(type(birth_year))
age=2019-birth_year
print(type(age))
print(age)



weight_lbs=input('weight lbs:')
weight_kgs=weight_lbs*.45
print(weight_kg)


course='Python for beginners'
another=course[:]
print(another)
print(course[-1])
print(course[-2])


print(course[0:3])
print(course[:5])

print(course[1:])

name='Hefner'
print(name[1:-1])

first='angie'
last='shanghai'
message=first+'['+last+'] is a code'
msg=f'{first}  [{last}] is a coder'
print(message)

print(msg)





course='Python for Beginners'

print(len(course))

course=course.upper()


print(course)

print(course.find('BEGINN'))

print(course.replace('BEGINNERS','absolute'))


print('PYTHON' in course)

print(10//3)
print(10**3)
x=3
print(++x)
print(x)

import math

print(math.ceil(2.9))
x=2.9
print(round(x))


print(abs(-2.9))

swimming_pools=False
is_cold=True

if swimming_pools:
    print("pass out")
    print("Drank")
elif is_cold:
    print("sub zero")
else:
    print("now open your mind and listen me kendrick")

    price = 1000000
    has_good_credit = True

    if has_good_credit:
        down_payment = .1 * price

    else:
        down_payment = .2 * price

    print(f"Down Payment: ${down_payment}")

    has_high_income = True

    has_good_credit = False

    isnot_badass = False

    if has_high_income or has_good_credit:
        print("eligible")
    elif not isnot_badass:
        print("eligible because savage")

temperature=666

if temperature!=30:
    print("it's sunny")

else:
    print("not sunny")

    name = "Kjhdnfjsknfjdfnskdnfkdsnfksdnfdsfjkdnsjfnkds"

    if len(name) < 3:
        print("name too short")

    elif len(name) > 50:
        print("name too long")
i=1
while i<=5:
    print('*'*i)
    i+=1
print("Done")

secret_answer=412
guess_count=0
guess_limit=3
while guess_count<guess_limit:
    guess=int(input('Guess:'))
    guess_count+=1
    if guess==secret_answer:
        print("you won")
        break
else:
    print('wrong')

    command = ""

    started = False

    while True:
        command = input("> ").lower()
        if command == "start":
            if started:
                print("car already started, no need to toggle")

            elif not started:
                started = True;
                print("start")
        elif command == "stop":
            if not started:
                print("car already stopped")
            else:
                started = False
                print("stop")
        elif command == "quit":
            break
        elif command == "help":
            print("""
            start-to start
            stop-to stop
            quit-to quit

            """)
        else:
            print("sorry i can't understand your accent")

for item in range(4, 9, 2):
    print(item)
prices=[10,20,30]
total=0
for pri in prices:
    total+=pri


print(f"Total:{total}")


for x in range(4):
    for y in range(7):
     print(f'({x},{y})')



numbers=[5,2,5,2,2]

for x in numbers:
    result=''
    for j in range(x):
        result+='x'
    print(result)

names=['A','Gie','Changpagne']
print(names[-1])
names[0]='-A'
print(names[2:])
print(names)

numbers=[3,6,4,2,10]

max=numbers[0]
for number in numbers:
    if number>max:
        max=number


print(max)

matrix=[[1,2,3],
        [4,5,6],
        [7,8,9]]




matrix[0][1]=20

print(matrix)


for row in matrix:
    for element in row:
        print(element)

numbers=[5,2,7,3,7,2,1,4,2]
print(numbers)

numbers.insert(4,20)
print(numbers)

numbers.remove(2)

print(numbers)


numbers.pop()

print(numbers)

print(50 in numbers)

print(numbers.count(2))


print(numbers.sort())
print(numbers)


print(numbers.copy())
numbers2=numbers.copy()
print(numbers2)


liss=[2,1,3,1,4,1,2,3]

for e in liss:
    count=liss.count(e)
    while count>1:
        liss.remove(e)
        count=liss.count(e)
liss.sort()
print(liss)


numbers=(1,2,3)


coordinates=(1,2,3)

x,y,z=coordinates

print(x)


customer={



    "name":"John Smith",
    "age":30,
    "is_verified":True

}

customer["name"]="Smithsonian"
customer["agency"]="Next Management"
print(customer.get("is_verified"))
print(customer.get("agency"))
print(customer.get("birthday","Jan 1, 1980"))

phone=input("Phone: ")
digits_mapping={
    "1": "One",
    "2": "Two",
    "3": "Three",
    "4": "Four"

}
output=""
for ch in phone:
    output+=digits_mapping.get(ch,"!")

print(output)







def greet_user(firstname,lastname):
    print(f'Hi there {firstname} {lastname}!')
    print('Welcome to location')


print("Start, what is your first and last name")
greet_user(firstname=input(),lastname=input())
print("Finished")


def square(number):
    return (number*number)




print(square(5))


def emoji_converter(message):
    words = message.split(' ')
    emojis = {
        ":):": ":)",
        ":(": ":("
    }
    output = ""
    for word in words:
        output += emojis.get(word, word) + " "
    return output



message=input(">")
print(emoji_converter(message))


try:
    age=int(input('Age: '))
    income=100000
    risk=income/age
    print(age)
except ZeroDivisionError:
    print('Minimum age of 10 to have income')
except ValueError:
    print('Invalid Values')


#reminder
#of a commentator
print("flight")


class Point:
    def __init__(self,x,y):
        self.x=x
        self.y=y
    def move(self):
        print("move")

    def draw(self):
        print("draw")



point1=Point(5,60)
point1.draw()

point1.x=10
point1.y=20
print(point1.x)
point1.draw()

point2=Point(23,12)
point2.x=1
print(point2.x)


class Person:
    def __init__(self,name):
        self.name=name


    def talk(self):
        print(f"Hello, I am {self.name}")



john=Person("Michael Well Made It")
print(john.name)
john.talk()



class Mammal:
    def walk(self):
        print("Walk")


class Dog(Mammal):
    def bark(self):
        print("arf")


class Cat(Mammal):
    def be_annoying(self):
        print("annoying")


dog1=Dog()
dog1.walk()
dog1.bark()


cat1=Cat()
cat1.be_annoying()
cat1.walk()



import converters
from converters import lbs_to_kg

print(converters.kg_to_lbs(50))
print(converters.lbs_to_kg(110))



from util import find_max

numbers=[10,3,6,1]
maxim=find_max(numbers)
print(maxim)



from ecommerce.shipping import calc_shipping




import random


members=['John','Drogon','Khaleesi', 'Vittoria', 'Eve','Iver']
leader=random.choice(members)
print(leader)
for i in range(10):
    print(random.random())



import random


class Dice:
    def roll(self):
        first=random.randint(1,6)
        second=random.randint(1,6)
        return first,second



d1=Dice()
print(d1.roll())



def find_max(numbers):
    maxim=numbers[0]
    #for number in numbers:
        #if number>maxim:
           # max=number

    return max(numbers)




from pathlib import Path


#Absolute path
#relative path

path=Path()
print(path.exists)
for file in path.glob('*.py'):
    print(file)
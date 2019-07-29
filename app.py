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
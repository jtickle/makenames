#!/usr/bin/env /usr/bin/python
import argparse
import random
import re
from usgovdata import lastNames, maleFirstNames, femaleFirstNames

genderNames = {
        'M': maleFirstNames,
        'F': femaleFirstNames
}

# Given a list, selects a random item by Gamma distribution
def selectRandomGamma(vals): return vals[clampGamma(len(vals))]

# I failed statistics several times so instead of doing it right, we just throw
# away values that are too big for the given list.
def clampGamma(max):
    val=max+1
    while val >= max:
        val = int(random.gammavariate(1,125))
    return val

# Shortcut to get the last name using Gamma distribution
def getLastName():
    return selectRandomGamma(lastNames)

# Shortcut to get the first/middle name using Gamma distribution
def getGenderName(gender):
    return selectRandomGamma(genderNames[gender])

# Makes a name for given gender
def makename(gender):
    last = getLastName()
    if(random.randint(0,9) == 3):
        last += '-' + getLastName()

    middle = getGenderName(gender)
    if(random.randint(0,20) == 10):
        middle += ' ' + getGenderName(gender)
    
    return { 'first':  getGenderName(gender)
           , 'middle': middle
           , 'last':   last
           , 'gender': gender
           }

def getGender(wantMale, wantFemale):
    if wantMale and wantFemale:
        return random.choice(dict.keys(genderNames))
    elif wantMale:
        return 'M'
    elif wantFemale:
        return 'F'

def makenames(count, wantMale, wantFemale):
    return [makename(getGender(wantMale, wantFemale)) for i in range(count)]

usernames = {}

def ASUUsernameFormatter(person):
    # Generate in format LastFM, but lowercase
    username = ("%s%s%s" % (person['last'], person['first'][0],
            person['middle'][0])).lower()

    # Remove hyphens
    username = re.sub('-', '', username)

    # Occasionally, remove all vowels
    if(random.randint(0,99) == 69):
        username = re.sub('[aeiou]', '', username)

    # If we have generated this one before, stick sequence number on the end
    if username in usernames.keys():
        usernames[username] += 1
        username = username + str(usernames[username])
    else:
        usernames[username] = 0

    return username

def ASUEmailFormatter(username):
    return (username + '@appstate.edu').lower()

ids = []

def ASUBannerIdGenerator():
    while True:
        id = random.randint(900000000,900999999)
        if id not in ids:
            break

    ids.append(id)
    return id

def makestudents(count, wantMale, wantFemale,
        idgen=lambda:random.randint(0,2000000000),
        emailformat=lambda x: x,
        usernameformat=lambda x: x['first']+x['last']):
    students = []
    for i in range(count):
        gender = getGender(wantMale, wantFemale)
        student = makename(gender)
        student['gender'] = gender
        student['id'] = idgen()
        student['username'] = usernameformat(student)
        student['email'] = emailformat(student['username'])
        students.append(student)

    return students

parser = argparse.ArgumentParser(description='Generate random English names.')
parser.add_argument('number', help='How many names', type=int)
parser.add_argument('-m', '--male', help='Only male names', action='store_true')
parser.add_argument('-f', '--female', help='Only female names', action='store_true')

args = parser.parse_args()

if not args.male and not args.female:
    args.male = args.female = True

for person in makestudents(args.number, args.male, args.female,
        idgen=ASUBannerIdGenerator,
        emailformat=ASUEmailFormatter,
        usernameformat=ASUUsernameFormatter):
    print "%(id)d,%(gender)s,%(username)s,%(email)s,%(first)s,%(middle)s,%(last)s" % person

from Customer import Customer
from random import *
from datetime import *

def generateNameList():
    x = open('names.txt', 'r')
    l = [line.strip() for line in x]
    x.close()
    return l

def formatList(list):
    #take in a list, and return it correctly formatted: "____" or "____, ____"
    if len(list) == 2:
        list = "\"{}, {}\"".format(list[0],list[1])
    else: 
        list = "\"{}\"".format(list[0])
    return list

def randDate(start = None, end = None, years = 1):
    """
    Given a start and end date as datetime.datetime objects, find a random date between the two dates.
    """
    formatter = "%m/%d/%Y"
    # if no start is provided, set it to this current date
    if start is None:
        start = datetime.now()

    # if no end is provided, set it to be one year after start
    if end is None:
        end = start + timedelta(days = 365 *years)

    difference = end-start
    #random second between two dates
    randomSecond = randint(0,(difference.days * 24 * 60 * 60 + difference.seconds)+1)
    #return time in specified format
    return start + timedelta(seconds=randomSecond)
 
def writeFile(numRecords, yearSpan):
    file = open("sampleRecords.csv", 'w')
    file.write('Delivery Date,Organization Name / Name,Class Year,Phone,Email,Beverage,Quantity,Price,Total Revenue\n')
    startingMonth = str(randint(1,6))
    sampleCustomers = []

    #list of names
    names = generateNameList()
    #length of list of names
    length = len(names)

    for x in range(numRecords):
        ### NAME
        #pick a random first and last name
        randFirstName = names[randint(0,length-1)]
        randLastName = names[randint(0,length-1)]
        name = randFirstName + ' ' + randLastName

        ### YEAR
        currYear = datetime.today().year
        year = randint(currYear, currYear+4)

        ### PHONE NUMBER
        #create a random phone number
        phoneNum = str(randint(10000000000,19999999999))[1:]
        phoneNum = phoneNum[0:3] + '-' + phoneNum[3:6] + '-' + phoneNum[6:]


        ### EMAIL
        email = randFirstName[0].lower() + randLastName.lower() + '@gmail.com'


        ### DELIVERY DATE
        #create a random delivery date
        deliveryDate = randDate(years = yearSpan)
        #format deliveryDate correctly
        deliveryDate = deliveryDate.strftime("%m/%d/%Y")


        ### BEVERAGES
        #create a list of beverage(s)
        decision = randint(0,1)
        choices = ['Duke Juice', 'Mango Lime']
        beverages = []
        #pick a random juice
        rand = randint(0,len(choices)-1)
        #add that juice to the list first
        beverages.append(choices[rand])
        if decision == 1:
            #add whichever juice remains
            beverages.append(choices[not(rand)])
        formattedBeverages = formatList(beverages)
        
        
        ### QUANTITIES
        #create quantities. make as many quantities as you have beverages
        quantities = []
        for x in range(len(beverages)):
            quantity = randint(1,40)
            quantities.append(str(quantity))
        formattedQuantities = formatList(quantities)


        ### PRICES
        #generate price based on quantity
        price = 0
        for x in range(len(quantities)):
            price += int(quantities[x])
        price *= 3.75 if price < 5 else 3.50


        newCustomer = Customer(name, year, phoneNum, email, deliveryDate, formattedBeverages, formattedQuantities, price)
        sampleCustomers.append(newCustomer)
    
    sampleCustomers.sort(key = lambda x : datetime.strptime(x.deliveryDate, "%m/%d/%Y"))

    for customer in sampleCustomers:
        file.write("{},{},{},{},{},{},{},${},\n".format(customer.deliveryDate,customer.name,customer.year,customer.phone,customer.email,customer.beverages,customer.quantities,customer.price))

def help():
    return """
   Please enter a positive number of sample records to produce...
        python3 generateSampleCustomers.py -n 35
"""


if __name__ == "__main__":
    from sys import argv
    import textwrap
    import argparse

    # ALLOW FOR ARGUMENT PARSING 
    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, description='Generate n sample customers of Duke Beverages.', epilog = textwrap.dedent(help()))
    parser.add_argument('-n', type=int, action='store', dest='numRecords', help="Number of sample customers to be created. Default = 35", default = 35)
    parser.add_argument('-y','--years', type=int, action='store', dest='years', help="Number of years over which the records should span from current date. Default = 1. Max = 10", default=1)
    args = parser.parse_args()

    if args.years > 10:
        parser.print_help()
        quit()
        
    if args.numRecords == 1:
        print("Generating {} sample record...".format(args.numRecords))
    else:
        print("Generating {} sample records...".format(args.numRecords))

    writeFile(args.numRecords, args.years)
        
        

#(c) 2019 nathan thimothe
from Customer import *
from datetime import *
from dateutil.relativedelta import relativedelta
from collections import OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import csv



def _populate(x):
    """
    Populate a list of Customers based on a csv file. 
    """
    result = []
    f = open(x)
    count = 0
    for row in csv.reader(f):
        if count == 0:
            count+=1
            continue
        deliveryDate = row[0].strip()
        name = row[1].strip()
        phone = row[2].strip()
        email = row[3].strip()
        #list comprehension to remove whitespace of each element in list
        beverages = [juice.strip() for juice in row[4].split(",")]
        quantity = [amount.strip() for amount in row[5].split(",")]
        price = row[6].strip()
        customer = Customer(name,phone,email,deliveryDate,beverages,quantity,price)
        result.append(customer)
    f.close()
    return result

def _rename(x, year=None): # x is an int 
    """
    monthMap is a dictionary of key - numericalMonth , V - stringMonth 
    """
    monthMap= {
        1:"Jan",
        2:"Feb",
        3:"Mar",
        4:"Apr",
        5:"May",
        6:"Jun",
        7:"Jul",
        8:"Aug",
        9:"Sep",
        10:"Oct",
        11:"Nov",
        12:"Dec"
        }
    return monthMap.get(x)

def _numYears(dictionary):
    # get the first key in the dictionary (e.g. Jan '20)
    first = list(dictionary.keys())[0]
    last = list(dictionary.keys())[-1]
    # split the key by space (e.g. ['Jan', ''20']), get the last element (e,g, ''20'), and ignore the apostrophe (e.g '20')
    sYear = int(first.split()[-1][1:])
    eYear = int(last.split()[-1][1:])
    return eYear - sYear

def _numRecords(x):
    f = open(x, 'r')
    count = 0
    for x in f:
        count += 1
    f.close()
    return count-1

def _find(value, id): 
    """
    Find a certain string key (id) in a tuple of two dictionaries, and return that dictionary so that 
    it may be modified # e.g. ({id: value}, {id:value}),
    >>> find( ({'id': 30}, {'id1':45}) , 'id1')
    45
    """
    for dict in value:
        if dict.__contains__(id):
            return dict

def _retValues(iterable, id):
    """
    Traverses a list of dictionaries and finds all dicionaries that contain a certain key.
    """
    return [each[id] for each in iterable]

def _createDict(start, end):
    dictionary = OrderedDict()
    assert end >= start, "end date before start date"

    startMonth = start.month
    currDate = start
    months = ((end.year - start.year) * 12) + (end.month - start.month)
    # iterate months+1 times for start (inclsuive) through end (inclusive)
    for month in range(months+1):
        # get the numerical month
        nMonth = (startMonth + month) % 12
        if nMonth == 0: nMonth += 12
        # ex dict key: "Jul '20"
        dictionary[_rename(nMonth) + " '" + str(currDate.year%100)] = {'dj': 0, 'ml': 0}
        # advance current date by one month
        currDate += relativedelta(months = 1)

    return dictionary
    
def _updateDict(dictionary, key, id, addedValue):
    dictionary[key][id] += addedValue
        

def collectData(x):
    months = []
    customers = _populate(x) #list of customers
    #dictionary where the month is the key and the value is a tuple of dictionaries of DJ and ML quantities. 
    #create a from the least recent to the most recent date of customer purchases
    counts = _createDict(datetime.strptime(customers[0].deliveryDate, "%m/%d/%Y"), datetime.strptime(customers[-1].deliveryDate, "%m/%d/%Y"))

    for customer in customers:
        # 1) GET THE MONTH FROM THE APPROPRIATE SECTION OF CUSTOMER CLASS
        date = datetime.strptime(customer.deliveryDate, "%m/%d/%Y")

        #the month is the first element
        month = _rename(int(date.month)) + " '" + str(date.year%100)
        

        # 2) BUILD THE DICTIONARY
        #the order of the beverages reflects the order of the quantity of the drinks
        beverages = customer.beverages
        quantity = customer.quantities
        #if the first item in the beverages section says "Duke Juice", make the dictionary reflect that there are x duke juices
        if beverages[0] == "Duke Juice":
            # example dict: {month : {djq: 1, mlq:x} }
            _updateDict(counts, month, 'dj', int(quantity[0]))
        else:
            _updateDict(counts, month, 'ml', int(quantity[0]))
        try:
            if beverages[1] == "Duke Juice":
                _updateDict(counts, month, 'dj', int(quantity[1]))
            else:
                _updateDict(counts, month, 'ml', int(quantity[1]))
        except:
            pass

    return counts

def _checkYearCount(nYears):
    if nYears > 10:
        print("Exceeded year count.")
        quit()

def determineGraphSize(nRecords, nYears):
    # the more years included, the wider the graph should be
    # the more records included, the taller the graph should be    
    MIN_GRAPH_WIDTH = 15
    MAX_GRAPH_WIDTH = 150

    MIN_GRAPH_HEIGHT = 8
    MAX_GRAPH_HEIGHT = 50

    if nYears * 15 <= MIN_GRAPH_WIDTH:
        width = MIN_GRAPH_WIDTH
    elif nYears * 15 >= MAX_GRAPH_WIDTH:
        width = MAX_GRAPH_WIDTH
    else:
        width = nYears * 15

    if nRecords * 0.2 <= MIN_GRAPH_HEIGHT:
        height = MIN_GRAPH_HEIGHT
    elif nRecords * 0.2 >= MAX_GRAPH_HEIGHT:
        height = MAX_GRAPH_HEIGHT
    else:
        height = nRecords * 0.2
    
    return width, height

def graphCreation(x, graph = 'bar'):
    counts = collectData(x)
    print(counts)


    # CREATE GRAPH    
    months = list(counts.keys())
    monthlyDJ = _retValues(counts.values(),'dj')
    monthlyML = _retValues(counts.values(),'ml')
    # SIZE OF GRAPH
    nRecords = _numRecords(x)
    nYears = _numYears(counts)
    print("nRecords:{}\nnYears:{}\n".format(nRecords, nYears))

    _checkYearCount(nYears)

    width, height = determineGraphSize(nRecords, nYears)
    print("width:{}\nheight:{}".format(width, height))
    plt.figure(figsize=(width,height))
    # TITLE, X LABEL, Y LABEL
    plt.title("Duke Beverages Sales Per Month",fontweight = 'bold', fontsize = 18)
    plt.xlabel("Months", fontweight = 'bold', fontsize = 12)
    plt.ylabel("Number of Sales", fontweight = 'bold', fontsize = 12)


    # TYPE OF GRAPH
    if graph.strip() == 'bar':
        barWidth = 0.25
        #setting positions of bars
        bar1 = np.arange(len(months))
        bar2 = [x+barWidth for x in bar1]
        #plotting bars
        plt.bar(bar1,monthlyDJ,width = barWidth, color = 'b', label = 'Duke Juice' )
        plt.bar(bar2,monthlyML,width = barWidth, color = 'C1', label = 'Mango Lime')
        #set the x ticks
        plt.xticks([x + (barWidth/2) for x in range(len(bar1))], months)
    elif graph.strip() == 'line':
        plt.plot(months,monthlyDJ,'b', label = 'Duke Juice')
        plt.plot(months,monthlyML,'C1', label = 'Mango Lime')
    elif graph.strip() == 'lineX':
        plt.plot(months,monthlyDJ, 'xb-', label = 'Duke Juice')
        plt.plot(months,monthlyML, 'xC1-', label = 'Mango Lime')
    elif graph.strip() == 'line.':
        plt.scatter(months,monthlyDJ, color = 'b')
        plt.plot(months,monthlyDJ,color = 'b', label = 'Duke Juice')
        plt.scatter(months,monthlyML, color = 'C1')
        plt.plot(months,monthlyML, color = 'C1', label = 'Mango Lime')
    plt.legend()
    
    plt.savefig("MonthlySales.pdf")
    return counts

def help():
    return """
Run the program as follows:
      python3 CustomerStatistics.py line. sampleRecords.csv
"""

if __name__ == "__main__":
    import argparse
    import textwrap
    from sys import argv
    
    # ALLOW FOR ARGUMENT PARSING 
    parser = argparse.ArgumentParser(formatter_class = argparse.RawDescriptionHelpFormatter, description='Generate a graph describing sales per month for n sample records.', epilog = textwrap.dedent(help()))
    parser.add_argument('-t','--type', type=str, action='store', dest='type', help="Type of graph to create...options include: 'line.', 'lineX', 'line', 'bar' (default).", default = 'bar')
    parser.add_argument('-f','--file', type=str, action='store', dest='filename', help="CSV file that contains n sample records that will be parsed by this program. sampleRecords.csv (default).", default = 'sampleRecords.csv')
    args = parser.parse_args()
    
    graphCreation(args.filename.lower(), args.type.lower())
    

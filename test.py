
def average(values):
    """Computes the arithmetic mean of a list of numbers.
    >>> print average([20, 30, 70])
    40.0
    """
    return sum(values, 0.0) / len(values)

import doctest
doctest.testmod()
# automatically validate the embedded tests


import csv
with open('example.csv', 'r') as csvfile:
    spamreader = csv.reader(csvfile)
    for row in spamreader:
        print row

# This file contains some common util methods used in the project.


'''
Python does not have enum. This method supports automatic enumeration.
Usage example:
>>> Numbers = enum('ZERO', 'ONE', 'TWO')
>>> Numbers.ZERO
0
>>> Numbers.reverse_mapping[0]
'ZERO'
'''
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    reverse = dict((value, key) for key, value in enums.iteritems())
    enums['reverse_mapping'] = reverse
    return type('Enum', (), enums)

import re
txt = 'The rain in Spain'
x = re.findall('[a-c]', txt) #find all char from a to c
print(x) # outputs ['a','a']

x = re.search('a', txt) # match occurence of a
print(x.start()) # output 5 (first occurence index)

x = re.search('\s', txt) # match whitespace occurence
print(x.start()) # "T-h-e- " 0-1-2-3: The output is 3

x = re.search('b', txt) # match 'b' occurence
print(x) # No 'b' in txt, output (return value) None, x is not <Match> object
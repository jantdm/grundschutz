import os, sys, re, copy

fn = 'IT-GSK-13-EL-en-all_v940-2.md'

f = open(fn,"rt")
f.read(1)

headingRegex = "^# T [0-9]{1,3}"
headingRegexComp = re.compile(headingRegex)

exampleRegex = "^## Example(|s):"
exampleRegexComp = re.compile(exampleRegex)

# ueberschrift -> (example) ueberschrift
# example -> uebershrift

counter = 0
stateHeading = 1
stateExample = 2
state = -1

resultlist = []
result = None

template = {"heading" : "", "description" : "", "examples" : ""}

for line in f:

    counter += 1

    if headingRegexComp.match(line):

        if result:
            resultlist.append(result)
            print(result)

        result = copy.deepcopy(template)

        print("Head!")
        result["heading"] = line.strip()
        state = stateHeading

    elif state == stateHeading and not exampleRegexComp.match(line):
        print("Body!")
        result["description"]+=line ### 1

    elif state == stateHeading and exampleRegexComp.match(line):
        state = stateExample ### 2
        print("Start Example!")

    elif state == stateExample:
        if not headingRegexComp.match(line):
            print("Example!")
            result["examples"]+=line
        else:
            print("Error in line %i!" % counter)
            exit()

    else:
        print("Fatal Error") ### 3 Was not reachable
        exit()

#pip install xlsxwriter

# import xlsxwriter

# workbook = xlsxwriter.Workbook('out.xlsx')
# worksheet = workbook.add_worksheet()

# row = 0
# col = 0

# for r in resultlist:
#     worksheet.write(row,col,r["heading"])
#     worksheet.write(row,col+1,r["description"])
#     worksheet.write(row,col+2,r["examples"])
#     row+=1

# workbook.close()

import json

with open('out.json', 'w') as outfile:
    json.dump(resultlist, outfile)
# Aung Kaung Khant, Kenny Wu
#2.1
import re,sys
from collections import OrderedDict 


stack = []

OPERATORS = OrderedDict([ \
    ['+', lambda a, b: int(a) + int(b)], \
    ['-', lambda a, b: int(a) - int(b)], \
    ['*', lambda a, b: int(a) * int(b)], \
    ['/', lambda a, b: int(a) / int(b)], \
    ])


SYM = r'[+\-\(\)\/*]'

#easiet within the 3 segments
def gettype(i):
    identifier = "([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*"
    num = "[0-9]+"
    symbol = r'\+|\-|\*|\(|\)|\/|:=|\;'
    keyword = "if|then|else|endif|while|do|endwhile|skip"
    if re.match(identifier, i):
        return 'IDENTIFIER'
    elif re.match(num, i):
        return 'NUMBER'
    elif re.match(symbol, i):
        return 'SYMBOL'
    else:
        return 'KEYWORD'


def findpos(s, line):
    inbrackets=0
    j=-1
    for i in line:
        j+=1
        if i == '(':
            inbrackets+=1
        elif i == ')':
            inbrackets-=1
        elif inbrackets!=0: # so this is going to search for the enclosed brackets. If inbrackets != 0 then, it is going to search for it til it does
            continue # so when the input is 3*(..)it prints out * first even though it is at last in precedence. For symbols like +-/ it never goes beyond this point
        elif i == s:
            return j
    return -1

def asttree(line, tabs=0): 
    #grammar is defined top-down 
    #but actual ast tree construction happens bottom-up
    tabulation = '\t'*tabs
    if line == []:
        return
    if len(line) == 1: # only one token in token list. 
        #And this is used when creating ast tree for 3. This is going to work after every +-/*. for the numbers.
        print(tabulation+line[0]+' : ' +gettype(line[0]))
        stack.append(line[0])#
        #evaluator(stack)
        return
    try:
        if line[0] == '(' and line[-1] ==')': #case for if it starts with (). And this is used when creating the tree for inside the brackets
            asttree(line[1:-1], tabs)
            return
    except IndexError as IE:
        print(line)
        sys.exit()
    symbols='+-/*'
    for s in symbols: # here we have implicitly established precedence rules. In terms of plotting, first come first plotted on tree. However, in terms of execution, last come first executed.
        pos = findpos(s, line) # we are going to first match with + in s for every stack.
        if pos != -1:
            print(tabulation+s+' : SYMBOL')#  \t \t + : SYMBOL. This is string concatenation, the +'s.
            stack.append(s)
            asttree(line[:pos],tabs=tabs+1)   # recurse on line before pos
            asttree(line[pos+1:],tabs=tabs+1) # on line after pos
            return


def evaluator(stack1):
    operations="*/-+"
    for i in reversed(range(len(stack1))):
        if stack1[i] in operations:
            if stack1[i] == '/':
                result=int(stack1[i+1])/int(stack1[i+2])
                for count in range(3):
                    stack1.pop(i)
                stack1.insert(i,int(result))

            if stack1[i] == '-':
                result=int(stack1[i+1])-int(stack1[i+2])
                for count in range(3):
                    stack1.pop(i)
                stack1.insert(i,int(result))

            if stack1[i] == '+':
                result=int(stack1[i+1])+int(stack1[i+2])
                for count in range(3):
                    stack1.pop(i)
                stack1.insert(i,int(result))

            if stack1[i] == '*':
                result=int(stack1[i+1])*int(stack1[i+2])
                for count in range(3):
                    stack1.pop(i)
                stack1.insert(i,int(result))

    return stack1


PAT=r'[0-9]+|[a-zA-Z][a-zA-Z0-9]*|[+\-\(\)/*\;]|:=|[if|then|else|endif|while|do|endwhile|skip]'# added keyword

def scanner(input_file, output_file):
    identifier = "([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*"
    num = "[0-9]+"
    symbol = r'\+|\-|\*|\(|\)|\/|:=|\;'
    keyword = "if|then|else|endif|while|do|endwhile|skip" # added keyword


    with open(input_file, 'r') as reader:
        with open(output_file, 'w+') as writefile:
            for line in reader:
                #Prints line out
                printline = "Line: " + line
                print(printline) 
                writefile.write(printline)
                writefile.write('\n')
                tokenlist = re.findall(PAT,line)
                print (tokenlist)

                #Logic to distinguish each token
                for token in tokenlist:
                    symbolmatch = re.search(symbol, token)
                    nummatch = re.search(num, token)
                    idmatch = re.search(identifier, token)
                    keywordmatch = re.search(keyword, token)

                    if keywordmatch:
                        keywordoutput =  keywordmatch.group() + " KEYWORD\n"
                        print(keywordoutput)
                        writefile.write(keywordoutput)

                    elif symbolmatch:
                        symboloutput = symbolmatch.group() + " SYMBOL\n" #.group() converts the searched object into string
                        print(symboloutput)
                        writefile.write(symboloutput)

                    elif nummatch:
                        numoutput = nummatch.group() + " NUMBER\n"
                        print(numoutput)
                        writefile.write(numoutput)

                    elif idmatch:
                        idoutput = idmatch.group() + " IDENTIFIER\n"
                        print(idoutput)
                        writefile.write(idoutput)
                writefile.write("\n")
                asttree(tokenlist)

def main():
    #FOR TESTING
    # scanner("inputs.txt")
    input_file = input("Please enter name of input file for scanning:  ")
    output_file = input("Please enter name of output file that you would like to write to:  ")
    scanner(input_file, output_file)
    print("This is my stack: ",stack)# so passing by reference is not an issue.
    print("This is my evaluation for the stack: ",evaluator(stack))


if __name__ == "__main__":
    main()
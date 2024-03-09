# Aung Kaung Khant, Kenny Wu
#2.1
import re,sys
from collections import OrderedDict


stack = []




SYM = r'[+\-\(\)\/*]'

#easiet within the 3 segments
def gettype(i):
    identifier = "([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*"
    num = "[0-9]+"
    symbol = r'\+|\-|\*|\(|\)|\/|\:=|\;'#if it is a raw string already why we need to have '\'
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
        if i is '(':
            inbrackets+=1
        elif i is ')':
            inbrackets-=1
        elif inbrackets!=0: # so this is going to search for the enclosed brackets. If inbrackets != 0 then, it is going to search for it til it does
            continue # so when the input is 3*(..)it prints out * first even though it is at last in precedence. For symbols like +-/ it never goes beyond this point
        elif i is s:
            return j
    return -1

def asttree(line, tabs=0): # so two parameters but we only passed one. and line is an array
    tabulation = '\t'*tabs

    if line == []:
        return
    if len(line) == 1: # only one token in token list. And this is used when creating ast tree for 3. This is going to work after every +-/*. for the numbers.
        print(tabulation+line[0]+' : ' +gettype(line[0]))
        stack.append(line[0])#
        #evaluator(stack)#
        return
    try:
        if line[0] == '(' and line[-1] ==')': #case for if it starts with (). And this is used when creating the tree for inside the brackets
            asttree(line[1:-1], tabs)
            return
    except IndexError as IE:
        print(line)
        sys.exit()
    # term

    symbols='+-/*'
    for s in symbols: # here we have implicitly established precedence rules. In terms of plotting, first come first plotted on tree. However, in terms of execution, last come first executed.
        pos = findpos(s, line) # we are going to first match with + in s for every stack.
        if pos != -1:
            print(tabulation+s+' : SYMBOL')#  \t \t + : SYMBOL. This is string concatenation, the +'s.
            stack.append(s)#
            #evaluator(stack)
            asttree(line[:pos],tabs=tabs+1)   # recurse on line before pos
            asttree(line[pos+1:],tabs=tabs+1) # on line after pos
            return


def evaluator(stack1):

    '''if len(stack)>=2:

        while  gettype(stack[-1]) == 'NUMBER' and gettype(stack[-2]) == 'NUMBER' and gettype(stack[-3]) == 'SYMBOL':
            y=stack.pop()
            x=stack.pop()
            op=stack.pop()
            #print(x, op, y)#debugging
            print(gettype(int(OPERATORS[op](x, y))))
            #stack.append(int(OPERATORS[op](x, y)))
            #evaluator(stack1)
            print(stack)

    else:


       print(stack)#can't put print here as it will print within the ast tree
    #print (stack1)#the last one never made it to the stack

'''


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




PAT=r'[0-9]+|[a-zA-Z][a-zA-Z0-9]*|[+\-\(\)\/*\;]|:=|[if|then|else|endif|while|do|endwhile|skip]'# added keyword

def scanner(input_file, output_file):
    identifier = "([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*"
    num = "[0-9]+"
    symbol = r'\+|\-|\*|\(|\)|\/|:=|\;'#if it is a raw string already why we need to have '\' # added new symbols
    keyword = "if|then|else|endif|while|do|endwhile|skip" # added keyword


    with open(input_file, 'r') as reader:
        with open(output_file, 'w+') as writefile:
            for line in reader:
                #Prints line out
                printline = "Line: " + line
                print(printline) #test
                writefile.write(printline)
                writefile.write('\n')

                #so in this case, tokenlist is an array
                tokenlist = re.findall(PAT,line)
                print (tokenlist) #test


                #Logic to distinguish each token
                for token in tokenlist:
                    symbolmatch = re.search(symbol, token)
                    nummatch = re.search(num, token)
                    idmatch = re.search(identifier, token)
                    keywordmatch = re.search(keyword, token)

                    if keywordmatch:
                        keywordoutput =  keywordmatch.group() + " KEYWORD\n"
                        #stack.append(keywordoutput[0] +": KEYWORD")
                        print(keywordoutput)
                        writefile.write(keywordoutput)




                    elif symbolmatch:
                        symboloutput = symbolmatch.group() + " SYMBOL\n" #.group() converts the searched object into string
                        #stack.append(symboloutput[0] + ": SYMBOL") #This steps adds current token to array stack
                        print(symboloutput)
                        writefile.write(symboloutput)



                    elif nummatch:
                        numoutput = nummatch.group() + " NUMBER\n"
                        #stack.append(numoutput + ": NUMBER")
                        print(numoutput)
                        writefile.write(numoutput)



                    elif idmatch:
                        idoutput = idmatch.group() + " IDENTIFIER\n"
                        #stack.append(idoutput)
                        print(idoutput)
                        writefile.write(idoutput)
                        continue
                asttree(tokenlist)







def main():
    #FOR TESTING
    # scanner("inputs.txt")
    # input_file = input("Please enter name of input file for scanning:  ")
    # output_file = input("Please enter name of output file that you would like to write to:  ")
    input_file = "inputs3.txt"
    output_file = "output3.txt"
    scanner(input_file, output_file)
    print("This is my stack: ",stack)# so passing by reference is not an issue.
    print("This is my evaluation for the stack: ",evaluator(stack))


if __name__ == "__main__":
    main()
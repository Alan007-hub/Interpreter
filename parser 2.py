import sys
import re

printlines=[]

def print2(a):
    global printlines
    printlines+=[a+'\n']

def gettype(i):
    identifier = "([a-z]|[A-Z])([a-z]|[A-Z]|[0-9])*"
    num = "[0-9]+"
    symbol = r'\+|\-|\*|\(|\)|\/|:=|;'#if it is a raw string already why we need to have '\'
    keyword = "if|then|else|endif|while|do|endwhile|skip"
    if re.match(identifier, i):
        return 'IDENTIFIER'
    elif re.match(num, i):
        return 'NUMBER'
    elif re.match(symbol, i):
        return 'SYMBOL'
    else:
        return 'KEYWORD'
PAT=r'[0-9]+|[a-zA-Z][a-zA-Z0-9]*|[+\-\(\)\/*\;]|:=|[if|then|else|endif|while|do|endwhile|skip]'# added keyword


def asttree(line, tabs=0): # so two parameters but we only passed one. and line is an array
    tabulation = '\t'*tabs

    if line == []:
        return
    if len(line) == 1: # only one token in token list. And this is used when creating ast tree for 3. This is going to work after every +-/*. for the numbers.
        print2(tabulation+line[0]+' : ' +gettype(line[0]))
        print(tabulation+line[0]+' : ' +gettype(line[0]))
        return # returns nothing so you just want to exit the function
    try:
        if line[0] == '(' and line[-1] ==')': #case for if it starts with (). And this is used when creating the tree for inside the brackets
            asttree(line[1:-1], tabs) # can we delete the tabs part. Will it change anything?
            return
    except IndexError as IE:
        print2(line)
        print(line)
        sys.exit()
    # term


    symbols=[ ';', ':=' , '+', '-', '/', '*']
    xline= ' '.join(line)
    brapat = r'\([a-zA-Z0-9\s\+\-\/\*]+?\)'
    while '(' in xline :
        xline= re.sub(brapat, '', xline)
    xline = re.findall(PAT, xline)
    for s in symbols: # here we have implicitly established precedence rules. In terms of plotting, first come first plotted on tree. However, in terms of execution, last come first executed.
        if s in xline:
            pos  = line.index(s)
            print2(tabulation+s+'  SYMBOL') #  \t \t + : SYMBOL. This is string concatenation, the +'s.
            print(tabulation+s+'  SYMBOL')
            asttree(line[:pos],tabs=tabs+1)   # recurse on line before pos
            asttree(line[pos+1:],tabs=tabs+1) # on line after pos
            return



exppat = r'[0-9]|[a-zA-Z][a-zA-Z0-9]*|[\+\-\*\/\(\)]|:=|;|if|while|do|then'
def blocksplit(lines):
    nesting = 0
    blocks = []
    blockcode = []
    blockcode+=[[]]
    for i in d.split('\n'):
        ws = i.split(' ')
        if ws[0] == 'while' or ws[0]=='if':
            if nesting == 0:
                blockcode+=[[]]
            nesting +=1
            blockcode[-1] += [i]
        elif ws[0] == 'endwhile' or ws[0] == 'endif':
            blockcode[-1] += [i]
            nesting -= 1
            if nesting == 0:
                blockcode+=[[]]
        else:
            blockcode[-1] += [i]
    if len(blockcode[0])==0:
        blockcode=blockcode[1:]
    if len(blockcode[0])==1 and len(blockcode[0][0])==0 :
        blockcode = blockcode[1:]
    if len(blockcode[-1][0])==0:
        blockcode.pop()
    return blockcode













def bloctree(block, tabs = 0):
    #print2('block exec')
    #print2(block)
    #return
    ws = block[0].split()
    if ws[0] == 'while':
        print2(tabs*'\t'+ 'WHILE-LOOP')
        print(tabs*'\t'+ 'WHILE-LOOP')
        tokens = re.findall(PAT, block[0])

        asttree(tokens[1:-1], tabs+1)
        tree([block[1:-1]],tabs+1)
        return
    l = ''.join(block)
    tokens = re.findall(PAT, l)
    asttree(tokens, tabs)


def tree(blocks, tabs=0):
    if len(blocks)==0 :
        return
    if len(blocks)==1:
        bloctree(blocks[0], tabs)
        return
    print2(tabs*'\t'+ '; SYMBOL')
    print(tabs*'\t'+ '; SYMBOL')
    tree([blocks[0]], tabs+1)
    tree(blocks[1:],tabs+1)



f = open('inputs2.txt')

d = f.read()

f.close()

bs = blocksplit(d.split('\n'))
#print2(bs)

#asttree(tokens)
tree(bs)

f=  open('output2.txt', 'w')
f.writelines(printlines)
f.close()
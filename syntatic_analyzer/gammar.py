import sys
import os
sys.setrecursionlimit(60)

#se cambio el Tp B 
#se cambio Ep por A
#se cambio num por n
#se cambio id por i
#se cambio lambda por @

class Node:
    etiqueta = ''
    hijos = list()
    padre = None
    siguiente = None
    def __init__(self,e):
        self.etiqueta = e

def first_operation(pivot, literals):
    for s in literals:
        n = Node(s)
        pivot.hijos.append(n)
        
    
    for i in range(0,len(pivot.hijos)-1):
        pivot.hijos[i].padre = pivot
        pivot.hijos[i].siguiente = pivot.hijos[i+1]
    pivot.hijos[len(pivot.hijos)-1] = pivot
    return pivot.hijos[0]

def second_operation(pivot):
    if(pivot.siguiente != None):
        return pivot.siguiente
    if pivot.padre.siguiente != None:
        return pivot.padre.siguiente
    while(pivot == None):
        if(pivot.siguiente != None):
            pivot = pivot.siguiente
            break
        pivot = pivot.padre.siguiente
            
    return pivot

def thrid_operation(pivot):
    pivot = second_operation(pivot)
    pivot.etiqueta('$')


def first(string):
    #print("first({})".format(string))
    first_ = set()
    if string in non_terminals:
        alternatives = productions_dict[string]

        for alternative in alternatives:
            first_2 = ""
            if(len(alternative)==1):
                first_2 = first(alternative[0])
            else:
                first_2 = first(alternative)
            first_ = first_ |first_2

    elif string in terminals:
        first_ = {string}

    elif string=='' or string=='@':
        first_ = {'@'}

    else:
        first_2 = first(string[0])
        if '@' in first_2:
            i = 1
            while '@' in first_2:
                #print("inside while")

                first_ = first_ | (first_2 - {'@'})
                #print('string[i:]=', string[i:])
                if string[i:] in terminals:
                    first_ = first_ | {string[i:]}
                    break
                elif len(string[i:]) == 0:
                    first_ = first_ | {'@'}
                    break
                first_2 = first(string[i:])
                first_ = first_ | first_2 - {'@'}
                i += 1
        else:
            first_ = first_ | first_2


    #print("returning for first({})".format(string),first_)
    return  first_


def follow(nT):
    #print("inside follow({})".format(nT))
    follow_ = set()
    #print("FOLLOW", FOLLOW)
    prods = productions_dict.items()
    if nT==starting_symbol:
        follow_ = follow_ | {'$'}
    for nt,rhs in prods:
        #print("nt to rhs", nt,rhs)
        for alt in rhs:
            for char in alt:
                if char==nT:
                    following_str = alt[alt.index(char) + 1:]
                    if len(following_str)==0:
                        if nt==nT:
                            continue
                        else:
                            follow_ = follow_ | follow(nt)
                    else:
                        follow_2 = first(following_str)
                        if '@' in follow_2:
                            follow_ = follow_ | follow_2-{'@'}
                            follow_ = follow_ | follow(nt)
                        else:
                            follow_ = follow_ | follow_2
    #print("returning for follow({})".format(nT),follow_)
    return follow_


def createTable():
    table = {}
    getFollow = False
    temp = {}
    for nt in non_terminals:
        globalSet = FIRST[nt]
        productioSet = productions_dict[nt]
        
        if '@' in globalSet:
            globalSet.remove('@')
            getFollow = True
        if len(productioSet) == 1:
            for f in globalSet:
                temp[f] = productioSet[0]
                #table.update({ nt: {f: productioSet[0]} })
            table[nt] = temp
            temp = {}
                
        else:
            for f in globalSet:
                for prod in productioSet:
                    if f in prod:
                        temp[f] = prod
                        #table.update({ nt: {f: prod} })
                        break
            table[nt] = temp
            temp = {}
        if getFollow:
            globalSet = FOLLOW[nt]
            for f in globalSet:
                temp[f] = ['@']
                #table.update({ nt: {f: '@'} })
            table[nt].update(temp)
            temp = {}
            getFollow = False
                

    return table

def validatorString(s):
    symbolStack = ['$',starting_symbol]
    inputQueue = []
    #root = Node(starting_symbol)
    #node = root
    #pivot = node


    correctString = False
    tmpString = ""
    for c in s:
        if c == " ":
            continue
        correctString = False
        
        tmpString+=c
        if tmpString in terminals:
            correctString = True
            inputQueue.append(tmpString)
            tmpString = ""

    if(not correctString):
        print('error el simbolo no existe en la gramatica')
        exit(1)

    inputQueue.append('$')
    while len(inputQueue) != 0 and len(symbolStack) != 0:
        x = symbolStack[len(symbolStack)-1]
        a = inputQueue[0]



        if (x == '$' and a == '$') or (x in terminals and x == a) :
            inputQueue.pop(0)
            symbolStack.pop()
            #thrid_operation(pivot)
        else:
            tmp = x
            symbolStack.pop()
            if tmp in table.keys() and a in table[tmp].keys():
                newProd = table[tmp][a].copy()
                newProd.reverse()
                #pivot = first_operation(pivot,newProd)
                for c in newProd:
                    if c != '@':
                        symbolStack.append(c)
                    #else:
                    #    pivot = second_operation(pivot)

            
            
    
    if(len(inputQueue) == 0 and len(symbolStack) == 0):
        print("cadena valida")
    else:
        print("error sintaxis invalida")

def createGramaticFileStructure(list_of_terminals,list_of_no_terminals):
    path = os.getcwd()
    directory_name = "gramaticDir"
    full_path = path +'/'+directory_name
    try:
        if not os.path.exists(full_path):
            os.mkdir(full_path)
    except OSError:
        print("directory creation failed in %s" % path)
    else:
        print("directory creation successfull")
    f = open(full_path+'/AbstractExpressionNT.py',"w+")
    f.write("class AbstractExpressionNT:\n")
    f.write("\t def __init__(self):\n")
    f.write("\t\t print('AbstractExpressionNT')\n")
    f.close()
    f = open(full_path+'/AbstractExpressionT.py',"w+")
    f.write("class AbstractExpressionT:\n")
    f.write("\t def __init__(self):\n")
    f.write("\t\t print('AbstractExpressionT')\n")
    f.close()
    symbolNames={'+':'Add','-':'Minus','*':'Product','/':'Division','%':'Module'}
    for t in list_of_terminals:
        if t in symbolNames.keys():
            name_class =symbolNames[t].capitalize()+'Terminal' 
            name_class.replace(" ","")
            name_file = name_class+'.py'
            f = open(full_path+'/'+name_file,"w+")
            f.write("from AbstractExpressionT import AbstractExpressionT\n")
            f.write("class "+name_class+"(AbstractExpressionT):\n")
            f.write("\t def interprets(self,val):\n")
            f.write("\t\t return(0)\n")
            f.close()

    for nt in list_of_no_terminals:
        name_class =nt.capitalize()+'NonTerminal' 
        name_class.replace(" ","")
        name_file = name_class+'.py'
        f = open(full_path+'/'+name_file,"w+")
        f.write("from AbstractExpressionNT import AbstractExpressionNT\n")
        f.write("class "+name_class+"(AbstractExpressionNT):\n")
        f.write("\t valor = 0\n")
        f.write("\t def interprets(self):\n")
        f.write("\t\t return self.valor\n")
        f.close()

    return 0



#no_of_terminals=int(input("Enter no. of terminals: "))

terminals = ['+','-','*','/','(',')','num','id']

print("Enter the terminals :")
#for _ in range(no_of_terminals):
#    terminals.append(input())

#no_of_non_terminals=int(input("Enter no. of non terminals: "))

non_terminals = ['E','Ep','T','Tp','F']

print("Enter the non terminals :")
#for _ in range(no_of_non_terminals):
#    non_terminals.append(input())

#starting_symbol = input("Enter the starting symbol: ")
starting_symbol = 'E'
#no_of_productions = int(input("Enter no of productions: "))
no_of_productions = 5
productions = ["E:=T Ep","Ep:=+ T Ep|- T Ep|@","T:=F Tp","Tp:=* F Tp|/ F Tp|@","F:=( E )|num|id"]

print("Enter the productions:")
#for _ in range(no_of_productions):
#    productions.append(input())


#print("terminals", terminals)

#print("non terminals", non_terminals)

#print("productions",productions)


productions_dict = {}

for nT in non_terminals:
    productions_dict[nT] = []


#print("productions_dict",productions_dict)

for production in productions:
    nonterm_to_prod = production.split(":=")
    alternatives = nonterm_to_prod[1].split("|")
    for alternative in alternatives:
        productions_dict[nonterm_to_prod[0]].append(alternative.split(" "))

print("productions_dict",productions_dict)

#print("nonterm_to_prod",nonterm_to_prod)
#print("alternatives",alternatives)


FIRST = {}
FOLLOW = {}

for non_terminal in non_terminals:
    FIRST[non_terminal] = set()

for non_terminal in non_terminals:
    FOLLOW[non_terminal] = set()

#print("FIRST",FIRST)

for non_terminal in non_terminals:
    FIRST[non_terminal] = FIRST[non_terminal] | first(non_terminal)

#print("FIRST",FIRST)


FOLLOW[starting_symbol] = FOLLOW[starting_symbol] | {'$'}
for non_terminal in non_terminals:
    FOLLOW[non_terminal] = FOLLOW[non_terminal] | follow(non_terminal)

#print("FOLLOW", FOLLOW)

#print("{: ^20}{: ^20}{: ^20}".format('Non Terminals','First','Follow'))
#for non_terminal in non_terminals:
#    print("{: ^20}{: ^20}{: ^20}".format(non_terminal,str(FIRST[non_terminal]),str(FOLLOW[non_terminal])))

table = createTable()
#for nt in non_terminals:
#    print("-----------------------------")
#    print("Non terminal: " + nt)
#    for t in terminals:
#        if t in table[nt].keys():
#            print( t + ":",end="")
#            for j in table[nt][t]:
#                print(str(j),end=" ")
#            print()
validatorString("num + num + num + num")
createGramaticFileStructure(terminals,non_terminals)
    
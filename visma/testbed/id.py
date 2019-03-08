############
# Token ID #
############

'''
Following is an example list of IDs (func.tid property of Function class) of the functions generated during calculations/simplifications
Only + and * are used as binary operations, the - and / will be taken care by func.coefficient and func.power respectively.
'''

# NOTE: Not required currently. Leaving here for future use.

random = ['a0', 'b0', 'b0a2', 'b0a1', 'b0a3',
          'b0b0', 'a0b0', 'a0a1', 'a0a2', 'a0a2a0', 'a0a3', 'c1', 'c2']

'''
random sorted :-
['a0', 'a0a1', 'a0a2', 'a0a2a0', 'a0a3', 'a0b0', 'b0', 'b0a1', 'b0a2', 'b0a3', 'b0b0', 'c1', 'c2']

final expected equation :-
a0(a0a1*a0a2(a0a2a0)*a0a3 + a0b0) + b0(b0a1*b0a2*b0a3 + b0b0) + c1*c2
'''

final = []
list.sort(random)
levelold = 0
openbrac = 0
closebrac = 0

for func in random:
    level = int(len(func) / 2 - 1)
    if(levelold < level):
        final.append('(')
        openbrac += 1
    elif(levelold > level):
        for i in range(0, levelold - level):
            final.append(')')
            closebrac += 1
        if(func[2 * level + 1] <= '1'):
            final.append('+')
        else:
            final.append('*')
    elif(levelold == level):
        if(func[2 * level + 1] <= '1'):
            final.append('+')
        else:
            final.append('*')
    final.append(func)

    levelold = level

# FIXME: Find a way to handle functions in exponentials Ex: f1^(f2+f3)

for i in range(0, openbrac - closebrac):
    final.append(')')
eqstring = ""
for func in final:
    eqstring += str(func)

print(eqstring)

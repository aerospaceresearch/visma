###############
# ID printing #
###############

'''
Following is a list of random IDs (func.id property of func class) of a functions generated during calculations/simplifications
'''

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
    level = int(len(func)/2 - 1)
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

for i in range(0, openbrac - closebrac):
    final.append(')')

for func in final:
    print(func, end=' ')

print()

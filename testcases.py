MAX_EXERCISES = 25
MAX_MODULES = 3

#testcases = [ [{}]*MAX_EXERCISES for i in range(MAX_MODULES+1) ]
testcases = [ [] ]
testcases.append([ [] ])

# mod = 1, ex = 1
testcases[1].append([])
testcases[1][1] = [{
    'description': 'vetor de elementos sem sinal',
    'line': 17, 'grade': 3,
    'result': [(12, 0x7F)], 
},{
    'description': 'vetor de elementos negativos',
    'line': 22, 'grade': 3,
    'result': [(12, 0xFF)], 
},{
    'description': 'vetor misto com e sem sinal',
    'line': 27, 'grade': 3,
    'result': [(12, 0xE4)], 
},{
    'description': 'vetor vazio',
    'line': 32, 'grade': 1,
    'result': [(12, 0x00)], 
}]

# mode = 1, ex = 2 
testcases[1].append([])
testcases[1][2] = [{
    'description': 'vetor de elementos sem sinal',
    'line': 17, 'grade': 10,
    'result': [(12, 0x01)], 
}]

# mode = 1, ex = 3 
testcases[1].append([])
testcases[1][3] = [{
    'description': 'soma de elementos de 32 bits',
    'line': 17, 'grade': 10,
    'result': [(12, 0x1234), (13, 0x5678)], 
}]


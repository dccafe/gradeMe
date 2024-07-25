MAX_EXERCISES = 25
MAX_MODULES = 3

#testcases = [ [{}]*MAX_EXERCISES for i in range(MAX_MODULES+1) ]
testcases = [ [] ]
testcases.append([ [] ])

# mod = 1, ex = 1
testcases[1].append([])
testcases[1][1] = [{
    'description': 'vetor de elementos sem sinal', 
    'input'      : [0x10, 0x7F, 0x73, 0x5A],
    'output'     : 0x7F,
    'grade'      : 3,
},{
    'description': 'vetor de elementos negativos',
    'result': [(12, 0xFF)], 'grade': 3, 
},{
    'description': 'vetor misto com e sem sinal',
    'result': [(12, 0xE4)], 'grade': 3, 
},{
    'description': 'vetor vazio',
    'result': [(12, 0x00)], 'grade': 1, 
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


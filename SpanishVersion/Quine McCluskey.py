# Algoritmo de Quinne McCluskey para minimización de expresiones lógicas
# Author: Suman Adhikari

def mul(x,y): # Multiplica 2 mintérminos
    res = []
    for i in x:
        if i+"'" in y or (len(i)==2 and i[0] in y):
            return []
        else:
            res.append(i)
    for i in y:
        if i not in res:
            res.append(i)
    return res

def multiplica(x,y): # Multiplica 2 expresiones
    res = []
    for i in x:
        for j in y:
            tmp = multiplica0,2,8,10,11,20,21,22,23,26,27,28(i,j)
            res.append(tmp) if len(tmp) != 0 else None
    return res

def refinar(my_list,dc_list): # Remueve los términos don't care de una lista dada y retorna la lista refinada
    res = []
    for i in my_list:
        if int(i) not in dc_list:
            res.append(i)
    return res

def BuscarIPE(x): # Función para encontrar los implicantes primos esenciales
    res = []
    for i in x:
        if len(x[i]) == 1:
            res.append(x[i][0]) if x[i][0] not in res else None
    return res

def BuscarVariables(x): # Función para encontrar las variables en los términos. Por ejemplo, el mintérmino --01 tiene a C' y D como variables
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
            var_list.append(chr(i+65)+"'")
        elif x[i] == '1':
            var_list.append(chr(i+65))
    return var_list

def recorta(x): # Recorta la lista
    elementos_recortados = []
    for i in x:
        elementos_recortados.extend(x[i])
    return elementos_recortados

def buscaMinterminos(a): # Función para encontrar a los mintérminos mezclados. Por ejemplo, 10-1 son obtenidos al combinar 9(1001) y 11(1011)
    gaps = a.count('-')
    if gaps == 0:
        return [str(int(a,2))]
    x = [bin(i)[2:].zfill(gaps) for i in range(pow(2,gaps))]
    temp = []
    for i in range(pow(2,gaps)):
        temp2,ind = a[:],-1
        for j in x[0]:
            if ind != -1:
                ind = ind+temp2[ind+1:].find('-')+1
            else:
                ind = temp2[ind+1:].find('-')
            temp2 = temp2[:ind]+j+temp2[ind+1:]
        temp.append(str(int(temp2,2)))
        x.pop(0)
    return temp

def compara(a,b): # Función para checar si dos mintérminos difieren en un bit
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            mismatch_index = i
            c += 1
            if c>1:
                return (False,None)
    return (True,mismatch_index)

def remueveTerminos(_chart,terms): # Remueve mintérminos que ya fueron seleccionados previamente
    for i in terms:
        for j in buscaMinterminos(i):
            try:
                del _chart[j]
            except KeyError:
                pass
print('Por favor ingrese los términos separados por un espacio')
mt = [int(i) for i in input("Ingrese los mintérminos ").strip().split()]
dc = [int(i) for i in input("Ingrese los don't care (Si existen): ").strip().split()]
mt.sort()
minterminos = mt+dc
minterminos.sort()
size = len(bin(minterminos[-1]))-2
grupos,all_pi = {},set()

# Comenzamos la agrupación primaria
for minterm in minterminos:
    try:
        grupos[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(size))
    except KeyError:
        grupos[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(size)]
# Término de la agrupación primaria

#Comenzamos la impresión de la agrupación primaria
print("\n\n\n\nNúmero de Gpo.\tMintérminos\t\tExpresión en BCD\n%s"%('='*60))
for i in sorted(grupos.keys()):
    print("%5d:"%i) # Prints group number
    for j in grupos[i]:
        print("\t\t    %-20d%s"%(int(j,2),j)) # Imprime los mintérminos y su representación binaria (BCD)
    print('-'*60)
#Término de la impresión de la agrupación primara

# Proceso para crear las tablas y encontrar los implicantes primos 
while True:
    tmp = grupos.copy()
    grupos,m,marcados,debo_parar = {},0,set(),True
    l = sorted(list(tmp.keys()))
    for i in range(len(l)-1):
        for j in tmp[l[i]]: # Iteración a través del grupo de elementos actual 
            for k in tmp[l[i+1]]: # Iteración a través del siguiente grupo de elementos
                res = compara(j,k) # Comparamos los mintérminos
                if res[0]: # Si los mintérminos difieren solamente en un bit
                    try:
                        grupos[m].append(j[:res[1]]+'-'+j[res[1]+1:]) if j[:res[1]]+'-'+j[res[1]+1:] not in grupos[m] else None # Imprimimos un guión '-' en el bit que cambia y lo agregamos al grupo correspondiente
                    except KeyError:
                        grupos[m] = [j[:res[1]]+'-'+j[res[1]+1:]] # Si el grupo no existe, crearemos un grupo al principio y pondremos un guión '-' en el cambio de bi, además de agregarlo a un nuevo grupo
                    debo_parar = False
                    marcados.add(j) # Marca el elemento j
                    marcados.add(k) # Marca el elemento k
        m += 1
    desmarcados_local = set(recorta(tmp)).difference(marcados) # Desmarcamos los elemntos de cada tabla
    all_pi = all_pi.union(desmarcados_local) # Agregamos el implicante primo a la lita global.
    print("Elementos desmarcados(Implicantes Primos) de la tabla:",None if len(desmarcados_local)==0 else ', '.join(desmarcados_local)) # Imprimimos los implicantes promos en la tabla actual
    if debo_parar: # Si los mintérminos no pueden ser combinados
        print("\n\nAll Implicantes Primos: ",None if len(all_pi)==0 else ', '.join(all_pi)) # Imprimimos todos los implicantes primos
        break
    # Imprimimos en todos los grupos siguientes
    print("\n\n\n\nNúmero de Gpo\tMintérminos\t\tExpresión en BCD\n%s"%('='*60))
    for i in sorted(grupos.keys()):
        print("%5d:"%i) # Imprimimos el número de grupo
        for j in grupos[i]:
            print("\t\t%-24s%s"%(','.join(buscaMinterminos(j)),j)) # Imprimimos los mintérminos y su representación binaria.
        print('-'*60)
    # Terminamos la impresión de los grupos siguientes
# Terminamos el proceso de la creación de tablas y encontrar los implicantes primos


# Comenzamos la impresión y procesamiento de los implicantes primos 
sz = len(str(mt[-1])) # El número de los dígitos del mintérmino más largo
chart = {}
print('\n\n\nImpresión de los implicantes primos escenciales:\n\n  Mintérminos  |%s\n%s'%(' '.join((' '*(sz-len(str(i))))+str(i) for i in mt),'='*(len(mt)*(sz+1)+16)))
for i in all_pi:
    minterminos_mezclados,y = buscaMinterminos(i),0
    print("%-16s|"%','.join(minterminos_mezclados),end='')
    for j in refinar(minterminos_mezclados,dc):
        x = mt.index(int(j))*(sz+1) # La posicioón donde debemos de marcar con una x
        print(' '*abs(x-y)+' '*(sz-1)+'X',end='')
        y = x+sz
        try:
            chart[j].append(i) if i not in chart[j] else None # Agregamos el mintérmino a la impresión
        except KeyError:
            chart[j] = [i]
    print('\n'+'-'*(len(mt)*(sz+1)+16))
# Terminamos la impresión y procesamiento de los implicantes primos

IPE = BuscarIPE(chart) # Encontramos los implicantes primos escenciales
print("\nImplicantes Primos Escenciales: "+', '.join(str(i) for i in IPE))
remueveTerminos(chart,IPE) #Removemos los Implicantes Primos Escenciales de las columnas relacionadas de la impresión

if(len(chart) == 0): # Si los imintérminos premanecen después de remover los Implicantes Primos de las columnas relacionadas
    resultado_final = [BuscarVariables(i) for i in IPE] # Resultado Final solamente con los Implicantes Primos Escenciales
else: # Sino, proseguimos con el método de Petricl para una mejor simplificación
    P = [[BuscarVariables(j) for j in chart[i]] for i in chart]
    while len(P)>1: # Nos quedaremos multiplicando hara que obtenfamos la suma de productos de P
        P[1] = multiplica(P[0],P[1])
        P.pop(0)
    resultado_final = [min(P[0],key=len)] # Seleccionamos el término con menor númerno de variables de P
    resultado_final.extend(BuscarVariables(i) for i in IPE) # Agregamos los Implicantes Primos Escenciales en la solución
print('\nSolución: F = '+' + '.join(''.join(i) for i in resultado_final))

input("\nPresione enter para salir ")

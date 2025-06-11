import hashlib
import math
# import random
# import time

####################
#  Початкові дані  #
####################
leaves = [1, 2, 3, 4, 5, 6, 7]
# leaves = []
# for i in range(2**8):
#     leaves.append(i)
# leaves = [random.randint(0, 100) for _ in range(2**16)]


#######################
#  Функція хешування  #
#######################
def hash(x):
    if x in (None,
             'dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91',
             2 * 'dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91'):
        return 'dc937b59892604f5a86ac96936cd7ff09e25f18ae6b758e8014a24c7fa039e91'
    
    bytes_obj = str(x).encode('utf-8')
    hash_obj = hashlib.sha256(bytes_obj)
    return hash_obj.hexdigest()

# extra_list = [random.randint(0, 100) for _ in range(100000)]


###################################
#  Функція пошуку індекса батька  #
###################################
def parent_searcher(k):
    if k % 2 == 0:
        return (k // 2)
    else:
        return ((k - 1) // 2)


########################################
#  Функція знаходження індекса сусіда  #
########################################
def neighbour_searcher(k):
    if k % 2 == 0:
        return (k + 1)
    else:
        return (k - 1)


############################################################################
##                           БІНАРНЕ ДЕРЕВО МЕРКЛА                        ##
############################################################################
def binary_tree_builder(x):
    tree, Level, temp = [], [], x[:]

    if len(temp) % 2 != 0:
        temp.append(temp[-1])
    tree.append([hash(i) for i in temp])

    for i in range(1, math.ceil(math.log2(len(temp))) + 1):
        for j in range(0, len(tree[i - 1]), 2):
            Level.append(hash(tree[i - 1][j] + tree[i - 1][j + 1]))
        if len(Level) % 2 != 0 and i != math.ceil(math.log2(len(temp))):
            Level.append(Level[-1])
        tree.append(Level)
        Level = []

    return tree
 
BMT = binary_tree_builder(leaves)

###################################################
#  Побудова БДМ з розширеними початковими даними  #
###################################################
def extra_binary_tree_builder(data, extra):
    temp = data + extra
    return binary_tree_builder(temp)


################################
#  Генерація доказу включення  #
################################
def binary_tree_mp(x):
    proof, n, k = [], 0, 0

    for i in range(len(leaves)):
        if x == leaves[i]:
            k = i
            break
        else:
            for i in range(1, len(BMT)):
                for j in range(len(BMT[i])):
                    if x == BMT[i][j]:
                        n, k = i, j

    proof.append(BMT[n][neighbour_searcher(k)])

    for i in range(n + 1, len(BMT) - 1):
        proof.append(BMT[i][neighbour_searcher(parent_searcher(k))])
        for j in range(len(BMT[i])):
            if proof[-1] == BMT[i][j]:
                k = j
    return proof


#######################################
#       Розмір у байтах елемента      #
#######################################
def bytesize(x):                      #
    string = str(x).encode('utf-8')   #
    return len(string)                #
#######################################


###############################
#  Підрахунок розміру списку  #
###############################
def proofsize(x):
    size = 0
    for i in range(len(x)):
        size = size + bytesize(x[i])
    return size


#################################################
#  Верифікація доказу включення (х - наявність  #
#  якого доводимо, у - binary_tree_mp(x))       #
#################################################
def binary_proof_verification(x, y):
    L, n = [], 0

    for i in range(len(leaves)):
        if x == leaves[i]:
            n = 0
            L.append(hash(x))
            break

    for i in range(1, len(BMT)):
        for j in range(len(BMT[i])):
            if x == BMT[i][j]:
                n = i
                L.append(x)
                break

    if len(L) == 0:
        return 'Немає такого елемента в дереві.'

    if n == 0:
        for i in range(len(y)):
            for j in range(len(BMT[i])):
                if y[i] == BMT[i][j] and j % 2 == 0:
                    L.append(hash(y[i] + L[i]))
                    break
                elif y[i] == BMT[i][j] and j % 2 != 0:
                    L.append(hash(L[i] + y[i]))
                    break
    else:
        for i in range(n, len(y) + 1):
            for j in range(len(BMT[i])):
                if y[i - n] == BMT[i][j] and j % 2 == 0:
                    L.append(hash(y[i - n] + L[-1]))
                    break
                elif y[i - n] == BMT[i][j] and j % 2 != 0:
                    L.append(hash(L[-1] + y[i - n]))
                    break

    if L[-1] == BMT[-1][-1]:
        return True
    else:
        return False


#######################################
#  Зрозумілий принт дерева у консоль  #
#######################################
def print_tree(x):
    for i in range(len(x)):
        print(x[len(x) - i - 1])



###########################################################################
##                       РОЗРІДЖЕНЕ ДЕРЕВО МЕРКЛА                        ##
###########################################################################
def sparse_tree_builder(x):
    height = math.ceil(math.log2(len(x)))
    L = [None] * (2**height)   
    for i in range(len(x)):
        L[i] = x[i]
    
    SMT = binary_tree_builder(L)
    root = SMT[-1][-1]
    j = len(binary_tree_builder(L))
    while j < 256:
        if j == 255:
            root = hash(root + hash(None))
            SMT.append(root)
        else:
            root = hash(root + hash(None))
            SMT.append([root, hash(None)])
        j += 1
    return SMT

SMT = sparse_tree_builder(leaves)

#####################################
#  Додавання нових елементів у SMT  #
#####################################
def extra_sparse_tree_builder(data, extra):
    l = data + extra
    return sparse_tree_builder(l)


################################
#  Генерація доказу включення  #
################################
def sparse_tree_mp(x):
    proof, n, k, found = [], 0, 0, False
    l = leaves[:] + [None] * (2**(math.ceil(math.log2(len(leaves)))) - len(leaves))
        
    tree = binary_tree_builder(l)
    
    for i in range(len(leaves)):
        if x == leaves[i]:
            k = i
            found = True
            break
        else:
            for i in range(1, len(tree)):
                for j in range(len(tree[i])):
                    if x == tree[i][j]:
                        n, k = i, j
                        found = True
                        break
    if not found:
        return None
    else:
        proof.append(tree[n][neighbour_searcher(k)])
    
        for i in range(n + 1, len(tree) - 1):
            proof.append(tree[i][neighbour_searcher(parent_searcher(k))])
            for j in range(len(tree[i])):
                if proof[-1] == tree[i][j]:
                    k = j
    
        for i in range(len(tree) - 1, 256):
            proof.append(hash(None))
            
        return proof

# print(len(sparse_tree_mp(3)))
# print(SMT[-1])
#################################################
#  Верифікація доказу включення (х - наявність  #
#  якого доводимо, у - sparce_tree_mp(x))       #
#################################################
def sparse_proof_verification(x, y):
    if y == None:
        return None
    
    L, n = [], 0
    
    l = leaves[:] + [None] * (2**(math.ceil(math.log2(len(leaves)))) - len(leaves))
    tree = binary_tree_builder(l)
    
    for i in range(len(leaves)):
        if x == leaves[i]:
            n = 0
            L.append(hash(x))
    
    if len(L) == 0:
        for i in range(len(SMT)):
            for j in range(len(SMT[i])):
                if x == SMT[i][j]:
                    n = i
                    L.append(x)
    else:
        pass
    
    if len(L) == 0:
        return 'Немає такого елемента в дереві.'
    
    if n == 0:
        for i in range(len(tree)):
            for j in range(len(tree[i])):
                if y[i] == tree[i][j] and j % 2 == 0:
                    L.append(hash(y[i] + L[i]))
                    break
                elif y[i] == tree[i][j] and j % 2 != 0:
                    L.append(hash(L[i] + y[i]))
                    break
    else:
        for i in range(n, len(tree) + 1):
            for j in range(len(SMT[i])):
                if y[i - n] == SMT[i][j] and j % 2 == 0:
                    L.append(hash(y[i - n] + L[-1]))
                    break
                elif y[i - n] == SMT[i][j] and j % 2 != 0:
                    L.append(hash(L[-1] + y[i - n]))
                    break
    
    for i in range(len(tree), len(y)):
        L.append(hash(L[i - 1] + hash(None)))
        
    if L[-1] == SMT[-1]:
        return True
    else:
        return False


# print(sparse_tree_mp(1))
# print(SMT_proof_verification(7, sparse_tree_mp(7)))


# #########################################################
# #               ІНДЕКСОВАНЕ ДЕРЕВО МЕРКЛА               #
# #########################################################
def indexed_tree_builder(x):
    tree, Level = [], []
    for i in range(len(x)):
        Level.append([hash(x[i]), [i]])
    
    tree.append(Level)
    for i in range(1, math.ceil(math.log2(len(x))) + 1):
        Level = []
        
        for j in range(0, 2 * math.floor(len(tree[i - 1]) / 2), 2):
            Level.append([hash(tree[i - 1][j][0] + tree[i - 1][j + 1][0]), [*tree[i - 1][j][1], *tree[i - 1][j + 1][1]]])
        
        if len(tree[i - 1]) % 2 != 0:
            Level.append(tree[i - 1][-1])
        else:
            pass
        
        tree.append(Level)

    return tree


IMT = indexed_tree_builder(leaves)
# print(IMT)


###################################
# Додавання нових елементів в ІДМ #
###################################
def extra_indexed_tree_builder(data, extra_data):
    l = [*data, *extra_data]
    return indexed_tree_builder(l)


###############################
# Формування доказу включення #
###############################
def indexed_tree_mp(x):
    proof, n, k = [], 0, 0
    
    if len(leaves) % 2 != 0 and x == leaves[-1]:
        k = len(leaves) - 1
        while len(IMT[n + 1][-1][1]) == 1:
            n += 1
            k = len(IMT[n]) - 1
    else:
        for i in range(len(leaves)):
            if x == leaves[i]:
                k = i
                break
            else:
                for i in range(1, len(IMT)):
                    for j in range(len(IMT[i])):
                        if x == IMT[i][j][0]:
                            n, k = i, j
    
    proof.append(IMT[n][neighbour_searcher(k)])

    for i in range(n + 1, len(IMT) - 1):
        proof.append(IMT[i][neighbour_searcher(parent_searcher(k))])
        for j in range(len(IMT[i])):
            if proof[-1][0] == IMT[i][j][0]:
                k = j

    return proof

################################
# Верифікація доказу включення #
################################
def indexed_proof_verification(x, k, y):
    L = []
    
    if x in leaves:
        L.append([hash(x), [k]])
        for i in range(len(y) - 1):
            if int(y[i][1][-1]) < int(L[i][1][-1]):
                L.append([hash(y[i][0] + L[i][0]), [*y[i][1], *L[i][1]]])
            else:
                L.append([hash(L[i][0] + y[i][0]), [*L[i][1], *y[i][1]]])
            
        if L[-1][0] == IMT[-2][0][0]:
            L.append([hash(L[-1][0] + y[-1][0]), [*L[-1][1], *y[-1][1]]])
        else:
            L.append([hash(y[-1][0] + L[-1][0]), [*y[-1][1], *L[-1][1]]])
    else:
        L.append([x, k])
        for i in range(len(y) - 1):
            if int(y[i][1][-1]) < int(L[i][1][-1]):
                L.append([hash(y[i][0] + L[i][0]), [*y[i][1], *L[i][1]]])
            else:
                L.append([hash(L[i][0] + y[i][0]), [*L[i][1], *y[i][1]]])
            
        if L[-1][0] == IMT[-2][0][0]:
            L.append([hash(L[-1][0] + y[-1][0]), [*L[-1][1], *y[-1][1]]])
        else:
            L.append([hash(y[-1][0] + L[-1][0]), [*y[-1][1], *L[-1][1]]])
            
    if L[-1][0] == IMT[-1][0][0]:
        return True
    else:
        return False

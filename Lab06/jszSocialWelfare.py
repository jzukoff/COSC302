import itertools
# Josh Zukoff

def case1Naming(B,S):
    
    for i in range(len(B)):
        B[i] = list(B[i]) + [i]
    for j in range(len(S)):
        S[j] = list(S[j]) + [j]
    return B,S

def case2Naming(B,S):
    Bnew = []
    Snew = []
    
    for i in range(len(B)):
        B[i][0] = list(B[i][0]) + [i]
        Bnew.append(B[i][0])
        for x in range(len(B[i])-1,0,-1):
            B[i][x] = list(B[i][x]) + [i]
            B[i][x][0] -= B[i][x-1][0]
            Bnew.append(B[i][x])
            
    for j in range(len(S)):
        S[j][0] = list(S[j][0]) + [j]
        Snew.append(S[j][0])
        for y in range(len(S[i])-1,0,-1):
            S[j][y] = list(S[j][y]) + [j]
            S[j][y][0] -= S[j][y-1][0]
            Snew.append(S[j][y])
    B = Bnew
    S = Snew

    return B,S

def case1(B,S):
    
    if type(B[0]) == type (()):
        B,S = case1Naming(B,S)
    elif type(B[0]) == type([]):
        B,S = case2Naming(B,S)
        
    B = sorted(B, key = lambda v: v[1], reverse=True)
    S = sorted(S, key = lambda p: p[1])
    buyTransactions = {}
    sellTransactions = {}
    while True:
        if len(B) == 0 or len(S) == 0:
            break
        
        currBuyer = B[0]
        currSeller = S[0]

        if currBuyer[1] < currSeller[1]:
            break

        elif currBuyer[0] < currSeller[0]:
            
            if currBuyer[2] not in buyTransactions:
                buyTransactions[currBuyer[2]] = currBuyer[0]
            else:
                buyTransactions[currBuyer[2]] += currBuyer[0]
                
            if currSeller[2] not in sellTransactions:
                sellTransactions[currSeller[2]] = currBuyer[0]
            else:
                sellTransactions[currSeller[2]] += currBuyer[0]
                
            currSeller[0] -= currBuyer[0]
            B.pop(0)

            

        elif currBuyer[0] == currSeller[0]:
            
            if currBuyer[2] not in buyTransactions:
                buyTransactions[currBuyer[2]] = currBuyer[0]
            else:
                buyTransactions[currBuyer[2]] += currBuyer[0]
                
            if currSeller[2] not in sellTransactions:
                sellTransactions[currSeller[2]] = currSeller[0]
            else:
                sellTransactions[currSeller[2]] += currSeller[0]

            B.pop(0)
            S.pop(0)

        else:
            
            if currBuyer[2] not in buyTransactions:
                buyTransactions[currBuyer[2]] = currSeller[0]
            else:
                buyTransactions[currBuyer[2]] += currSeller[0]
                
            if currSeller[2] not in sellTransactions:
                sellTransactions[currSeller[2]] = currSeller[0]
            else:
                sellTransactions[currSeller[2]] += currSeller[0]

            currBuyer[0] -= currSeller[0]
            S.pop(0)

    print ('Buyers \n', buyTransactions)
    print ('Sellers \n', sellTransactions)

def case2(B,S):
    case1(B,S)

def case3(B,S):
    
    B,S = case1Naming(B,S)
    
    Bdict = {}
    Sdict = {}

    for b in B:
        Bdict[b[2]] = b[0]

    for s in S:
        Sdict[s[2]] = s[0]
        
    buyTransactions = {}
    sellTransactions = {}

    buyCombinations = []
    sellCombinations = []

    for i in range(1,len(B)+1):
        for comb in itertools.combinations(B,i):
            
            totalN = 0
            minPrice = float('inf')
            label = []
            for element in comb:
                
                totalN += element[0]
                if element[1] < minPrice:
                    minPrice = element[1]
                label.append(element[2])
            buyCombinations.append((totalN, minPrice, tuple(label)))

    
    for j in range(1,len(S)+1):
        for comb in itertools.combinations(S,j):
            totalN = 0
            maxPrice = 0
            label = []
            for element in comb:
                totalN += element[0]
                if element[1] > maxPrice:
                    maxPrice = element[1]
                label.append(element[2])
            sellCombinations.append((totalN, maxPrice, tuple(label)))       
            
    B = sorted(buyCombinations, key = lambda v: v[1], reverse=True)
    S = sorted(sellCombinations, key = lambda p: p[1])     

    usedB = {}
    usedS = {}

    for buyer in B:
        for seller in S:
            
            if buyer[0] == seller[0] and buyer[1] >= seller[1]:
                taken = False
                for label in buyer[2]:
                    if label in usedB:
                        taken = True
                        break
                for label2 in seller[2]:
                    if label2 in usedS:
                        taken = True
                        break
                if taken == False:
                    for label in buyer[2]:
                        usedB[label] = Bdict[label]
                    for label in seller[2]:
                        usedS[label] = Sdict[label]

    print ('Buyers \n', usedB)
    print ('Sellers \n', usedS)
    


def main():
    
    B = [(5,10),(3,12)]
    S = [(5,2),(3,3)]

    Bp = [[(2,5),(4,4),(7,3)],[(1,3),(2,2),(5,1)]]
    Sp = [[(2,5),(4,4),(7,3)],[(1,3),(2,2),(5,1)]]

    Bn = [(5,20),(3,20)]
    Sn = [(5,8),(3,19), (2,2)]

    print ('Case1\n')
    case1 (B,S)

    print ('\n\nCase2\n')
    case2 (Bp,Sp)

    print ('\n\nCase3\n')
    case3 (Bn,Sn)
        

if __name__ == '__main__':
    main()

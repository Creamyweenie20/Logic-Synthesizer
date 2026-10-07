import re

def getPrimeImplicants(minterms):  # psuedo code on wikipedia for Quine-McCluskey algorithm
    primeImplicants = []
    num_min = len(minterms)
    merges = [False] * num_min
    numberOfMergers = 0 
    mergedMinterm, minterm1, minterm2 = '','',''
    for i in range(num_min): 
        for c in range(i + 1, num_min): 
            minterm1 = minterms[i]
            minterm2 = minterms[c]

            if checkDashesAlign(minterm1, minterm2) and checkMintermDifference(minterm1, minterm2): 
                mergedMinterm = mergeMinterms(minterm1, minterm2)
                if mergedMinterm not in primeImplicants: 
                    primeImplicants.append(mergedMinterm)

                numberOfMergers += 1
                merges[i] = True 
                merges[c] = True 
    for j in range(num_min): 
        if merges[j] == False and minterms[j] not in primeImplicants: 
            primeImplicants.append(minterms[j])
    if numberOfMergers == 0:
        return primeImplicants
    else: 
        return getPrimeImplicants(primeImplicants)


def mergeMinterms(minterm1, minterm2): 
    mergedMinterm = ''
    for i in range(len(minterm1)): 
        if minterm1[i] != minterm2[i]:
            mergedMinterm += '-'
        else: 
            mergedMinterm += minterm1[i]

    return mergedMinterm


def checkDashesAlign(minterm1, minterm2): 
    for i in range(len(minterm1)): 
        if minterm1[i] != '-' and minterm2[i] == '-':
            return False 
    return True 

def checkMintermDifference(minterm1, minterm2): 
    m1 = int(minterm1.replace('-','0'), 2)
    m2 = int(minterm2.replace('-','0'), 2)

    result = m1 ^ m2

    return result != 0 and (result & (result - 1)) == 0 

def createPrimeImplicantChart(primeImplicants, minterms): 
    primeImplicantChart = {}
    for i in range(len(primeImplicants)): 
        primeImplicantChart.update({primeImplicants[i]: ''})

    primeImplicantKeys = list(primeImplicantChart.keys())
    for i in range(len(primeImplicantKeys)): 
        primeImplicant = primeImplicantKeys[i]
        regularExpression = convertToRegularExpression(primeImplicant)
        for j in range(len(minterms)): 
            if re.fullmatch(regularExpression, minterms[j]): 
                primeImplicantChart[primeImplicant] += "1"
            else: 
                primeImplicantChart[primeImplicant] += "0"
    return primeImplicantChart

def convertToRegularExpression(primeImplicant): 
    regularExpression = '' 
    for i in range(len(primeImplicant)): 
        if primeImplicant[i] == '-': 
            regularExpression += r'[01]'
        else: 
            regularExpression += primeImplicant[i]

    return regularExpression

def getEssentialPrimeImplicants(primeImplicants, minterms): 
    essentialPrimeImplicants = []
    chart = createPrimeImplicantChart(primeImplicants, minterms)
    primeKeys = list(chart.keys())
    #Below is pseudocode adapted by Claude
    for j in range(len(minterms)):

        covers = []

        for i in range(len(primeKeys)):
            if chart[primeKeys[i]][j] == '1':
                covers.append(primeKeys[i])

        if len(covers) == 1:
            if covers[0] not in essentialPrimeImplicants:
                essentialPrimeImplicants.append(covers[0])

    return essentialPrimeImplicants, chart

#Petrick's method found via the Quine wikipedia page. Needed to get other implicants to cover all minterms

def petrickMethod(primeImplicants, minterms): 
    essentials, chart = getEssentialPrimeImplicants(primeImplicants, minterms)

    uncoveredColumns = []
    for i in range(len(minterms)): 
        covered = False 
        for primeImplicant in essentials: 
            if chart[primeImplicant][i] == '1':
                covered = True
        if not covered: 
            uncoveredColumns.append(i)

    if not uncoveredColumns: 
        return essentials

    notEssentials = list(set(primeImplicants).difference(essentials))
    clauses = []
    for i in uncoveredColumns: 
        clause = set()
        for pi in notEssentials: 
            if chart[pi][i] == '1':
                clause.add(pi)

        if not clause: 
            raise ValueError('minterm j cannot be covered')

        clauses.append(clause)

    products = [frozenset()]
    for clause in clauses: 
        newProducts = []
        for product in products: 
            for pi in clause: 
                newProducts.append(product | {pi})
        products = absorb(newProducts)
    best = min(products, key=cost)
    return essentials + list(best)

def literalCount(primeImplicant):
    return sum(1 for ch in primeImplicant if ch != '-')

def cost(product):
    return (len(product), sum(literalCount(p) for p in product))

def absorb(products):
    kept = []
    for p in products: 
        if not any(k <= p for k in kept): 
            kept.append(p)
    return kept
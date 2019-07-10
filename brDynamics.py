import sys
##main loop with inputs of uniform is 0, non is 1, set of thetas, if asynch (0) or synch (1)
##a "company" is a tuple of (performance, price)
def rounds(uniformMode = 0, thetas = None, selectMode):
    performances = [1, 3, 6, 8, 10]
    prices = [2, 4, 8, 16, 20]
    if thetas == None:
        thetas = list(range(0, 1001))
    companyA = (0,0)
    companyB = (0,0)
    oldA = (0,0)
    oldB = (0,0)
    turn = companyA
    pastValues = set()

    ##loop for the rounds (will check if oscillation later)
    while oldA != companyA and oldB != companyB and !(companyA in pastValues) and !(companyB in pastValues):
        if selectMode == 0:
            if turn == companyA:
                temp = companyA
                companyA = select(turn, performances, prices, thetas, companyB, uniformMode, 0)
                turn = companyB
                oldA = temp
                pastValues.add(oldA)
            else:
                temp = companyB
                companyB = select(turn, performances, prices, thetas, companyA, uniformMode, 1)
                turn = companyA
                oldB = temp
                pastValues.add(oldB)
        else:
            oldA = companyA
            oldB = companyB
            companyA = select(companyA, performances, prices, thetas, oldB, uniformMode, 0)
            companyB = select(companyB, performances, prices, thetas, oldA, uniformMode, 1)
            pastValues.add(oldA)
            pastValues.add(oldB)
        ##add other updates later


##selects new performace/price based on other company's performance/price
def select(company, performances, prices, thetas, other, uniformMode, evenIDs):
    maxProfit = sys.minint
    maxTup = company
    for p in performances:
        for t in prices:
            if uniformMode == 0:
                companyCustomers = numCustomersUniform(p, t, thetas, other)
            else:
                companyCustomers = numCustomers(p, t, thetas, other, evenIDs)
            cost = cost(p)
            if (companyCustomers * t) - cost > maxProfit:
                maxProfit = (companyCustomers * t) - cost
                maxTup = (p, t)
    return maxTup

##determines number of customers for a company with a certain performance and price
def numCustomers(performance, price, thetas, other, evenIDs):
    count = 0
    for theta in thetas:
        if (theta * performance) - price > 0 and (theta * performance) - price >(theta * other[0]) - other[1]:
            count += 1
        elif (theta * performance) - price == (theta * other[0]) - other[1]:
            if thetas.index(theta) % 2 == 0 and evenIDs == 0:
                count += 1
            elif thetas.index(theta) % 2 == 1 and evenIDs == 1:
                count += 1
                
    return count

##calculates cost for a company
def cost(performance):
    return (performace * performance) / (1 - performance)

##if uniform
def numCustomersUniform(performance, price, thetas, other):
    ratioCompany = price / performance
    if ratioCompany > 1 or ratioCompany <= 0:
        return 0
    ratioOther = other[1] / other[0]
    if ratioOther > 1 or ratioOther <= 0:
        return (1 - ratioCompany) * len(thetas)
    if ratioCompany == ratioOther:
        return ((1 - ratioCompany) * len(thetas)) / 2
    minRatio = min(ratioCompany, ratioOther)
    maxRatio = max(ratioCompany, ratioOther)
    if minRatio == ratioCompany:
        return (maxRatio - minRatio) * len(thetas)
    else:
        return (1 - maxRatio) * len(thetas)
    
    
    
    
        
        
    


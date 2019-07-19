import sys
import csv
##main loop with inputs of if asynch (0) or synch (1), uniform is 0, non is 1, set of thetas 
##a "company" is a tuple of (performance, price)
def rounds(selectMode, uniformMode = 0, thetas = None):
    performancesA = [6, 12, 18, 24, 30]
    pricesA = [3, 6, 9, 12, 15]
    performancesB = [18, 36, 54, 72, 90]
    pricesB = [9, 18, 27, 36, 45]
    if thetas == None:
        thetas = list(x / 1000 for x in range(0, 1000))
    if selectMode == 0:
        companyA = (-1,0)
        companyB = (0,0)
    else:
        companyA = (0,0)
        companyB = (10,8)
    oldA = (None,None)
    oldB = (None,None)
    turn = companyA
    pastValues = set()
    myTable()
    rnd = 1
    ##loop for the rounds

    while oldA != companyA and oldB != companyB and companyA not in pastValues and companyB not in pastValues:
        if selectMode == 0:
            if turn == companyA:
                temp = companyA
                companyA = select(turn, performancesA, pricesA, thetas, companyB, uniformMode, 0)
                turn = companyB
                oldA = temp
                pastValues.add(oldA)
            else:
                temp = companyB
                companyB = select(turn, performancesB, pricesB, thetas, companyA, uniformMode, 1)
                turn = companyA
                oldB = temp
                pastValues.add(oldB)
        else:
            oldA = companyA
            oldB = companyB
            companyA = select(companyA, performancesA, pricesA, thetas, oldB, uniformMode, 0)
            companyB = select(companyB, performancesB, pricesB, thetas, oldA, uniformMode, 1)
            pastValues.add(oldA)
            pastValues.add(oldB)

        if uniformMode == 0:
            aNC = numCustomersUniform(companyA[0], companyA[1], thetas, companyB)
            bNC = numCustomersUniform(companyB[0], companyB[1], thetas, companyA)
        else:
            aNC = numCustomers(companyA[0], companyA[1], thetas, companyB, 0)
            bNC = numCustomers(companyB[0], companyB[1], thetas, companyA, 1)
        nP = len(thetas) - aNC - bNC
        aProf = (aNC * companyA[1]) - cost(companyA[0], aNC)
        bProf = (bNC * companyB[1]) - cost(companyB[0], bNC)
        updateTable(rnd, companyA[0], companyA[1], companyB[0], companyB[1], cost(companyA[0], aNC), aProf, cost(companyB[0], bNC), bProf, aNC, bNC, nP)
        rnd += 1
         
        


##selects new performace/price based on other company's performance/price
def select(company, performances, prices, thetas, other, uniformMode, evenIDs):
    maxProfit = -(sys.maxsize) - 1
    maxTup = company
    for p in performances:
        for t in prices:
            if uniformMode == 0:
                companyCustomers = numCustomersUniform(p, t, thetas, other)
            else:
                companyCustomers = numCustomers(p, t, thetas, other, evenIDs)
            cst = cost(p, companyCustomers)
            if (companyCustomers * t) - cst > maxProfit:
                maxProfit = (companyCustomers * t) - cst
                maxTup = (p, t)
    return maxTup

##determines number of customers for a company with a certain performance and price
def numCustomers(performance, price, thetas, other, evenIDs):
    count = 0
    for theta in thetas:
        if (theta * performance) - price > 0 and (theta * performance) - price > (theta * other[0]) - other[1]:
            count += 1
        elif (theta * performance) - price == (theta * other[0]) - other[1]:
            if (theta* performance) - price > 0:
                if thetas.index(theta) % 2 == 0 and evenIDs == 0:
                    count += 1
                elif thetas.index(theta) % 2 == 1 and evenIDs == 1:
                    count += 1               
    return count

##calculates cost for a company
def cost(performance, customers):
    return performance * performance * (customers**(1/3)) 

##if uniform
def numCustomersUniform(performance, price, thetas, other):
    ##in order to not divide by zero, assume performance of 0 will lead to return 0
    if performance == 0:
        return 0
    else:
        ratioCompany = price / performance
    ##check if anyone will buy from company
    if ratioCompany > 1 or ratioCompany < 0:
        return 0
    ##in order to not divide by zero, assume performance of 0 will lead to return 0
    if other[0] == 0:
        ratioOther = sys.maxsize
    else:    
        ratioOther = other[1] / other[0]
    ##if no one buys from other 
    if ratioOther > 1 or ratioOther < 0:
        return int((1 - ratioCompany) * len(thetas))
    ##if equal split customers
    if ratioCompany == ratioOther:
        return int(((1 - ratioCompany) * len(thetas)) / 2)
    minRatio = min(ratioCompany, ratioOther)
    maxRatio = max(ratioCompany, ratioOther)
    if minRatio == ratioCompany:
        return int((maxRatio - minRatio) * len(thetas))
    else:
        return int((1 - maxRatio)* len(thetas))
    
##creates initial table
def myTable():
    with open('brDynamics.csv', mode='w') as brDynamics:
        brDynamics = csv.writer(brDynamics, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        brDynamics.writerow(['Round', 'A Performance', 'A Price', 'B Performance', 'B Price', 'A Cost', 'A Profit', 'B Cost', 'B Profit', 'A Num Customers', 'B Num Customers', 'Non Participating'])

def updateTable(rnd, aPerf, aPric, bPerf, bPric, aCost, aProf, bCost, bProf, aNC, bNC, nP):
    with open('brDynamics.csv', mode='a') as brDynamics:
        brDynamics = csv.writer(brDynamics, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        brDynamics.writerow([rnd, aPerf, aPric, bPerf, bPric, aCost, aProf, bCost, bProf, aNC, bNC, nP])
    
        



    
    
        
        
    


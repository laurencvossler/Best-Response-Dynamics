import sys
import csv
##main loop with inputs of if asynch (0) or synch (1), uniform is 0, non is 1, set of thetas 
##a "company" is a tuple of (performance, price)
def rounds(selectMode, uniformMode = 0, thetas = None):

    ##set initial values
    performancesA = [10, 11,12,13,14,15,16,17,18,19,20]
    pricesA = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14]
    performancesB = performancesA
    pricesB = [5.5, 6.5, 7.5, 8.5, 9.5, 10.5, 11.5, 12.5, 13.5, 14.5]
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
            ##if asynchronous, play turn of whichever company
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
            ##if synchronous, have both companies select new values
            oldA = companyA
            oldB = companyB
            companyA = select(companyA, performancesA, pricesA, thetas, oldB, uniformMode, 0)
            companyB = select(companyB, performancesB, pricesB, thetas, oldA, uniformMode, 1)
            pastValues.add(oldA)
            pastValues.add(oldB)

        ##extract values needed for table/csv
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
    ##loop to find performance and price combo that results in maximum profit
    for p in performances:
        for t in prices:
            if uniformMode == 0:
                companyCustomers = numCustomersUniform(p, t, thetas, other)
            else:
                companyCustomers = numCustomers(p, t, thetas, other, evenIDs)
            cst = cost(p, companyCustomers)
            ##save this combination if larger than maxProfit
            if (companyCustomers * t) - cst > maxProfit:
                maxProfit = (companyCustomers * t) - cst
                maxTup = (p, t)
    return maxTup

##determines number of customers for a company with a certain performance and price
def numCustomers(performance, price, thetas, other, evenIDs):
    count = 0
    ##loop through each theta and calculate utility to determine if would be a customer of this company
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

##calculates cost for a company based on performance and number of customers
def cost(performance, customers):
    return (performance**2) * (customers**(1/3))

##if uniform, way to find number of customers
##was not working so I have been using the non-uniform function 
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
    
##creates initial table/csv
def myTable():
    with open('brDynamics.csv', mode='w') as brDynamics:
        brDynamics = csv.writer(brDynamics, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        brDynamics.writerow(['Round', 'A Performance', 'A Price', 'B Performance', 'B Price', 'A Cost', 'A Profit', 'B Cost', 'B Profit', 'A Num Customers', 'B Num Customers', 'Non Participating'])

def updateTable(rnd, aPerf, aPric, bPerf, bPric, aCost, aProf, bCost, bProf, aNC, bNC, nP):
    with open('brDynamics.csv', mode='a') as brDynamics:
        brDynamics = csv.writer(brDynamics, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        brDynamics.writerow([rnd, aPerf, aPric, bPerf, bPric, aCost, aProf, bCost, bProf, aNC, bNC, nP])
    
        



    
    
        
        
    


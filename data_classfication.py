import pandas as pd
from datetime import datetime

classes = {}
# key = year, value = [success, failed, special]

def isDust(in_out: str) -> bool:
    if (in_out != ''): #check if string is not empty
        for input in in_out.split(';'):
            values = input.split(',')
            amount = int(values[1])
            if(amount >= 1 and amount <= 545): #check if is dust
                return True
        return False      
    return False

#infos := timestamp','blockId','txId','isCoinbase','fee','approxSize
#inputs := 0 or more input semicolon';' separated where input := addrId','amount','prevTxSpending',' position_of_output_in_prevTxSpending
#outputs := 1 or more output semicolon';' separated where output := addrId','amount',' scriptType
def tx_category(infos, inputs, outputs):
    addresses = set([])
    fee = int(infos[4]) #to check if tx is dust collecting
    tot_import = 0

    for input in inputs.split(";"):
        values = input.split(",")
        addr = int(values[0])
        addresses.add(addr)
        amount = int(values[1])
        tot_import += amount

    #0->sucess; 1->failed; 2->special(dust collecting or other)    
    if(fee == tot_import):
        return 2
    
    if(len(addresses) == 1):
        return 1

    return 0

def classification(file):
    for line in file:
        fields = line.split(":")
        infos = fields[0].split(",")
        timestamp = int(infos[0])
        year = datetime.fromtimestamp(timestamp).year
        outputs = fields[2]
        inputs = fields[1]
        if(len(inputs.split(";")) > 1 and isDust(inputs)):
            index = tx_category(infos, inputs, outputs)
            classes[year][index] += 1
    


def main():
    #intialize dict for temporal statistics
    for i in range(2010, 2022):
        classes[i] = [0, 0, 0]

    file = open("../dust_notSD.txt", 'r')
    classification(file)
    tot_0 = 0
    tot_1 = 0
    tot_2 = 0

    for year in classes:
        tot_0 += classes[year][0]
        tot_1 += classes[year][1]
        tot_2 += classes[year][2]
    
    print("Tx totali in cui viene speso il dust: ", tot_0 + tot_1 + tot_2)
    print("Attacco di successo: ", tot_0)
    print("Attacco fallito: ", tot_1)
    print("Transazioni speciali: ", tot_2)

    return 0

if __name__ == "__main__":
    main()
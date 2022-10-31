import pandas as pd
from datetime import datetime

def collect_tx(filename):
    txs = []
    with open(filename, 'r') as file:
        for line in file:
            line = line.strip()
            tx = int(line)
            txs.append(tx)
    return txs

def classify(df):
    df_t = df[df.amount > 545]
    txs_nod = set(df_t['TxId'].to_list())
    tot = len(set(df['TxId'].to_list()))
    print("TOT: ", tot)
    print("NOD: ", len(txs_nod))
    print("OD: ", len(set(df['TxId'].to_list())) - len(txs_nod)) #OD = TOTAL - NOD

def analyze_success(df):
    df_dust = df[df.amount <= 545]
    df_nonDust = df[df.amount > 545]
    print("MEDIA INPUT: ", df.groupby("TxId").count()['addrId'].mean())
    print("MODA INPUT: ", df.groupby("TxId").count().mode()['addrId'].iloc[0])
    dg = df.groupby("TxId").count()
    dg['amount'] = df[df.amount <= 545].groupby("TxId").count()['amount'] / df.groupby("TxId").count()['amount']
    print("PERCENTUALE DUST MEDIA: ", dg['amount'].mean()*100)
    print("MEDIA INDIRIZZI DIVERSI: ", df.groupby("TxId").agg({'addrId':'nunique'})['addrId'].mean())
    print("MODA INDIRIZZI DIVERSI: ", df.groupby("TxId").agg({'addrId':'nunique'})['addrId'].mode().iloc[0])
    
    return 0

def main():
    #special TxId
    tx_sp = collect_tx("../tx_special.txt")
    #spent success TxId
    tx_success = collect_tx("../tx_spent_dust.txt")

    spent = pd.read_csv("../data_csv/spent_dust.csv.xz", sep=',', header=0, compression='xz')
    sp = spent[~spent.spentTxId.isin(tx_success)]
    sp = sp[~sp.spentTxId.isin(tx_sp)]
    inputs = pd.read_csv("../data_csv/inputs.csv.xz", sep=',', header=0, compression='xz')
    inp_succ = inputs[inputs.TxId.isin(tx_success)] 
    inp_failed = inputs[inputs.TxId.isin(sp['spentTxId'].to_list())]

    #classify(inp_failed)
    #classify(inp_succ)
    analyze_success(inp_succ)

    return 0

if __name__ == '__main__':
    main()
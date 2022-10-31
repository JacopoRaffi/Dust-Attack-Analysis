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

def classify_failed(df):
    df_t = df[df.amount > 545]
    txs_nod = set(df_t['TxId'].to_list())
    tot = len(set(df['TxId'].to_list()))
    print("TOT: ", tot)
    print("NOD: ", len(txs_nod))
    print("OD: ", len(set(df['TxId'].to_list())) - len(txs_nod)) #OD = TOTAL - NOD

def analyze_success(df):
    df_dust = df[df.amount <= 545]
    df_nonDust = df[df.amount > 545]

    print("MEDIA INPUT DUST: ", df_dust.groupby("TxId").count()['addrId'].mean())
    print("MEDIA INPUT NOT-DUST: ", df_nonDust.groupby("TxId").count()['addrId'].mean())
    print("MODA GENERALE INPUT: ", df.groupby("TxId").count().mode()['addrId'].iloc[0])

    df_g = df_dust.groupby("TxId").agg({'addrId':'nunique'})
    df_g_n = df_nonDust.groupby("TxId").agg({'addrId':'nunique'})
    print("MODA INDIRIZZI NON DUST DIVERSI: ", df_g.mode()['addrId'].iloc[0])
    print("MODA INDIRIZZI DUST DIVERSI", df_g_n.mode()['addrId'].iloc[0])
    
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

    classify_failed(inp_failed)
    analyze_success(inp_succ)

    return 0

if __name__ == '__main__':
    main()
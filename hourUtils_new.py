import pandas as pd
from datetime import datetime
from datetime import date

def main(nona, anon, parameters={}): #Compute the utility in function of the date gap

    #pour tester temps d'exec
    start_time = datetime.now()

    hourdec = [1, 0.9, 0.8, 0.6, 0.4, 0.2, 0, 0.1, 0.2, 0.3, 0.4, 0.5,
               0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0, 0.2, 0.4, 0.6, 0.8, 0.9]

    df_anon = pd.read_csv(anon, sep="\t", header=None ).set_axis(['QId', 'dateAno', 'longitude', 'lattitude'], axis=1, inplace=False)
    df_orig = pd.read_csv(nona, sep="\t", header=None).set_axis(['Id', 'dateOrg', 'longitude', 'lattitude'], axis=1, inplace=False)
    length = len(df_orig)
    df_anon['dateAno'] = pd.to_datetime(df_anon['dateAno'], errors='coerce')
    df_orig['dateOrg'] = pd.to_datetime(df_orig['dateOrg'], errors='coerce')
    print("Starting...")  
    #optimisation en mémoire, on va travailler qu'avec 1 df['date']
    frames = [df_anon['QId'],df_orig['dateOrg'], df_anon['dateAno']]
    df_concat = pd.concat(frames,axis=1)
    df_concat = df_concat[df_concat['QId']!="DEL"]

    # normalement ça doit etre abs
    df_diff = df_concat['dateAno'].dt.hour - df_concat['dateOrg'].dt.hour
    lenBeforeDel = len(df_diff)
    df_diff = df_diff[df_diff!=0]

    lenDiff = lenBeforeDel - len(df_diff)

    #pour chaque ligne on prend l'element x de df_diff et on return l'element dans hourdec avec la position = x
    df_diff = df_diff.apply(lambda x: hourdec[x])
    df_diff = 1 - df_diff
    a = df_diff.sum() + lenDiff
    print(a/length)
    #pour tester temps d'exec
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    return a/length
    
    

#main(r"C:\Users\imadf\Desktop\insa\Projet\AnonyM212-\DB\V_2\base_org22.csv",r"C:\Users\imadf\Desktop\insa\Projet\AnonyM212-\DB\V_2\base_ano22.csv")
main(r"C:\Users\imadf\Desktop\insa\Projet\base_orgfinal.csv",r"C:\Users\imadf\Desktop\insa\Projet\soumission_1.csv")
import pandas as pd
from datetime import datetime
from datetime import date

def main(nona, anon, parameters={}): #Compute the utility in function of the date gap

    #pour tester temps d'exec
    start_time = datetime.now()

    df_anon = pd.read_csv(anon, sep="\t", header=None ).set_axis(['QId', 'dateAno', 'longitude', 'lattitude'], axis=1, inplace=False)
    df_orig = pd.read_csv(nona, sep="\t", header=None).set_axis(['Id', 'dateOrg', 'longitude', 'lattitude'], axis=1, inplace=False)
    length = len(df_orig)
    df_anon['dateAno'] = pd.to_datetime(df_anon['dateAno'], errors='coerce')
    df_orig['dateOrg'] = pd.to_datetime(df_orig['dateOrg'], errors='coerce')
    
    print("Starting...")
    
    if (df_anon['dateAno'].dt.isocalendar().week == df_orig['dateOrg'].dt.isocalendar().week).all():
        #optimisation en mémoire, on va travailler qu'avec 1 df 
        frames = [df_anon['QId'],df_orig['dateOrg'], df_anon['dateAno']]
        df_concat = pd.concat(frames,axis=1)
        # on supprime les lignes avec "DEL" en convservant l'ordre des lignes (ano et orig) car on indexe avec le QId (=pseudoId)
        df_concat = df_concat[df_concat['QId']!="DEL"]
        df_diff = abs(df_concat['dateOrg'].dt.weekday-df_concat['dateAno'].dt.weekday)

        #enlever les lignes où la difference est supperieur à 3 puisque ça vaut 0 (car chaque jour d'ecart vaut -1/3)
        df_diff = df_diff[df_diff<3]
        df_diff = 1 - df_diff/3
        a = df_diff.sum()
        print(a/length)
        #pour tester temps d'exec
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))
        return a/length
    
    else:
        print("Weeks must be the same in the two dataframes !")

#main(r"C:\Users\imadf\Desktop\insa\Projet\AnonyM212-\DB\V_2\base_org22.csv",r"C:\Users\imadf\Desktop\insa\Projet\AnonyM212-\DB\V_2\base_ano22.csv")
main(r"C:\Users\imadf\Desktop\insa\Projet\base_orgfinal.csv",r"C:\Users\imadf\Desktop\insa\Projet\soumission_1.csv")
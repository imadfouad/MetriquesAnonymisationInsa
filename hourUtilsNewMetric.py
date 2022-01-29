import pandas as pd
from datetime import datetime
from datetime import date

#si un changement est fait entre les heures actives / ou entre les heures inactives => -0.1 points pour chaque heure de difference
#si un changement est fait entre heure active et heure inactive ou le contraire => -0.2 points pour chaque heure de difference 
def f(x):
    if   (7 <= x[1] <= 20 and (21 <= x[2] <= 0 or 1 <= x[2] <= 6)) or (7 <= x[2] <= 20 and (21 <= x[1] <= 0 or 1 <= x[1] <= 6)) :
        a = abs(x[1] - x[2]) * 0.2 
    else :
        a = abs(x[1] - x[2]) * 0.1
    if a > 1:
        a = 1 
    return a

def main(nona, anon, parameters={}): #Compute the utility in function of the date gap

    #pour tester temps d'exec
    start_time = datetime.now()

    df_anon = pd.read_csv(anon, sep="\t", header=None ).set_axis(['QId', 'dateAno', 'longitude', 'lattitude'], axis=1, inplace=False)
    df_orig = pd.read_csv(nona, sep="\t", header=None).set_axis(['Id', 'dateOrg', 'longitude', 'lattitude'], axis=1, inplace=False)
    length = len(df_orig)
    df_anon['dateAno'] = pd.to_datetime(df_anon['dateAno'], errors='coerce')
    df_orig['dateOrg'] = pd.to_datetime(df_orig['dateOrg'], errors='coerce')
    
    print("Starting...")
    
    #optimisation en mémoire, on va travailler qu'avec 1 df['date']
    frames = [df_anon['QId'],df_orig['dateOrg'].dt.hour, df_anon['dateAno'].dt.hour]
    df_concat = pd.concat(frames,axis=1)
    df_concat = df_concat[df_concat['QId']!="DEL"]

    #modif pour changement de metrique : 
    scoree = df_concat.apply(f, axis=1)

    scoree = 1 - scoree
    a = scoree.sum()

    #pour tester temps d'exec
    end_time = datetime.now()
    print('Duration: {}'.format(end_time - start_time))
    print("resultat : " + str(a/length))
    return a/length
    
    

#main(r"C:\Users\imadf\Desktop\insa\Projet\AnonyM212-\DB\V_2\base_org22.csv",r"C:\Users\imadf\Desktop\insa\Projet\AnonyM212-\DB\V_2\base_ano22.csv")
main(r"C:\Users\imadf\Desktop\insa\Projet\base_orgfinal.csv",r"C:\Users\imadf\Desktop\insa\Projet\soumission_1.csv")
import pandas as pd
from datetime import datetime
from datetime import date


#si un jour de workdays est changé vers un autre jour de workdays ça coute 0.1 points (meme chose pour les jours de weekends entre eux) 
#si un jour de workdays est changé vers un jour de weekend ou le contraire ça coute 0.2 points
#  

def f(x):
    if  (0 <= x[1] <= 4 and 5 <= x[2] <= 6) or (0 <= x[2] <= 4 and 5 <= x[1] <= 6) :
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
    
    if (df_anon['dateAno'].dt.isocalendar().week == df_orig['dateOrg'].dt.isocalendar().week).all():
        #optimisation en mémoire, on va travailler qu'avec 1 df['date']
        frames = [df_anon['QId'],df_orig['dateOrg'].dt.weekday, df_anon['dateAno'].dt.weekday]
        df_concat = pd.concat(frames,axis=1)
        df_concat = df_concat[df_concat['QId']!="DEL"]

        #modif pour changement de metrique : 
        scoree = df_concat.apply(f, axis=1)
        scoree = 1 - scoree
        a = scoree.sum()
        print(a/length)
        #pour tester temps d'exec
        end_time = datetime.now()
        print('Duration: {}'.format(end_time - start_time))
        return a/length
    
    else:
        print("Weeks must be the same in the two dataframes !")

#main(r"C:\Users\imadf\Desktop\insa\Projet\AnonyM212-\DB\V_2\base_org22.csv",r"C:\Users\imadf\Desktop\insa\Projet\AnonyM212-\DB\V_2\base_ano22.csv")
main(r"C:\Users\imadf\Desktop\insa\Projet\base_orgfinal.csv",r"C:\Users\imadf\Desktop\insa\Projet\soumission_1.csv")
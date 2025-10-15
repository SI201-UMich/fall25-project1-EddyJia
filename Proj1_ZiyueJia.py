#Name: Ziyue Jia
#UMID: 19041337
#email: eddyjia@umich.edu
#I am working alone, no collaborators. All works done by myself.
#GenAI usage:
#The actual calculations and structure is different from the checkpoint. Refer to the code but not the checkpoint, thank you!
import csv
import os
os.chdir(os.path.dirname(__file__)) #Python reads the parent folder but not the project folder so I asked GenAI for help. This line fixes the problem.
def read_csv(fname):
    dl = []
    with open(fname, 'r') as f:
        r = csv.DictReader(f)
        for pgd in r:
            dl.append(pgd)
    return dl
rawdata = read_csv("penguins.csv")
#print(rawdata)

#Calculation 1: Calculate the average body mass of penguins, grouped by both species and sex.
cl1 = []# first clean the dataset
for i in rawdata:
    if i["body_mass_g"] != "NA" and i["species"] != "NA" and i["sex"] != "NA":
        cl1.append(i)

#Calculation 2: Calculate the correlation between flipper length and bill length, grouped by species.
cl2 = []# clean the dataset for calculation 2
for i in rawdata:
    if i["species"] != "NA" and i["flipper_length_mm"] != "NA" and i["bill_length_mm"] != "NA":
        cl2.append(i)

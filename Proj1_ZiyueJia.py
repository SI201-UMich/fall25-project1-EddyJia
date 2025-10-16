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
def calcavg(avgl):
    sum = 0
    op = 0
    for i in avgl:
        sum += float(i)
    op = round(sum / len(avgl),2)
    return op
    
def Calculation1(cldt):
    opl = []
    spl = []

    for i in cldt:
        if i["species"] not in spl:
            spl.append(i["species"])
    
    for i in spl:
        maled = {}
        femaled = {}
        malel = []
        femalel = []
        maled["species"] = i
        maled["sex"] = "Male"
        femaled["species"] = i
        femaled["sex"] = "Female"
        for x in cldt:
            if x["species"] == i:
                if x["sex"] == "male":
                    malel.append(x["body_mass_g"])
                if x["sex"] == "female":
                    femalel.append(x["body_mass_g"])
        mavg = calcavg(malel)
        fmavg = calcavg(femalel)
        maled["average body mass (g)"] = mavg
        femaled["average body mass (g)"] = fmavg
        opl.append(maled)
        opl.append(femaled)
    return opl

#print(Calculation1(cl1))

    

#Calculation 2: Calculate the correlation between flipper length and bill length, grouped by species.
cl2 = []# clean the dataset for calculation 2
for i in rawdata:
    if i["species"] != "NA" and i["flipper_length_mm"] != "NA" and i["bill_length_mm"] != "NA":
        cl2.append(i)

def calc_corr(fll, bll):  # function to calculate correlation between flipper length and bill length for each species
    n = len(fll)
    if n == 0:
        return 0
    mean_fl = calcavg(fll)
    mean_bl = calcavg(bll)
    num = 0
    denx = 0
    deny = 0
    for i in range(n):
        x = float(fll[i]) - mean_fl
        y = float(bll[i]) - mean_bl
        num += x * y
        denx += x ** 2
        deny += y ** 2
    if denx == 0 or deny == 0:
        return 0
    r = num / ((denx ** 0.5) * (deny ** 0.5))
    return round(r, 4)


def Calculation2(cldt2):  #perform the calculation using calc_corr
    spl = []
    for i in cldt2:
        if i["species"] not in spl:
            spl.append(i["species"])
    opl = []
    for sp in spl:
        fll = []
        bll = []
        for i in cldt2:
            if i["species"] == sp:
                fll.append(i["flipper_length_mm"])
                bll.append(i["bill_length_mm"])
        corr = calc_corr(fll, bll)
        opl.append({"species": sp, "correlation between flipper length and bill length": corr})
    return opl
#print(Calculation2(cl2))
def write_outputs(res1, res2):
    import csv
    # Calculation 1 results
    with open("Calculation1_results.csv", "w", newline="") as f1:
        w1 = csv.DictWriter(f1, fieldnames=["species", "sex", "average body mass (g)"])
        w1.writeheader()
        w1.writerows(res1)

    # Calculation 2 results in a another csv
    with open("Calculation2_results.csv", "w", newline="") as f2:
        w2 = csv.DictWriter(f2, fieldnames=["species", "correlation between flipper length and bill length"])
        w2.writeheader()
        w2.writerows(res2)

    print("Files 'Calculation1_results.csv' and 'Calculation2_results.csv' created successfully.")
def main():
    rc1 = Calculation1(cl1)
    rc2 = Calculation2(cl2)
    write_outputs(rc1, rc2)
main()

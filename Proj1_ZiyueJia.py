#Name: Ziyue Jia
#UMID: 19041337
#email: eddyjia@umich.edu
#I am working alone, no collaborators. All works done by myself.
#GenAI usage: Used GenAI to assist the coding of calculating correlation(help on math), used GenAI to help with certain minor difficulties(marked out), and used GenAI to assist writing the test cases.
#IMPORTANT: The function decompostion diagram is in the repository. Forgot to include it in the checkpoint.
#The actual calculations and structure is different from the checkpoint. Refer to the code but not the checkpoint, thank you!

import csv
import os
import unittest

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

    print("Have written the results of calculation1 into 'Calculation1_results.csv' and results of calculation2 into 'Calculation2_results.csv'.")
def main():
    rc1 = Calculation1(cl1)
    rc2 = Calculation2(cl2)
    write_outputs(rc1, rc2)
main()



class TestCalcs(unittest.TestCase):
    #Test calcavg()
    def test_calcavg_normal_list_of_str_numbers(self):
        self.assertAlmostEqual(calcavg(["1","2","3","4"]), 2.5, places=2)

    def test_calcavg_normal_decimals(self):
        self.assertAlmostEqual(calcavg(["3.5","4.5","5.0"]), 4.33, places=2)

    def test_calcavg_edge_single_value(self):
        self.assertAlmostEqual(calcavg(["7"]), 7.00, places=2)

    def test_calcavg_edge_empty_raises(self):
        with self.assertRaises(ZeroDivisionError):
            calcavg([])

    # Test Calculation1()
    def test_calculation1_normal_two_species(self):
        cldt = [
            {"species":"Adelie","sex":"male","body_mass_g":"4000"},
            {"species":"Adelie","sex":"female","body_mass_g":"3000"},
            {"species":"Adelie","sex":"male","body_mass_g":"4200"},
            {"species":"Chinstrap","sex":"female","body_mass_g":"3400"},
            {"species":"Chinstrap","sex":"male","body_mass_g":"3600"},
        ]
        res = Calculation1(cldt)
        res_map = {(d["species"], d["sex"]): d["average body mass (g)"] for d in res}
        self.assertAlmostEqual(res_map[("Adelie","Male")], 4100.00, places=2)
        self.assertAlmostEqual(res_map[("Adelie","Female")], 3000.00, places=2)
        self.assertAlmostEqual(res_map[("Chinstrap","Male")], 3600.00, places=2)
        self.assertAlmostEqual(res_map[("Chinstrap","Female")], 3400.00, places=2)

    def test_calculation1_normal_out_of_order_rows(self):
        cldt = [
            {"species":"Gentoo","sex":"female","body_mass_g":"4600"},
            {"species":"Adelie","sex":"male","body_mass_g":"3900"},
            {"species":"Gentoo","sex":"male","body_mass_g":"5000"},
            {"species":"Adelie","sex":"male","body_mass_g":"4100"},
            {"species":"Adelie","sex":"female","body_mass_g":"3300"},
        ]
        res = Calculation1(cldt)
        res_map = {(d["species"], d["sex"]): d["average body mass (g)"] for d in res}
        self.assertAlmostEqual(res_map[("Gentoo","Male")], 5000.00, places=2)
        self.assertAlmostEqual(res_map[("Gentoo","Female")], 4600.00, places=2)
        self.assertAlmostEqual(res_map[("Adelie","Male")], 4000.00, places=2)
        self.assertAlmostEqual(res_map[("Adelie","Female")], 3300.00, places=2)

    def test_calculation1_edge_minimal_per_species(self):
        cldt = [
            {"species":"Adelie","sex":"male","body_mass_g":"3800"},
            {"species":"Adelie","sex":"female","body_mass_g":"3200"},
        ]
        res = Calculation1(cldt)
        res_map = {(d["species"], d["sex"]): d["average body mass (g)"] for d in res}
        self.assertAlmostEqual(res_map[("Adelie","Male")], 3800.00, places=2)
        self.assertAlmostEqual(res_map[("Adelie","Female")], 3200.00, places=2)

    def test_calculation1_edge_decimal_strings(self):
        cldt = [
            {"species":"Chinstrap","sex":"male","body_mass_g":"3650.5"},
            {"species":"Chinstrap","sex":"female","body_mass_g":"3349.5"},
        ]
        res = Calculation1(cldt)
        res_map = {(d["species"], d["sex"]): d["average body mass (g)"] for d in res}
        self.assertAlmostEqual(res_map[("Chinstrap","Male")], 3650.50, places=2)
        self.assertAlmostEqual(res_map[("Chinstrap","Female")], 3349.50, places=2)

    # Test calc_corr()
    def test_calc_corr_normal_perfect_positive(self):
        fl = ["1","2","3","4"]
        bl = ["2","4","6","8"]
        self.assertAlmostEqual(calc_corr(fl, bl), 1.0, places=4)

    def test_calc_corr_normal_perfect_negative(self):
        fl = ["1","2","3","4"]
        bl = ["8","6","4","2"]
        self.assertAlmostEqual(calc_corr(fl, bl), -1.0, places=4)

    def test_calc_corr_edge_zero_variance_returns_zero(self):
        fl = ["5","5","5","5"]
        bl = ["1","2","3","4"]
        self.assertEqual(calc_corr(fl, bl), 0.0)

    def test_calc_corr_edge_empty_lists_returns_zero(self):
        self.assertEqual(calc_corr([], []), 0.0)

    # Test Calculation2()
    def test_calculation2_normal_two_species(self):
        cldt2 = [
            {"species":"Adelie","flipper_length_mm":"1","bill_length_mm":"2"},
            {"species":"Adelie","flipper_length_mm":"2","bill_length_mm":"4"},
            {"species":"Chinstrap","flipper_length_mm":"1","bill_length_mm":"8"},
            {"species":"Chinstrap","flipper_length_mm":"2","bill_length_mm":"6"},
            {"species":"Chinstrap","flipper_length_mm":"3","bill_length_mm":"4"},
            {"species":"Chinstrap","flipper_length_mm":"4","bill_length_mm":"2"},
        ]
        res = Calculation2(cldt2)
        m = {d["species"]: d["correlation between flipper length and bill length"] for d in res}
        self.assertAlmostEqual(m["Adelie"], 1.0, places=4)
        self.assertAlmostEqual(m["Chinstrap"], -1.0, places=4)

    def test_calculation2_normal_mixed_strength(self):
        cldt2 = [
            {"species":"Gentoo","flipper_length_mm":"10","bill_length_mm":"11"},
            {"species":"Gentoo","flipper_length_mm":"11","bill_length_mm":"12"},
            {"species":"Gentoo","flipper_length_mm":"12","bill_length_mm":"13"},
            {"species":"Gentoo","flipper_length_mm":"13","bill_length_mm":"14"},
            {"species":"Adelie","flipper_length_mm":"10","bill_length_mm":"1"},
            {"species":"Adelie","flipper_length_mm":"20","bill_length_mm":"2"},
        ]
        res = Calculation2(cldt2)
        m = {d["species"]: d["correlation between flipper length and bill length"] for d in res}
        self.assertTrue(0.9 <= m["Gentoo"] <= 1.0)
        self.assertAlmostEqual(m["Adelie"], 1.0, places=4)

    def test_calculation2_edge_single_row_species(self):
        cldt2 = [
            {"species":"Adelie","flipper_length_mm":"10","bill_length_mm":"20"},
            {"species":"Chinstrap","flipper_length_mm":"15","bill_length_mm":"30"},
            {"species":"Chinstrap","flipper_length_mm":"16","bill_length_mm":"32"},
        ]
        res = Calculation2(cldt2)
        m = {d["species"]: d["correlation between flipper length and bill length"] for d in res}
        self.assertEqual(m["Adelie"], 0.0)
        self.assertAlmostEqual(m["Chinstrap"], 1.0, places=4)

    def test_calculation2_edge_constant_values_species(self):
        cldt2 = [
            {"species":"Gentoo","flipper_length_mm":"10","bill_length_mm":"5"},
            {"species":"Gentoo","flipper_length_mm":"10","bill_length_mm":"6"},
            {"species":"Gentoo","flipper_length_mm":"10","bill_length_mm":"7"},
        ]
        res = Calculation2(cldt2)
        m = {d["species"]: d["correlation between flipper length and bill length"] for d in res}
        self.assertEqual(m["Gentoo"], 0.0)

if __name__ == "__main__":
    unittest.main()



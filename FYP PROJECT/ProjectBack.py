import pandas as pd, numpy as np
import random,requests
from bs4 import BeautifulSoup
from faker import Faker
import seaborn as sns
import math
from matplotlib import pyplot as plt
#initialize Faker
fake=Faker()


# Creating Dataset

age = []
height = []
glucose_level = []
diabetic = []
weight = []

n_names=2000
for n in range(n_names):
    age_cat = ['Below 40', '40 - 49','50 - 59','60+']
#     age_confidentiality_level=["High","Medium","Low","Very low"]
#     age_confidentiality_dict=dict(zip(age_cat,age_confidentiality_level))
    age_cats=np.random.choice(age_cat,n_names, p=[.50,.30,.15,.05])
#     age_claim_confidentiality_levels=[age_confidentiality_dict[age_cats[i]] for i in range(len(age_cats))]
    
    age.append(np.random.choice(np.arange(22,80,3)))
    
    sex_cat = ['Male','Female', 'Other']
    sex_confidentiality_level=["High","Hight","Very low"]
    sex_claim_reasons=np.random.choice(sex_cat,n_names, p=[.47,.47,.06])
    
    height_val = [147,150,152,155,157,160,163,165,168,170,173,175,178,180,183,185,188,191,193]
    height.append(np.random.choice(height_val))
    
    weight.append(np.random.choice(np.arange(40,105,5)))
    weight_cat = ['40 - 50','51 - 60','61 - 80','81 - 100','100+']
    weight_claim_reasons = np.random.choice(weight_cat,n_names,p=['.20','.30','.27','.21','.02'])
    
    physical_cat = ['High','Moderate','Low','Not at All']
    physical_claim_reason = np.random.choice(physical_cat,n_names,p=['.11','.44','.35','.10'])
    
    life_style_smoker =['No','Yes']
    life_style_claim = np.random.choice(life_style_smoker,n_names,p=['.88','.12'])
    
    member_diabetic = ['Father','Mother','Sister','Brother','None','Mother;Father','Father;Mother;Sister','Mother;Sister',
                      'Mother;Brother','Father;Sister','Father;Brother','Father;Mother;Brother','Father;Mother;Sister;Brother']
    member_diabetic_claim = np.random.choice(member_diabetic,n_names,p=['.30','.15','.03','.04','.38','.025','0.005','0.005',
                                                                        '.005','.01','0.02','0.01','0.02'])
    
    blood_cat = ['Normal','Elivated','High','Very High','Extremely High']
    blood_cat_claim = np.random.choice(blood_cat,n_names,p=['.60','.11','.15','.10','.04'])
    
    glucose_level.append(np.random.choice(np.arange(70,310,5)))
    
    
    
variables=[age,sex_claim_reasons,height,weight,
           physical_claim_reason,life_style_claim,member_diabetic_claim,blood_cat_claim,glucose_level]

df_diabetes=pd.DataFrame(variables).transpose()
df_diabetes.columns=["Age","Gender","Height (centimeters)","Weight (Kg)","Physical Activities",
                     "Life Style (Smoking)","Member Diabetic","Blood Pressure","Glucose Level (Random mg/dl)"]
    
    
    

df_diabetes['BMI'] = df_diabetes.apply(lambda x: round(x["Weight (Kg)"]/(math.pow(x['Height (centimeters)']/100,2)),1),axis=1)

# Who is diabetic 


def diabetic_logic(x):
    calculation = 0
    alert = 0
    info = 0
    success = 0
    if x['Glucose Level (Random mg/dl)'] < 140:
        success = 1
    elif x['Glucose Level (Random mg/dl)'] >=140 and  x['Glucose Level (Random mg/dl)'] < 199:
        info = 1
        calculation+=25
    else:
        alert = 1
        calculation+=50
        
    matching_meb = set(x['Member Diabetic'].split(";")) & set(['Mother','Father','Sister','Brother'])
    if len(matching_meb) > 0:
        for i in matching_meb:
            if i.lower() == "Father".lower():
                calculation+=7.5
            if i.lower() == "Mother".lower():
                calculation+=10
            if i.lower() == "Brother".lower():
                calculation+=3.75
            if i.lower() == "Sister".lower():
                calculation+=3.75
    if x['Blood Pressure'].lower() == 'High'.lower():
        calculation+=3
    elif x['Blood Pressure'].lower() == 'Very High'.lower():
        calculation+=4
    elif x['Blood Pressure'].lower() == 'Extremely High'.lower():
        calculation+=5
    

    if x['BMI'] >=25.0 and x['BMI'] <=29.9:
        # Overweight
        calculation+=4
    else:
#         Obesity
        calculation+=5 
        
    if x['Physical Activities'].lower()  == "Low".lower():
        calculation+=3
    elif x['Physical Activities'].lower() == "Not at all".lower():
        calculation+=5
        
    if x['Life Style (Smoking)'].lower() == "Yes".lower():
        calculation+=5
    
    if x['Age'] > 40 and x['Age'] < 60:
        calculation+=4
        
    elif x['Age'] > 60:
        calculation+=5
    if alert:
        return "Diabetic", calculation
            
    elif info:
        return "Prediabetic", calculation
    elif success:
        return "Non-diabetic", calculation

    
   df_diabetes['Diagnoses'],df_diabetes["Severity"] = zip(*df_diabetes.apply(lambda x: diabetic_logic(x), axis=1))

   df_diabetes.head(20)
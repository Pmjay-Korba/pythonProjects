

age_is = 99
sex_is = "Female"
newborn = "nn"


age_sex_newborn_is = str(age_is) +">"+ sex_is +">"+ newborn
print(age_sex_newborn_is)
age_sex_newborn_iss = ">".join([str(age_is), sex_is, newborn])
print(age_sex_newborn_iss)
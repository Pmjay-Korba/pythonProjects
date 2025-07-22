ll = '''10094	CASE/PS5/HOSP22G146659/CK6007159	Hospital Initiated	 
10095	CASE/PS6/HOSP22G146659/CK6509896	Hospital Initiated	 
10096	CASE/PS6/HOSP22G146659/CK6618794	Hospital Initiated	 
10097	CASE/PS6/HOSP22G146659/CK6349872	Hospital Initiated	 
10098	CASE/PS6/HOSP22G146659/CK6931474	Hospital Initiated	 
10099	CASE/PS6/HOSP22G146659/CK6960311	Hospital Initiated	 
10100	CASE/PS6/HOSP22G146659/CK6979729	Hospital Initiated	 
10101	CASE/PS6/HOSP22G146659/CK6816446	Hospital Initiated	 
10102	CASE/PS6/HOSP22G146659/CK6711691	Hospital Initiated	 
10103	CASE/PS6/HOSP22G146659/CK7106771	Hospital Initiated	 
10104	CASE/PS6/HOSP22G146659/CK7062904	Hospital Initiated	 
10105	CASE/PS6/HOSP22G146659/CK7053618	Hospital Initiated	 
10106	CASE/PS6/HOSP22G146659/CK7229429	Hospital Initiated	 
10107	CASE/PS6/HOSP22G146659/CK7220856    k'''

l = [z.split('\t')[1] for z in ll.split('\n')]
print(l)

for case_num in l:
    approve =  f'https://dkbssy.cg.nic.in/secure/incentivemodule/incentivemoduleApViewDME.aspx?ci={case_num}'
    print(approve)
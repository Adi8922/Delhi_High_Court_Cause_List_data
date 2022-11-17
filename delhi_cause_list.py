from bs4 import BeautifulSoup
import requests
import json
import sys
from datetime import datetime

session = requests.session()
url = "https://delhihighcourt.nic.in/xml_parse"


value = sys.argv[1]
now = datetime.strptime(value,"%d/%m/%Y")
date = now.strftime("%d").replace("0", "")
month = now.strftime("%m").replace("0", "")
year = now.strftime("%Y")

final_data_details = []

Headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en-US,en;q=0.9",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Content-Type": "application/x-www-form-urlencoded",
        "Host": "delhihighcourt.nic.in",
        "Origin": "https://delhihighcourt.nic.in",
        "Referer": "https://delhihighcourt.nic.in/reports/customised_cause_list",
        "sec-ch-ua": """Google Chrome";v="107", "Chromium";v="107", "Not=A?Brand";v="24""",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36"
        }

payload = {
        "ci_csrf_token": "",
        "drpMonth": month,
        "drpDay": date,
        "drpYear": year,
        "criteria": "FULL",
        "advocateNameAsSunstring": "",
        "courtnoId": "",
        "Submit": "Submit",
        "advName": "",
        "judgeName": ""
        }

responce = session.post(url, headers=Headers, data=payload, verify=False )
content = responce.content
soup = BeautifulSoup(content, "lxml")

total_data = soup.find_all("tr")

if len(total_data) == 0:                              
    print("Cause List Data is not available")
else:
    for data in total_data[1:]:
        data_details = {}
        try:                
            court_no = data.find("td").text   
        except:
            court_no = ""
        try:
            Judge_officer = data.find("td",{"id":"tcol2"}).text
        except:
            Judge_officer = ""
        try:
            location = data.find("td",{"id":"tcol3"}).text
        except:
            location = ""
        try:                
            item_no = data.find("td",{"id":"tcol4"}).text   
        except:
            item_no = ""
        try:
            case_no = data.find("td",{"id":"tcol5"}).text
        except:
            case_no = ""
        try:                
            case_type = data.find("td",{"id":"tcol5"}).text.split("With")[0].split(" ")[0]   
        except:
            case_type = ""
        try:
            case_id = data.find("td",{"id":"tcol5"}).text.split("With")[0].split(" ")[1]
        except:
            case_id = ""
        try:                
            final_case_id = case_id.split("/")[0]   
        except:
            final_case_id = ""
        try:
            case_year = case_id.split("/")[1]
        except:
            case_year = ""
        try:                
            matter_type = data.find("td",{"id":"tcol6"}).text    
        except:
            matter_type = ""
        try:
            party = data.find("td",{"id":"tcol7"}).text
        except:
            party = ""
        try:                
            petitioner = data.find("td",{"id":"tcol7"}).text.split("Vs")[0]   
        except:
            petitioner = ""
        try:
            respondent = data.find("td",{"id":"tcol7"}).text.split("Vs")[1] 
        except:
            respondent = ""
        try:                
            petitioner_advocate = data.find("td",{"id":"tcol8"}).text  
        except:
            petitioner_advocate = ""
        try:
            respondent_advocate = data.find("td",{"id":"tcol8"}).text
        except:
            respondent_advocate = ""
        
        data_details["Court No."] = court_no
        data_details["Judge/Officer"] = Judge_officer
        data_details["Location"] = location
        data_details["Item No"] = item_no
        data_details["Case No"] = case_no
        data_details["Case Type"] = case_type
        data_details["Case Id"] = final_case_id
        data_details["Case Year"] = case_year
        data_details["Matter Type"] = matter_type
        data_details["Party"] = party
        data_details["Petitioner"] = petitioner
        data_details["Respondent"] = respondent
        data_details["Petitioner Advocate"] = petitioner_advocate
        data_details["Respondent Advocate"] = respondent_advocate

        final_data_details.append(data_details)
    json_object = json.dumps(final_data_details)
    # print(json_object)

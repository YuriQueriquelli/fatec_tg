from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options  import Options
from bs4 import BeautifulSoup
from time import sleep
from datetime import date, timedelta
import os
from unicodedata import normalize
import csv

driver_location = "/usr/local/bin/chromedriver"
binary_location = "/usr/bin/google-chrome"

option = webdriver.ChromeOptions()
option.binary_location = binary_location

driver = webdriver.Chrome(executable_path=driver_location, chrome_options=option)

def listToString(s):  
    
    # initialize an empty string 
    str1 = " "  
    
    # traverse in the string   
    for ele in s:
        ele = ele.replace('\n', ' ').replace('\xa0',' ').replace(',',' | ').replace(';', ' | ')
        str1 = str1 + ' ' + ele + ' '
      
    # return string   
    return str1  

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

if __name__ == '__main__':
    from doctest import testmod
    testmod()

#today
today = date.today()

linkedins = ["https://br.linkedin.com/jobs/search?keywords=TI&location=&geoId=&trk=homepage-jobseeker_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0" , 
"https://br.linkedin.com/jobs/search?keywords=analise%20e%20desenvolvimento%20de%20sistemas&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0", 
"https://br.linkedin.com/jobs/search?keywords=Com%C3%A9rcio%20Exterior&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0", 
"https://br.linkedin.com/jobs/search?keywords=Gest%C3%A3o%20Empresarial&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0", 
"https://br.linkedin.com/jobs/search?keywords=Servi%C3%A7os%20de%20gest%C3%A3o&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0",
"https://br.linkedin.com/jobs/search?keywords=Log%C3%ADstica&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0",
"https://br.linkedin.com/jobs/search?keywords=Redes%20de%20Computadores&location=Brasil&geoId=106057199&trk=public_jobs_jobs-search-bar_search-submit&redirect=false&position=1&pageNum=0"]

subject = 0
row_list = [["Materia" , "Titulo", "link", "Descricao"]]

for linkedin in linkedins:
    driver.get(linkedin)
    sleep(3)

    subject = subject + 1

    if subject == 1:
        text_subject = "Análise e Desenvolvimento de Sistemas"
    elif subject == 2:
        text_subject = "Análise e Desenvolvimento de Sistemas"
    elif subject == 3:
        text_subject = "Comércio Exterior"
    elif subject == 4:
        text_subject = "Gestão Empresarial"
    elif subject == 5:
        text_subject = "Gestão de Serviços"
    elif subject == 6:
        text_subject = "Logística Aeroportuária"
    elif subject == 7:
        text_subject = "Redes de Computadores"

    #Find the load button and click
    i = 0
    while (i < 3):
        try:
            button = driver.find_element_by_xpath('//*[@id="main-content"]/section[2]/button')
            button.click()
            sleep(2)
            i = i + 1
            print('pinto')    
        except:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            i = i + 1  
            
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    
    vaga_linkedins = soup.findAll("a", {"class":"result-card job-result-card result-card--with-hover-state"})
    print(len(vaga_linkedins))
   
    for vaga_linkedin in vaga_linkedins:

        try:
            #extract job title
            vaga_linkedin_title = vaga_linkedin.h3.text.strip()

            #extract job link
            vaga_linkedin_link = vaga_linkedin.a["href"]
            print(vaga_linkedin_link)
        
            driver.get(vaga_linkedin_link)
            sleep(3)

            html_desc = driver.page_source

            soup_vaga_desc = BeautifulSoup(html_desc, 'html.parser')
            container_vaga_desc = soup_vaga_desc.findAll("div", {"class": "description__text description__text--rich"})
            text_desc = container_vaga_desc[0].get_text()
            words_text_desc = text_desc.split(' ')
            join_text_desc = listToString(words_text_desc)
        except:
            continue

        try:
            text_subject.replace(',', ' ')
            vaga_linkedin_title.replace(',', ' ')
            vaga_linkedin_link.replace(',', ' ')
            join_text_desc.replace(',', ' ')
            
            actual_list = [text_subject, vaga_linkedin_title, vaga_linkedin_link, join_text_desc]   
            row_list.append(actual_list)

        except:
            continue

with open('reports/linkedin_formated_data.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(row_list)


driver.quit()

#close file
file.close()
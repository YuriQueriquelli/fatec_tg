from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options  import Options
from bs4 import BeautifulSoup
from time import sleep
from datetime import date, timedelta
import os
from unicodedata import normalize
import csv

driver_location = "../chromedriver"
binary_location = "/usr/bin/google-chrome-stable"


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

#Open webdriver and site vagas.com

urls = ["https://www.vagas.com.br/vagas-de-ti", "https://www.vagas.com.br/vagas-de-An%C3%A1lise-e-Desenvolvimento-de-Sistemas", "https://www.vagas.com.br/vagas-de-Com%C3%A9rcio-Exterior", "https://www.vagas.com.br/vagas-de-Gest%C3%A3o-Empresarial", "https://www.vagas.com.br/vagas-de-Gest%C3%A3o-de-Servi%C3%A7os", "https://www.vagas.com.br/vagas-de-Log%C3%ADstica", "https://www.vagas.com.br/vagas-de-Redes-de-Computadores"]

subject = 1

row_list = [["Materia" , "Titulo", "link", "Descricao"]]

for url in urls:
    driver.get(url)
   
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
    while (i < 20):
        try:
            button = driver.find_element_by_xpath('//*[@id="maisVagas"]')
            button.click()
            sleep(2)
            i = i + 1
        except:
            i = 5000
        
    #html parsing
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')

    #find all jobs
    vaga_odd = soup.findAll("li", {"class":"vaga odd"})
    vaga_even = soup.findAll("li", {"class":"vaga even"})
    vaga_total = vaga_even + vaga_odd
    print(len(vaga_total))

    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    #loops over all vaga_total
    for vagas in vaga_total:
        #extract job title
        vaga_title = vagas.a["title"]

        #extract job link
        vaga_link = "https://www.vagas.com.br" + vagas.a["href"]

        #extract job description     
        driver.get(vaga_link)
        sleep(1)
        html_desc = driver.page_source
        soup_vaga_desc = BeautifulSoup(html_desc, 'html.parser')

        try:
            container_vaga_desc = soup_vaga_desc.find("div","job-tab-content job-description__text texto")
            vaga_desc_texto = container_vaga_desc.get_text()
            vaga_desc_texto = vaga_desc_texto.replace(",", "-").replace(";","-")
            vaga_desc_words = vaga_desc_texto.split(' ')
            join_vaga_desc = listToString(vaga_desc_words)
        
        except:
            join_vaga_desc  = "confidencial"
        
        try:
            text_subject.replace(',', ' ') 
            vaga_title.replace(',', ' ')
            vaga_link.replace(',', ' ')

            actual_list = [text_subject, vaga_title, vaga_link, join_vaga_desc]   
            row_list.append(actual_list.replace(";","-"))
    
        except:
            continue


with open('../db/vagas_formated_data.csv', 'w', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(row_list)


#close chrome
driver.quit()

#close file
file.close()
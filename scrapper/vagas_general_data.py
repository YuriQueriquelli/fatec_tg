from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options  import Options
from bs4 import BeautifulSoup
from time import sleep
from datetime import date, timedelta
import os
from unicodedata import normalize
import csv

#specify chrome locations
driver_location = "../chromedriver"
binary_location = "/usr/bin/chromium"

#add options
options = webdriver.ChromeOptions()
options.add_argument('--start-fullscreen')
options.binary_location = binary_location

driver = webdriver.Chrome(executable_path=driver_location, options=options)

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

#Open webdriver at site vagas.com
urls = ["https://www.vagas.com.br/vagas-de-campinas", "https://www.vagas.com.br/vagas-de-s%C3%A3o-paulo",
         "https://www.vagas.com.br/vagas-de-Indaiatuba", "https://www.vagas.com.br/vagas-em-sao-paulo"
         , "https://www.vagas.com.br/vagas-de-sorocaba", "https://www.vagas.com.br/vagas-de-Piracicaba"]

row_list = [[ "Titulo", "link", "Descricao"]]

for url in urls:
    driver.get(url)

    #Find the load button and click
    while True:
        try:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(2)
            button = driver.find_element_by_xpath('//*[@id="maisVagas"]')
            button.click()
            sleep(2)
        except:
            break
            
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
        try:
            #extract job title
            vaga_title = vagas.a["title"]

            #extract job link
            vaga_link = "https://www.vagas.com.br" + vagas.a["href"]

            #extract job description     
            driver.get(vaga_link)
            sleep(1)
            html_desc = driver.page_source
            soup_vaga_desc = BeautifulSoup(html_desc, 'html.parser')

        
            container_vaga_desc = soup_vaga_desc.find("div","job-tab-content job-description__text texto")
            vaga_desc_texto = container_vaga_desc.get_text()
            vaga_desc_texto = vaga_desc_texto.replace(",", "-").replace(";","-")
            vaga_desc_words = vaga_desc_texto.split(' ')
            join_vaga_desc = listToString(vaga_desc_words)
        
        except:
            continue
        
        try:
            vaga_title.replace(',', ' ')
            vaga_link.replace(',', ' ')

            actual_list = [vaga_title, vaga_link, join_vaga_desc]   
            row_list.append(actual_list.replace(";","-"))
    
        except:
            continue


with open('../db/reports/vagas_general_data.csv', 'a', newline='') as file:
    writer = csv.writer(file, delimiter=';')
    writer.writerows(row_list)



#close chrome
driver.quit()

#close file
file.close()
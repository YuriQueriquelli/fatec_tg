import psycopg2
from instance.config import config
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options  import Options
from bs4 import BeautifulSoup
from time import sleep
from datetime import date, datetime, timedelta
import datetime
import os
from unicodedata import normalize
import csv
from configparser import ConfigParser
import argparse

def listToString(s):  
    
    # initialize an empty string 
    str1 = " "  
    
    # traverse in the string   
    for ele in s:
        ele = ele.replace('\n', ' ').replace('\xa0',' ').replace(',',' | ').replace(';', ' | ')
        str1 = str1 + ' ' + ele + ' '
      
    # return string   
    return str1  

def insert_vaga_geral(vaga_link, vaga_title, vaga_nivel, join_vaga_desc, vaga_data):
    conn = None
    try:
        params =  config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""INSERT INTO vaga_geral(geral_url, geral_titulo, geral_cargo, geral_desc, geral_data, curso_id) VALUES(%s, %s, %s, %s, %s, %s)""",
                    (vaga_link, vaga_title, vaga_nivel, join_vaga_desc, vaga_data, 7))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')

def main():
    parser = argparse.ArgumentParser(description='choose some browser chrome or chromium')
    parser.add_argument('-b', action='store', dest='browser', help='write chrome or chromium')

    browser = parser.parse_args().browser

    if browser == 'chrome':
        binary_location = "/usr/bin/google-chrome-stable" 
    elif browser == 'chromium':
        binary_location = "/usr/bin/chromium"
    else:
        print('choose a valid browser! chrome or chromium')

    #specify chrome locations
    driver_location = "chromedriver"

    #add options
    options = webdriver.ChromeOptions()
    options.add_argument('--start-fullscreen')
    options.binary_location = binary_location

    driver = webdriver.Chrome(executable_path=driver_location, options=options)

    #today
    today = date.today()

    #Open webdriver at site vagas.com
    urls = ["https://www.vagas.com.br/vagas-de-campinas", "https://www.vagas.com.br/vagas-de-s%C3%A3o-paulo",
            "https://www.vagas.com.br/vagas-de-Indaiatuba", "https://www.vagas.com.br/vagas-em-sao-paulo", 
            "https://www.vagas.com.br/vagas-de-sorocaba", "https://www.vagas.com.br/vagas-de-Piracicaba"]

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

                #extract company name
                container_vaga_empresa = vagas.findAll("span", {"class": "emprVaga"})
                vaga_empresa = container_vaga_empresa[0].text.strip()


                #extract job publication date    
                container_data = vagas.findAll("span", {"class": "data-publicacao"})
                vaga_data = container_data[0].text

                #extract job relevance
                container_vaga_nivel = vagas.findAll("span", {"class": "nivelVaga"})
                vaga_nivel = container_vaga_nivel[0].text.strip()

                format_str = '%d/%m/%Y'


                print(vaga_data)

                if vaga_data == "Hoje" :
                    vaga_data = today.strftime("%Y/%m/%d")
                elif vaga_data == "Ontem" :
                    vaga_data = today.strftime("%Y/%m/%d")
                elif vaga_data == "H?? 2 dias" :
                    vaga_data = today.strftime("%Y/%m/%d")
                elif vaga_data == "H?? 3 dias" :
                    vaga_data = today.strftime("%Y/%m/%d")
                elif vaga_data == "H?? 4 dias" :
                    vaga_data = today.strftime("%Y/%m/%d")
                elif vaga_data == "H?? 5 dias" :
                    vaga_data = today.strftime("%Y/%m/%d")
                elif vaga_data == "H?? 6 dias" :
                    vaga_data = today.strftime("%Y/%m/%d")
                elif vaga_data == "H?? 7 dias" :
                    vaga_data = today.strftime("%Y/%m/%d")
                else:
                    vaga_data = datetime.datetime.strptime(vaga_data, format_str)
                    vaga_data = vaga_data.strftime("%Y/%m/%d")     

                print(vaga_data)
                  
            
                container_vaga_desc = soup_vaga_desc.find("div","job-tab-content job-description__text texto")
                vaga_desc_texto = container_vaga_desc.get_text()
                vaga_desc_texto = vaga_desc_texto.replace(",", "-").replace(";","-").replace("Descri????o"," ")
                vaga_desc_words = vaga_desc_texto.split(' ')
                join_vaga_desc = listToString(vaga_desc_words)
            
            except:
                continue
            
            try:
                vaga_title.replace(',', ' ')
                vaga_link.replace(',', ' ')

                #Insert BD
                insert_vaga_geral(vaga_link, vaga_title, vaga_nivel, join_vaga_desc, vaga_data)

                actual_list = [vaga_link, vaga_title, vaga_nivel, join_vaga_desc, vaga_data]   
                row_list.append(actual_list.replace(";","-"))
        
            except:
                continue


    with open('./db/reports/vagas_general_data.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(row_list)


    #close chrome
    driver.quit()

    #close file
    file.close()

if __name__ == '__main__':
    main()
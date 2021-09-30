import psycopg2
from instance.config import config
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options  import Options
from bs4 import BeautifulSoup
from time import sleep
from datetime import date, timedelta
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

def remover_acentos(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')


def insert_vaga_formatada(text_subject, vaga_title, vaga_link, join_vaga_desc):
    conn = None
    try:
        params =  config()
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        cur.execute("""INSERT INTO vaga_formatada(formatada_url, formatada_titulo, formatada_desc, curso_id) VALUES(%s, %s, %s, %s);""",
                    (text_subject, vaga_title, vaga_link, join_vaga_desc))
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


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
    urls = ["https://www.vagas.com.br/vagas-de-ti", "https://www.vagas.com.br/vagas-de-Com%C3%A9rcio-Exterior", "https://www.vagas.com.br/vagas-de-Gest%C3%A3o-Empresarial", "https://www.vagas.com.br/vagas-de-Gest%C3%A3o-de-Servi%C3%A7os", "https://www.vagas.com.br/vagas-de-Log%C3%ADstica", "https://www.vagas.com.br/vagas-de-Redes-de-Computadores"]

    subject = 1

    row_list = [["Materia" , "Titulo", "link", "Descricao"]]

    for url in urls:
        driver.get(url)   

        if subject == 1:
            text_subject = "Análise e Desenvolvimento de Sistemas"
        elif subject == 2:
            text_subject = "Comércio Exterior"
        elif subject == 3:
            text_subject = "Gestão Empresarial"
        elif subject == 4:
            text_subject = "Gestão de Serviços"
        elif subject == 5:
            text_subject = "Logística Aeroportuária"
        elif subject == 6:
            text_subject = "Redes de Computadores"

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
                vaga_desc_texto = vaga_desc_texto.replace(",", "-").replace(";","-").replace("Descrição"," ")
                vaga_desc_words = vaga_desc_texto.split(' ')
                join_vaga_desc = listToString(vaga_desc_words)
            
            except:
                join_vaga_desc  = "confidencial"
            
            try:
                text_subject.replace(',', ' ') 
                vaga_title.replace(',', ' ')
                vaga_link.replace(',', ' ')

                #Insert BD
                insert_vaga_formatada(vaga_link, vaga_title, join_vaga_desc, subject)
                
                #CSV file
                actual_list = [text_subject, vaga_title, vaga_link, join_vaga_desc]   
                row_list.append(actual_list.replace(";","-"))
        
            except:
                continue

        subject =  subject + 1


    with open('./db/vagas_formated_data.csv', 'a', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerows(row_list)


    #close chrome
    driver.quit()

    #close file
    file.close()

if __name__ == '__main__':
    main()
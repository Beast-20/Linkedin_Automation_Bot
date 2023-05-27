import requests, time, random
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import csv

# Keyword and number
keyword = input("Please Enter the keyword:- ")
number = int(input("Please enter number of profiles you want:- "))
while(True):
    if(number<=0):
        number =  int(input("Please enter valid number:- "))
    else:
        break 

# Candidate Login
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
browser = webdriver.Chrome(options=options)
browser.get('https://www.linkedin.com/uas/login')
file = open('config.txt.txt')
lines = file.readlines()
username = lines[0]
password = lines[1]
elementID = browser.find_element(By.ID, 'username')
elementID.send_keys(username)
time.sleep(random.uniform(3, 7))
elementPass = browser.find_element(By.ID, 'password')
elementPass.send_keys(password)
time.sleep(random.uniform(3, 7))
browser.find_element(By.CLASS_NAME,'login__form_action_container ').click()
time.sleep(random.uniform(20,25))
elementkeyword = browser.find_element(By.CLASS_NAME,'search-global-typeahead__input')
time.sleep(random.uniform(3, 7))


# Keyword Search
elementkeyword.send_keys(keyword)
elementkeyword.send_keys(Keys.ENTER)
time.sleep(random.uniform(10,15))
# Going to people section
button = browser.find_element(By.XPATH, "//button[text()='People']")
button.click()
profilesID = []
while(len(profilesID)<=number):
    SCROLL_PAUSE_TIME = 5

# Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while(True):
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
    time.sleep(random.uniform(5,10))
    soup = BeautifulSoup(browser.page_source,'html.parser')

    pageprofiles = soup.find('ul',{'class':'reusable-search__entity-result-list list-style-none'})
    # print(pageprofiles)
    profiles = pageprofiles.find_all('div',{'class':'entity-result__universal-image'})
    print(len(profiles))
    
    for profile in profiles:
        atag = profile.find('a',{'class':'app-aware-link scale-down'})
        link = atag.get('href')
        if(link not in profilesID):
            profilesID.append(link)
        if(len(profilesID)>=number):
            break
        
    if(len(profilesID)>=number):
        break
    time.sleep(random.uniform(3,5))
    try:
       next_button = browser.find_element(By.XPATH, "//button/span[text()='Next']")
       next_button.click()
    except:
        print("Over")

# --------------------------Break--------------------------------------#
with open('Database.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Network Link', 'Name', 'Location','Connections', 'Company', 'Position', 'Duration', 'Company Location', 'Course', 'Institution', 'Course Duration'])
for links in profilesID:
    link = links
    browser.get(link)
    name = 'NA'
    location = 'NA'
    comp = 'NA'
    posi = 'NA'
    duration = 'NA'
    connections = 'NA'
    course = 'NA'
    company_location = 'NA'
    college = 'NA'
    year = 'NA'

    # Scroll full page to get source code fully
    SCROLL_PAUSE_TIME = 7

    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    while True:
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")

        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

    # Data Scraping
    soup = BeautifulSoup(browser.page_source, 'html.parser')

    # Name and location Scraping
    try:
        name_div = soup.find('h1', {'class': 'text-heading-xlarge inline t-24 v-align-middle break-words'})
        name = name_div.get_text().strip()
    except:
        name = "Name not found"

    try:
        location_add = soup.find('span', {'class': 'text-body-small inline t-black--light break-words'})
        location = location_add.get_text().strip()
    except:
        location = "Location Not Found"

    # Number of connections
    try:
        connections_ul = soup.find('ul', {'class': 'pv-top-card--list pv-top-card--list-bullet'})
        connections = connections_ul.find('span', {'class': 't-bold'}).get_text().strip()
    except:
        connections = "Connections Not Found"

    # Position of Responsibility
    try:
        por = soup.find_all('section', {'class': 'artdeco-card ember-view relative break-words pb3 mt2'})
        i = 0
        for num in por:
            if num.find('div', {'id': 'experience'}) is not None:
                break
            i += 1
    except:
        print("continue")

    try:
      exist_comp = por[i].find('div', {'class': 'display-flex flex-column full-width align-self-center'})
    

    # Company
      compan = exist_comp.find('span', {'class': 'mr1 hoverable-link-text t-bold'})
      if compan is None:
          try:
              comp = exist_comp.find('span', {'class': 't-14 t-normal'}).find('span', {'class': 'visually-hidden'}).get_text().strip()
          except:
              comp = 'Company Not Found'
          try:
              posi = exist_comp.find('span', {'class': 'mr1 t-bold'}).find('span', {'class': 'visually-hidden'}).get_text().strip()
          except:
              posi = 'Position Not Found'
          try:
              duration = exist_comp.find('span', {'class': 't-14 t-normal t-black--light'}).find('span', {'class': 'visually-hidden'}).get_text().strip()
          except:
              duration = 'Duration Not Found'
          try:
              company_location = exist_comp.find_all('span', {'class': 't-14 t-normal t-black--light'})[1].find('span', {'class': 'visually-hidden'}).get_text().strip()
          except:
              company_location = "Location Not Found"
      else:
          try:
              comp = exist_comp.find_all('span', {'class': 'mr1 hoverable-link-text t-bold'})[0].find('span', {'class': 'visually-hidden'}).get_text().strip()
          except:
              comp = 'company not found'
          try:
              posi = exist_comp.find_all('span', {'class': 'mr1 hoverable-link-text t-bold'})[1].find('span', {'class': 'visually-hidden'}).get_text().strip()
          except:
              posi = 'Position Not Found'
          try:
              duration = exist_comp.find('span', {'class': 't-14 t-normal'}).find('span', {'class': 'visually-hidden'}).get_text().strip()
          except:
              duration = "Duration Not Found"
          try:
              company_location = exist_comp.find_all('span', {'class': 't-14 t-normal t-black--light'})[1].find('span', {'class': 'visually-hidden'}).get_text().strip()
          except:
              company_location = "Location Not Found"
    except:
        print("No experience Found")
    try:
        yearooo = soup.find_all('section', {'class': 'artdeco-card ember-view relative break-words pb3 mt2'})
        i = 0
        for num in yearooo:
            if num.find('div', {'id': 'education'}) is not None:
                break
            i += 1
        try:

          course = yearooo[i].find('span', {'class': 't-14 t-normal'}).find('span', {'class': 'visually-hidden'}).get_text().strip()
        except:
            course = "Not Found"

        # College
        try:
            college = yearooo[i].find('span', {'class': 'mr1 hoverable-link-text t-bold'}).find('span', {'class': 'visually-hidden'}).get_text().strip()
        except:
            college = "Not Found"

        # Course Year
        try:
            year = yearooo[i].find('span', {'class': 't-14 t-normal t-black--light'}).find('span', {'class': 'visually-hidden'}).get_text().strip()
        except:
            year = "Not found"
    except:
        print("Education Not Found")
    # Write data to the CSV file
    with open('Database.csv', 'a', newline='') as file:
     writer = csv.writer(file)
    # writer.writerow(['Network Link', 'Name', 'Location', 'Connections', 'Company', 'Position', 'Duration', 'Company Location', 'Course', 'Institution', 'Course Duration'])

    # Write the new row of data
     writer.writerow([f'=HYPERLINK("{link}")', name, location, connections, comp, posi, duration, company_location, course, college, year])

file.close()
browser.quit()


   


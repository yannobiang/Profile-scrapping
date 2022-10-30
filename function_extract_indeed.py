


def scrape_job_details(url, job_position = "Data Scientist", location = "Paris"):
  
  
  from selenium.webdriver import Firefox
  from selenium.webdriver.firefox.options import Options
  from selenium.webdriver import FirefoxProfile
  import pandas as pd
    
#     driver = webdriver.Firefox()
#     indeed_url = str(url)
#     driver.get(indeed_url)
    
    #################################################################### Ajout ###############################

  driver = webdriver.Firefox()
  indeed_url = str(url)
  driver.get(indeed_url)
  time.sleep(2)

  ## acceptation on the cookies

  click_conditions = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
  click_conditions.click()
  time.sleep(2)

  ## key word of searching 

  key_word = str(job_position)
  search_indeed = driver.find_element(By.XPATH, '//*[@id="text-input-what"]')
  search_indeed.send_keys(key_word)

  location = str(location)
  clique_search = driver.find_element(By.ID, 'text-input-where')
  clique_search.send_keys(location)

  driver.find_element(By.XPATH, """
      /html/body/div[1]/div[2]/div/span/div[4]/div[2]/div/div/div/div/form/button""").click()
  ## footer numero de page
  counts_idx = len(driver.find_elements(By.XPATH, '/html/body/main/div/div[1]/div/div/div[5]/div[1]/nav/div'))

  page = {}
  full_dataframe = pd.DataFrame()

  for i in range(1, 4):

      ## taken of index
      time.sleep(2)

      idx = driver.find_element(By.XPATH, f"""/html/body/main/div/div[1]/div/div/div[5]/div[1]/nav/div[{i}]""")
      idx.click()

  #################################################################### code to extract #####################

      soup = BeautifulSoup(driver.page_source, "html.parser")

      jobs_list = []

      for post in soup.select('.job_seen_beacon'):
          try:
              data = {
                  "job_title":post.select('.jobTitle')[0].get_text().strip(),
                  "company":post.select('.companyName')[0].get_text().strip(),
                  "rating":post.select('.ratingNumber')[0].get_text().strip(),
                  "location":post.select('.companyLocation')[0].get_text().strip(),
                  "date":post.select('.date')[0].get_text().strip(),
                  "job_desc":post.select('.job-snippet')[0].get_text().strip()

              }
              #print(data)
          except IndexError:
              continue          
          jobs_list.append(data)
          dataframe = pd.DataFrame(jobs_list)

      full_dataframe = pd.concat([full_dataframe, dataframe])

  return full_dataframe

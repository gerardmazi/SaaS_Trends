"""
DISTRIBUTION OF PEOPLE ROLES

@author:    Gerard Mazi
@date:      2020-04-25
@email:     gerard.mazi@gmail.com
@phone:     862-221-2477

"""

import pandas as pd
import numpy as np
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import re
import matplotlib.pyplot as plt

trend = pd.read_pickle('trend.pkl')

'=============================================================='

time_stamp = pd.to_datetime('2020-12-31')

userid = 'gerard.mazi@gmail.com'
password = ''
'=============================================================='

driver = webdriver.Chrome(r"chromedriver.exe")

driver.get('https://www.linkedin.com/login?fromSignIn=true&trk=guest_homepage-basic_nav-header-signin')
driver.maximize_window()
time.sleep(2)

# Login
driver.find_element_by_xpath('//*[@id="username"]').send_keys(userid)
driver.find_element_by_xpath('//*[@id="password"]').send_keys(password)
driver.find_element_by_xpath('//*[@class="login__form_action_container "]').click()
time.sleep(5)

# Run above first
#######################################################################################################################

comps = pd.read_csv('comps.csv').values.tolist()
trend_temp = pd.DataFrame(
    {
        'Date':     [],
        'Comp':     [],
        'FTE':      [],
        'Jobs':     [],
        'Role':     [],
        'Count':    []
    }
)

for c in range(len(comps)):

    driver.get(comps[c][0])

    # Company name
    t_comp = driver.find_element_by_xpath(
        '//*[@class="org-top-card-summary__title t-24 t-black  truncate"]'
    ).text
    time.sleep(1)

    # Navigate to jobs page
    try:
        driver.find_element_by_xpath(
            '//*[@class="org-page-navigation__items "]/li[4]'
        ).click()
        time.sleep(3)

        # Get open roles
        try:
            t_jobs = re.findall(
                r'\d+(?:,\d+)?',
                driver.find_element_by_xpath(
                    '//*[@class="org-jobs-job-search-form-module__headline"]'
                ).text
            )[1]
        except:
            t_jobs = re.findall(
                r'\d+(?:,\d+)?',
                driver.find_element_by_xpath(
                    '//*[@class="org-jobs-job-search-form-module__headline"]'
                ).text
            )

        # Navigate to people
        driver.find_element_by_xpath(
            '//*[@class="org-page-navigation__items "]/li[5]'
        ).click()
        time.sleep(3)

    except:
        driver.find_element_by_xpath(
            '//*[@class="org-page-navigation__items "]/li[3]'
        ).click()
        time.sleep(3)

        # Get open roles
        try:
            t_jobs = re.findall(
                r'\d+(?:,\d+)?',
                driver.find_element_by_xpath(
                    '//*[@class="org-jobs-job-search-form-module__headline"]'
                ).text
            )[1]
        except:
            t_jobs = re.findall(
                r'\d+(?:,\d+)?',
                driver.find_element_by_xpath(
                    '//*[@class="org-jobs-job-search-form-module__headline"]'
                ).text
            )

            # Navigate to people
        driver.find_element_by_xpath(
            '//*[@class="org-page-navigation__items "]/li[4]'
        ).click()
        time.sleep(3)

    # Get full time employees
    t_fte = re.findall(
        r'\d+(?:,\d+)?',
        driver.find_element_by_xpath(
            '//*[@class="t-20 t-black"]'
        ).text
    )

    # Next Page
    driver.find_element_by_xpath(
        '//*[@class="artdeco-carousel__navigation "]/div/button[2]'
    ).click()
    time.sleep(3)

    # Show more drop down
    driver.find_element_by_xpath(
        '//*[@class="org-people__show-more-button t-16 t-16--open t-black--light t-bold"]'
    ).click()
    time.sleep(3)

    # Roles Distribution
    t_role, t_count = [], []
    for i in range(2, 17):
        # Role
        t_role.append(
            driver.find_element_by_xpath(
                '//*[@class="artdeco-carousel__content"]/ul/li[3]/div/div/div/div[' + str(i) + ']/div/span'
            ).text
        )
        # Role count
        t_count.append(
            driver.find_element_by_xpath(
                '//*[@class="artdeco-carousel__content"]/ul/li[3]/div/div/div/div[' + str(i) + ']/div/strong'
            ).text
        )
    time.sleep(2)

    dist_temp = pd.DataFrame(
        {
            'Role':     t_role,
            'Count':    t_count
        }
    )

    main_temp = pd.DataFrame(
        {
            'Date':     time_stamp._short_repr,
            'Comp':     t_comp,
            'FTE':      t_fte,
            'Jobs':     t_jobs
        }
    )

    comb_temp = pd.concat([main_temp, dist_temp], axis=1).ffill()

    trend_temp = pd.concat([trend_temp, comb_temp], ignore_index=True)

trend = pd.concat([trend, trend_temp], ignore_index=True)

pd.to_pickle(trend, 'trend.pkl')
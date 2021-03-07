import sys
from selenium import webdriver
import time

teamOneName = input('Enter first team name: ')
teamTwoName = input('Enter second team name: ')

DRIVER_PATH = r'C:\Users\navir\Documents\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://kenpom.com/')

def getESPNTeamInfo():
    driver.get('https://www.espn.com/search/_/q/lsu')

    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)

    elem = driver.find_element_by_xpath('//*[@id="fittPageContainer"]/div[2]/div/div/div[3]/section[1]/div/ul')

    count = 1

    all_li = elem.find_elements_by_tag_name("li")
    for li in all_li:
        text = li.text

        text = text.replace('\n', ' ')

        if 'NCAAM' in text:
            break
    
        count += 1

    elementXPATH = '//*[@id="fittPageContainer"]/div/div/div/div[3]/section[1]/div/ul/div/div[' + str(count) + ']/li'

    driver.find_element_by_xpath(elementXPATH).click()

class Team:
    def __init__(self,name):
        self.name = name

    def getTeamDataInfo(self):
        for tableRow in driver.find_elements_by_xpath('//*[@id="ratings-table"]//tr'): 
            data = [item.text for item in tableRow.find_elements_by_xpath(".//*[self::td]")]
            if len(data) > 0 and data[0] == '100':
                break

            if len(data) > 0 and data[1] == self.name:
                self.teamRank = data[0]
                self.teamConference = data[2]
                self.teamRecord = data[3]
                self.teamOffensiveEfficiency = data[5]
                self.teamOffensiveRating = data[6]
                self.teamDefensiveEfficiency = data[7]
                self.teamDefensiveRating = data[8]
                self.strengthOfScheduleRating = data[14]

        print(self.teamRank, self.teamConference)

teamOne = Team(teamOneName)
teamTwo = Team(teamTwoName)

teamOne.getTeamDataInfo()
teamTwo.getTeamDataInfo()

getESPNTeamInfo()

#TODO Integrate the KENPON team to ESPN schedule to check if teams played eachother
#TODO potentially lower number of table rows searched
#TODO wins and losses against ranked teams and potentially largest win margin and loss margin
#TODO Check if teams have played eachother
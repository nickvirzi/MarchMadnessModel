import sys
from selenium import webdriver

teamOneName = input('Enter first team name: ')
teamTwoName = input('Enter second team name: ')

DRIVER_PATH = r'C:\Users\navir\Documents\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://kenpom.com/')

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

        print(self.teamRank, self.teamConference)

teamOne = Team(teamOneName)
teamTwo = Team(teamTwoName)

teamOne.getTeamDataInfo()
teamTwo.getTeamDataInfo()
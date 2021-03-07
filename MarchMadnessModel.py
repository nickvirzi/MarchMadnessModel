import sys
from selenium import webdriver
import time

teamOneName = input('Enter first team name: ')
teamTwoName = input('Enter second team name: ')

DRIVER_PATH = r'C:\Users\navir\Documents\ChromeDriver\chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH)
driver.get('https://kenpom.com/')

def goToESPN():
    driver.get('https://www.espn.com/')
    
    window_after = driver.window_handles[0]
    driver.switch_to.window(window_after)

class Team:
    def __init__(self,name):
        self.name = name

    def getTeamDataInfo(self):
        for tableRow in driver.find_elements_by_xpath('//*[@id="ratings-table"]//tr'): 
            data = [item.text for item in tableRow.find_elements_by_xpath(".//*[self::td]")]
            if len(data) > 0 and data[0] == '70':
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

    def getToESPNTeamInfo(self):
        driver.find_element_by_xpath('//*[@id="global-search-trigger"]').click()
        driver.find_element_by_xpath('//*[@id="global-search"]/input[1]').send_keys(self.name)
        driver.find_element_by_xpath('//*[@id="global-search"]/input[2]').click()

        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)

        time.sleep(2)

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

        window_after = driver.window_handles[0]
        driver.switch_to.window(window_after)

    def getTeamScheduleData(self, opponentName):

        self.rankedOpponentsStats = []
        self.lossesStats = []

        driver.find_element_by_xpath('//*[@id="global-nav-secondary"]/div[2]/ul/li[3]/a').click()

        for tableRow in driver.find_elements_by_xpath('//*[@id="fittPageContainer"]/div[2]/div[5]/div/div[1]/section/div/section/section/div/div/div/div[2]/table//tr'): 
            data = [item.text for item in tableRow.find_elements_by_xpath(".//*[self::td]")]
            
            if len(data) > 3:
                #Find Ranked Results 
                for char in data[1]:
                    if char.isdigit():
                        self.rankedOpponentsStats.append(data)
                        break

                #Finds Losses
                if data[2][0] == 'L':
                    self.lossesStats.append(data)

                #Check if played opponent
                if opponentName in data[1]:
                    self.hasPlayedOpponent = True
                    self.playedOpponentStats = data
                else:
                    self.hasPlayedOpponent = False

teamOne = Team(teamOneName)
teamTwo = Team(teamTwoName)

teamOne.getTeamDataInfo()
teamTwo.getTeamDataInfo()

goToESPN()

teamOne.getToESPNTeamInfo()
teamOne.getTeamScheduleData(teamTwo.name)

goToESPN()

teamTwo.getToESPNTeamInfo()

#TODO ESPN cannot find if they played each other unless name is exactly case sensitive typed
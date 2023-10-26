# -*- coding: utf-8 -*-
"""
@author: harsh
"""
import requests
from bs4 import BeautifulSoup
''' Using BeautifulSoup to scrape details from the web.

1) Finding Team Rankings

This code sends an HTTP GET request to the specified URL and stores the response in response. 
The print() function is used to print the response object. 
Furthermore, it also creates BeautifulSoup object from the response content and prints it. 
'''
url = "https://www.icc-cricket.com/rankings/mens/team-rankings/odi"
response = requests.get(url)
print(response)
soup = BeautifulSoup(response.content, "html.parser")
print(soup)


'''This finds the HTML table element with class table and prints it.'''
table = soup.find("table", {"class": "table"})
print(table)

'''It finds all the rows in the table and prints them.'''
rows = table.find_all("tr")
print(rows)

'''
Initializing empty lists for each column of data. 
It then loops through each row of the table (excluding the header row) and extracts the data 
from each cell. 
(Excluding Header Row:) -> Reason is because it stores heading of the table which I want to make 
my own and not use this.
The extracted data is appended to the appropriate list.

Here, row is the string containing the data. 
The split() method is used to split the string into a list of lines. 
The strip() method is used to remove any leading or trailing whitespaces from each line. 
The if statement is used to filter out any empty lines.
The resulting list data_list will contain the data without any whitespaces.

For Team_Name, I am saving full name with short name as INDIA(IND)
'''
Rank= []
Team_Name = []
Matches = []
Points = []
Ratings = []

for row in rows[1:]:
    row = row.text.strip()
    #print(row)
    data_list = [i.strip() for i in row.split('\n') if i.strip()]
    Rank.append(data_list[0])
    Team_Name.append(data_list[1]+"("+data_list[2]+")")
    Matches.append(data_list[3])
    Points.append(data_list[4])
    Ratings.append(data_list[5])
    #print(data_list)


''' creates a Pandas DataFrame from the extracted data and writes it to an Excel file.'''
import pandas as pd
ODI_Team_Rankings = pd.DataFrame({'Pos(Rank)':Rank, 'Team Name': Team_Name, 'Matches':Matches, 
                   'Points':Points, 'Ratings':Ratings})
ODI_Team_Rankings.to_excel("C:\\Users\\harsh\\Desktop\\Scrapping\\team_rank.xlsx")




# ------------------------------------------------------------------------

# Now finding out the Top 10 odi players

# 2) Batsman

''' 
 This code finds all the links with class rankings-menu__link inside an unordered list with
 class rankings-menu__list. 
 It then loops through each link and checks if its text matches "Player Rankings". 
 If it does, it constructs a URL for the ODI player rankings page.
 
 Here the href value present in the HTML context was incomplete. 
 I tried to find out full link, however I couldn't and instead of wasting more time, I decided to
 scrape the incomplete link and complete it on my own. 
 Hence, I had to append and prepend
'''

navigating_urls = soup.find("ul", attrs={'class':'rankings-menu__list'})
navigating_urls = navigating_urls.find_all("a", attrs={'class':'rankings-menu__link'})
print(navigating_urls)
print(navigating_urls[0].text)
for i in navigating_urls:
    if(i.text=="Player Rankings"):
        player_ranking_url = "https://www.icc-cricket.com" + i.get('href') + "/odi"
    
print(player_ranking_url)


''' 
This code sends an HTTP GET request to the player_ranking_url URL scraped from above steps
and stores the response in response. 
The print() function is used to print the response object.
'''
        
response = requests.get(player_ranking_url)
print(response)
player_soup = BeautifulSoup(response.content, "html.parser")
print(player_soup)


'''
Finds the HTML table element with class table rankings-card-table which stores details of
batsman and prints it.
'''
batsman_table = player_soup.find('table', {'class':'table rankings-card-table'})
print(batsman_table)

'''
This code finds all the rows in the table and prints the second row just to observe the output.
'''
batsman_rows = batsman_table.find_all("tr")
print(batsman_rows[1])

''' Initializing the variables to store details '''
Player_rank = []
Player_name = []
Player_team = []
Player_rating = []


'''
I am fetching the first rank player seperately because in the HTML context the 
first player is not present inside the table attribute, instead it is present in seperate div
section. Hence, to fetch first players details I am using the following code and formatting the 
data and appending it to the respective variables.
'''
first_player_details = player_soup.find('div', {'class':'rankings-block__top-player'}).text.strip()
print(first_player_details)
first_player_details = [i.strip() for i in first_player_details.split('\n') if i.strip()]
print(first_player_details)
Player_rank.append(first_player_details[0])
Player_name.append(first_player_details[2])
Player_team.append(first_player_details[3])
Player_rating.append(first_player_details[4])


'''
This code loops through each row of the table (excluding the header row) and extracts 
the rank, name, team, and rating from each cell. The extracted data is appended to the 
appropriate list.
'''
for row in batsman_rows[1:]:
    row = row.text.strip()
    #print(row)
    data_list = [i.strip() for i in row.split('\n') if i.strip()]
    Player_rank.append(data_list[0])
    Player_name.append(data_list[2])
    Player_team.append(data_list[3])
    Player_rating.append(data_list[4])
    
    
'''
This code creates a Pandas DataFrame from the extracted data and writes it to an Excel file.
'''
import pandas as pd
ODI_batsman_Rankings = pd.DataFrame({'Pos(Rank)':Player_rank, 'Player Name': Player_name, 
                                  'Player Team':Player_team, 'Player Ratings':Player_rating})
print(ODI_batsman_Rankings)    
ODI_batsman_Rankings.to_excel("C:\\Users\\harsh\\Desktop\\Scrapping\\batsman_rank.xlsx")




#-----------------------------------------------------------------------------------
# 2) Bowlers

'''
This code finds the HTML div element with class rankings-block__container and 
attribute data-cricket-role set to bowling and prints it.
'''
bowler_details = player_soup.find('div', attrs = {'class':'rankings-block__container', 
                                                 'data-cricket-role':'bowling'})
print(bowler_details)

'''
This code finds the HTML table element with class table rankings-card-table and prints it.
'''
bowler_table = bowler_details.find('table',{'class':'table rankings-card-table'})
print(bowler_table)


'''
This code finds all the rows in the table and prints the fourth row to check the details.
Also, initializes the variables
'''
bowler_rows = bowler_table.find_all("tr")
print(bowler_rows[3].text)
Player_rank = []
Player_name = []
Player_team = []
Player_rating = []


'''
I am fetching the first rank player seperately because in the HTML context the 
first player is not present inside the table attribute, instead it is present in seperate div
section. Hence, to fetch first players details I am using the following code and formatting the 
data and appending it to the respective variables.
'''
first_player_details = bowler_details.find('div', {'class':'rankings-block__top-player'}).text.strip()
print(first_player_details)
first_player_details = [i.strip() for i in first_player_details.split('\n') if i.strip()]
print(first_player_details)
Player_rank.append(first_player_details[0])
Player_name.append(first_player_details[2])
Player_team.append(first_player_details[3])
Player_rating.append(first_player_details[4])


'''
This code loops through each row of the table (excluding the header row) and extracts 
the rank, name, team, and rating from each cell. The extracted data is appended to the 
appropriate list.

Here, there are some players whose details include jump of rank by certain position. I am not 
looking to fetch this details from the data. Hence, I came up with a logic to find out the total 
length of the data_list containing details of player which helps me know that a player is having
rank jump information or not. The reason for this is because I am fetching certain index from the
data_list. Hence, when length is more than I am skipping one index and following with next otherwise,
not skipping the index and fetch details normally.
'''
for row in bowler_rows[1:]:
    row = row.text.strip()
    #print(row)
    data_list = [i.strip() for i in row.split('\n') if i.strip()]
    if(data_list.__len__()==6):
        Player_name.append(data_list[3])
        Player_team.append(data_list[4])
        Player_rating.append(data_list[5])
    else:
        Player_name.append(data_list[2])
        Player_team.append(data_list[3])
        Player_rating.append(data_list[4])
    Player_rank.append(data_list[0])
    
    
'''
This code creates a Pandas DataFrame from the extracted data and writes it to an Excel file.
'''
import pandas as pd
ODI_Bowler_Rankings = pd.DataFrame({'Pos(Rank)':Player_rank, 'Player Name': Player_name, 
                                  'Player Team':Player_team, 'Player Ratings':Player_rating})
print(ODI_Bowler_Rankings)    
ODI_Bowler_Rankings.to_excel("C:\\Users\\harsh\\Desktop\\Scrapping\\bowler_rank.xlsx")

#-----------------------------------------------------------------------------------
# 3) All-Rounders Rankings

'''
This code finds the HTML div element with class rankings-block__container and 
attribute data-cricket-role set to all_round and prints it.
'''
all_rounder_details = player_soup.find('div', attrs = {'class':'rankings-block__container', 
                                                 'data-cricket-role':'all_round'})
print(all_rounder_details)

'''
This code finds the HTML table element with class table rankings-card-table and prints it.
'''
all_rounder_table = all_rounder_details.find('table',{'class':'table rankings-card-table'})
print(all_rounder_table)

'''
This code finds all the rows in the table and prints the fourth row to check the details.
Also, initializes the variables
'''
all_rounder_rows = all_rounder_table.find_all("tr")
print(all_rounder_rows[8].text)
Player_rank = []
Player_name = []
Player_team = []
Player_rating = []


'''
I am fetching the first rank player seperately because in the HTML context the 
first player is not present inside the table attribute, instead it is present in seperate div
section. Hence, to fetch first players details I am using the following code and formatting the 
data and appending it to the respective variables. 
'''
first_player_details = all_rounder_details.find('div', {'class':'rankings-block__top-player'}).text.strip()
print(first_player_details)
first_player_details = [i.strip() for i in first_player_details.split('\n') if i.strip()]
print(first_player_details)
Player_rank.append(first_player_details[0])
if(data_list.__len__()==6):
    Player_name.append(first_player_details[3])
else:
    Player_name.append(first_player_details[2])
Player_team.append(first_player_details[3])
Player_rating.append(first_player_details[4])


'''
This code loops through each row of the table (excluding the header row) and extracts 
the rank, name, team, and rating from each cell. The extracted data is appended to the 
appropriate list.

Here, there are some players whose details include jump of rank by certain position. I am not 
looking to fetch this details from the data. Hence, I came up with a logic to find out the total 
length of the data_list containing details of player which helps me know that a player is having
rank jump information or not. The reason for this is because I am fetching certain index from the
data_list. Hence, when length is more than I am skipping one index and following with next otherwise,
not skipping the index and fetch details normally.
'''
for row in all_rounder_rows[1:]:
    row = row.text.strip()
    #print(row)
    data_list = [i.strip() for i in row.split('\n') if i.strip()]
    #print(data_list.__len__())
    if(data_list.__len__()==6):
        Player_name.append(data_list[3])
        Player_team.append(data_list[4])
        Player_rating.append(data_list[5])
    else:
        Player_name.append(data_list[2])
        Player_team.append(data_list[3])
        Player_rating.append(data_list[4])
    Player_rank.append(data_list[0])
    
    
'''
This code creates a Pandas DataFrame from the extracted data and writes it to an Excel file.
'''
import pandas as pd
ODI_All_Rounder_Rankings = pd.DataFrame({'Pos(Rank)':Player_rank, 'Player Name': Player_name, 
                                  'Player Team':Player_team, 'Player Ratings':Player_rating})
print(ODI_All_Rounder_Rankings)    
ODI_All_Rounder_Rankings.to_excel("C:\\Users\\harsh\\Desktop\\Scrapping\\all_rounder_rank.xlsx")
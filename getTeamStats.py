# Note: Python 3.9+ code compatibility
# import HTTP fetching library
import requests
import json
# declare API URL as constant
API_URL = "https://statsapi.web.nhl.com/api/v1"
# fetch player stats for Ovechkin, ask server to serve in
# JSON format
data = [0,0]
teamNum1 = 1
teamNum2 = 2

# response = requests.get(API_URL + "/schedule", params="?teamId=1&season=20222023&gameType=R")

  
def number_to_name(num):
  with open('team_ID.json', 'r') as f:
    data = json.load(f)
  for key, value in data.items():
    if num == value:
      return key

  return "key doesn't exist"
  
  
  
  
  
def get_head_2_heads():
  response = requests.get("https://statsapi.web.nhl.com/api/v1/schedule?teamId={}&season=20222023&gameType=R&detailedState=Final".format(teamNum1))
  scheddy = response.json()
  # with open('sched.json','w') as f:
  #   json.dump(scheddy,f)
  # f.close()
  gameIDS = []
  for i in range(len(scheddy["dates"])):
    awayTeam = scheddy["dates"][i]["games"][0]["teams"]["away"]["team"]["id"]
    homeTeam = scheddy["dates"][i]["games"][0]["teams"]["home"]["team"]["id"]
    gamePk = scheddy["dates"][i]["games"][0]["gamePk"]
    
    if(awayTeam == teamNum2 or homeTeam == teamNum2):
      gameIDS.append(gamePk);
      # print("away team {}".format(homeTeam))
      # print("home team {}".format(awayTeam))
      # print(gamePk)
      # print('\n')
        
  # print(gameIDS)
  
  for i in gameIDS:
    response = requests.get("https://statsapi.web.nhl.com/api/v1/game/{}/linescore".format(i))
    gameData = response.json()
    homeInfo = gameData["teams"]["home"]["team"]["name"], gameData["teams"]["home"]["shotsOnGoal"]
    awayInfo = gameData["teams"]["away"]["team"]["name"], gameData["teams"]["away"]["shotsOnGoal"]
    print("\nHEAD 2 HEAD NUMBER {}".format(i))
    print("away team:  \n\t{}\tshots on goal {}".format(*homeInfo))
    print("home team: \n\t{}\tshots on goal {}".format(*awayInfo))
      
    
def get_shot_stat():
  response = requests.get(API_URL + "/teams/{}/stats".format(teamNum1), params="?stats=statsSingleSeason")
  data[0] = response.json()
  response = requests.get(API_URL + "/teams/{}/stats".format(teamNum2), params="?stats=statsSingleSeason")
  data[1] = response.json()

  with open('data.json', 'w') as f:
    json.dump({"team1":data[0]['stats'][0]['splits'][0]['stat'], "team2":data[1]['stats'][0]['splits'][0]['stat']}, f, ensure_ascii=False) #gets the season data for team
  f.close()
  team1 =  data[0]['stats'][0]['splits'][0]['stat']["shotsAllowed"],data[0]['stats'][0]['splits'][0]['stat']["shotsPerGame"]
  team2 =  data[1]['stats'][0]['splits'][0]['stat']["shotsAllowed"],data[1]['stats'][0]['splits'][0]['stat']["shotsPerGame"]
  print("TEAM: {} \naverage shots agaisnt: {} \naverage shots for {}\n".format(number_to_name(teamNum1),*team1))
  print("TEAM: {} \naverage shots agaisnt: {} \naverage shots for {}\n".format(number_to_name(teamNum2),*team2))



get_shot_stat()
get_head_2_heads()







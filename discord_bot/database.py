import psycopg2
import requests
api_key = ''

conn = psycopg2.connect(database="postgres",
                        host="127.0.0.1",
                        user="postgres",
                        password="",
                        port="5433")

cursor = conn.cursor()

checkData = {}

def registerUserDB(player_summary: dict, discord_id: str, steam_id: str):
    try:
        status = player_summary['response']['players'][0]['personastate']
        status = bool(status)
        name = player_summary['response']['players'][0]['personaname']

        insert_query = """
            INSERT INTO users (name, discord_id, steam_id, status)
            VALUES (%s, %s, %s, %s)
            ON CONFLICT (discord_id, steam_id) DO NOTHING;
            """
    
        cursor.execute(insert_query, (name, discord_id, steam_id, status))

        conn.commit()
        print("Insert success")
        fetchStartdataDB()
    except psycopg2.Error as e:
        print(f"Database error: {e}")


#return current Infos about every User registered
def updateStatusHelper(ids: list):
    updatedInfo = []

    for item in ids:
        url = f'http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={item}'
        response = requests.get(url)
        if response.status_code == 200:

            # Parse the JSON response
            updatedInfo.append(response.json())
            
            

        else: 
            print("Failed to request from Steam")
    return updatedInfo


#loads all Users Online-Info
def fetchStartdataDB():
    global checkData
    cursor.execute("SELECT steam_id FROM users")
    updatedInfo = updateStatusHelper(cursor.fetchall())
    checkData = updatedInfo.copy()
    insert_query = """
                    UPDATE users SET status = %s WHERE steam_id = %s
                """
    for item in updatedInfo:
        
        status = item['response']['players'][0]['personastate']
        status = bool(status)
        steam_id = item['response']['players'][0]['steamid']
        cursor.execute(insert_query, (status, steam_id))

   
#check Differences // check if user went online
def checkDifferences():
    cursor.execute("SELECT steam_id FROM users")
    updatedInfo = updateStatusHelper(cursor.fetchall())
    toSend = []

    for personNew, personOld in zip(updatedInfo, checkData):
        print("hello")

        if personOld['response']['players'][0]['personastate'] == 1 and personNew['response']['players'][0]['personastate'] == 0:
            personOld['response']['players'][0]['personastate'] = 0

        if personOld['response']['players'][0]['personastate'] == 0 and personNew['response']['players'][0]['personastate'] == 1:
            personOld['response']['players'][0]['personastate'] = 1
            print("inside")
            toSend.append(personOld)

        

    return toSend


    
    



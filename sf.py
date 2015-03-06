import beatbox
import time

service = beatbox.PythonClient()
accounts = []
account_managers = []

def sfdcLogin():
  try:
    service.login('username', 'key')
    return True
  except:
    return False

def rules():
  cur_time = time.strftime("%Y-%m-%dT%H:%M:00.000+0000")


  query = "SELECT Name FROM RecentlyViewed WHERE TYPE = 'Account' AND LastViewedDate > " + cur_time + " ORDER BY LastViewedDate DESC"
  query_result = service.query(query)
  result = query_result['records']
 

  for res in result:
    account_name = str(res['Name'])
    accounts.append(account_name)
    query = "SELECT OwnerId FROM Account WHERE Name = '" + account_name + "'"

    owner_id = service.query(query)['records'][0]['OwnerId']
    query = "SELECT Name FROM USER WHERE Id = '" + owner_id + "'"

    manager = service.query(query)['records'][0]['Name']
    account_managers.append(manager)


def sendToWatchlist():
  a = ",".join(accounts)
  am = ",".join(account_managers)
  
  if len(a) > 0 or len(am) > 0:
    print a + " " + am 

  # TODO - make some watch call
 
if __name__ == "__main__":
  #print "\n\nSFDC Event Monitoring..."

  #print "Logging into SFDC..."
  conn = sfdcLogin()
  #print "  Success!"
  
  while conn:
    try:
      #print "\nMonitoring User Event Data..."
      rules()
      #print "  Success!"
    except:
      #print "  Failed."
      break

    try:
      #print "\nSending records to watchlist..."
      sendToWatchlist()
      #print "  Success!"
    except:
      #print "  Failed."
      break
    time.sleep(10)
    accounts = []
    account_managers = []

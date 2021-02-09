import os, sys, re, json, flask, ruamel

inventoryApp = flask.Flask('InventoryApp')

@inventoryApp.route('/')
def usage():
  return 'Simple inventory server to add new hosts'


#@inventoryApp.route('/newhost', methods=['GET', 'POST'])
@inventoryApp.route('/newhost', methods=['POST'])
def newhost():
  print('Data: ' + repr(flask.request.data), file=sys.stdout)
  jsonData = flask.request.get_json()
  print('JSON-Data: ' + json.dumps(jsonData), file=sys.stdout)
  if 'Name' not in jsonData or 'CPU' not in jsonData or 'RAM' not in jsonData:
    return 'ERROR: Some keys are missing!', 500
  hostname = jsonData['Name']
  threads  = jsonData['CPU']
  memory   = jsonData['RAM']
  return 'Created new host ' + hostname + ' with ' + str(threads) + ' processors and ' + str(memory) + ' memory'


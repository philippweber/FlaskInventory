import os, sys, re, json, flask, ruamel.yaml
#from flask import request, Response, send_file, stream_with_context
#try:
#  from StringIO import StringIO
#except ImportError:
#  from io import StringIO

inventoryApp = flask.Flask('InventoryApp')

@inventoryApp.route('/')
def usage():
  return 'Simple inventory server to add new hosts'


#@inventoryApp.route('/newhost', methods=['GET', 'POST'])
@inventoryApp.route('/newhost', methods=['POST'])
def newHost():
  def processHost():
    print('Data: ' + repr(flask.request.data), file=sys.stdout)
    jsonData = flask.request.get_json()
    print('JSON-Data: ' + json.dumps(jsonData), file=sys.stdout)
    if 'Name' not in jsonData or 'CPU' not in jsonData or 'RAM' not in jsonData:
      return 'ERROR: Some keys are missing!', 500
    hostname  = jsonData['Name']
    groupname = jsonData['Group']
    threads   = jsonData['CPU']
    memory    = jsonData['RAM']
    yaml      = ruamel.yaml.YAML()
    yaml.indent(mapping=2, sequence=4, offset=2)
    yaml.preserve_quotes = True
    yaml.boolean_representation = [ 'False', 'True' ]
    returnJson = { "status": "AddingHost", "msg": "Adding host " + hostname + " to hosts file" }
    yield json.dumps(returnJson)
    hostsFile = 'Inventory/fakeInv/hosts.yaml'
    try:
      with open(hostsFile, 'r+') as fd:
        hostsContent = fd.readlines()
        if '[' + groupname + ']' in hostsContent[-1]:
          hostsContent.append(hostname)
        else:
          for index, line in enumerate(hostsContent):
            if '[' + groupname + ']' in line:
              afterGroup = index + 1 
            if hostname in line:
              returnJson = { "status": "Failed", "msg": "Host " + hostname + " exists in " + hostsFile }
              yield json.dumps(returnJson)
              return
        hostsContent.insert(afterGroup, hostname)
        fd.seek(0)
        fd.writelines(hostsContent)
    except Exception as e:
      returnJson = { "status": "Failed", "msg": "Cannot write to " + hostsFile + "\nException:\n" + repr(e) }
      yield json.dumps(returnJson)
      return
    hostVars = ruamel.yaml.comments.CommentedMap({ "threads": threads, "memory": memory })
    hostVars.ca.comment = [ None, [ ruamel.yaml.tokens.CommentToken('---\n', ruamel.yaml.error.CommentMark(0), None) ] ]
    yaml.dump(hostVars, sys.stdout)
    #print(os.path.dirname(os.path.realpath(__file__)))
    #print(os.getcwd())
    hostVarsFile = 'Inventory/fakeInv/host_vars/' + hostname + '.yaml'
    returnJson = { "status": "FileCreation", "msg": "Creating host_vars in " + hostVarsFile }
    yield json.dumps(returnJson)
    try:
      with open(hostVarsFile, 'w+') as yamlFile:
        yaml.dump(hostVars, yamlFile)
    except Exception as e:
      returnJson = { "status": "Failed", "msg": "Cannot write to " + hostVarsFile + "\nException:\n" + repr(e) }
      yield json.dumps(returnJson)
      return
    returnJson = { "status": "Completed", "msg": "Created new host " + hostname + " in " + groupname + " with " + str(threads) + " processors and " + str(memory) + " memory" }
    yield json.dumps(returnJson)
  return flask.Response(flask.stream_with_context(processHost()))



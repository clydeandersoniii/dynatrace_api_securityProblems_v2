import json, requests, sys
credentials_security_path = "credentials_securityapi_v2.json"
credentials_entity_path = "credentials_entityapi_v2.json"

with open(credentials_security_path) as file:
    credentials_security = json.load(file)

with open(credentials_entity_path) as file:
    credentials_entity = json.load(file)

def GET_problem(problem_id,parameters=''):
    #If some parameters were passed, prepend a comma to make the comma-separated list
    if len(parameters) > 0:
        parameters += ','

    parameters += '+affectedEntities,+exposedEntities'

    encodedParams = requests.utils.quote(parameters)

    try:
        response = requests.get(credentials_security['environment'] + credentials_security['api'] + '/' + problem_id + '?fields=' + encodedParams, headers={'Authorization':'Api-Token ' + credentials_security['token']})

        if response.status_code != 200:
            print(str(response.status_code) + '\n' + str(response.content))
            sys.exit(0)

        output = response.content.decode('utf8')
        output = json.loads(output)

        return formatProblem(output)
    except Exception as e:
        print("GET_problem: " + str(e))

def GET_entityAPI(entitySelector):
    try:
        response = requests.get(credentials_entity['environment'] + credentials_entity['api'] + entitySelector, headers={'Authorization':'Api-Token ' + credentials_entity['token']})
    
        if response.status_code != 200:
            print(str(response.status_code) + '\n' + str(response.content))
            sys.exit(0)

        return response
    except Exception as e:
        print("GET_entityAPI: " + str(e))

def GET_processes(processIDs):
    ids = ''

    for id in processIDs: 
        ids = ids + '\"' + id + '\",'

    ids = ids[0:len(ids)-1]

    entitySelector = '?entitySelector=entityId(' + ids + ')&fields=fromRelationships.isProcessOf'

    response = GET_entityAPI(entitySelector)
    
    output = response.content.decode('utf8')
    output = json.loads(output)

    for entity in output['entities']:
        entity['fromRelationships']['isProcessOf'] = GET_host(entity['fromRelationships']['isProcessOf'][0]['id'])

    return output['entities']

def GET_host(hostID):
    entitySelector = '?entitySelector=entityId(' + hostID + ')'

    response = GET_entityAPI(entitySelector)

    output = response.content.decode('utf8')
    output = json.loads(output)

    return output['entities']

def formatProblem(problem):

    if len(problem['affectedEntities']) > 0:
        problem['affectedEntities'] = GET_processes(problem['affectedEntities'])

    if len(problem['exposedEntities']) > 0:
        problem['exposedEntities'] = GET_processes(problem['exposedEntities'])

    return problem

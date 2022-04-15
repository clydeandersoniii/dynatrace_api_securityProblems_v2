import json, requests, os, sys
import getProblemDetails
import argparse

# Initialize parser
parser = argparse.ArgumentParser(description = "This will pull a list of problems including the Affected and Exposed entities.\nOfficial documentation on arguments can be found at: https://www.dynatrace.com/support/help/shortlink/api-v2-security-problems-get-all#parameters")
 
helpMsg = "See the above link for documentation."

# Adding optional argument
parser.add_argument('-npk', '--nextPageKey', help=helpMsg, default='', metavar='nextPageKey')
parser.add_argument('-ps', '--pageSize', help=helpMsg, default='', metavar='pageSize')
parser.add_argument('-sps', '--securityProblemSelector', help=helpMsg, default='', metavar='securityProblemSelector')
parser.add_argument('-s', '--sort',help=helpMsg, default='', metavar='sort')
parser.add_argument('-fr', help=helpMsg, default='', metavar='from')
parser.add_argument('-t', '--to',help=helpMsg, default='', metavar='to')
parser.add_argument('-f', '--fields',help="Please see documentation on the 'fields' paremeter found here: https://www.dynatrace.com/support/help/shortlink/api-v2-security-problems-get-problem#parameters | \n affectedEntities and exposedEntities cannot be passed as valid arguments.", default='', metavar='fields')
parser.add_argument('-w', '--write', help='true (t) or false (f) (Default: true) \n Creates a problems.json file', default='true')
parser.add_argument('-p', '--print', help='true (t) or false (f) (Default: false) \n Print to the console.', default='false')

# Read arguments from command line
args = parser.parse_args()

parameters = ''

if len(args.to) > 0:
    parameters += '&to=' + args.to
if len(args.fr) > 0:
    parameters += '&from=' + args.fr
if len(args.sort) > 0:
    parameters += '&sort=' + args.sort
if len(args.securityProblemSelector) > 0:
    parameters += '&securityProblemSelector=' + args.securityProblemSelector
if len(args.pageSize) > 0:
    parameters += '&pageSize=' + args.pageSize
if len(args.nextPageKey) > 0:
    parameters += '&nextPageKey=' + args.nextPageKey

#remove the first ampersand and prepend a ? to start the query paremeters
parameters = '?' + parameters[1::]

credentials_security_path = "credentials_securityapi_v2.json"
credentials_entity_path = "credentials_entityapi_v2.json"

with open(credentials_security_path) as file:
    credentials_security = json.load(file)

strRequest = credentials_security['environment'] + credentials_security['api'] + parameters
print('\n' + strRequest + '\n')

try:
    response = requests.get(strRequest, headers={'Authorization':'Api-Token ' + credentials_security['token']})

    if response.status_code != 200:
        print(str(response.status_code) + '\n' + str(response.content))
        sys.exit(0)

    output = response.content.decode('utf8')
    output = json.loads(output)

    print("Next page key: " + output['nextPageKey'] + '\n')

    index = -1

    for problem in output['securityProblems']:
        index += 1
        #print(problem['securityProblemId'])
        output['securityProblems'][index] = getProblemDetails.GET_problem(problem['securityProblemId'],args.fields if len(args.fields) > 0 else '')

    if args.print == 't' or args.print == 'true':
        print(json.dumps(output))

    if args.write == 't' or args.write == 'true':
        file_output = open('problems.json','w')
        file_output.write(json.dumps(output))
        file_output.close()
except Exception as e:
    print('ERROR: ' + str(e))

# dynatrace_api_securityProblems_v2
## WHAT
This project uses python scripts and the Dynatrace API to retrieve security problems in a JSON format.  More specifically, it allows interacting with 
the [GET all problems](https://www.dynatrace.com/support/help/shortlink/api-v2-security-problems-get-all) endpoint while essentially replacing the funtionality of the
`fields` parameter with the more thorough `fields` parameter of the [GET a problem](https://www.dynatrace.com/support/help/shortlink/api-v2-security-problems-get-problem)
endpoint.

#### Example: `GET all problems` endpoint without modification
```
{
    "totalCount": 299,
    "pageSize": 1,
    "nextPageKey": "<nextPageKey>",
    "securityProblems": [
        {
            "securityProblemId": "<problem_id>",
            "displayId": "S-3",
            "status": "OPEN",
            "muted": false,
            "externalVulnerabilityId": "<external_id>",
            "vulnerabilityType": "THIRD_PARTY",
            "title": "Information Disclosure",
            "packageName": "<package_name>",
            "url": "<environment_url>/ui/security/problem/<problem_id>",
            "technology": "JAVA",
            "firstSeenTimestamp": 1620903510186,
            "lastUpdatedTimestamp": 1649973756886,
            "cveIds": [
                "<CVE>"
            ]
        }
    ]
}
```

#### Example: Same call using this project
```
{
    "totalCount": 299,
    "pageSize": 1,
    "nextPageKey": "<nextPageKey>",
    "securityProblems": [
        {
            "securityProblemId": "<problem_id>",
            "displayId": "S-3",
            "status": "OPEN",
            "muted": false,
            "externalVulnerabilityId": "<external_id>",
            "vulnerabilityType": "THIRD_PARTY",
            "title": "Information Disclosure",
            "packageName": "<package_name>",
            "url": "<environment_url>/ui/security/problem/<problem_id>",
            "technology": "JAVA",
            "firstSeenTimestamp": 1620903510186,
            "lastUpdatedTimestamp": 1649973756886,
            "cveIds": [
                "<CVE>"
            ],
            "affectedEntities": [
                {
                    "entityId": "<PROCESS_INSTANCE_ID>",
                    "displayName": "<friendly_display_name>",
                    "fromRelationships": {
                        "isProcessOf": [
                            {
                                "entityId": "<HOST_ID>",
                                "displayName": "<friendly_display_name>"
                            }
                        ]
                    }
                }
            ],
            "exposedEntities": [
                {
                    "entityId": "<PROCESS_INSTANCE_ID>",
                    "displayName": "<friendly_display_name>",
                    "fromRelationships": {
                        "isProcessOf": [
                            {
                                "entityId": "<HOST_ID>",
                                "displayName": "<friendly_display_name>"
                            }
                        ]
                    }
                }
            ],
            "muteStateChangeInProgress": false
        }
    ]
}
```

## WHY
With the release of Dynatrace's [Application Security platform](https://www.dynatrace.com/platform/application-security/) and recent vulnerabilities (log4j, spring4shell, etc.), it has become more important that companies and organizations
can keep track of how their environments are impacted. Being able to export the auto-detected vulnerabilities from Dynatrace with the affected/exposed entities saves time
on remediating and mitigating these vulnerabilities.

## HOW (does it work)
This leverages 3 Dynatrace APIs:
- [GET all problems](https://www.dynatrace.com/support/help/shortlink/api-v2-security-problems-get-all)
- [GET a problem](https://www.dynatrace.com/support/help/shortlink/api-v2-security-problems-get-problem)
- [GET entities list](https://www.dynatrace.com/support/help/shortlink/api-entities-v2-get-all-entities-list)

1. Pull a list of problems (`GET all problems`)
2. Take the ID from each problem and pass it to the `GET a problem` API and pull the affected and exposed entities IDs
3. Call the `GET entities list` with each entity ID and pull additional info including ID, display name, Host that the Process Instance runs on, and the display name

## HOW (to use)

### Prep
1. Install python
2. Pull repo
3. Create virtual env
4. Activate virtual env
5. Use `pip install -r requirements.txt` to install dependencies
6. Update both **credentials\_\*\_v2.json** files with appropriate environment URLs and API tokens

### Usage
`python3 getProblems.py --from now-7d --fields +riskAssessment`

Use `-p|--print true|t|false|f` to print to the console. Default: `false`

Use `-w|--write true|t|false|f` to write to a **problems.json** file. Default: `true`

`python3 getProblems.py -w false -p true`

### Help docs
```
$ python3 getProblems.py -h

usage: getProblems.py [-h] [-npk nextPageKey] [-ps pageSize]
                      [-sps securityProblemSelector] [-s sort] [-fr from]
                      [-t to] [-f fields] [-w WRITE] [-p PRINT]

This will pull a list of problems including the Affected and Exposed entities.
Official documentation on arguments can be found at:
https://www.dynatrace.com/support/help/shortlink/api-v2-security-problems-get-
all#parameters

optional arguments:
  -h, --help            show this help message and exit
  -npk nextPageKey, --nextPageKey nextPageKey
                        See the above link for documentation.
  -ps pageSize, --pageSize pageSize
                        See the above link for documentation.
  -sps securityProblemSelector, --securityProblemSelector securityProblemSelector
                        See the above link for documentation.
  -s sort, --sort sort  See the above link for documentation.
  -fr from              See the above link for documentation.
  -t to, --to to        See the above link for documentation.
  -f fields, --fields fields
                        Please see documentation on the 'fields' paremeter
                        found here: https://www.dynatrace.com/support/help/sho
                        rtlink/api-v2-security-problems-get-problem#parameters
                        | affectedEntities and exposedEntities cannot be
                        passed as valid arguments.
  -w WRITE, --write WRITE
                        true (t) or false (f) (Default: true) Creates a
                        problems.json file
  -p PRINT, --print PRINT
                        true (t) or false (f) (Default: false) Print to the
                        console.
```

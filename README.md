Proof
=====

Running this is really simple.

From the directory this README is in (the top level directory):

    docker-compose up -d

that will initialize the database, start it, and run the app, listening on port 5000.

When the app begins, it will add the user data from ./app/data/Proof_homework.csv and begin serving requests.

The API
-------

URL | Description
--- | -----------
`GET /` | show default image for the user (as defined in the configuration)
`GET /testip/<ip-address>` | show image determined for ip address given
`GET /rules` | list the rules as they exist
`POST /rule/move/<rule-name-2>/before/<rule-name-1>` | Move the rule named `rule-name-2` before the rule named `rule-name-1` in the rules list
`POST /rule/move/<rule-name-1>/after/<rule-name-2>` | Move the rule named `rule-name-2` after the rule named `rule-name-1` in the rules list


Note: Currently this is a pure demo mode implementation, there is no true persistence.
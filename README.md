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
---   -----------
/ | show default image for the user (as defined in the configuration)
/testip/<ip-address> | show image determined for ip address given
/rules | list the rules as they exist
/rule/move/<rule-name-2>/before/<rule-name-1> | moves rule rule-name2 before rule-name-1
/rule/move/<rule-name-1>/after/<rule-name-2> |  moves rule rule-name1 after rule-name-2





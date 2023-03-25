# Week 4 — Postgres and RDS

### Docker

My disk partiton is miserable. Lack of free space at root partiton makes me constantely prune docker images when I switch from bootcamp project to work project and back.

When I initially created partitons I didn't realize that docker is infinite eater of gigabytes.

(sigh) Had to buy a new ssd to make brand new installation.


### Postgres

Well, this is pretty familiar topic for all the developers. Quite easy start and run it in the docker container locally.

As I said previously, creating bash scripts took too much time, because I stopped the video and tried to create scripts on my own.

psql is handy but I prefer to use DBeaver for a long time.


### RDS

I like the way Andrew provisioning resources with aws cli command. Guess, in future he will say something like "and now let's terraformize it all, my little devops".

This is really better way to create services, AWS UI is constantely changing.

Security of RDS and other public resources is a huge topic. Actually, nothing should be public without good reason. On the other hand, makeing access to private resource is pain in the ass as well.

At least we have to create strong firewall rules.

And yeah, DON'T FORGET TO TURN OFF THE INSTACE (as I did)


### Postgres client for Python

Oh my gott, forgot to rebuid containers after adding psycopg to requirements.txt - no psycopg_pool lib found. Better to run everytime `docker compose up --build`

Watching part where Andrew is trying to return fetched rows for home activity page. How long it will take him to initialize poll with propriate row factory `pool = ConnectionPool(connection_url, kwargs={"row_factory": dict_row})`? I'm curious, how it works in Ruby.

Yyayks! Andrew went most ugly way - convert rows to json with Postgres. Sorry but not today.


### Lambda confirmation hook

Well, for testing we can actually use testing fuctionality of the Lambda instead of cre-creating user.

Security groups.I forgot to create rule to allow all connections inside the VPC. 

Say "Task timed out" again! I dare you! I double-dare you, motherf*****, say "Task timed out" one more goddamn time (c)


BTW, Andrew, do not insert user data to DB in splain text. Alwasy use param sustitution `cursor.execute(sql, (email, name)` Unless you like users with name like `'; drop table`
        )

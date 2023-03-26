# Week 4 — Postgres and RDS

### Docker

My disk partition is miserable. The lack of free space at the root partition makes me constantly prune docker images when I switch from bootcamp project to work project and back.

When I initially created partitions, I didn't realize that docker is the infinite eater of gigabytes.

(sigh) Had to buy a new ssd to make a brand new installation.


### Postgres

Well, this is a pretty familiar topic for all the developers. Quite an easy start, and run it in the docker container locally.

As I said previously, creating bash scripts took too much time because I stopped the video and tried to make scripts on my own.

psql is handy, but I prefer to use DBeaver for a long time.


### RDS

I like the way Andrew is provisioning resources with aws cli command. Guess, in the future, he will say something like, "and now let's terraformize it all, my little devops".

This is a really better way to create services, AWS UI is constantly changing.

The security of RDS and other public resources is a vast topic. Actually, nothing should be public without good reason. On the other hand, making access to private resource is a pain in the ass as well.

At least we have to create strict firewall rules.

And yeah, DON'T FORGET TO TURN OFF THE INSTANCE (as I did)


### Postgres client for Python

Oh my gott, I forgot to rebuild containers after adding psycopg to requirements.txt - no psycopg_pool lib found. Better to run every time `docker compose up --build`

I was watching the part where Andrew is trying to return fetched rows for the home activity page. How long will it take him to initialize poll with appropriate row factory `pool = ConnectionPool(connection_url, kwargs={"row_factory": dict_row})`? I'm curious about how it works in Ruby.

Yyayks! Andrew went the most ugly way - converting rows to json with Postgres. Sorry but not today.


### Lambda confirmation hook

Well, for testing, we can actually use the testing fuctionality of the Lambda instead of cre-creating a user.

Security groups. I forgot to create a rule to allow all connections inside the VPC. 

Say "Task timed out" again! I dare you! I double-dare you, motherf*****, say "Task timed out" one more goddamn time (c)


BTW, Andrew, do not insert user data to DB in plain text. Alwasy use param sustitution `cursor.execute(sql, (email, name)` Unless you like users with name like `'; drop table`. Oh, at the last video he fixed that.



### Activity handling

Sorry, I didn't follow step by step to Andrew's code. The ideas make sense, but implementing them is scaring me, lol. At least we made protection against sql injection. Sql module has to be refactored in the future. For now, it's better to leave it "as is".

Still, a lot of work to do here.

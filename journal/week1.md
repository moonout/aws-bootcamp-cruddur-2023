# Week 1 — App Containerization

## Homework Technical Assignments
Did all the staff. Marked all the checkboxes.
Pretty straightforward except for one point. Even using dockerization you might encounter unexpected issues. So did I.
The Frontend part worked like a charm when I ran it with Dockerfile. But when I ran all containers with docker compose, it threw an issue.
To be honest, I do not have experience with the js world - almost zero knowledge of tools and ideas, only common sense of js syntaxis.
npm makes me sad. During installation, npm writes modules to the same directory where scripts are located. This is fine until we mount this directory with docker compose because docker mounts dirs at late steps or something like that, so modules are not available during the start.

Here is the [thread on stackoverflow](https://stackoverflow.com/questions/30043872/docker-compose-node-modules-not-present-in-a-volume-after-npm-install-succeeds/32785014#32785014)

Easy-peasy, the best solution is to add a new directory. 
```
    volumes:
      - ./frontend-react-js:/frontend-react-js
      - /frontend-react-js/node_modules
```

Errr! (EACCES: permission denied, mkdir '/usr/app/node_modules/.cache) Welcome to Ubuntu!
[Here](https://stackoverflow.com/questions/67087735/eacces-permission-denied-mkdir-usr-app-node-modules-cache-how-can-i-creat) goes fix for the fix.

This line should be added to frontend Dockerfile
```
RUN mkdir -p node_modules/.cache && chmod -R 777 node_modules/.cache
```

## Security
I like all the tools that allow us to check vulnerabilities and notify about new versions automatically. And their integration to Github and CICD.

Unfortunately, due to lack of time, there needed to be more talk about best practices for keeping and passing secrets to containers.


## Pricing
I've got a billing alarm - I forgot to disable the key for CoudTrail. Now Amazon will charge me 6 cents. Well, after that, I watched the video with a warning to remember to disable the encryption key. 
Fair enough

## CDE
Useful sort of thing but not for everyone. Here in Ukraine, we used to have blackouts when ruzzia bombs our powerplants and infrastructure. 
I remember who it started, Cloud 9 was extremely unfriendly. Now they all mimic vs code and you can literally replace your local setup.

## Docker and docker compose
So many questions and magic under the hood. I work with them daily and still need to learn how it works beyond my usual workflow.

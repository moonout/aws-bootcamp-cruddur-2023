# Week 3 — Decentralized Authentication

### Authentication and Authorization

Absolutely complicated topic. Each of the services require hard work to understand and implement, even if you use existing frameworks.

OAuth - protocol which allows services (sites) to access user profiles on other services by delegating authentication. This allows user to use some resources without passing his credentials. Main purpose of this protocol is authorization.

SAML - this protocol describes authentication process. It is used in SSO applications such as Okta. 

OpenId  - guess, this allows to do both auths: authentication and authorization. Just one more standard

### AWS Cognito

Cognito is a service for two things - user pool and identity pool.

User pool allows to get rid of boilerplate of users management. Application can create new users, authenticate, log in, recreate passwords, validate emails, provide additional security with 2FA.

Cognito identity pool is similar service but it allows users to assume IAM roles - access various AWS resources.


### AWS Amplify

Amplify is the framework which helps to use the whole power of Cognito. Used both with frontend and backend.


### Actual homework

#### Cognito

This was the most challenging part :) Theory is good but we have to implement user management with our application.

I have to re-create user pool once again and again due to issues with configuration (which cannot be edited). The error messages were confusing and meaningless, all I got was that email cannot be used as login and vice versa. Even if I used same fields as Andrew. And these issues are not mentioned in Discord channel. Guess none of students explored them.

>I've seen things you people wouldn't believe... Attack ships on fire off the shoulder of Orion... I watched C-beams glitter in the dark near the Tannhäuser Gate.

#### Amplify

This part was also a bit confusing only because I familiar with js syntax but not with React and frontend. Should take some simple course.

Thankfully, everything works as expected.

Backend was much easier. Andrew stuck with primitive issues although I always thought that Ruby is bit more complex than Python.

For processing tokens I found library called `cognitojwt`, instead of copy-pasting some weird code. No surprize Andrew found same library in the next video.


#### UI improvement

It should be done someday! And today is the day. I reproduced same steps as Andrew did. And this is not enough.
I'm not a designer, this is completely black whole for me. So todo: find some good css library, nice example and implement complete redesign.
But not today. It was an bad week for me and my country. 

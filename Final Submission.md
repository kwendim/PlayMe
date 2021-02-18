# PlayMe

Web Software development project: PlayMe, an online game store for JavaScript games

## Team Members

1. Kidus Mammo - 727820
2. Mohammad Elhariry - 727451
3. Sonika Ujjwal - 728285

## Implemented Features

### Mandatory features
1. Authentication
    Our system uses the django auth to register and authenticate developers and players. All functionalities listed are implemented, including email verification through the django console (also available on heroku log) to verify the email of a user. (200 points) 

2. Basic player Functionalities
    Our website allows users to purchase games using the courses mockup payment service. Cancellation, success and error are handled properly to not allow a user to purchase a game without paying for it.

    The user can sort through available games by using the search bar or the categories filter. Having purchased a game, the user can proceed to play a game and register the scores for his game. A user can only play games he/she has purchased. (300 points)

3. Basic Developer functionalities
    A developer can use his/her account to both purchase other developer games and upload his own. A developer can upload a game by providing basic inforamtion about the game and a link to the game. The developer can edit and delete the game after it has first been uploaded; and can only do this to only his own uploads. 

    The develoepr has a dashboard to view statistics about the number of game purchases for his uploads. Security restrictions are also in place. (200 points)

4. Game/service Interaction
    A user can submit his/her scores for a particular game they have purchased and played. They can submit their score as many times as they'd like and a history of their scores is maintained. In addition, they can save and load the state of the game. 

    The scores submitted from all users are used to generate a leaderboard that display the highest score of a particular game. Having viewed this in the leaderboard, a player can also view the three high scores of a game and his own three highest scores while playing a game. (200 points)

5. Quality of Work
    The web software was developed utilizing an MVC principle. There is a separation of concerns with forms, models, views and templates being used in the intended purpose. Comments are added on the code to further elaborate the purposes a function or a particularly confusing line does. 
    
    The user experience was also considered in development, with much focus going into the front end of our web software. By utilizing bootstrap, we have made the site friendly for any device. 

    Though there were no programatical tests done on the code, the developers have spent extra effort in manually testing the website to help avoid bad user experience, and website failure. (80 points)

6. Non-functional requirements
    The project plan provided an excellent skeleton for the development of the website. In its esssence, a project plan can not forsee all the details of implementation and as such, we had to add new views, templates and make modifications to the models during the course of the project work. There were no significantlly challenging aspects of the work that could not be solved with the extensive amount of support there is for django. The course work was divided equally among the memebers and gitlab was utilized for merging. (200 points)

### Extra features

1. Save/load and resolution
    Our web software allows a player to save and load a game state in addition to submitting scores. Furthermore, the game supports resolution messaging, which is displayed in the play page accordingly. (100 points)

2. 3rd party login
    our website supports signup and login using Gmail and github (100 points)

3. Own Game
    We have implemented a simple educational game that asks loads two random numbers and a mathematical operation, and the user has to fill in the result. User gets points for correct answers, and looses if he looses 3 times in a row. (100 points)

4. Mobile Friendly
    By utilizing bootstrap, the website scales properly for devices of all size. (50 points)

5. Social media sharing
    The website allows sharing a game on facebook and Google plus (50 points)

  
## Division of Work

The work was divided based on the three important aspects of the project. The game messaging, backend data storage/payment and front end development

    1. Mohammad Elhariry :- Game messaging, own game, heroku deployment
    2. Kidus Mammo :- Backend development, game upload, payment system
    3. Sonika Ujjwal :- Front end development, leaderboard, developer dashboard

    The above description provides the official roles designated for the members of the team. However, througout the course work, members had to collaborate with each other in order to have a better understaning of the requirements of their role and completley understand each aspect of the work needed to make the complete website. There was 


## Instructions on how to use the website

Heroku Link :-  demo-playme.herokuapp.com

The home page displays the list of all games available on the website. From here, a user can search, categorize, view more information about the games, and view the leaderboard without having to login. There is a login and sign up buttons available on the top right corner. 

Afer having signed up or logged in, the user can find his/her purhcased games in the "My Games" link on the navigation bar. In addition, on the top right of the navigation bar, the user can find a drop down menu that is stylized with the first and last name of the user. When clicking this, a user can access the dashboard, game uploading page, and choice to logout if the user is a developer. If user is only a player, there will only be the logout button. 

A developer can upload a game from the upload page. He will then be able to see his game in the dashboard where he/she can view the purchase statistics of the game. In addition, from the dashboard the user can edit any of the games he/she has uploaded. One of the options while editing the game is to delete it. 

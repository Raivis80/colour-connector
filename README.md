# The Colour Connector

# Code Institute May 2022 Hackathon

# Team - The Lightsabres

# Overview

The theme of the Code Insitute May 2022 hackathon was 'Getting Connected'. To begin with, we considered 4 ideas - a social media site for disabled users to discuss assistive technologies, a multiplayer game, a pub quiz, and a messenger app. Ultimately we went with the 4th idea, but incorporating elements of the 1st. 

The inspiration behind this project was a gift given to one of our team by his partner during the Covid-19 lockdowns. This gift was a colour lamp. One partner had one lamp, and the other partner had the other lamp. When one partner touches their lamp, the companion lamp lights up, which lets that person know that you are thinking of them. 

We thought that this was a very sweet idea, and an excellent way of combatting loneliness. Another team member who works with disabled patients informed us that people who rely on assistive technologies are significantly more prone to loneliness, so we decided to build the site with those people in mind, using a minimum amount of text, and using images and icons as much as possible. 

Our goal was to digitise this idea, and create an application that mimics the function of a colour lamp. Users can create accounts, log in and find their friends. Users can send friend requests to their friends, and once accepted, can send coloured messages and notes. The idea is for groups of users who perhaps do not see each other very often, or who cannot meet up, to maintain connections, and perhaps spark conversation using other apps and services, such as text messages or Facebook. 

[Am I Responsive](#)


# User Experience (UX)

## User Stories

Users must be able to determine the point of the site as soon as they navigate to it

Users must be to able create accounts easily

Returning users must be able to sign in easily

Users must be able to search for and find their friends

Users must be able to send friend requests

Users who have been sent friend requests must be able to accept and reject them

Once a pair of users are linked via an accepted friend request, they must be able to send messages and notes to each other

## User Experience in this Site
This website takes the users stories mentioned above into consideration to create a positive UX.  The users experience is discussed in more detail below with examples.

## Design

As the site was designed with disabled people in mind, we decided to use a light, positive colour palette, using blues, greens, oranges and yellows. 

## Design Research

## Design Wireframes

### Initial Wireframes

The wireframes below lay out how the initial design of the project, and the layout of its pages:

![index-page](media/wireframes/index-page.png)

![index-logged-in-page](media/wireframes/index-page-logged-in.png)

![sign-up-page](media/wireframes/sign-up-page.png)

![user-profile-page](media/wireframes/user-profile-page.png)

![non-user-profile-page](media/wireframes/non-user-profile-page.png)

![about-page](media/wireframes/about-page.png)

### Final Wireframes

As expected, the project's design changed significantly throughout the project. The final design wireframes are below:

# Features

The project uses the Python Django framework to allow users to create accounts and sign in. Once signed in, users can access the full features of the site. 

Once signed in, users may search for friends and send friend requests

Once a friend request has been accepted, linked users may send messages and notes to each other

The project also includes an About page, which includes links to the LinkedIn and Github profiles of the team. 

### Fonts
### Colour Scheme

# Design


## Favicon


## Header

* Logo

* Navigation Bar


## Landing Page

## Footer


## Other Sections


## Error Pages

404 Page A customised 404 page not found was added to the site to support the professionalism design and ensure appropriate link was added back to the main site to guide users who come across this message.



# Future Work


# Testing

## Validation Testing

### HTML Validation

### CSS Validation

### PEP8 Python Validation

### Lighthouse testing

#### Landing page

#### Sign up page

#### Login page


# Deployment

The project was deployed to Heroku. Unfortunately, some weeks prior to the start of the Hackathon, Github and Heroku suffered security breaches. This required the project to be deployed via the terminal using the following steps:
1. Login to Heroku using `heroku login -i`
2. Check that the login was successful by displaying the list of Heroku apps with `heroku apps`
3. Connect Heroku to the project repository with `heroku git:remote -a colour-connector`
4. Make a small change to the project so as to initiate the deployment process with `git add .` and `git commit -m "message"`
5. Push those changes to both Heroku and Github with the commands `git push origin main` and `git push heroku main`
6. On Heroku - select the heroku/python and heroky/nodejs buildpacks
7. Set the environment variables - 


# Version Control
1.	The main repository was created by Adam Boley, and was then forked by all collaborators
2.	Branch protection was added to ensure pull requests were reviewed before merging
3.	Each team member ensured their development environment was linked by using the command:  git remote -v 
4.	For each new feature, team members created a new branch: git checkout -b branch-name
5.	To ensure this branch was being tracked: git push -u origin branch-name
6.	 In order to update the project files in their own work space:  git pull upstream main this was important to limit the amount of merge conflicts a team member came across
7.	Each team member used git add . git commit and git push to add, stage and save their work to their branch. 
8.	When a team member finished a feature they made a Pull Request.  A template was used for this Pull Request so all team members information was structured the same.  This Pull Request was then checked by another member of the team.  If a merge conflict arose the team member would be notified by a comment otherwise the branch was merged.

### Cloning

### Content
### Media

# Credits

## Team

<br>Adam Boley - [Github](https://github.com/AdamBoley), [LinkedIn](https://www.linkedin.com/in/adam-boley-196420a8/)
<br>Ciara O'Sullivan - [Github](https://github.com/ciaraosull), [LinkedIn](https://www.linkedin.com/in/ciara-o-sullivan-2834378b/)
<br>Nazia Siddique - [Github](https://github.com/NaziaSiddique), [LinkedIn]()
<br>Raivis Petrovskis  - [Github](https://github.com/Raivis80), [LinkedIn](https://www.linkedin.com/in/raivis-petrovskis/)
<br>Lane-Sawyer Thompson - [Github](https://github.com/LaneSawyerT), [LinkedIn](https://www.linkedin.com/in/lanesawyert/)

## Resources

[This site](https://amasty.com/blog/30-best-meet-the-team-pages-examples-and-trends/) was used as the inspiration of the about page

## Acknowledgements

Trust in SODA - 
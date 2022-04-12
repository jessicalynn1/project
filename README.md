# Dream Disney Day

Welcome to Dream Disney Day! The answer to the age old dilemma for all Disneyland fans, what ride should we go on next?

On the landing page you are greeted with my son's sweet face as he looks around at everything to see on 'it's a small world' on his first trip on the ride. Next you are prompted to either create a new account or login to an existing account. After login you will be asked if you'd like to see your saved itinerary from a previous login or create a new itinerary. The next page is the form which asks you a series of questions about your travel plans and preferences. This form submission then takes you to your Dream Disney Day! The user can see their most recent saved itinerary at the 'See Saved' tab so they can access their itinerary whenever they want.

![waltmickey](/static/img/waltmickey.jpg "waltmickey")

**CONTENTS**

- [Tech Stack](#tech-stack)
- [Features](#features)
- [Future Features](#future-features)
- [Installation](#installation)
- [About the Developer](#about-the-developer)

## Tech Stack

**Backend:** Python3, Flask, Jinja, SQLAlchemy\
**Frontend:** HTML5, CSS3, Bootstrap\
**Database:** PostgreSQL\
**API:** Disney API

## Features

### SAVED ITINERARY

Users can login and see their previous saved itinerary.

### REPEAT THE FORM

A user can log in and fill out the form as many times as they'd like. If their travel plans change or they're planning a new trip, they can change their answers on the form to get new results.

## Future Features

- Emailing itinerary to the user
- UI/UX improvements
- Different parks made available (could be it's own project/app)

## Installation

#### Requirements:

- PostgreSQL
- Python 3.7.3

To have this app running on your local computer, please follow the below steps:

Clone repository:

```
$ git clone https://github.com/jessicalynn1/project.git
```

Create and activate a virtual environment:

```
$ pip3 install virtualenv
$ virtualenv env
$ source env/bin/activate
```

Install dependencies:

```
(env) $ pip3 install -r requirements.txt
```

Create database tables and seed database:

```
(env) $ python3 seeds_database.py
```

Start backend server:

```
(env) $ python3 server.py
```

Navigate to `localhost:5000/` to plan your Dream Disney Day!

## About the Developer

Jessica Faylor is a software engineer in the Greater San Diego Area, and previously worked in various fields, inclduing finance, accounting and administration. A combined love for family time, learning new things, and all things Disney, led to the creation of Dream Disney Day, her capstone project for Hackbright Academy.

Let's connect!

<p><a href="https://www.linkedin.com/in/jessica-faylor-0377b35/">
  <img
    alt="LinkedIn"
    src="https://img.shields.io/badge/linkedin-%230077B5.svg?style=for-the-badge&logo=linkedin&logoColor=white"
  />
</a>
</p>
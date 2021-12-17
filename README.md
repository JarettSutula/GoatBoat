 <p align="center">
    <img src="https://i.imgur.com/sUh3mN4.png" >
<p align="center">
    <a href="https://www.python.org/" alt="python">
        <img src="https://img.shields.io/badge/Made%20with-python-1f425f.svg" /></a>
    <a href="https://choosealicense.com/licenses/mit/" alt="MIT">
        <img src="https://img.shields.io/badge/license-MIT-orange" /></a>
</p>

# Mission Statement
To connect students with mentors to foster academic growth

# Hill Statements
1. In one minute, a student can find an effective and relatable tutor to study with.
2. A tutor should be able to connect with students at just the touch of a button.
3. A university can subscribe to the service on behalf of students, reducing labor cost.
4. Our team is committed to keeping up-to-date with changing educational circumstances even in a post-pandemic world.

# Branches
Branching on this project is inspired by the Gitflow method of branching. The main branch will be used for all major releases. Updates to main will come directly from the development branch as we do not plan on using release branches. New branches will be made off of dev for each feature that will be developed. Once a feature has been completed and merged into dev, tested, and approved, the feature branch will be deleted.

Before merging a branch to dev or main, developers must create a pull request. Each pull request must be reviewed by and meet the standards of team members other than the developer who authored the pull request.

# Project Summary
Goat Boat is a web application that pairs students with tutors. When signing up for the service, both students and tutors will be asked to share a few, select details about themselves. Their responses allow our team to find ideal pairs that we guarantee will lead to a better academic experience for our users.

Users can select classes from their school course catalog to look for help with or to help others with. This way, users can decide to be a Mentor, a Mentee, or a mix of both, all through a simple form. From there, users can choose from a list of candidates that would help them with what they are looking for.

# Installation and Usage
If you are looking to install GoatBoat, create users, and help us develop and maintain our web-app approach to mentoring, please install GoatBoat with these following steps.

**Note - GoatBoat is not currently in a production server and will require developers to install the repository on the local machine to use its services.**
1. Clone the GoatBoat repository to your local machine.
2. Create a new .env file without a name, simply, ".env". Inside that file there will should be two lines that contain database credentials needed to access GoatBoat. **If you are looking to install and work on GoatBoat, please reach out to @JarettSutula @McDaPick for the database credentials. The project will not run without these credentials.**

3. Start up [Docker Desktop](https://www.docker.com/products/docker-desktop) for a secure place for the GoatBoat web server to run. GoatBoat will spin up a Docker image for you.
4. Open your terminal of choice and navigate to the root directory of GoatBoat.
5. Run the command 'make'. This will run the Makefile in GoatBoat.

**The Makefile in GoatBoat is set up to do a few different things - it should:**

1. Clean eggs, caches, and wheels inside of GoatBoat if they exist.
2. Run setup.py and install requirements listed in requirements.txt for you.
3. Runs safety checks on dependencies and their licenses.
4. Runs tests (including ones with database calls).
5. Runs mutation testing (which is currently failing due to an issue with an emoji).
6. Builds the dist.
7. Adds any outstanding migrations and migrates them before the server starts up.

Once the make command is done running, GoatBoat spins up a Docker image and attempts to connect it to the Docker Desktop you should have running. From there, you should eventually see something along the lines of this:

```
docker compose up
Container goatboat-web-1  Recreate
Container goatboat-web-1  Recreated
Attaching to goatboat-web-1
goatboat-web-1  | Performing system checks...
goatboat-web-1  |
goatboat-web-1  | System check identified no issues (0 silenced).
goatboat-web-1  | December 17, 2021 - 02:06:29
goatboat-web-1  | Django version 3.2.8, using settings 'mentor.settings'
goatboat-web-1  | Starting development server at http://0.0.0.0:8000/
goatboat-web-1  | Quit the server with CONTROL-C.
```

**Congratulations!** This means the GoatBoat Web Server is running on your machine. Open up your favorite Web Browser and type in 'localhost:8000' and you should be able to connect to GoatBoat and set up accounts, match, and more.

# Contributing To GoatBoat
If you are looking to contribute to GoatBoat, please visit contributing.md [here](contributing.md) for more information. Please direct any questions, feedback, or pull requests towards **@JarettSutula** or **@McDaPick**.

# Authors
Check out the authors [here](https://github.com/JarettSutula/GoatBoat/graphs/contributors).

# License Information
GoatBoat adheres to the MIT license. For more information, see [here](https://choosealicense.com/licenses/mit/).

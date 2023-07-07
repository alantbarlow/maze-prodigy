# Maze Prodigy
> Welcome to the Maze Prodigy project! This is a Python-based game for Windows, MacOS, and Linux that challenges you to solve mazes using your keyboard's arrow keys. The project provides an interactive and engaging experience where you can test your speed and accuracy in solving various mazes.
<!--
> You can download the latest version of the game [_here_](https://maze_prodigy.alantbarlow.dev).
-->


## Table of Contents
<!-- * [Screenshots](#screenshots) -->
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Setting Up Your Dev Environment](#setting-up-your-dev-environment)
* [Usage](#usage)
* [Project Status](#project-status)
* [Possible Improvements](#possible-improvements)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)
<!-- * [License](#license) -->

<!--
## Screenshots
![Example screenshot](./img/screenshot.png)
-->

## General Information
This game was created for Maze lovers and people who want to improve their problem-solving, decision-making, and their logical thinking skills. With an endless amount of procedurally generated mazes, you can keep yourself entertained while improving the speed and accuracy of your decisions. 


## Technologies Used
This project is built using the following technologies:

- **Python 3.11**: The core programming language used for developing the project.
- **CustomTkinter 5.2.0**: A customized version of the Tkinter library, which provides modernizes the set of tools and widgets for building graphical user interfaces in Python.
- **Pillow 9.5.0**: A powerful library for image processing and manipulation in Python, used for handling images and graphics in the Maze Solver project.
- **VSCode Dev Containers / Docker Dev Environments**: A development environment based on Docker containers, which allows for consistent and reproducible development setups. It simplifies the setup process and provides a consistent environment across different machines.

These technologies were chosen for their reliability, flexibility, and ease of use in building Maze Prodigy. They provide the necessary tools and libraries to create an engaging and interactive maze-solving experience.

Feel free to explore the project's codebase to see how these technologies are utilized and integrated into the overall implementation.


## Features
1. **Difficulty Selection**: Choose your preferred difficulty level before starting the maze-solving adventure. Select from multiple difficulty options to match your skill level and challenge yourself.
2. **Maze Generation**: The project generates mazes dynamically, providing you with unique and exciting challenges every time you play. Each maze is designed to test your problem-solving skills and navigation abilities.
3. **Keyboard Controls**: Use the arrow keys on your keyboard to maneuver through the maze and find the exit. The intuitive controls make it easy to navigate through the maze and complete the challenge.
4. **Speed and Accuracy Tracking**: The Maze Solver project keeps track of your solving speed and accuracy, providing you with valuable feedback on your performance. You can analyze your results and aim for improvement with each attempt.

## Setting Up Your Dev Environment
If you want to modify this project to fit your own needs, the recommended method to do so is to open this project in a docker development container. The following are the requirements to get this set up on your machine: 

- [**Docker Desktop**](https://www.docker.com/products/docker-desktop/): Used as a GUI to run and manage your docker containers and to install the docker daemon. 
- [**VSCode**](https://code.visualstudio.com/): Used as the code editor for the development container.
- [**VSCode Dev Containers**](https://code.visualstudio.com/docs/devcontainers/containers) - Used to open the VSCode project in a development container.
- [**Git**](https://git-scm.com/downloads): Used to clone this project into the development container.
- **OS Specific X11 Server**: Used as the x11 server for viewing the project's GUI when running in a docker container. [XQuartz](https://www.xquartz.org/) is recommended for MacOS. 

Once you have installed the requirements, you can get started by opening VSCode, going to the Remote Explorer, and adding a new Dev Container. Just press "Clone Repository in Container Volume" and put paste the URL of this repo. This should create the dev container with all the project dependancies and open the project in your workspace. 

To run the project you can either type `python maze_prodigy` or you can navigate to "maze_prodigy/\__main__.py" and pressing "Debug Python File" in the upper right side of the VSCode window.


## Project Status
The project's initial features have been completed. Future development plans are to be determined based on the game's popularity and my time available.


## Possible Improvements
The following are features or improvements that can be added to future versions of this project:

- Persist stats such as games completed and stars collected.
- Add sounds for moves and button presses.
- Add controller support.
- Improve main menu by adding a GIF in the background.
- Add settings for changing the color theme, window resolution, and sounds.
- Add player leveling system to gain experience and level up from completing mazes.

Don't forget to leave a feature request if there is something you'd like to add to this list.


## Acknowledgements
This project was inspired by the [Build A Maze Solver](https://boot.dev/project/2b266bb4-2262-49c0-b6d1-75cd8c5e8be8/fb0967e1-a304-4110-8bf3-41071d99af0c) guided project on [Boot.dev](https://boot.dev/).


## Contact
Created by [@alantbarlow](https://www.linkedin.com/in/alantbarlow/) - feel free to contact me on LinkedIn!


<!--
## License
This project is open source and available under the [... License]().
-->

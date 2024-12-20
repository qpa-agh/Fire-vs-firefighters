﻿# Fire-vs-firefighters

https://github.com/user-attachments/assets/b54a01a8-64b9-45f8-a49a-cda94d838393


## Fire Model

Fire spreads under the provided conditions. Factors like wind, tree type etc. are taken into consideration and can be randomly selected or provided by the user.


## Fire Fighters model

Fire fighters team are managed by two self-interested agents, who make decsision based on game theory.
Logistical managers assigns as little as possible resources for the fire to be quenched.
Fire team leader wants to put out fire as fast as possible, with as little damages to the forest as possible.
Fire team leader predicts fire spread by using special heuristics.


## How to run
1. Clone the repository inside empty folder
    ``` bash
    cd ${project folder}
    git clone https://github.com/PaulinaGacek/A-.git
    ```
2. Create virtual environment in the project directory
    ``` bash
    python -m venv venv
    # on windows
    venv\Scripts\activate
    # on linux/mac
    source venv/bin/activate
    ```
3. Install `pygame`
    ``` bash
    pip install pygame
    ```
4. Run the app
    ``` bash
    python .\scripts\main.py
    ```

## Fire simulation manual
1. Initial map is randomly generated, if you want to generate it again click `C`, if you want to see generated sectors press `Z`
2. To paint the fire click with `LEFT MOUSE CLICK` on certain spot, where is forest - you cannot put ground on fire
3. If you want to undo your painting click `RIGHT MOUSE CLICK` on certain fire spot and it will become forest again
4. To start the animation press `SPACE`. After simulation starts you cannot paint new fire spots.
5. To stop the simulation and generate new map click `CTRL`+`C`

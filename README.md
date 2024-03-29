# Fire-vs-firefighters

## Fire Model

**1st approach**

Fire spreads under the provided conditions. Factors like wind, tree type etc. are taken into consideration and can be randomly selected or provided by the user.

**2nd approach**

Fire is a self-interested agent which aims at spreading to the greatest extend.

## Fire Fighters model

**1st approach**

Fire fighters are self-interested agents which cooperates in order to reach common goal - quench the fire.

**2nd approach**

Fire fighters team is one self-interested agent, it diverts its resources to fight the fire as fast as possible.

The fire fighters predicts fire spread by using special heuristics.


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
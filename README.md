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
    venv\Scripts\activate
    ```
3. Install `pygame`
    ``` bash
    pip install pygame
    ```
4. Run the app
    ``` bash
    python .\scripts\main.py
    ```
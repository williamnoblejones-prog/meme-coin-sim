# meme-coin-sim
## **Dependancies:**
-Python3
-numpy
-pandas
-matplotlib - pyplot

## **How to run:**
### **1) Install dep.**
    Sudo apt update
    Sudo apt install python3, python3-numpy, python3-pandas, python3-matplotlib
### **2) Install repo**
    git clone https://github.com/williamnoblejones-prog/meme-coin-sim.git
    cd ~/meme-coin-sim/
### **3) Conf variables** <br />
*lines 5-10, 18, 22-25 can be changed* <br />
	TIME_STEPS = "<1, >300" <br />
    N_RUNS = "rec: 500, max: 10_000, min: 50" <br />
    INITIAL_LIQUIDITY = "rec: 1_000, min 1, max: >100_000" <br />
    INITIAL_PRICE = "=<1,~500" <br />
    ALPHA_BUYERS = "rec: 4.0" <br />
    AVG_BUY_SIZE = "rec: 250" <br />
    SELL_BASE_PROB = "rec: 1.0" <br />
    *i wouldnt change ALPHA_BUYERS, AVG_BUY_SIZE, SELL_BASE_PROB unless you know what you're doing.* <br />
### **4) Run** <br />
    sudo python3 ./meme-coin-sim.py <br />
    OR <br />
    python3 ./meme-coin-sim.py <br />
Examples of running script with base params. : <br />
![command line calling python3 to run script as sudo](https://github.com/williamnoblejones-prog/meme-coin-sim/blob/main/montCarloCryptoCMD.png) <br />
(Example of running script with base params) <br />
![graph representing results of script](https://github.com/williamnoblejones-prog/meme-coin-sim/blob/main/montCarloCrytoN1000.png) <br />
(Example output of the above line, using N_RUNS = 1_000) <br />

## Explination
First, the model creates a value called hype, which represents how interested people are in the coin. This hype rises and falls in a somewhat random way, similar to trends on social media. When hype is high, more people want to buy. When hype starts to fall, more people choose to sell.

Next, the program simulates a basic market:

A different number of buyers appear each day.

Each buyer spends a random amount of money.

People who already own the coin can decide to sell, especially if hype is decreasing.

The balance between buying and selling determines the price:

If more money is being spent buying than selling, the price goes up.

If more people are selling than buying, the price goes down.

This entire process is repeated 1,000 times using a Monte Carlo simulation. Running the model many times shows many possible outcomes instead of relying on a single scenario.

At the end, the program calculates:

The highest price reached in each simulation.

The final return (profit or loss) for someone who bought at the start and sold at the end.

The percentage of simulations where the investment was profitable.

The results are displayed as summary statistics and a graph that shows how often different gains and losses occur.

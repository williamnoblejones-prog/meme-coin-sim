import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TIME_STEPS = 500
N_RUNS = 1000
INITIAL_LIQUIDITY = 1_000
INITIAL_PRICE = 1.0
TOTAL_MARKET_CAPITAL = 50_000_000

ALPHA_BUYERS = 4.0
AVG_BUY_SIZE = 250
SELL_BASE_PROB = 1.0

np.random.seed(42)

def generate_hype_series():

    hype_series = []
    hype = 1.0  # starting hype

    for t in range(TIME_STEPS):
        # random walk with slight decay
        #change = np.random.normal(0, 0.05)

        # rare viral event
        if np.random.rand() < 0.03: #2% chance of change
            change = np.random.normal(2.0, 0.8)
        # tormal drift
        else:
            change = np.random.normal(-0.005, 0.05)

        hype += change

        # gentaly decay
        hype *= 0.995

        hype_series.append(hype)

    return hype_series 

def run_single_sim():
    liquidity = INITIAL_LIQUIDITY
    holders = []
    price_series = []
    hype_series = generate_hype_series()
    price = INITIAL_PRICE
    remaining_capital = TOTAL_MARKET_CAPITAL

    for t in range(TIME_STEPS):
        hype = hype_series[t]
        #add pos. feedback to hype
        if len(price_series) >= 2:
            price_momentum = (price_series[-1] - price_series[-2]) / price_series[-2]
        else:
            price_momentum = 0
        #hype += 15 to 100
        hype += 80 * max(price_momentum, 0)

        # clamp
        hype = max(hype, 0.1)
        hype = min(hype, 50)

        price_series.append(price)

        n_buyers = np.random.poisson(ALPHA_BUYERS * (hype ** 3))

        expected_volume = n_buyers * AVG_BUY_SIZE

        buy_volume = np.random.lognormal(
            mean=np.log(max(expected_volume, 1)),
            sigma=0.6
        )

        buy_volume = min(buy_volume, remaining_capital)
        remaining_capital -= buy_volume

        holders.append({
            "entry_price": price,
            "entry_time": t
        })
            
        
        sell_volume = 0
        remaining_holders = []

        if t == 0:
            hype_slope = 0
        else:
            hype_slope = hype_series[t] - hype_series[t-1]
        sell_prob = min(0.05 + 0.0005*t + 1.2 * max(0, -hype_slope), 0.5)

        for h in holders:
            if np.random.rand() < sell_prob:
                sell_volume += AVG_BUY_SIZE
            else:
                remaining_holders.append(h)

        holders = remaining_holders

        net_flow = buy_volume - sell_volume
        effective_liquidity = liquidity ** 0.7 # sublinear depth
        impact = net_flow / max(effective_liquidity, 1)

        # clamp impact to realistic bounds
        impact = np.clip(impact, -2, 2)
        price *= np.exp(impact * 0.12)

        #rare whale
        if np.random.rand() < 0.01:
            whale_buy = np.random.uniform(10_000, 100_000)
            buy_volume += whale_buy

        #rug pull
        if np.random.rand() < 0.002:
            price *= np.random.uniform(0.05, 0.3)
            liquidity *= 0.2

        liquidity += buy_volume - sell_volume
        liquidity = max(liquidity, 500)

        price_series.append(price)
        price = min(price, 1_000_000)  # prevent numeric insanity

    return price_series, hype_series

def run_simulation():
    all_peaks = []
    final_returns = []

    for _ in range(N_RUNS):
        prices, hype = run_single_sim()
        peak_price = max(prices)
        all_peaks.append(peak_price)

        final_returns.append(prices[-1] / prices[0] - 1)
    
    return all_peaks, final_returns


all_peaks, final_returns = run_simulation()


print("Monte Carlo results")
print("-------------------")
print(f"Time steps: {TIME_STEPS}")
print(f"Runs: {N_RUNS}")
print(f"Median peak multiple: {np.median(all_peaks):.2f}x")
print(f"Max peak multiple: {np.max(all_peaks):.2f}x")
print(f"95th percentile peak multiple: {np.percentile(all_peaks, 95):.2f}x")
print(f"Mean final return: {np.mean(final_returns)*100:.2f}%")
print(f"Median final return: {np.median(final_returns)*100:.2f}%")
print(f"% profitable runs: {(np.array(final_returns) > 0).mean()*100:.1f}%")
print(f"Creator Profit: {1000*np.max(all_peaks):.2f}")

plt.hist(final_returns, bins=50)
plt.axvline(0, color="red", linestyle="--")
plt.title("Distribution of Final Returns")
plt.xlabel("Return")
plt.ylabel("Frequency")
plt.show()

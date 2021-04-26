import numpy as np


class GeometricBrownianMotion:
    """
    A class to implement a GBM model with given drift, volatility, time span,
    """
    def __init__(self, s0, mu, sigma, T=1, dt=0.01):
        self.s0 = s0          # the starting level/price
        self.mu = mu          # drift/expected return component
        self.sigma = sigma    # volatility component
        self.T = T            # time span over which to simulate
        self.dt = dt          # number of steps to simulate (i.e. the granularity for simulation over T)
        self.N = int(T / dt)  # the number of total simulation steps

    def simulate(self):
        """
        simulate GBM and return the prices over time as an array

        :return: a Numpy array of prices for this simulated price motion
        """
        ticks = np.linspace(0, self.T, num=self.N)
        # calculate standard Brownian motion over the tick-space
        W = np.random.standard_normal(size=self.N)
        W = np.cumsum(W) * np.sqrt(self.dt)
        # geometric Brownian motion over the tick-space
        X = (self.mu - (self.sigma ** 2) / 2) * ticks + self.sigma * W
        return np.array(self.s0 * np.exp(X))

    def simulate_average_sT(self, n_simulations):
        """
        Return the average final price sT for this GBM over a given number of simulations

        :param n_simulations: the number of simulations to run
        :return: the average ending price, sT
        """
        sT = 0.0
        for i in range(n_simulations):
            sT += self.simulate()[-1]
        return sT / n_simulations


class PairsRNN:
    pass

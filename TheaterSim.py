#%%
# Simulation code adapted from https://github.com/realpython/materials/blob/master/simulation-with-simpy/simulate.py
import simpy
import random
import statistics


wait_times = 0
number_ppl = 0


class Theater(object):
    """Object that holds all simpy Resources for the theater
    """

    def __init__(self, env, num_cashiers, num_servers, num_ushers):
        """initializes 

        Args:
            env (simpy.environment): a Simpy environment for simulation
            num_cashiers (int): number of cashiers
            num_servers (int): number of servers
            num_ushers (int): number of ushers
        """
        self.env = env
        self.cashier = simpy.Resource(env, num_cashiers)
        self.server = simpy.Resource(env, num_servers)
        self.usher = simpy.Resource(env, num_ushers)

    def purchase_ticket(self, moviegoer):
        # 1-3 minutes to buy ticket
        yield self.env.timeout(random.randint(1, 3))

    def check_ticket(self, moviegoer):
        # 3 seconds to check ticket
        yield self.env.timeout(3 / 60)

    def sell_food(self, moviegoer):
        # 1-5 minutes to buy food
        yield self.env.timeout(random.randint(1, 5))


def go_to_movies(env, moviegoer, theater):
    # Moviegoer arrives at the theater
    arrival_time = env.now

    with theater.cashier.request() as request:
        yield request
        yield env.process(theater.purchase_ticket(moviegoer))

    with theater.usher.request() as request:
        yield request
        yield env.process(theater.check_ticket(moviegoer))

    if random.choice([True, False]):
        with theater.server.request() as request:
            yield request
            yield env.process(theater.sell_food(moviegoer))

    # Moviegoer heads into the theater
    global wait_times
    global number_ppl
    wait_times += (env.now - arrival_time)
    number_ppl += 1



def run_theater(env, num_cashiers, num_servers, num_ushers):
    theater = Theater(env, num_cashiers, num_servers, num_ushers)

    # initial 3 movie goers
    for moviegoer in range(1):
        env.process(go_to_movies(env, moviegoer, theater))

    while True:
        yield env.timeout(.2)  # Wait a bit before generating a new person

        moviegoer += 1
        env.process(go_to_movies(env, moviegoer, theater))



def oneSimRun(state):
    """Takes a state for number of chasiers, servers and ushers and runs a
    hour and a half sim and returns the score

    Args:
        state (tuple(int)): holds state for number of cashiers, servers and
        ushers respectfully.

    Returns:
        float: the sum of the ratios avg_waitime/max_weight_time and cost/budget
    """
    global wait_times
    global number_ppl
    wait_times = 0
    number_ppl = 0

    num_cashiers, num_servers, num_ushers = state
    env = simpy.Environment()
    env.process(run_theater(env, num_cashiers, num_servers, num_ushers))
    env.run(until=90)

    total_cost = num_servers + num_cashiers + num_ushers

    wait_score = (wait_times/number_ppl)/10
    print    
    cost_score = total_cost/20

    if wait_score > 1:
        wait_score += 100
    
    if cost_score > 1:
        cost_score += 100

    return  wait_score + cost_score



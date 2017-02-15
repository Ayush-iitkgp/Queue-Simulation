import random
import simpy
from scipy.optimize import fsolve

f1 = lambda x : math.exp(-x)*x-0.05
result1 = fsolve(f1,0)
RENEGE_RATE = result1[0]

f2 = lambda x : math.exp(-x)*x-0.25
result2 = fsolve(f2,0)
MEW = result2[0]

f3 = lambda x : math.exp(-x)-0.4
result3 = fsolve(f3,0)
INTERVAL_CUSTOMERS = result3[0]

INTERVAL_CUSTOMERS/(MEW*RENEGE_RATE)


# Set the Seed
RANDOM_SEED = 42
NEW_CUSTOMERS = 10000  # Total number of customers



def source(env, number, lambd, counter):
    """Source generates customers randomly"""
    for i in range(number):
        c = customer(env, 'Customer%02d' % i, counter)
        env.process(c)
        t = random.expovariate(lambd)
        yield env.timeout(t)


def customer(env, name, counter):
    """Customer arrives, is served and leaves."""
    arrive = env.now
    print('%7.4f %s: Here I am' % (arrive, name))

    with counter.request() as req:
        patience = random.expovariate(RENEGE_RATE)
        # Wait for the counter or abort at the end of our tether
        results = yield req | env.timeout(patience)

        wait = env.now - arrive
        global TOTAL_WAITING_TIME,RENEGED
        TOTAL_WAITING_TIME = TOTAL_WAITING_TIME + wait

        if req in results:
            # We got to the counter
            print('%7.4f %s: Waited %6.3f' % (env.now, name, wait))

            tib = random.expovariate(MEW)
            yield env.timeout(tib)
            print('%7.4f %s: Finished' % (env.now, name))

        else:
            # We reneged
            print('%7.4f %s: RENEGED after %6.3f' % (env.now, name, wait))
            RENEGED = RENEGED + 1


# Setup and start the simulation
print('Bank renege')
random.seed(RANDOM_SEED)
env = simpy.Environment()
#global TOTAL_WAITING_TIME
TOTAL_WAITING_TIME = 0
RENEGED = 0

# Start processes and run
counter = simpy.Resource(env, capacity=2)
env.process(source(env, NEW_CUSTOMERS, INTERVAL_CUSTOMERS, counter))
env.run()


print(TOTAL_WAITING_TIME)
print(RENEGED)
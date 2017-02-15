import simpy
import random

def main():
    # Create an environment
    env = simpy.Environment()
    # Create the instance of the process/simulation
    env.process(traffic_light(env))
    # Give the running time of simulation and run it
    # Run the process
    env.run(until=120)   #Simulation will run for 120 seconds
    print("Simulation Completes")

# Define the process Traffic light is a process inside Environment "env"
def traffic_light(env):
    while True:
         print("Light turned GRN at t= "+str(env.now)) 
         yield env.timeout(neg_exp(2)) 
         print("Light turned YEL at t= "+str(env.now)) 
         yield env.timeout(neg_exp(3)) 
         print("Light turned RED at t= "+str(env.now)) 
         yield env.timeout(neg_exp(4))

# define clock for the simulation
def clock(env,name,tick):
    while True :
        print(name,env.now)
        yield env.timeout(tick)        

# Random arrival of customers
def neg_exp(lambd):
    return random.expovariate(lambd)


if __name__ == '__main__':
    main()
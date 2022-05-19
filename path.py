import numpy as np

def ind3dto1d(x, y, z):
    return x+y*5+z*25

def ind1dto3d(a):
    z = a//25
    y = (a-a//25*25)//5
    x = a % 5
    return x, y, z

np.random.seed(1)
state_size = (5*5)*(3+1)
action_size = 4
alpha = 0.8 #Learning rate
gamma = 0.6 #Decay rate
epsilon = 0 or 1

Q = np.random.normal(size=(state_size, action_size)) #U, L, D, R
act_options = "ULDR"
## Train
for i in range(10000):
    x = 0 #axis 1
    y = 0 #axis 2
    z = 0 #gold carried
    
    for j in range(40):
        current_state = ind3dto1d(x, y, z)
        if np.random.rand() > epsilon:
            act = Q[current_state, :].argmax()
        else:
            act = np.random.randint(0, 4)
        
        if act == 0: #Go up
            if x == 0 and y == 3: #If the target is the house
                r = z
                z = 0
            else:
                r = 0
                y = min(y+1, 4)              
        elif act == 1: #Go left
            if x == 1 and y == 4: #If the target is the house
                r = z
                z = 0
            else:
                r = 0
                x = max(x-1, 0)
        else:
            r = 0
            if act == 2:#Go down
                if x == 4 and y == 1: #If the target is the mine
                    z = min(z+1, 3)
                else:
                    y = max(y-1, 0)
            else: #Go right
                if x == 3 and y == 0: #If the target is the mine
                    z = min(z+1, 3)
                else:
                    x = min(x+1, 4)
       
        new_state = ind3dto1d(x, y, z)        
        Q[current_state, act] = (1-alpha)*Q[current_state, act] + alpha*(r+gamma*Q[new_state, :].max())
    
## Test
actions = ''
reward = 0
states = []
x = 0 #axis 1
y = 0 #axis 2
z = 0 #gold carried
for i in range(40):
    current_state = ind3dto1d(x, y, z)
    act = Q[current_state, :].argmax()
    states.append(current_state)
    if act == 0: #Go up
        if x == 0 and y == 3: #If the target is the house
            r = z
            z = 0
        else:
            r = 0
            y = min(y+1, 4)          
    elif act == 1: #Go left
        if x == 1 and y == 4: #If the target is the house
            r = z
            z = 0
        else:
            r = 0
            x = max(x-1, 0)
    else:
        r = 0
        if act == 2:#Go down
            if x == 4 and y == 1: #If the target is the mine
                z = min(z+1, 3)
            else:
                y = max(y-1, 0)
        else: #Go right
            if x == 3 and y == 0: #If the target is the mine
                z = min(z+1, 3)
            else:
                x = min(x+1, 4)
    actions += act_options[act]
    reward += r*gamma**i
print('Actions: '+actions)
print('Reward: '+str(reward))

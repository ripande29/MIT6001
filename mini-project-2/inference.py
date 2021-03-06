#!/usr/bin/env python
# inference.py
# Base code by George H. Chen (georgehc@mit.edu) -- updated 10/18/2016
import collections
import sys

import graphics
import numpy as np
import robot


# Throughout the code, we use these variables.
# Do NOT change these (but you'll need to use them!):
# - all_possible_hidden_states: a list of possible hidden states
# - all_possible_observed_states: a list of possible observed states
# - prior_distribution: a distribution over states
# - transition_model: a function that takes a hidden state and returns a
#     Distribution for the next state
# - observation_model: a function that takes a hidden state and returns a
#     Distribution for the observation from that hidden state
all_possible_hidden_states = robot.get_all_hidden_states()
all_possible_observed_states = robot.get_all_observed_states()
prior_distribution = robot.initial_distribution()
transition_model = robot.transition_model
observation_model = robot.observation_model

class ValToIndex:
    def __init__( self, a  ):
        self.sDict = dict()    
        for idx, v in enumerate(a ):
            self.sDict[v] = idx
        
    def vToIndex( self, v ):
        return self.sDict[v]



        
class TransitionMatrix:
    def __init__( self, stateDict ):
        N = len(all_possible_hidden_states)
        self.A = np.zeros((N,N))
        
        for s in all_possible_hidden_states:
            nextStates = transition_model(s)
            sIdx = stateDict.vToIndex(s)
            for ns in nextStates.keys():
                nsIdx = stateDict.vToIndex(ns)
                p= nextStates[ns]
                self.A[sIdx,nsIdx] = p 
                    

    def getTransitionMatrix( self ):
        return self.A
        
class EmissionMatrx:
    def __init__( self, sDict, oDict ):
        N = len(all_possible_hidden_states)
        L = len( all_possible_observed_states )
        self.B = np.zeros((N,L))
        
        for s in all_possible_hidden_states:
            obs = observation_model(s)
            sIdx = sDict.vToIndex(s)
            for o in obs.keys():
                oIdx = oDict.vToIndex(o)
                p = obs[o]
                self.B[sIdx, oIdx] = p
            
    def getEmissionMatrix( self ):
        return self.B
    

class DMatrix:
    def __init__( self, d , matrixSize , sDict ):
       
        self.M = np.zeros((matrixSize,))
        for s in d.keys():
            sIdx = sDict.vToIndex(s)
            self.M[sIdx] = d[s]
            
    def getMatrix( self ):
        
        return self.M
       

    

# You may find this function helpful for computing logs without yielding a
# NumPy warning when taking the log of 0.
def careful_log(x):
    # computes the log of a non-negative real number
    if x == 0:
        return np.inf
    else:
        return (-1 * np.log(x))


# -----------------------------------------------------------------------------
# Functions for you to implement
#
def getEmissionProb( obs, B, oDict, useLog =False ):
    N = len(all_possible_hidden_states)
    if obs == None:
        if useLog == False:
            emmisProb = np.ones(N,)
        else:
            emmisProb = np.zeros(N,)
    else:
        obsIndex  = oDict.vToIndex(obs)
        emmisProb = B[:, obsIndex ]
    return emmisProb    
    
def forward_backward(observations):
    """
    Input
    -----
    observations: a list of observations, one per hidden state
        (a missing observation is encoded as None)

    Output
    ------
    A list of marginal distributions at each time step; each distribution
    should be encoded as a Distribution (see the Distribution class in
    robot.py and see how it is used in both robot.py and the function
    generate_data() above, and the i-th Distribution should correspond to time
    step i
    """

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE
    #

    
    sDict = ValToIndex(all_possible_hidden_states)
    oDict = ValToIndex(all_possible_observed_states)
    A = TransitionMatrix(sDict).getTransitionMatrix()
    
    B = EmissionMatrx( sDict, oDict).getEmissionMatrix()

    
    forward_messages = calcForwardMessages( observations, A, B, sDict, oDict )
    #print(forward_messages[:,0])
    #print(forward_messages[:,1])
    # TODO: Compute the forward messages
    backward_messages = calcBackwardMessages(observations, A, B, sDict, oDict )

    marginals = calcMarginals( observations, forward_messages, backward_messages, B, sDict, oDict)
    
    
    
    
    return marginals


def calcForwardMessages(observations, A, B, sDict, oDict):
    
    num_time_steps = len(observations)
    N = len(all_possible_hidden_states)
    forward_messages = np.zeros( (N,num_time_steps)  )
    prior = DMatrix( prior_distribution, N, sDict)
    forward_messages[:,0] = prior.getMatrix()
    
    for i in range(0,num_time_steps-1):
        prevAlpha = forward_messages[:,i]
        emmisProb = getEmissionProb( observations[i], B, oDict )
        
        forward_messages[:,i+1] = A.T@(emmisProb * prevAlpha)
        forward_messages[:,i+1] = forward_messages[:,i+1]/sum(forward_messages[:,i+1])
                    
    return forward_messages
    
def calcBackwardMessages(observations,A, B, sDict, oDict):
    
    num_time_steps = len(observations)
    N = len(all_possible_hidden_states)
    backward_messages = np.zeros( (N,num_time_steps)  )
    backward_messages[:,num_time_steps-1] = np.ones((N,))
    for i in reversed(range(1,num_time_steps)):
        
        prevBeta = backward_messages[:,i]
        emmisProb = getEmissionProb( observations[i], B, oDict )
        backward_messages[:,i-1] = A@(emmisProb * prevBeta)
        backward_messages[:,i-1] = backward_messages[:,i-1]/sum(backward_messages[:,i-1])
                   
    return backward_messages

def calcMarginals ( observations, forward_messages, backward_messages, B, sDict, oDict)  :
  
    num_time_steps = len(observations)
    marginals = []  
    
    
    for i in range(num_time_steps):
        d = robot.Distribution()
        
        emmisProb = getEmissionProb( observations[i], B, oDict )

        m = (forward_messages[:,i] * backward_messages[:,i])*emmisProb
        m[:] = m[:]/sum(m)
        for idx, p in enumerate(m):
            state = all_possible_hidden_states[idx]
            d[state] = p

        marginals.append(d)
    
    return marginals
    
    
def Viterbi(observations):
    """
    Input
    -----
    observations: a list of observations, one per hidden state
        (a missing observation is encoded as None)

    Output
    ------
    A list of esimated hidden states, each encoded as a tuple
    (<x>, <y>, <action>)
    """

    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE
    #
    num_time_steps = len(observations)
    
    estimated_hidden_states = [] # remove this
    
        
    sDict = ValToIndex(all_possible_hidden_states)
    oDict = ValToIndex(all_possible_observed_states)
    A = TransitionMatrix(sDict).getTransitionMatrix()
    B = EmissionMatrx( sDict, oDict).getEmissionMatrix()
    np.place(A, A == 0, 10**-20 )
    np.place(B, B == 0, 10**-20 )
    A = -np.log2(A)
    B = -np.log2(B)
    
    
    N = len(all_possible_hidden_states)
    prior = DMatrix( prior_distribution, N, sDict)
    forward_messages = np.zeros( (N,num_time_steps)  )
    back_pointers = np.zeros( (N,num_time_steps), int  )
    P = prior.getMatrix()
    np.place(P, P == 0, 10**-20 )
    forward_messages[:,0] = -np.log2(P)

    for i in  range(num_time_steps -1 ):
        prevMsg = forward_messages[:,i]
        emmisProb = getEmissionProb( observations[i], B, oDict, True )
        w = prevMsg + emmisProb
        v = A.T + w
        forward_messages[:,i+1] = v.min(axis = 1)
        back_pointers[:,i + 1] = v.argmin(axis = 1)
        
     
    m = forward_messages[:, num_time_steps - 1]
    emmisProb = getEmissionProb( observations[num_time_steps - 1], B, oDict, True )
    m = m + emmisProb
    t = m.argmin()
    for i in reversed(range(1,num_time_steps)):
        estimated_hidden_states.append( all_possible_hidden_states[t] )
        t = back_pointers[t,i]
    estimated_hidden_states.append( all_possible_hidden_states[t] )    
    return list(reversed(estimated_hidden_states))


def second_best(observations):
    """
    Input
    -----
    observations: a list of observations, one per hidden state
        (a missing observation is encoded as None)

    Output
    ------
    A list of esimated hidden states, each encoded as a tuple
    (<x>, <y>, <action>)
    """
    num_time_steps = len(observations)
    
    estimated_hidden_states = [] # remove this
    
        
    sDict = ValToIndex(all_possible_hidden_states)
    oDict = ValToIndex(all_possible_observed_states)
    A = TransitionMatrix(sDict).getTransitionMatrix()
    B = EmissionMatrx( sDict, oDict).getEmissionMatrix()
    np.place(A, A == 0, 10**-20 )
    np.place(B, B == 0, 10**-20 )
    A = -np.log2(A)
    B = -np.log2(B)
    
    
    N = len(all_possible_hidden_states)
    prior = DMatrix( prior_distribution, N, sDict)
    forward_messages_1 = np.zeros( (N,num_time_steps)  )
    forward_messages_2 = np.zeros( (N,num_time_steps)  )
    back_pointers_1 = np.zeros( (N,num_time_steps), int  )
    back_pointers_2 = np.zeros( (N,num_time_steps), int  )
   # rank_2 =   np.zeros( (N,num_time_steps), int  )  
    
    P = prior.getMatrix()
    np.place(P, P == 0, 10**-20 )
    forward_messages_1[:,0] = -np.log2(P)
    forward_messages_2[:,0] = -np.log2(P)

    for i in  range(num_time_steps -1 ):
        prevMsg_1 = forward_messages_1[:,i]
        prevMsg_2 = forward_messages_2[:,i]
        emmisProb = getEmissionProb( observations[i], B, oDict, True )
        w_1 = prevMsg_1 + emmisProb
        v_1 = A.T + w_1
        forward_messages_1[:,i+1] = v_1.min(axis = 1)
        back_pointers_1[:,i + 1] = v_1.argmin(axis = 1)
        
        w_2 = prevMsg_2 + emmisProb
        v_2 = A.T + w_2
        if i == 0:
            v = v_2.T
                       
        else:
            v = np.concatenate((v_1.T, v_2.T), axis = 0)
            
        minIndices = v.argsort(axis = 0)[1,:]
        back_pointers_2[:,i+1] = minIndices
        v.sort(axis = 0)
        forward_messages_2[:,i+1] = v[1,:]

     
    m = np.concatenate((forward_messages_1[:, num_time_steps - 1], forward_messages_2[:, num_time_steps - 1]))
    emmisProb = getEmissionProb( observations[num_time_steps - 1], B, oDict, True )
    m = m + np.concatenate((emmisProb, emmisProb) )
    t = m.argsort()[1]
    print(t)
    for i in reversed(range(1,num_time_steps)):
        if t >= N:
            tIndex =  t - N
            t = back_pointers_2[tIndex,i]
        else:
            tIndex = t
            t = back_pointers_1[tIndex,i]
        print(t)
        estimated_hidden_states.append( all_possible_hidden_states[tIndex] )
        
    estimated_hidden_states.append( all_possible_hidden_states[t] )    
    return list(reversed(estimated_hidden_states))


    # -------------------------------------------------------------------------
    # YOUR CODE GOES HERE
    #




    return estimated_hidden_states


# -----------------------------------------------------------------------------
# Generating data from the hidden Markov model
#

def generate_data(num_time_steps, make_some_observations_missing=False,
                  random_seed=None):
    # generate samples from this project's hidden Markov model
    hidden_states = []
    observations = []

    # if the random seed is not None, then this makes the randomness
    # deterministic, which may be helpful for debug purposes
    np.random.seed(random_seed)

    # draw initial state and emit an observation
    initial_state = prior_distribution.sample()
    initial_observation = observation_model(initial_state).sample()

    hidden_states.append(initial_state)
    observations.append(initial_observation)

    for time_step in range(1, num_time_steps):
        # move the robot
        prev_state = hidden_states[-1]
        new_state = transition_model(prev_state).sample()

        # maybe emit an observation
        if not make_some_observations_missing:
            new_observation = observation_model(new_state).sample()
        else:
            if np.random.rand() < .1:  # 0.1 prob. of observation being missing
                new_observation = None
            else:
                new_observation = observation_model(new_state).sample()

        hidden_states.append(new_state)
        observations.append(new_observation)

    return hidden_states, observations


# -----------------------------------------------------------------------------
# Main
#

def main():
    # flags
    make_some_observations_missing = False
    use_graphics = True
    need_to_generate_data = True

    # parse command line arguments
    for arg in sys.argv[1:]:
        if arg == '--missing':
            make_some_observations_missing = True
        elif arg == '--nographics':
            use_graphics = False
        elif arg.startswith('--load='):
            filename = arg[7:]
            hidden_states, observations = robot.load_data(filename)
            need_to_generate_data = False
            num_time_steps = len(hidden_states)

    # if no data is loaded, then generate new data
    if need_to_generate_data:
        num_time_steps = 100
        hidden_states, observations = \
            generate_data(num_time_steps,
                          make_some_observations_missing)

    print('Running forward-backward...')
    marginals = forward_backward(observations)
    print("\n")

    timestep = 2
    print("Most likely parts of marginal at time %d:" % (timestep))
    if marginals[timestep] is not None:
        print(sorted(marginals[timestep].items(),
                     key=lambda x: x[1],
                     reverse=True)[:10])
    else:
        print('*No marginal computed*')
    print("\n")

    print('Running Viterbi...')
    estimated_states = Viterbi(observations)
    print("\n")

    print("Last 10 hidden states in the MAP estimate:")
    for time_step in range(num_time_steps - 10 - 1, num_time_steps):
        if estimated_states[time_step] is None:
            print('Missing')
        else:
            print(estimated_states[time_step])
    print("\n")

    print('Finding second-best MAP estimate...')
    estimated_states2 = second_best(observations)
    print("\n")

    print("Last 10 hidden states in the second-best MAP estimate:")
    for time_step in range(num_time_steps - 10 - 1, num_time_steps):
        if estimated_states2[time_step] is None:
            print('Missing')
        else:
            print(estimated_states2[time_step])
    print("\n")

    difference = 0
    difference_time_steps = []
    for time_step in range(num_time_steps):
        if estimated_states[time_step] != hidden_states[time_step]:
            difference += 1
            difference_time_steps.append(time_step)
    print("Number of differences between MAP estimate and true hidden " +
          "states:", difference)
    if difference > 0:
        print("Differences are at the following time steps: " +
              ", ".join(["%d" % time_step
                         for time_step in difference_time_steps]))
    print("\n")

    difference = 0
    difference_time_steps = []
    for time_step in range(num_time_steps):
        if estimated_states2[time_step] != hidden_states[time_step]:
            difference += 1
            difference_time_steps.append(time_step)
    print("Number of differences between second-best MAP estimate and " +
          "true hidden states:", difference)
    if difference > 0:
        print("Differences are at the following time steps: " +
              ", ".join(["%d" % time_step
                         for time_step in difference_time_steps]))
    print("\n")

    difference = 0
    difference_time_steps = []
    for time_step in range(num_time_steps):
        if estimated_states[time_step] != estimated_states2[time_step]:
            difference += 1
            difference_time_steps.append(time_step)
    print("Number of differences between MAP and second-best MAP " +
          "estimates:", difference)
    if difference > 0:
        print("Differences are at the following time steps: " +
              ", ".join(["%d" % time_step
                         for time_step in difference_time_steps]))
    print("\n")

    # display
    if use_graphics:
        app = graphics.playback_positions(hidden_states,
                                          observations,
                                          estimated_states,
                                          marginals)
        app.mainloop()


if __name__ == '__main__':
    main()

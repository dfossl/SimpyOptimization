

def k_beam_search(set_population, fittness_func, state_to_fitness = None, stop_step = 100 ,time_step=0):

    if state_to_fitness is None:
        state_to_fitness = dict()

    all_states = []

    for state in set_population:
        child_states = generate_all_states(state)
        for child in child_states:
            if child not in state_to_fitness:
                state_to_fitness[child] = fittness_func(child)

        all_states.extend(child_states)

    all_states.sort(key=lambda x: state_to_fitness[x])

    if time_step == stop_step-1:
        return all_states[0]
    else:
        set_population = all_states[:len(set_population)]
        return k_beam_search(set_population, 
                                        fittness_func, 
                                        state_to_fitness, 
                                        stop_step, 
                                        time_step=time_step+1)


def generate_all_states(state):
    states = [state]

    for i in range(len(state)):

        states.append(state[:i] + (state[i]+1,) + state[i+1:])

        if state[i]-1 > 0:
            states.append(state[:i] + (state[i]-1,) + state[i+1:])
    
    return states


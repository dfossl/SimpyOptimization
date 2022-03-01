import numpy as np
import simpy

wait_times = []

class Patient():
    """
    Patient object holds all patient information, most importantly with patient_type
    and processing path.
    """

    def __init__(self,
                patient_id,
                patient_type = None,
                rand_state = None,
                display=False):


        self.patient_id = patient_id
        self.name = f"Patient_{patient_id}"
        self.display = display

        if patient_type is None:
            self.patient_type = rand_state.choice([0,1,2,3], p=[1/10, 4/10, 3/10, 2/10])
        else:
            self.patient_type = patient_type

        if self.display:
            print(f"Patient generated: {self.name} of type {self.patient_type}")
        
        current_path_state = "WAITING_ROOM"

        self.path = ["WAITING_ROOM"]

        # while loop not usefil here but important for future implimentation
        # that will based on distributions pick paths
        while current_path_state != "END":

            if self.patient_type == 0:
                self.path.append("END")
                current_path_state = "END"
            else:
                self.path.append("TREATMENT")
                self.path.append("END")
                current_path_state = "END"


def utilize_nurses(env, patient, nurses, needed, time, display = True):
    """Generic funcition that will allocate the 'needed' nurses for an alloted
    amount of time.

    Args:
        env (simpy.environemtn)): simpy environment for simulation
        patient (Patient): Patient object requesting nurses
        nurses (Container): simpy container from wich nurses are withdrown
        needed (int): number of nurses needed
        time (float): amount of time a nurses are needed for.
        display (bool, optional): Should simulation print display. Defaults to True.
    """
    start = env.now

    if display:
        print(f"{patient.name} Request nurses {needed} | available {nurses.level}")
    
    yield nurses.get(needed)

    if display:
        print(f"{patient.name} Get nurses {env.now - start}")
    
    yield env.timeout(time)
    yield nurses.put(needed)

    if display:
        print(f"{patient.name}, Finished: {env.now-start}")


def utilize_doctors(env, patient, doctors, needed, time, display = True):
    """Generic funcition that will allocate the 'needed' doctors for an alloted
    amount of time.

    Args:
        env (simpy.environemtn): simpy environment for simulation
        patient (Patient): Patient object requesting doctors
        doctors (Container): simpy container from wich doctors are withdrown
        needed (int): number of doctors needed
        time (float): amount of time a doctors are needed for.
        display (bool, optional): Should simulation print display. Defaults to True.
    """
    start = env.now

    if display:
        print(f"{patient.name} Request Doctors {needed} | available {doctors.level}")
    
    yield doctors.get(needed)

    if display:
        print(f"{patient.name} Get doctors {env.now - start}")
    
    yield env.timeout(time)
    yield doctors.put(needed)

    if display:
        print(f"{patient.name}, Finished: {env.now-start}")


def do_processes(env, patient, nurses, doctors, display):
    """Iterates through patients path yielding the appropriate processes.

    Args:
        env (simpy.environment): simpy environment for simulation.
        patient (Patient): Patient object moving through path.
        nurses (simpy.container): simpy container holding available nurses
        doctors (simpy.container): simpy container holding available doctors
        display (bool): weither the simulation should display outputs or not.
    """
    start = env.now
    for process in patient.path:
        if process == "WAITING_ROOM":
            yield env.process(utilize_nurses(env, patient, nurses, needed=1, time=10/60, display=display))
        elif process == "TREATMENT":
            yield env.process(utilize_doctors(env, patient, doctors,
                                            needed=1,
                                            time=(patient.patient_type*30)/60,
                                            display=display))
    wait_times.append(env.now - start)


def run_sim(env, nurses, doctors, rand_state, display = True):
    """Runs the ER simulation with provided nurses and doctors.

    Args:
        env (simpy.environment): simpy environment for simulation
        nurses (simpy.container): Container of nurses for sim.
        doctors (simpy.doctors): Container of doctors for sim.
        rand_state (np.random.Randomstate): specific random state for sim.
        display (bool, optional): Should sim print display. Defaults to True.
    """

    patient_id = 1
    patient = Patient(
                        patient_id=patient_id,
                        rand_state=rand_state,
                        display=display,
                        patient_type=1)
    patient_id += 1

    env.process(do_processes(env, patient, nurses, doctors, display))
    
    while True:
        
        patient = Patient(
                    patient_id=patient_id,
                    rand_state=rand_state,
                    display=display)
        
        yield env.timeout(rand_state.exponential(1.0/.4))

        patient_id += 1

        env.process(do_processes(env, patient, nurses, doctors, display))


def oneSimRun(state):
    """Takes a state for number of doctors and nurses and runs a 
    week long sim and returns the score

    Args:
        state (tuple(int)): holds state for number of doctors and nurses,
        respectfully.

    Returns:
        float: the sum of the ratios avg_waitime/max_weight_time and cost/budget
    """

    global wait_times

    num_doc, num_nurse = state
    env = simpy.Environment()
    nurses = simpy.Container(env, init=num_nurse)
    doctors = simpy.Container(env, init=num_doc)
    env.process(run_sim(env, nurses, doctors, rand_state=np.random.RandomState(123), display=False))
    env.run(until=24*7)

    total_cost = num_doc*4 + num_nurse

    wait_score = np.mean(wait_times)/(30/60)
  
    cost_score = total_cost/100

    if wait_score > 1:
        wait_score = wait_score*10
    
    if cost_score > 1:
        cost_score = cost_score*10

    return  wait_score + cost_score




import KBeam
import random
import EmergencyRoomSim as er_sim


def main():

    # Runs a beam search 10 times and takes average of all results

    results = []
    for _ in range(10):
        set_population = []
        for _ in range(50):
            set_population.append((random.randint(1,10), random.randint(1,20)))

        results.append(KBeam.k_beam_search(set_population=set_population,
                                        fittness_func=er_sim.oneSimRun,
                                        stop_step=100))
    

    num_docs = sum([x[0] for x in results])/len(results)
    num_nurses = sum([x[1] for x in results])/len(results)

    

    print(f"optimal Doctors: {num_docs}")
    print(f"optimal Nurses: {num_nurses}")

    


if __name__ == "__main__":
    main()

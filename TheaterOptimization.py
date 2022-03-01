import KBeam
import random
import TheaterSim


def main():

    # Runs a beam search 10 times and takes average of all results

    results = []
    for _ in range(10):
        set_population = []
        for i in range(100):
            set_population.append((random.randint(1,10), random.randint(1,10),
                                    random.randint(1,10)))


        results.append(KBeam.k_beam_search(set_population=set_population,
                                        fittness_func=TheaterSim.oneSimRun,
                                        stop_step=50))
    
    num_cashiers = sum([x[0] for x in results])/len(results)
    num_servers = sum([x[1] for x in results])/len(results)
    num_ushers = sum([x[2] for x in results])/len(results)
    

    print(f"optimal cashiers: {num_cashiers}")
    print(f"optimal servers: {num_servers}")
    print(f"optimal ushers: {num_ushers}")

    
    

if __name__ == "__main__":
    main()
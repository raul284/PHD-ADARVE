from objects.experiments.Experiment import Experiment

def main():

    experiment = Experiment()
    
    experiment.set_data()
    experiment.analyse_data()
    experiment.export_results()
    experiment.create_graphs()    

if __name__ == "__main__":
    main()
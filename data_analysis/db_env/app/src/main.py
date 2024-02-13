from models.managers.ExperimentManager import ExperimentManager

def main():

    experiment = ExperimentManager()
    
    experiment.set_data()
    experiment.analyse_data()
    experiment.export_results()
    #experiment.create_graphs()   

if __name__ == "__main__":
    main()
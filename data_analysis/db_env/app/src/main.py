from reports.ReportGenerator import ReportGenerator
from objects.experiments.Experiment import Experiment

from auxfile import *

def markdown_manage():
    report = ReportGenerator("../data", "clients.json", "./results", "user_report", {})
    report.generate_report()

def main():

    experiment_id = input("Identificador del experimento: ")

    experiment = Experiment(experiment_id)
    experiment.set_users_data()
    experiment.export_to_csv()
    experiment.analyse_users()
    #experiment.set_global_data()
    #experiment.analyse_global()
    #experiment.export_results()

if __name__ == "__main__":
    main()
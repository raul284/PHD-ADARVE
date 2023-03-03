import pandas as pd

from form.Form import Form
from form.MainInfoForm import MainInfoForm
from form.PersonalDataForm import PersonalDataForm
from form.VideogamesForm import VideogamesForm
from form.EmergencyForm import EmergencyForm
from form.StressForm import StressForm 
from form.ResultsForm import ResultsForm
from form.UXForm import UXForm
from form.DGD1Form import DGD1Form

EXPERIMENT_USER_DATA_PATH = "../data/users/"
EXPERIMENT_USER_RESULT_PATH = "../results/users/"

class FormManager:

    first_form: Form
    main_info_form: MainInfoForm
    personal_data_form: PersonalDataForm
    videogames_form: VideogamesForm
    emergency_form: EmergencyForm
    stress_form: StressForm
    results_form: ResultsForm


    def __init__(self) -> None:
        pass

    def form_to_dataframe(self):
        self.first_form = Form()
        self.first_form.from_csv("../data/estres_interactivo_1.csv")
        self.last_form = Form()
        self.last_form.from_csv("../data/estres_interactivo_2.csv")

        self.main_info_form = MainInfoForm()
        self.main_info_form.from_dataframe(self.first_form._df)
        self.main_info_form.to_csv(EXPERIMENT_USER_DATA_PATH + "{0}".format('main_info.csv'))

        self.personal_data_form = PersonalDataForm()
        self.personal_data_form.from_dataframe(self.first_form._df)
        self.personal_data_form.to_csv(EXPERIMENT_USER_DATA_PATH + "{0}".format('personal_data.csv'))

        self.videogames_form = VideogamesForm()
        self.videogames_form.from_dataframe(self.first_form._df)
        self.videogames_form.to_csv(EXPERIMENT_USER_DATA_PATH + "{0}".format('videogames.csv'))

        self.emergency_form = EmergencyForm()
        self.emergency_form.from_dataframe(self.first_form._df)
        self.emergency_form.to_csv(EXPERIMENT_USER_DATA_PATH + "{0}".format('emergency.csv'))

        self.stress_form = StressForm()
        self.stress_form.from_dataframe(self.first_form._df)
        self.stress_form.to_csv(EXPERIMENT_USER_DATA_PATH + "{0}".format('stress.csv'))

        self.results_form = ResultsForm()
        self.results_form.from_dataframe(self.first_form._df)
        self.results_form.to_csv(EXPERIMENT_USER_RESULT_PATH + "{0}".format('results.csv'))

        self.ux_form = UXForm()
        self.ux_form.from_dataframe(self.last_form._df)
        self.ux_form.to_csv(EXPERIMENT_USER_DATA_PATH + "{0}".format('ux.csv'))

        self.dgd1_form = DGD1Form()
        self.dgd1_form.from_dataframe(self.last_form._df)
        self.dgd1_form.to_csv(EXPERIMENT_USER_DATA_PATH + "{0}".format('dgd1.csv'))
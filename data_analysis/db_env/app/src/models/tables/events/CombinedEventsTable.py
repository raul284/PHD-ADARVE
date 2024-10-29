from models.tables.events.Table import *
from enums.E_UserInputType import UserInputType


class CombinedEventsTable():
    '''
    Class CombinedEventsTable
    -----------------------------
    '''

    #region VARIABLES PUBLICAS

    #endregion
    
    #region METODOS PUBLICOS

    def __init__(self) -> None:

        '''self._results = ResultsTable([
            "OI_NUM_GP_STEPS", 
            "NPC_NUM_GP_STEPS", 
            "MV_NUM_VR_GP_STEPS", 
            "MV_NUM_RL_GP_STEPS",
            "MV_DIST_VR_GP_STEPS", 
            "MV_DIST_RL_GP_STEPS",
            "UI_NUM_GP_STEPS"] + \
            ["UI_NUM_TYPE_{0}_GP_STEPS".format(index.name) for index in UserInputType])'''

    # __init__

    # read_data_from_csv


    def analyse_data(self, tables) -> None:

        aux_results = {
            "OI_NUM_GP_STEPS": self.calculate(tables.get_result_value_from_table("item_interaction_events", "OI_NUM"), tables.get_result_value_from_table("gameplay_events", "GP_NUM")), 
            "NPC_NUM_GP_STEPS": self.calculate(tables.get_result_value_from_table("npc_interaction_events", "NPC_NUM"), tables.get_result_value_from_table("gameplay_events", "GP_NUM")), 
            "MV_NUM_VR_GP_STEPS": self.calculate(tables.get_result_value_from_table("move_events", "MV_NUM_VR"), tables.get_result_value_from_table("gameplay_events", "GP_NUM")), 
            "MV_NUM_RL_GP_STEPS": self.calculate(tables.get_result_value_from_table("move_events", "MV_NUM_RL"), tables.get_result_value_from_table("gameplay_events", "GP_NUM")),
            "MV_DIST_VR_GP_STEPS": self.calculate(tables.get_result_value_from_table("move_events", "MV_DIST_VR"), tables.get_result_value_from_table("gameplay_events", "GP_NUM")), 
            "MV_DIST_RL_GP_STEPS": self.calculate(tables.get_result_value_from_table("move_events", "MV_DIST_RL"), tables.get_result_value_from_table("gameplay_events", "GP_NUM")),
            "UI_NUM_GP_STEPS": self.calculate(tables.get_result_value_from_table("user_input_events", "UI_NUM"), tables.get_result_value_from_table("gameplay_events", "GP_NUM")),
        }

        for index in UserInputType:
            aux_results["UI_NUM_TYPE_{0}_GP_STEPS".format(index.name)] = self.calculate(tables.get_result_value_from_table("user_input_events", "UI_NUM_TYPE_{0}".format(index.name)), tables.get_result_value_from_table("gameplay_events", "GP_NUM"))

        self._results.insert_row(aux_results)
    
    # analyse_data

    #endregion
        
    #region METODOS PRIVADOS

    def calculate(self, first_param, second_param):
        return round(first_param/second_param, 2)

    #endregion
        


    
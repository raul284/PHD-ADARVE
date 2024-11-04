import pandas as pd

from models.TablesGroup import TablesGroup

class CombinedTable():
    '''
    Class CombinedTable
    -----------------------------
    '''

    #region VARIABLES PUBLICAS

    _data: TablesGroup
    _results: dict
    _user_data: dict

    #endregion
    
    #region METODOS PUBLICOS

    def __init__(self, user_data):
        self._user_data = user_data
        self._results = {}

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

    def set_data(self, data):
        self._data = data

    def read_data(self):
        pass
    
    def analyse_data(self):
        self.analyse_number()
        self.analyse_time()
    
    def analyse_number(self):
        self._results["C_OI_GP_N"] = self.calculate("item_interaction", "OI_N", "gameplay", "GP_N")
        self._results["C_NPC_GP_N"] = self.calculate("npc_interaction", "NPC_N", "gameplay", "GP_N")
   
    def analyse_time(self):
        pass
    
    def get_results_df(self) -> pd.DataFrame:
        return pd.DataFrame(self._results)

    #endregion
        
    #region METODOS PRIVADO

    def calculate(self, fst_table, fst_factor_id, snd_table, snd_factor_id):
        return round(
            self.get_results_from_table(fst_table, fst_factor_id) / self.get_results_from_table(snd_table, snd_factor_id), 
            3)

    def get_results_from_table(self, table, key):
        return self._data.get_result_from_table(table)[key]

    #endregion
        


    
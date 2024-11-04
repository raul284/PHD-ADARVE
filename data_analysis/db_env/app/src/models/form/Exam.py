import pandas as pd

from dicts.ExamData import *

class Exam():

    _data: pd.DataFrame
    _results: dict
    _score: float
    
    def __init__(self, data: pd.DataFrame):
        self._data = data
        self._results = {}

    def analyse_data(self):
        for col in self._data:
            score_dict = self.process_answer({col: self._data.iloc[0][col]})
            self._results = {**self._results, **score_dict}

    def get_results(self) -> pd.DataFrame:
        return pd.DataFrame(self._results, index=[0])
    
    def process_answer(self, data):
        question = list(data.keys())[0]
        answer = list(data.values())[0]

        question_id = question.split("[")[1].split("]")[0]
        question_data = self.find_question_data(question_id)

        if question_data["type"] == "one_option":
            return self.process_one_option_answer(question_id, answer)
        else:
            return self.process_multiple_option_answer(question_id, answer)

    def process_one_option_answer(self, id, answer):
        #print(answer)
        return {id: [answer]}

    def process_multiple_option_answer(self, id, answer):
        aux_dict = {}
        question_data = self.find_question_data(id)

        a_index = 0
        for a in question_data["answers"]:
            key = "{0}_{1}".format(id, a_index)

            if a in answer: aux_dict[key] = [1]
            else: aux_dict[key] = [0]
            
            a_index += 1

        return aux_dict

    def find_question_data(self, id):
        for question in exam_data:
            if question["id"] == id:
                return question
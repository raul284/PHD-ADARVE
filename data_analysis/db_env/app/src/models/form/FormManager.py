import pandas as pd

from form.Form import Form

class FormManager:

    _form: Form


    def __init__(self) -> None:
        pass

    def set_data(self, filename):
        self.form = Form()
        self.first_form.from_excel("../data/from_marks.xlsx")

        print(self.first_form._df)
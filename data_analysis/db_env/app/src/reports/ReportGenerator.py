from mdutils.mdutils import MdUtils
from mdutils import Html
import os
import os.path
from datetime import date

class ReportGenerator():
    _markdown_file: MdUtils

    _data: dict

    _import_path:str
    _import_filename:str

    _export_path: str
    _export_filename: str

    def __init__(self, import_path, import_filename, export_path, export_filename, data):
        self._import_path = import_path
        self._import_filename = import_filename

        self._export_path = export_path
        self._export_filename = export_filename

        self._data = data        
            

    def generate_report(self):
        self.generate_md()
        self.insert_metadata()
        self.generate_pdf()
        

    def generate_md(self):
        self._markdown_file = MdUtils(
            file_name = self._export_path + "/" + self._export_filename, 
            title = "")

        self.section_user_info()
        self.section_user_actions()
        self.section_user_stress()
        self.section_user_events()
        self.section_user_images()

        self._markdown_file.new_table_of_contents(table_title='Tabla de Contenidos', depth=2)
        self._markdown_file.create_md_file()


    def generate_pdf(self):
        #os.system("pandoc -s -o {0}/{1}.pdf {2}/{3}.md  --from markdown --template eisvogel --listings".format(self._export_path, self._export_filename, self._export_path, self._export_filename))
        os.system("pandoc -s -o {0}/{1}.html {2}/{3}.md".format(self._export_path, self._export_filename, self._export_path, self._export_filename))

    def insert_metadata(self):
        title = "---\ntitle: Informe de USUARIO_ID de ADARVE\nauthor: [Consejo de Seguridad Nuclear]\ndate: {}\nkeywords: [Markdown, Example]\n...".format(date.today().strftime("%d/%m/%Y"))
        with open(self._export_path + "/" + self._export_filename + ".md", 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(title.rstrip('\r\n') + '\n' + content)


    def section_user_info(self):
        self._markdown_file.new_header(1, "Información del Usuario")

        self._markdown_file.write('Identificador del usuario: ', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("Alejandro"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Identificador de la sesión: ', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("1"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Fecha: ', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("30/11/2022"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Hora: ', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("HH:MM:SS"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Duración de la sesión: ', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("HH:MM:SS"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Puntuación final: ', bold_italics_code='bc')
        self._markdown_file.write(' {0} / 10'.format("10"))
        self._markdown_file.write('  \n')
        

    def section_user_actions(self):
        self._markdown_file.new_header(1, "Acciones realizadas")

        self._markdown_file.write('Ha protegido al conductor:', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("Sí"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Ha obtenido más datos del suceso:', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("Sí"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Ha cortado el tráfico:', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("Sí"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Ha identificado que no hay fuga radiactiva:', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("Sí"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Ha medido la radiación:', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("Sí"))
        self._markdown_file.write('  \n')

        self._markdown_file.write('Ha informado de la situación:', bold_italics_code='bc')
        self._markdown_file.write(' {0}'.format("Sí"))
        self._markdown_file.write('  \n')
    
    def section_user_stress(self):
        self._markdown_file.new_header(1, "Análisis del estrés producido")

        self._markdown_file.new_paragraph("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam convallis elementum est, maximus mattis diam dictum et. Morbi magna libero, accumsan ac vehicula vitae, ornare at diam. Praesent tempor volutpat aliquam. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas.")

        #self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path=self._export_path + "/example_graph_0.png"))
        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path="example_graph_0.png"))
        self._markdown_file.write('  \n')

        self._markdown_file.new_paragraph("Suspendisse potenti. Vivamus et interdum lacus. Etiam vestibulum semper tortor eget tempus. Fusce lacinia pretium elit, nec dapibus eros tempor sed. Maecenas eget venenatis tortor, non tristique lacus. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas ultrices justo magna. Nullam porttitor euismod magna, et tempus orci iaculis vitae. Ut nibh est, venenatis nec venenatis eu, dignissim a felis.")

        self._markdown_file.new_paragraph("Vestibulum blandit risus id rhoncus porta. Etiam metus nisl, vulputate at felis at, facilisis vulputate magna. Nullam nec vehicula nisi. Sed at arcu a nunc tempus aliquet in non libero. Integer nec lorem id lectus egestas laoreet. Vestibulum id nibh bibendum, vehicula velit non, fermentum erat. Ut imperdiet nisl non mollis consectetur. Sed sem tellus, suscipit id justo et, aliquet finibus eros. Vivamus eget purus id odio aliquam congue vitae vel justo.")

        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 2", path="example_graph_1.png"))
        self._markdown_file.write('  \n')

        self._markdown_file.new_paragraph("Sed nibh tellus, ultrices nec sodales in, sagittis viverra urna. Suspendisse potenti. In euismod sit amet mauris quis rhoncus. Suspendisse mi arcu, pharetra sit amet ultrices vel, rutrum id velit. Donec eu auctor diam. Maecenas risus risus, vulputate a felis ac, laoreet faucibus orci. Mauris vulputate id libero sed maximus. Nam auctor efficitur est, ut consectetur massa mattis sed. Nullam quis ullamcorper eros. Nulla et auctor tortor, at interdum quam. Pellentesque venenatis imperdiet felis, at luctus erat consequat vel.")
        self._markdown_file.write('  \n')

    def section_user_events(self):
        self._markdown_file.new_header(1, "Listado de eventos")

        list_of_strings = ["Evento", "Fecha", "Hora", "Nombre del actor"]
        list_of_strings.extend(["Hablar con obrero", "30/11/2022", "HH:MM:SS", "Alberto"])
        list_of_strings.extend(["Hablar con conductor", "30/11/2022", "HH:MM:SS", "Gavy"])
        list_of_strings.extend(["Coger un cono de tráfico", "30/11/2022", "HH:MM:SS", "Cono de tráfico"])
        list_of_strings.extend(["Cortado el tráfico en carríl", "30/11/2022", "HH:MM:SS", "Cono de tráfico"])
        list_of_strings.extend(["Abrir la furgoneta", "30/11/2022", "HH:MM:SS", "Furgoneta"])
        #for x in range(5):
        #    list_of_strings.extend(["Evento " + str(x), "Fecha " + str(x), "Hora " + str(x), "Nombre del actor " + str(x)])
        self._markdown_file.new_line()
        self._markdown_file.new_table(columns=4, rows=6, text=list_of_strings, text_align='center')

    def section_user_images(self):
        self._markdown_file.new_header(1, "Imágenes extraídas de la sesión")

        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path="Screenshot_Wed_Nov_30_12-27-25_2022.png"))
        self._markdown_file.write('  \n')

        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path="Screenshot_Wed_Nov_30_12-27-58_2022.png"))
        self._markdown_file.write('  \n')

        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path="Screenshot_Wed_Nov_30_12-28-04_2022.png"))
        self._markdown_file.write('  \n')

        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path="Screenshot_Wed_Nov_30_12-28-30_2022.png"))
        self._markdown_file.write('  \n')

        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path="Screenshot_Wed_Nov_30_12-28-56_2022.png"))
        self._markdown_file.write('  \n')

        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path="Screenshot_Wed_Nov_30_12-29-11_2022.png"))
        self._markdown_file.write('  \n')

        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path="Screenshot_Wed_Nov_30_12-29-27_2022.png"))
        self._markdown_file.write('  \n')

        self._markdown_file.new_line(self._markdown_file.new_inline_image(text="Ejemplo de gráfica 1", path="Screenshot_Wed_Nov_30_12-29-34_2022.png"))
        self._markdown_file.write('  \n')
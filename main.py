import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar
from kivy.uix.textinput import TextInput
from kivy.config import Config
from tkinter import Tk
from tkinter.filedialog import askdirectory
import glob
import img2pdf
from kivy.resources import resource_add_path, resource_find

Config.set('kivy', 'window_icon', resource_find('icons/icon.ico'))
resource_add_path('./icons')

Config.set('graphics', 'width', '400')
Config.set('graphics', 'height', '600')
Config.set('graphics', 'backend', 'gl')
class RootWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.orientation = 'vertical'


        self.current_folder_label = Label(text='No folder selected', size_hint=(1, 0.1))

        self.path = None

        self.top_box = BoxLayout(
            orientation='horizontal',
            size_hint=(1, 0.1),
            padding=(10, 10)
        )

        self.brand_label = Label(
            text='Img to PDF',
            font_size=20,
            bold=True,
            size_hint=(0.8, 1),
            valign='center'
        )
        self.top_box.add_widget(self.brand_label)

        self.add_widget(self.top_box)

        self.file_chooser = FileChooserListView(
            path=os.getcwd(),
            filters=['*.jpg', '*.png', '*.jpeg', "*.pdf"],
            size_hint=(1, 0.6),
            opacity=0.0 
        )

        self.conversion_text_input = TextInput(
            text='output.pdf',
            size_hint=(1, 0.1)
        )

        self.select_folder_button = Button(
            text='Select Folder',
            size_hint=(1, 0.1)
        )

        self.select_folder_button.bind(on_press=self.select_folder)

        self.convert_button = Button(
            text='Convert',
            size_hint=(1, 0.1)
        )

        self.convert_button.bind(on_press=self.convert_folder)

        self.add_widget(self.current_folder_label)
        self.add_widget(self.select_folder_button)
        self.add_widget(self.file_chooser)
        self.add_widget(self.conversion_text_input)
        self.add_widget(self.convert_button)

 
    def select_folder(self, instance):
        Tk().withdraw() 
        selected_folder = askdirectory()
        if selected_folder:
            self.file_chooser.rootpath = selected_folder
            self.file_chooser.path = selected_folder
            self.file_chooser.selection = []   
            self.file_chooser.opacity = 1.0
            self.current_folder_label.text = selected_folder
            self.path = selected_folder
            self.file_chooser._update_files() 
            self.convert_button.background_color = [0, 0.5, 1, 1]

    def convert_folder(self, instance):
        if not self.path:
            popup = Popup(
                title='Error',
                content=Label(text='No folder selected.'),
                size_hint=(None, None),
                size=(200, 100)
            )
            popup.open()
            return

        folder_path = self.path
        output_filename = self.conversion_text_input.text
        progress_bar = ProgressBar(max=1000)
        popup = Popup(
            title='Converting...',
            content=progress_bar,
            size_hint=(None, None),
            size=(200, 100)
        )

        ALLOWED_EXTENSIONS = ['jpg', 'jpeg', 'png']
        files = glob.glob(folder_path + '/*')
        images = [file for file in files if file.split('.')[-1] in ALLOWED_EXTENSIONS]
        images.sort(key=lambda f: int(''.join(filter(str.isdigit, f))))
        progress_bar.max = len(images)
        output_dir = os.path.join(folder_path, output_filename)
        with open(output_dir, 'wb') as f:
            f.write(img2pdf.convert(images))
            progress_bar.value += 1
        popup.title = 'Done!'
        self.file_chooser._update_files()
        success_popup = Popup(
            title='Success!',
            content=Label(text='Conversion complete.'),
            size_hint=(None, None),
            size=(200, 100)
        )
        success_popup.open()


class PDFConverterApp(App):
    def build(self):
        self.title = 'Img to PDF Converter'
        self.icon = 'icons/icon.ico'
        return RootWidget()
    
def reset():
    import kivy.core.window as window
    from kivy.base import EventLoop
    if not EventLoop.event_listeners:
        from kivy.cache import Cache
        window.Window = window.core_select_lib('window', window.window_impl, True)
        Cache.print_usage()
        for cat in Cache._categories:
            Cache._objects[cat] = {}
if __name__ == '__main__':
    reset()
    PDFConverterApp().run()
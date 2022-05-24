import dearpygui.dearpygui as dpg

class Interface:
    def __init__(self,reader,converter):
        dpg.create_context()
        dpg.create_viewport(title='PDF to Speech', width=800, height=800,resizable=False,max_width=800,max_height=800)
        dpg.set_viewport_small_icon("Misc/favicon.ico")

        self.filepaths =[]
        self.safedir = ""


        def convert():
            if  self.filepaths  == [] or self.filepaths[0][-5]=="\\":
                return dpg.configure_item("error", show=True)
            reader.pages_text = []
            dpg.configure_item("loading", show=True)
            dpg.configure_item(item="work", default_value="Extracting Pages")
            for i in range(len(self.filepaths)):
                reader.pages_text.append("")
                reader.measure_pages(self.filepaths[i])
                dpg.configure_item("loading", label=f"Work in Progress ({i} / {len(self.filepaths)})")
                dpg.configure_item(item="progress", default_value=0)
                for page in range(reader.number_of_pages):
                    reader.extract_page(page,i)
                    dpg.configure_item(item="progress", default_value = 1/reader.number_of_pages * (page+1))
            dpg.configure_item(item="progress", default_value=0)
            for i in range(len(self.filepaths)):
                dpg.configure_item("loading", label=f"Work in Progress ({i} / {len(self.filepaths)})")
                dpg.configure_item(item="work", default_value = "Converting To Speech")

                converter.create_mp3(text=reader.pages_text[i],name=self.filepaths[i].split('\\')[-1].split('.')[0],safedir=self.safedir)
                dpg.configure_item(item="progress", default_value=1/len(self.filepaths)*(i+1))

            dpg.configure_item(item="loading",label = "All Done")
            dpg.configure_item(item="work", default_value="Finished")
            dpg.show_item("Return")

        def select_file():
            dpg.show_item("file_dialog")

        def selected_file(sender, app_data, user_data):
            self.filepaths = []
            for value in app_data["selections"].values():
                self.filepaths.append(value)
                print(value)
            dpg.hide_item("dir_dialog")

        def select_dir():
            dpg.show_item("dir_dialog")

        def selected_dir(sender, app_data, user_data):
            self.safedir = app_data['file_path_name']

            dpg.hide_item("dir_dialog")

        # Main Window
        with dpg.window(tag="Window"):
            with dpg.group(horizontal=False,pos=[220,200]):
                select_file_btn = dpg.add_button(label="Select PDF Files", callback=select_file, tag="select_file",width=400)
                select_dir_btn= dpg.add_button(label="Select Output Directory",  callback=select_dir, tag="output_dir_btn", width=400)
                convert = dpg.add_button(label="Convert Files",callback=convert, tag="Go",width=400)



        # file dialogues
        with dpg.file_dialog(directory_selector=False, show=False, callback=selected_file, id="file_dialog",width=650,height=600):
            dpg.add_file_extension(".pdf", color=(0, 255, 0, 255), custom_text="[PDF]")

        dpg.add_file_dialog(directory_selector=True, show=False, callback=selected_dir, id="dir_dialog",width=650,height=600)

        # Selecting fonts
        with dpg.font_registry():
            default_font = dpg.add_font("Misc/Letters for Learners.ttf", 50)
            dpg.bind_item_font(item=select_file_btn, font=default_font)
            dpg.bind_item_font(item=convert, font=default_font)
            dpg.bind_item_font(item=select_dir_btn, font=default_font)


        #Error Popup
        with  dpg.window(label="Error", modal=True, show=False, id="error",pos=[100,200],no_resize=True) as error:
            with dpg.font_registry():
                dpg.bind_item_font(item=error, font=default_font)
            dpg.add_text("Please, select a file before proceeding")
            dpg.add_separator()
            dpg.add_button(label="OK",tag="ok", width=75, callback=lambda: dpg.configure_item("error", show=False))

        # Loading Popup
        with  dpg.window(label="Work in Progress",no_scrollbar=True, modal=True, show=False, id="loading", pos=[100, 130], width=600,height=255,no_resize=True, no_close=True,no_move=True) as loading:
            with dpg.font_registry():
                dpg.bind_item_font(item=loading, font=default_font)
            dpg.add_text(default_value="Extracting pages..",tag="work")
            dpg.add_separator()
            progress = dpg.add_progress_bar(label="Progress",tag="progress", default_value=0,width=600)
            dpg.add_separator()
            dpg.add_button(label="Return",show=False, tag="Return",width=600,callback=lambda: dpg.configure_item("loading", show=False))



        dpg.setup_dearpygui()
        dpg.show_viewport()

        dpg.set_primary_window("Window", True)
        dpg.start_dearpygui()
        dpg.destroy_context()



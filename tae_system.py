import customtkinter as ctk

class TaekwondoScoreboard(ctk.CTk):
    APP_NAME = "Taekwondo System"
    WIDTH = 850
    HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.title(TaekwondoScoreboard.APP_NAME)
        self.geometry(str(TaekwondoScoreboard.WIDTH) + "x" + str(TaekwondoScoreboard.HEIGHT))
        self.minsize(TaekwondoScoreboard.WIDTH, TaekwondoScoreboard.HEIGHT)

        self.blue_name = "Chung"
        self.red_name = "Hong"
        self.init_combat_time = (0*60) + 5
        self.init_rest_time = (0*60) + 40
        self.init_keyshi_time = (1*60) + 0
        self.gamjeom_limit = 6
        self.points_diff = 12

        self.combat_time = self.init_combat_time
        self.rest_time = self.init_rest_time
        self.run_combat_time = False
        self.run_rest_time = False

        self.blue_points = 0
        self.red_points = 0

        self.blue_gamjeoms = 0
        self.red_gamjeoms = 0

        self.blue_points_by_round = [0,0,0]
        self.red_points_by_round = [0,0,0]

        self.create_widgets()

    # Funciones para crear la interfaz y sus widgets
    # --------------------------------------------------------------------
    def create_widgets(self):
        # Configuramos la ventana
        self.rowconfigure(0, weight=59)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Frame para todos los elementos del marcador de taekwondo
        self.score_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.score_frame.grid(row=0, column=0, sticky="nesw")

        # Frame para los elementos de configuracion
        self.options_frame = ctk.CTkFrame(master=self, corner_radius=0)
        self.options_frame.grid(row=1, column=0, sticky="nesw")

        self.create_scoreboard()
        self.create_options_frame()
    
    def create_scoreboard(self):
        self.score_frame.rowconfigure(0, weight=1)
        for i, value in enumerate([2,1,2]):
            self.score_frame.columnconfigure(i, weight=value)
        
        self.middle_frame = ctk.CTkFrame(master=self.score_frame, fg_color="black", corner_radius=0)
        self.middle_frame.grid(row=0, column=1, sticky="nesw")

        self.blue_frame = ctk.CTkFrame(master=self.score_frame, fg_color="blue", corner_radius=0)
        self.blue_frame.grid(row=0, column=0, sticky="nesw")

        self.red_frame = ctk.CTkFrame(master=self.score_frame, fg_color="red", corner_radius=0)
        self.red_frame.grid(row=0, column=2, sticky="nesw")

        self.create_blue_board_elements()
        self.create_middle_board_elements()
        self.create_red_board_elements()
    
    def create_middle_board_elements(self):
        self.middle_frame.columnconfigure(0, weight=1)
        for i in range(5):
            self.middle_frame.rowconfigure(i, weight=1)

        label_vs = ctk.CTkLabel(master=self.middle_frame, text="VS", font=("consolas", 60))
        label_vs.grid(row=0, column=0, sticky="nesw")

        self.label_num_round = ctk.CTkLabel(master=self.middle_frame, text="R1", font=("consolas", 60))
        self.label_num_round.grid(row=1, column=0, sticky="nesw")

        self.label_time = ctk.CTkLabel(master=self.middle_frame, text=f"{self.init_combat_time//60}:{(self.init_combat_time%60):02}", font=("consolas", 100))
        self.label_time.grid(row=2, column=0, sticky="nesw")

        self.label_timeout = ctk.CTkLabel(master=self.middle_frame, text="", font=("consolas", 40))
        self.label_timeout.grid(row=3, column=0, sticky="nesw")

        self.label_keyshi_time = ctk.CTkLabel(master=self.middle_frame, text=f"{self.init_keyshi_time//60}:{(self.init_keyshi_time%60):02}", font=("consolas", 40))
        self.label_keyshi_time.grid(row=4, column=0, sticky="nesw")
    
    def create_blue_board_elements(self):
        for i in range(5):
            self.blue_frame.columnconfigure(i, weight=1)
            self.blue_frame.rowconfigure(i, weight=1)
        
        self.blue_name_label = ctk.CTkLabel(master=self.blue_frame, text=self.blue_name, font=("consolas", 60))
        self.blue_name_label.grid(row=0, column=0, columnspan=5, sticky="nesw") 

        self.blue_points_label = ctk.CTkLabel(master=self.blue_frame, text=str(self.blue_points), font=("consolas", 200))
        self.blue_points_label.grid(row=1, column=1, columnspan=3, rowspan=3, sticky="nesw")

        self.blue_gamjeon_label = ctk.CTkLabel(master=self.blue_frame, text=str(self.blue_gamjeoms), text_color="yellow", font=("consolas", 80))
        self.blue_gamjeon_label.grid(row=3, column=0, sticky="nesw")

        self.blue_J1_label = ctk.CTkLabel(master=self.blue_frame, text="J1", font=("consolas", 40))
        self.blue_J1_label.grid(row=4, column=1, sticky="nesw")

        self.blue_J2_label = ctk.CTkLabel(master=self.blue_frame, text="J2", font=("consolas", 40))
        self.blue_J2_label.grid(row=4, column=2, sticky="nesw")

        self.blue_J3_label = ctk.CTkLabel(master=self.blue_frame, text="J3", font=("consolas", 40))
        self.blue_J3_label.grid(row=4, column=3, sticky="nesw")
    
    def create_red_board_elements(self):
        for i in range(5):
            self.red_frame.columnconfigure(i, weight=1)
            self.red_frame.rowconfigure(i, weight=1)
        
        self.red_name_label = ctk.CTkLabel(master=self.red_frame, text=self.red_name, font=("consolas", 60))
        self.red_name_label.grid(row=0, column=0, columnspan=5, sticky="nesw") 

        self.red_points_label = ctk.CTkLabel(master=self.red_frame, text=str(self.red_points), font=("consolas", 200))
        self.red_points_label.grid(row=1, column=1, columnspan=3, rowspan=3, sticky="nesw")

        self.red_gamjeon_label = ctk.CTkLabel(master=self.red_frame, text=str(self.red_gamjeoms), text_color="yellow", font=("consolas", 80))
        self.red_gamjeon_label.grid(row=3, column=4, sticky="nesw")

        self.red_J1_label = ctk.CTkLabel(master=self.red_frame, text="J1", font=("consolas", 40))
        self.red_J1_label.grid(row=4, column=1, sticky="nesw")

        self.red_J2_label = ctk.CTkLabel(master=self.red_frame, text="J2", font=("consolas", 40))
        self.red_J2_label.grid(row=4, column=2, sticky="nesw")

        self.red_J3_label = ctk.CTkLabel(master=self.red_frame, text="J3", font=("consolas", 40))
        self.red_J3_label.grid(row=4, column=3, sticky="nesw")
    
    def create_options_frame(self):
        # Entry para ejecutar comandos y modificar el marcador
        self.command_entry = ctk.CTkEntry(master=self.options_frame, placeholder_text="Comandos")
        self.command_entry.grid(row=0, column=2, columnspan=3, sticky="nesw", padx=10, pady=10)
        self.command_entry.bind("<Return>", self.execute_command)    # Vincular la tecla Enter al Entry para ejecutar el comando

        # Creamos los botones
        # button_texts = ["Configuracion", "Pausar/Reanudar", "Modificar Marcador", "Key-shi", "Finalizar Round", "Finalizar Combate", "Siguiente Round"]
        # button_commands = [self.configuration, self.toggle_timer, self.edit_score, self.key_shi, self.finish_round, self.finish_combat, self.next_round]

        # # Agregamos funcionalidad a los botones
        # for i, (text, command) in enumerate(zip(button_texts, button_commands)):
        #     button = ctk.CTkButton(master=self.options_frame, text=text, fg_color="#464646", command=command)
        #     button.grid(row=1, column=i, sticky="nesw", padx=10, pady=10)
        
        self.btn_configuration = ctk.CTkButton(master=self.options_frame, text="Configuracion", fg_color="#464646", command=self.configuration, state="normal")
        self.btn_configuration.grid(row=1, column=0, sticky="nesw", padx=10, pady=10)
        self.btn_pause_resume = ctk.CTkButton(master=self.options_frame, text="Iniciar Combate", fg_color="#464646", command=self.toggle_timer, state="normal")
        self.btn_pause_resume.grid(row=1, column=1, sticky="nesw", padx=10, pady=10)
        self.btn_edit_score = ctk.CTkButton(master=self.options_frame, text="Modificar Marcador", fg_color="#464646", command=self.edit_score, state="normal")
        self.btn_edit_score.grid(row=1, column=2, sticky="nesw", padx=10, pady=10)
        self.btn_key_shi = ctk.CTkButton(master=self.options_frame, text="Keyshi", fg_color="#464646", command=self.keyshi, state="disabled")
        self.btn_key_shi.grid(row=1, column=3, sticky="nesw", padx=10, pady=10)
        self.btn_finish_round = ctk.CTkButton(master=self.options_frame, text="Finalizar Round", fg_color="#464646", command=self.finish_round, state="disabled")
        self.btn_finish_round.grid(row=1, column=4, sticky="nesw", padx=10, pady=10)
        self.btn_finish_combat = ctk.CTkButton(master=self.options_frame, text="Finalizar Combate", fg_color="#464646", command=self.finish_combat, state="disabled")
        self.btn_finish_combat.grid(row=1, column=5, sticky="nesw", padx=10, pady=10)
        self.btn_next_round = ctk.CTkButton(master=self.options_frame, text="Siguiente Round", fg_color="#464646", command=self.next_round, state="disabled")
        self.btn_next_round.grid(row=1, column=6, sticky="nesw", padx=10, pady=10)

        # Configuramos proporciones del frame
        self.options_frame.rowconfigure(0, weight=1)
        self.options_frame.rowconfigure(1, weight=1)
        for i in range(7):
            self.options_frame.columnconfigure(i, weight=1)
        # for i, text in enumerate(button_texts):
        #     self.options_frame.columnconfigure(i, weight=1)

    # Funciones de los botones
    # --------------------------------------------------------------------
    def execute_command(self, event=None):
        self.command_entry.delete(0, ctk.END)

    def configuration(self):
        # Crear ventana de configuración
        self.config_window = ctk.CTkToplevel(self)
        self.config_window.title("Configuración de combate")
        self.config_window.geometry("370x420")
        self.config_window.grab_set()

        # Deshabilitar redimensionamiento
        self.config_window.resizable(False, False)

        # Crear y colocar etiquetas y campos de entrada
        label_blue_name = ctk.CTkLabel(master=self.config_window, text="Nombre Jugador Azul:")
        label_blue_name.grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.entry_blue_name = ctk.CTkEntry(master=self.config_window, placeholder_text="Chung")
        self.entry_blue_name.grid(row=0, column=1, padx=10, pady=10, sticky="we")

        label_red_name = ctk.CTkLabel(master=self.config_window, text="Nombre Jugador Rojo:")
        label_red_name.grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.entry_red_name = ctk.CTkEntry(master=self.config_window, placeholder_text="Hong")
        self.entry_red_name.grid(row=1, column=1, padx=10, pady=10, sticky="we")

        label_time_config = ctk.CTkLabel(master=self.config_window, text="Tiempo de Combate [mm:ss]:")
        label_time_config.grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.entry_time = ctk.CTkEntry(master=self.config_window)
        self.entry_time.grid(row=2, column=1, padx=10, pady=10)
        self.entry_time.insert(0, f"{self.init_combat_time//60}:{(self.init_combat_time%60):02}")

        label_restTime_config = ctk.CTkLabel(master=self.config_window, text="Tiempo de Descanso [mm:ss]:")
        label_restTime_config.grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.entry_restTime = ctk.CTkEntry(master=self.config_window)
        self.entry_restTime.grid(row=3, column=1, padx=10, pady=10)
        self.entry_restTime.insert(0, f"{self.init_rest_time//60}:{(self.init_rest_time%60):02}")

        label_keyshiTime_config = ctk.CTkLabel(master=self.config_window, text="Tiempo para Keyshi [mm:ss]:")
        label_keyshiTime_config.grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.entry_keyshiTime = ctk.CTkEntry(master=self.config_window)
        self.entry_keyshiTime.grid(row=4, column=1, padx=10, pady=10)
        self.entry_keyshiTime.insert(0, f"{self.init_keyshi_time//60}:{(self.init_keyshi_time%60):02}")

        label_points_diff_config = ctk.CTkLabel(master=self.config_window, text="Diferencia de puntos:")
        label_points_diff_config.grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.entry_points_diff_config = ctk.CTkEntry(master=self.config_window)
        self.entry_points_diff_config.grid(row=5, column=1, padx=10, pady=10)
        self.entry_points_diff_config.insert(0, self.points_diff)

        label_gamjeon_limit_config = ctk.CTkLabel(master=self.config_window, text="Limite de Gamjeoms:")
        label_gamjeon_limit_config.grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.entry_gamjeon_limit_config = ctk.CTkEntry(master=self.config_window)
        self.entry_gamjeon_limit_config.grid(row=6, column=1, padx=10, pady=10)
        self.entry_gamjeon_limit_config.insert(0, self.gamjeom_limit)

        # Crear y colocar botón de aplicar cambios
        button_apply = ctk.CTkButton(master=self.config_window, text="Aplicar", command=self.apply_config)
        button_apply.grid(row=10, column=1, pady=20)

    def toggle_timer(self):
        self.run_combat_time = not self.run_combat_time
        if self.run_combat_time:
            self.btn_pause_resume.configure(text="Pausar")
            self.update_combat_timer()
        else:
            self.btn_pause_resume.configure(text="Reanudar")       

    def edit_score(self):
        return
    def keyshi(self):
        return
    def finish_round(self):
        return
    def finish_combat(self):
        return
    def next_round(self):
        return

    # Funciones auxiliares
    # --------------------------------------------------------------------
    def update_combat_timer(self):
        if self.run_combat_time and not self.run_rest_time:
            if self.combat_time > 0:
                minutes, seconds = divmod(self.combat_time, 60)
                self.label_time.configure(text=f"{minutes}:{seconds:02d}")
                self.combat_time -= 1
                self.after(1000, self.update_combat_timer)
            else:
                self.run_rest_time = True
                self.run_combat_time = False
                self.update_rest_timer()
    
    def update_rest_timer(self):
        if self.rest_time > 0:
            minutes, seconds = divmod(self.rest_time, 60)
            self.label_time.configure(text=f"{minutes}:{seconds:02d}")
            self.rest_time -= 1
            self.after(1000, self.update_rest_timer)
        else:
            self.label_time.configure(text="FIN")

    def apply_config(self):
        try:
            # Obtener valores de los campos de entrada 
            self.blue_name = self.entry_blue_name.get() if self.entry_blue_name.get() != "" else "Chung"
            self.red_name = self.entry_red_name.get() if self.entry_red_name.get() != "" else "Hong"

            time_min, time_seg = self.entry_time.get().split(":")
            rest_time_min, rest_time_seg = self.entry_restTime.get().split(":")
            keyshi_time_min, keyshi_time_seg = self.entry_keyshiTime.get().split(":")
            
            self.gamjeon_limit = int(self.entry_gamjeon_limit_config.get())
            self.points_diff = int(self.entry_points_diff_config.get())

            self.time = int(time_min)*60 + int(time_seg)
            self.rest_time = int(rest_time_min)*60 + int(rest_time_seg)
            self.keyshi_time = int(keyshi_time_min)*60 + int(keyshi_time_seg)

            # Actualizar etiquetas correspondientes
            self.blue_name_label.configure(text=self.blue_name)
            self.red_name_label.configure(text=self.red_name)
            self.label_time.configure(text=self.entry_time.get())
            self.label_keyshi_time.configure(text=self.entry_keyshiTime.get())

            # Cerrar ventana de configuración
            self.config_window.destroy()
        except Exception as e:
            print(e)
    
if __name__ == "__main__":
    app = TaekwondoScoreboard()
    app.mainloop()
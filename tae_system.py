import customtkinter as ctk
import pygame

# Modificando la apariencia
ctk.set_appearance_mode("System")           # Modes: "System" (standard), "Dark", "Light"
ctk.set_default_color_theme("dark-blue")    # Themes: "blue" (standard), "green", "dark-blue"

class TaekwondoScoreboard(ctk.CTk):
    APP_NAME = "Taekwondo System"
    WIDTH = 850
    HEIGHT = 600
    FONT_CONSOLAS_60 = ("consolas", 60)
    FONT_CONSOLAS_40 = ("consolas", 40)
    FONT_CONSOLAS_100 = ("consolas", 100)
    FONT_CONSOLAS_200 = ("consolas", 200)
    FONT_CONSOLAS_80 = ("consolas", 80)
    FG_COLOR_BLACK = "black"
    FG_COLOR_BLUE = "blue"
    FG_COLOR_RED = "red"
    FG_COLOR_YELLOW = "yellow"
    FG_COLOR_GRAY = "#464646"
    FG_COLOR_GRAY2 = "#212121"

    def __init__(self):
        super().__init__()
        self.title(TaekwondoScoreboard.APP_NAME)
        self.geometry(str(TaekwondoScoreboard.WIDTH) + "x" + str(TaekwondoScoreboard.HEIGHT))
        self.minsize(TaekwondoScoreboard.WIDTH, TaekwondoScoreboard.HEIGHT)

        self.initialize_variables()
        self.create_widgets()

        self.bind("<space>", self.on_key_press)

        # Inicializar pygame mixer y cargamos el sonido de la alarma
        pygame.mixer.init()
        pygame.mixer.music.load("alarm.wav")

    def on_key_press(self, event):
        if event.keysym == "space":
            self.btn_pause_resume.invoke()

    def initialize_variables(self):
        self.blue_name = "Chung"
        self.red_name = "Hong"
        self.init_combat_time = 5
        self.init_rest_time = 3
        self.init_keyshi_time = 60
        self.gamjeom_limit = 6
        self.points_diff = 12
        self.round = 1
        
        self.combat_time = self.init_combat_time
        self.rest_time = self.init_rest_time
        self.run_combat_time = False
        
        self.blue_points = 0
        self.red_points = 0
        
        self.blue_won_rounds = 0
        self.red_won_rounds = 0
        self.blue_gamjeoms = 0
        self.red_gamjeoms = 0

    def create_frame(self, parent, row, column, corner_radius=0, fg_color=None):
        frame = ctk.CTkFrame(master=parent, corner_radius=corner_radius, fg_color=fg_color)
        frame.grid(row=row, column=column, sticky="nesw")
        return frame

    def create_label(self, parent, text, row, column, columnspan=1, rowspan=1, sticky="nesw", font=None, text_color=None, bg_color="transparent"):
        label = ctk.CTkLabel(master=parent, text=text, font=font, bg_color=bg_color)
        label.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky=sticky)
        if text_color:
            label.configure(text_color=text_color)
        return label

    def create_button(self, parent, text, row, column, command, fg_color=None, state="normal"):
        button = ctk.CTkButton(master=parent, text=text, fg_color=fg_color, command=command, state=state)   # , hover_color="black"
        button.grid(row=row, column=column, sticky="nesw", padx=10, pady=10)
        return button

    def create_entry(self, parent, row, column, columnspan=1, rowspan=1, placeholder_text=None, text=None, state="normal"):
        entry = ctk.CTkEntry(master=parent, placeholder_text=placeholder_text, state=state)
        entry.grid(row=row, column=column, columnspan=columnspan, rowspan=rowspan, sticky="nesw", padx=10, pady=10)
        if text:
            entry.insert(0, text)
        return entry

    def create_widgets(self):
        # Configuramos la distribucion de laventana
        self.rowconfigure(0, weight=59)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1)

        # Frame para todos los elementos del marcador de taekwondo
        # y el frame para los elementos de configuracion
        self.score_frame = self.create_frame(parent=self, row=0, column=0)
        self.options_frame = self.create_frame(parent=self, row=1, column=0)

        self.create_scoreboard()
        self.create_options_frame()
    
    def create_scoreboard(self):
        # Configuramos la distribucion del frame
        self.score_frame.rowconfigure(0, weight=1)
        for i, value in enumerate([2,1,2]):
            self.score_frame.columnconfigure(i, weight=value)
        
        self.middle_frame = self.create_frame(parent=self.score_frame, row=0, column=1, fg_color=TaekwondoScoreboard.FG_COLOR_BLACK)
        self.blue_frame = self.create_frame(parent=self.score_frame, row=0, column=0, fg_color=TaekwondoScoreboard.FG_COLOR_BLUE)
        self.red_frame = self.create_frame(parent=self.score_frame, row=0, column=2, fg_color=TaekwondoScoreboard.FG_COLOR_RED)

        self.create_blue_board_elements()
        self.create_middle_board_elements()
        self.create_red_board_elements()
    
    def create_middle_board_elements(self):
        self.middle_frame.columnconfigure(0, weight=1)
        for i in range(5):
            self.middle_frame.rowconfigure(i, weight=1)

        self.create_label(parent=self.middle_frame, text="VS", row=0, column=0, font=TaekwondoScoreboard.FONT_CONSOLAS_60)
        self.label_num_round    = self.create_label(parent=self.middle_frame, text=f"R{self.round}", row=1, column=0, font=TaekwondoScoreboard.FONT_CONSOLAS_60)
        self.label_time         = self.create_label(parent=self.middle_frame, text=f"{self.init_combat_time//60}:{(self.init_combat_time%60):02}", row=2, column=0, font=TaekwondoScoreboard.FONT_CONSOLAS_100)
        self.label_actions      = self.create_label(parent=self.middle_frame, text="Esperando", row=3, column=0, font=TaekwondoScoreboard.FONT_CONSOLAS_40, bg_color=TaekwondoScoreboard.FG_COLOR_YELLOW, text_color="black")
        self.label_keyshi_time  = self.create_label(parent=self.middle_frame, text=f"{self.init_keyshi_time//60}:{(self.init_keyshi_time%60):02}", row=4, column=0, font=TaekwondoScoreboard.FONT_CONSOLAS_40)
    
    def create_blue_board_elements(self):
        for i in range(5):
            self.blue_frame.columnconfigure(i, weight=1)
            self.blue_frame.rowconfigure(i, weight=1)
        
        self.label_blue_name    = self.create_label(parent=self.blue_frame, text=self.blue_name, row=0, column=0, columnspan=5, font=TaekwondoScoreboard.FONT_CONSOLAS_60)
        self.label_blue_points  = self.create_label(parent=self.blue_frame, text=str(self.blue_points), row=1, column=1, columnspan=3, rowspan=3, font=TaekwondoScoreboard.FONT_CONSOLAS_200)
        self.label_blue_gamjeon = self.create_label(parent=self.blue_frame, text=str(self.blue_gamjeoms), row=3, column=0, text_color="yellow", font=TaekwondoScoreboard.FONT_CONSOLAS_80)

        judges_start_col = 1
        for i in range(3):
            self.create_label(parent=self.blue_frame, text=f"J{i+1}", row=4, column=judges_start_col + i, font=TaekwondoScoreboard.FONT_CONSOLAS_40)
    
    def create_red_board_elements(self):
        for i in range(5):
            self.red_frame.columnconfigure(i, weight=1)
            self.red_frame.rowconfigure(i, weight=1)
        
        self.label_red_name = self.create_label(parent=self.red_frame, text=self.red_name, row=0, column=0, columnspan=5, font=TaekwondoScoreboard.FONT_CONSOLAS_60)
        self.label_red_points = self.create_label(parent=self.red_frame, text=str(self.red_points), row=1, column=1, columnspan=3, rowspan=3, font=TaekwondoScoreboard.FONT_CONSOLAS_200)
        self.label_red_gamjeon = self.create_label(parent=self.red_frame, text=str(self.red_gamjeoms), row=3, column=4, text_color="yellow", font=TaekwondoScoreboard.FONT_CONSOLAS_80)

        judges_start_col = 1
        for i in range(3):
            self.create_label(parent=self.red_frame, text=f"J{i+1}", row=4, column=judges_start_col + i, font=TaekwondoScoreboard.FONT_CONSOLAS_40)
    
    def create_options_frame(self):
        # Entry para ejecutar comandos y modificar el marcador
        self.entry_command = self.create_entry(parent=self.options_frame, row=0, column=2, columnspan=3, placeholder_text="Commandos", state="disabled")
        self.entry_command.bind("<Return>", self.execute_command)    # Vincular la tecla Enter al Entry para ejecutar el comando

        # Creamos los botones
        self.btn_configuration  = self.create_button(parent=self.options_frame, text="Configuracion", row=1, column=0, command=self.configuration, fg_color=TaekwondoScoreboard.FG_COLOR_GRAY, state="normal")
        self.btn_pause_resume   = self.create_button(parent=self.options_frame, text="Iniciar Combate [space]", row=1, column=1, command=self.toggle_timer, fg_color=TaekwondoScoreboard.FG_COLOR_GRAY, state="normal")
        self.btn_edit_score     = self.create_button(parent=self.options_frame, text="Modificar Marcador", row=1, column=2, command=self.open_edit_score_win, fg_color=TaekwondoScoreboard.FG_COLOR_GRAY, state="normal")
        self.btn_keyshi         = self.create_button(parent=self.options_frame, text="Keyshi", row=1, column=3, command=self.keyshi, fg_color=TaekwondoScoreboard.FG_COLOR_GRAY, state="disabled")
        self.btn_finish_round   = self.create_button(parent=self.options_frame, text="Finalizar Round", row=1, column=4, command=self.finish_round, fg_color=TaekwondoScoreboard.FG_COLOR_GRAY, state="disabled")
        self.btn_finish_combat  = self.create_button(parent=self.options_frame, text="Finalizar Combate", row=1, column=5, command=self.finish_combat, fg_color=TaekwondoScoreboard.FG_COLOR_GRAY, state="disabled")
        self.btn_next_round     = self.create_button(parent=self.options_frame, text="Siguiente Round", row=1, column=6, command=self.next_round, fg_color=TaekwondoScoreboard.FG_COLOR_GRAY, state="disabled")

        self.options_frame.rowconfigure(0, weight=1)
        self.options_frame.rowconfigure(1, weight=1)
        for i in range(7):
            self.options_frame.columnconfigure(i, weight=1)

    # Funciones de los botones (opciones y configuracion)
    # --------------------------------------------------------------------
    def configuration(self):
        # Crear ventana de configuración
        self.config_window = ctk.CTkToplevel(self)
        self.config_window.title("Configuración de combate")
        self.config_window.geometry("370x420")
        self.config_window.grab_set()

        # Deshabilitar redimensionamiento
        self.config_window.resizable(False, False)

        # Configuramos la distribucion de la ventana
        self.config_window.columnconfigure(0, weight=1)
        self.config_window.columnconfigure(1, weight=1)
        for i in range(8):
            self.config_window.rowconfigure(i, weight=1)

        # Creamos las etiquetas y las colocamos en la ventana
        self.create_label(parent=self.config_window, text="Nombre Jugador Azul:", row=0, column=0, sticky="e")
        self.create_label(parent=self.config_window, text="Nombre Jugador Rojo:", row=1, column=0, sticky="e")
        self.create_label(parent=self.config_window, text="Tiempo de Combate [mm:ss]:", row=2, column=0, sticky="e")
        self.create_label(parent=self.config_window, text="Tiempo de Descanso [mm:ss]:", row=3, column=0, sticky="e")
        self.create_label(parent=self.config_window, text="Tiempo para Keyshi [mm:ss]:", row=4, column=0, sticky="e")
        self.create_label(parent=self.config_window, text="Diferencia de puntos:", row=5, column=0, sticky="e")
        self.create_label(parent=self.config_window, text="Limite de Gamjeoms:", row=6, column=0, sticky="e")
        
        # Creamos los entrys y los colocamos en la ventana
        self.entry_blue_name    = self.create_entry(parent=self.config_window, row=0, column=1, placeholder_text="Chung")
        self.entry_red_name     = self.create_entry(parent=self.config_window, row=1, column=1, placeholder_text="Hong")
        self.entry_combat_time  = self.create_entry(parent=self.config_window, row=2, column=1, text=f"{self.init_combat_time//60}:{(self.init_combat_time%60):02}")
        self.entry_restTime     = self.create_entry(parent=self.config_window, row=3, column=1, text=f"{self.init_rest_time//60}:{(self.init_rest_time%60):02}")
        self.entry_keyshiTime   = self.create_entry(parent=self.config_window, row=4, column=1, text=f"{self.init_keyshi_time//60}:{(self.init_keyshi_time%60):02}")
        self.entry_points_diff  = self.create_entry(parent=self.config_window, row=5, column=1, text=str(self.points_diff))
        self.entry_gamjeon_limit= self.create_entry(parent=self.config_window, row=6, column=1, text=str(self.gamjeom_limit))

        # Crear y colocar botón de aplicar cambios
        self.create_button(parent=self.config_window, text="Aplicar", row=7, column=1, command=self.apply_config)
    
    def open_edit_score_win(self):
        # Crear ventana de configuración
        self.edit_score_window = ctk.CTkToplevel(self)
        self.edit_score_window.title("Modificar Marcador")
        self.edit_score_window.geometry("320x320")  # widthXheight
        self.edit_score_window.grab_set()

        # Deshabilitar redimensionamiento
        self.edit_score_window.resizable(False, False)
        
        self.edit_score_window.columnconfigure(0, weight=1)
        self.edit_score_window.columnconfigure(1, weight=1)
        for i in range(6):
            self.edit_score_window.rowconfigure(i, weight=1)

        # Creamos y colocamos las etiquetas y los campos de entrada
        self.create_label(parent=self.edit_score_window, text="Reloj:", row=0, column=0, sticky="e")
        self.create_label(parent=self.edit_score_window, text="Puntos Azul:", row=1, column=0, sticky="e")
        self.create_label(parent=self.edit_score_window, text="Puntos Rojos:", row=2, column=0, sticky="e")
        self.create_label(parent=self.edit_score_window, text="Gamjeons Azul:", row=3, column=0, sticky="e")
        self.create_label(parent=self.edit_score_window, text="Gamjeons Rojo:", row=4, column=0, sticky="e")
        
        # Creamos y colocamos los entrys del formulario
        self.entry_new_time      = self.create_entry(parent=self.edit_score_window, row=0, column=1, text=f"{self.combat_time//60}:{self.combat_time%60:02d}")
        self.entry_blue_points   = self.create_entry(parent=self.edit_score_window, row=1, column=1, text=str(self.blue_points))
        self.entry_red_points    = self.create_entry(parent=self.edit_score_window, row=2, column=1, text=str(self.red_points))
        self.entry_blue_gamjeons = self.create_entry(parent=self.edit_score_window, row=3, column=1, text=str(self.blue_gamjeoms))
        self.entry_red_gamjeons  = self.create_entry(parent=self.edit_score_window, row=4, column=1, text=str(self.red_gamjeoms))

        # Crear y colocar botón de aplicar cambios
        self.create_button(parent=self.edit_score_window, text="Aplicar", row=5, column=1, command=self.edit_score)

    def execute_command(self, event=None):
        try:
            command = self.entry_command.get().upper()
            if "G" in command:
                value = command[:2]
                if value == "A+":
                    self.blue_gamjeoms += 1
                    self.red_points += 1

                elif value == "A-":
                    self.blue_gamjeoms -= 1
                    self.red_points -= 1
                    
                elif value == "R+":
                    self.red_gamjeoms += 1
                    self.blue_points += 1

                elif value == "R-":   
                    self.red_gamjeoms -= 1
                    self.blue_points -= 1
            
            else:
                value = int(command[1:]) if int(command[1:]) <= 5 else 0
                player = command[0]
                if player == "A":
                    self.blue_points += value
                    
                elif player == "R":
                    self.red_points += value
                    
        except Exception as e:
            print(e)
        finally:
            self.entry_command.delete(0, ctk.END)   # Borramos el texto dentro del entry
            
            self.blue_points = 0 if self.blue_points < 0 else self.blue_points
            self.red_points = 0 if self.red_points < 0 else self.red_points
            self.blue_gamjeoms = 0 if self.blue_gamjeoms < 0 else self.blue_gamjeoms
            self.red_gamjeoms = 0 if self.red_gamjeoms < 0 else self.red_gamjeoms

            self.update_labels()

            if (max(self.blue_gamjeoms, self.red_gamjeoms) >= self.gamjeom_limit) or (abs(self.blue_points - self.red_points) >= self.points_diff):
                self.finish_round()
    
    def toggle_timer(self):        
        self.run_combat_time = not self.run_combat_time
        if self.run_combat_time:
            self.btn_pause_resume.configure(text="Pausar [space]")
            self.label_actions.configure(text="Combate!")
            self.btns_config_state(btn_pause_resume="normal", btn_keyshi="normal")
            self.run_timer()
        else:
            self.btn_pause_resume.configure(text="Reanudar [space]")      
            self.label_actions.configure(text="Pausa") 
            self.btns_config_state(entry_command="normal", btn_pause_resume="normal", btn_edit_score="normal", btn_finish_round="normal", btn_finish_combat="normal")

    def keyshi(self):
        return
    
    def finish_round(self):
        pygame.mixer.music.play()
        self.run_combat_time = False
        self.get_winner_round()

    def finish_combat(self):
        self.blue_name = self.blue_name[:len(self.blue_name)-self.blue_won_rounds]
        self.red_name = self.red_name[:len(self.red_name)-self.red_won_rounds]
        self.blue_won_rounds = 0
        self.red_won_rounds = 0
        self.round = 0  
        self.reset_new_round_values()
        self.update_labels()
        self.btns_config_state(btn_config="normal", btn_pause_resume="normal", btn_edit_score="normal")
        self.label_actions.configure(text="Esperando")
        self.blue_frame.configure(fg_color=TaekwondoScoreboard.FG_COLOR_BLUE)
        self.red_frame.configure(fg_color=TaekwondoScoreboard.FG_COLOR_RED)

    def next_round(self):
        self.rest_time = 0

    # Funciones auxiliares
    # --------------------------------------------------------------------
    def run_timer(self):
        if self.run_combat_time:
            if self.combat_time > 0:
                mins, secs = divmod(self.combat_time, 60)
                self.label_time.configure(text=f"{mins}:{secs:02}")
                self.combat_time -= 1
                self.after(1000, self.run_timer)
            else:
                self.finish_round()
            
    def run_rest_timer(self):
        if self.rest_time > 0:
            mins, secs = divmod(self.rest_time, 60)
            self.label_time.configure(text=f"{mins}:{secs:02}")
            self.rest_time -= 1
            self.after(1000, self.run_rest_timer)
        else:
            self.reset_new_round_values()
        
    def get_winner_round(self):
        if (self.red_gamjeoms >= self.gamjeom_limit) or (self.blue_points > self.red_points):
            self.blue_won_rounds += 1
            self.blue_name += "*"
            print("Ganador Azul")
        elif (self.blue_gamjeoms >= self.gamjeom_limit) or (self.red_points > self.blue_points):
            self.red_won_rounds += 1
            self.red_name += "*"
            print("Ganador Rojo")
        else:
            print("Empate")
        
        self.update_labels()

        if max(self.blue_won_rounds, self.red_won_rounds) == 2:
            self.btns_config_state(btn_finish_combat="normal")
            self.label_actions.configure(text="FIN")
            print("Fin del Combate")
            if self.blue_won_rounds > self.red_won_rounds:
                self.label_blue_points.configure(text="W")
                self.red_frame.configure(fg_color=TaekwondoScoreboard.FG_COLOR_GRAY2)
            else:
                self.label_red_points.configure(text="W")
                self.blue_frame.configure(fg_color=TaekwondoScoreboard.FG_COLOR_GRAY2)
        else:
            # pygame.mixer.music.play()
            print("Correr tiempo de descanso")
            self.label_actions.configure(text="Descanso")
            self.btns_config_state(btn_next_round="normal")
            self.rest_time = self.init_rest_time
            self.run_rest_timer()

    def reset_new_round_values(self):
        self.label_actions.configure(text="Esperando")
        self.btn_pause_resume.configure(text="Iniciar Round [space]")
        self.btns_config_state(entry_command="normal", btn_pause_resume="normal", btn_edit_score="normal", btn_finish_round="normal", btn_finish_combat="normal")
        self.combat_time = self.init_combat_time
        self.round += 1
        self.blue_points = 0
        self.red_points = 0
        self.blue_gamjeoms = 0
        self.red_gamjeoms = 0
        self.update_labels()

    def apply_config(self):
        try:    
            # Obtener valores de los entrys y configurar valores del sistema
            self.blue_name          = self.entry_blue_name.get() or "Chung"
            self.red_name           = self.entry_red_name.get() or "Hong"
            self.init_combat_time   = self.parse_time(self.entry_combat_time.get())
            self.init_rest_time     = self.parse_time(self.entry_restTime.get())
            self.init_keyshi_time   = self.parse_time(self.entry_keyshiTime.get())
            self.gamjeon_limit      = int(self.entry_gamjeon_limit.get())
            self.points_diff        = int(self.entry_points_diff.get())

            # Actualizamos los timepos para los temporizadores
            self.combat_time = self.init_combat_time
            self.rest_time = self.init_rest_time

            # Actualizar etiquetas correspondientes
            self.update_labels()

            # Cerrar ventana de configuración
            self.config_window.destroy()
        except Exception as e:
            print(e)

    def edit_score(self):
        try:
            # Obtener datos de la ventana de Modificar Marcador
            self.combat_time    = self.parse_time(self.entry_new_time.get())
            self.blue_points    = int(self.entry_blue_points.get())
            self.red_points     = int(self.entry_red_points.get())
            self.blue_gamjeoms  = int(self.entry_blue_gamjeons.get())
            self.red_gamjeoms   = int(self.entry_red_gamjeons.get())

            # Actualizar las etiquetas correspondientes
            self.update_labels()

            # Cerramos la ventana
            self.edit_score_window.destroy()
        except Exception as e:
            print(e)

    def btns_config_state(self, btn_config="disabled", btn_pause_resume="disabled", btn_edit_score="disabled", btn_keyshi="disabled", btn_finish_round="disabled", btn_finish_combat="disabled", btn_next_round="disabled", entry_command="disabled"):
        self.entry_command.configure(state=entry_command)
        self.btn_configuration.configure(state=btn_config)
        self.btn_pause_resume.configure(state=btn_pause_resume)
        self.btn_edit_score.configure(state=btn_edit_score)
        self.btn_keyshi.configure(state=btn_keyshi)
        self.btn_finish_round.configure(state=btn_finish_round)
        self.btn_finish_combat.configure(state=btn_finish_combat)
        self.btn_next_round.configure(state=btn_next_round)

    def update_labels(self):
        # Actualizamos las etiquetas del marcador
        self.label_time.configure(text=f"{self.combat_time//60}:{self.combat_time%60:02d}")
        self.label_keyshi_time.configure(text=f"{self.init_keyshi_time//60}:{self.init_keyshi_time%60:02d}")

        self.label_num_round.configure(text=f"R{self.round}")

        self.label_blue_name.configure(text=self.blue_name)
        self.label_red_name.configure(text=self.red_name)

        self.label_blue_points.configure(text=self.blue_points)
        self.label_red_points.configure(text=self.red_points)

        self.label_blue_gamjeon.configure(text=self.blue_gamjeoms)
        self.label_red_gamjeon.configure(text=self.red_gamjeoms)
        return

    def parse_time(self, time_str):
        # Funcion para transformar el formato mm:ss a seg [Ejem]: "1:30" => 90seg
        minutes, seconds = map(int, time_str.split(":"))
        return minutes * 60 + seconds
    
if __name__ == "__main__":
    app = TaekwondoScoreboard()
    app.mainloop()
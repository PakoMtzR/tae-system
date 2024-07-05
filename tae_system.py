import customtkinter as ctk

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

    def __init__(self):
        super().__init__()
        self.title(TaekwondoScoreboard.APP_NAME)
        self.geometry(str(TaekwondoScoreboard.WIDTH) + "x" + str(TaekwondoScoreboard.HEIGHT))
        self.minsize(TaekwondoScoreboard.WIDTH, TaekwondoScoreboard.HEIGHT)

        self.initialize_variables()
        self.create_widgets()

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
        self.run_rest_time = False
        
        self.blue_points = 0
        self.red_points = 0
        self.blue_points_list = []
        self.red_points_list = []
        
        self.blue_won_rounds = 0
        self.red_won_rounds = 0
        self.blue_gamjeoms = 0
        self.red_gamjeoms = 0
        
        self.finished_combat = False

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

    def create_button(self, parent, text, row, column, command, state):
        button = ctk.CTkButton(master=parent, text=text, fg_color=TaekwondoScoreboard.FG_COLOR_GRAY, command=command, state=state)
        button.grid(row=row, column=column, sticky="nesw", padx=10, pady=10)

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
        self.command_entry = self.create_entry(parent=self.options_frame, row=0, column=2, columnspan=3, placeholder_text="Commandos", state="disabled")
        self.command_entry.bind("<Return>", self.execute_command)    # Vincular la tecla Enter al Entry para ejecutar el comando

        # Creamos los botones
        button_configs = [
            ("Configuracion", self.configuration, "normal"),
            ("Iniciar Combate", self.toggle_timer, "normal"),
            ("Modificar Marcador", self.open_edit_score_win, "normal"),
            ("Keyshi", self.keyshi, "disabled"),
            ("Finalizar Round", self.finish_round, "disabled"),
            ("Finalizar Combate", self.finish_combat, "disabled"),
            ("Siguiente Round", self.next_round, "disabled")
        ]

        for i, (text, command, state) in enumerate(button_configs):
            self.create_button(parent=self.options_frame, text=text, row=1, column=i, command=command, state=state)
        
        self.options_frame.rowconfigure(0, weight=1)
        self.options_frame.rowconfigure(1, weight=1)
        for i in range(7):
            self.options_frame.columnconfigure(i, weight=1)

    # Funciones de los botones (opciones y configuracion)
    # --------------------------------------------------------------------
    def execute_command(self, event=None):
        try:
            command = self.command_entry.get().upper()
            # print(command)
            if "G" in command:
                value = command[:2]
                if value == "A+":
                    self.blue_gamjeoms += 1
                    self.red_points += 1
                    self.red_points_list.append(1)

                if value == "A-":
                    self.blue_gamjeoms -= 1
                    self.red_points -= 1
                    
                if value == "R+":
                    self.red_gamjeoms += 1
                    self.blue_points += 1
                    self.blue_points_list.append(1)

                if value == "R-":   
                    self.red_gamjeoms -= 1
                    self.blue_points -= 1
            else:
                value = int(command[1:]) if int(command[1:]) <= 5 else 0
                if command[0] == "A":
                    self.blue_points += value
                    self.blue_points_list.append(value)
                    
                if command[0] == "R":
                    self.red_points += value
                    self.red_points_list.append(value)
                    
        except Exception as e:
            print(e)
        finally:
            # Borramos el texto dentro del entry
            self.command_entry.delete(0, ctk.END)

            # Verificamos si no existe valores negativos
            self.blue_points = 0 if self.blue_points < 0 else self.blue_points
            self.red_points = 0 if self.red_points < 0 else self.red_points
            self.blue_gamjeoms = 0 if self.blue_gamjeoms < 0 else self.blue_gamjeoms
            self.red_gamjeoms = 0 if self.red_gamjeoms < 0 else self.red_gamjeoms
            
            # Actualizamos las etiquetas
            self.update_labels()
            self.get_winner_round()

    def configuration(self):
        # Crear ventana de configuración
        self.config_window = ctk.CTkToplevel(self)
        self.config_window.title("Configuración de combate")
        self.config_window.geometry("370x420")
        self.config_window.grab_set()

        # Deshabilitar redimensionamiento
        self.config_window.resizable(False, False)

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
        button_apply = ctk.CTkButton(master=self.config_window, text="Aplicar", command=self.apply_config)
        button_apply.grid(row=10, column=1, pady=20)

    def toggle_timer(self):        
        # Alternar el temporizador del combate
        self.run_combat_time = not self.run_combat_time

        if self.run_combat_time:
            # Cambiar el texto de la etiqueta del boton btn_pause_resume
            self.btn_pause_resume.configure(text="Pausar")

            # Cambiar el texto de la etiqueta de acciones
            self.label_actions.configure(text="Combate!")

            # Habilitar o deshabilitar los botones correspondientes
            self.btns_config_state(btn_pause_resume="normal", btn_keyshi="normal")

            # Actualizar el temporizador
            self.update_combat_timer()
        else:
            # Cambiar el texto de la etiqueta del boton btn_pause_resume
            self.btn_pause_resume.configure(text="Reanudar")      

            # Cambiar el texto de la etiqueta de acciones
            self.label_actions.configure(text="Pausa") 

            # Habilitar o deshabilitar los botones correspondientes
            self.btns_config_state(entry_command="normal", btn_pause_resume="normal", btn_edit_score="normal", btn_finish_round="normal", btn_finish_combat="normal")

    def open_edit_score_win(self):
        # Crear ventana de configuración
        self.edit_score_window = ctk.CTkToplevel(self)
        self.edit_score_window.title("Modificar Marcador")
        self.edit_score_window.geometry("370x420")
        self.edit_score_window.grab_set()

        # Deshabilitar redimensionamiento
        self.edit_score_window.resizable(False, False)

        # Creamos y colocamos las etiquetas y los campos de entrada
        self.create_label(parent=self.edit_score_window, text="Reloj:", row=0, column=0, sticky="e")
        self.create_label(parent=self.edit_score_window, text="Puntos Azul:", row=1, column=0, sticky="e")
        self.create_label(parent=self.edit_score_window, text="Puntos Rojos:", row=2, column=0, sticky="e")
        self.create_label(parent=self.edit_score_window, text="Gamjeons Azul:", row=3, column=0, sticky="e")
        self.create_label(parent=self.edit_score_window, text="Gamjeons Rojo:", row=4, column=0, sticky="e")
        
        self.entry_new_time      = self.create_entry(parent=self.edit_score_window, row=0, column=1, text=f"{self.combat_time//60}:{self.combat_time%60:02d}")
        self.entry_blue_points   = self.create_entry(parent=self.edit_score_window, row=1, column=1, text=str(self.blue_points))
        self.entry_red_points    = self.create_entry(parent=self.edit_score_window, row=2, column=1, text=str(self.red_points))
        self.entry_blue_gamjeons = self.create_entry(parent=self.edit_score_window, row=3, column=1, text=str(self.blue_gamjeoms))
        self.entry_red_gamjeons  = self.create_entry(parent=self.edit_score_window, row=4, column=1, text=str(self.red_gamjeoms))

        # Crear y colocar botón de aplicar cambios
        button_apply = ctk.CTkButton(master=self.edit_score_window, text="Aplicar", command=self.edit_score)
        button_apply.grid(row=5, column=1, pady=20)

    def keyshi(self):
        return
    
    def finish_round(self):
        self.combat_time = 0
        self.run_combat_time = True
        self.update_combat_timer()

    def finish_combat(self):
        self.finished_combat = False
        self.blue_won_rounds = 0
        self.red_won_rounds = 0
        self.round = 1  
        self.blue_frame.configure(fg_color="blue")
        self.red_frame.configure(fg_color="red")
        self.reset_round_points()
        self.update_labels()
        self.btns_config_state(btn_config="normal", btn_pause_resume="normal" ,btn_edit_score="normal")
        self.label_actions.configure(text="Esperando")

    def next_round(self):
        self.rest_time = 0

    # Funciones auxiliares
    # --------------------------------------------------------------------
    def update_combat_timer(self):
        if self.run_combat_time:
            if self.combat_time > 0:
                minutes, seconds = divmod(self.combat_time, 60)
                self.label_time.configure(text=f"{minutes}:{seconds:02d}")
                self.combat_time -= 1
                self.after(1000, self.update_combat_timer)
            else:
                self.get_winner_round(required_winner=True)
                self.update_labels()
                # 
                self.run_combat_time = False
                self.combat_time = self.init_combat_time

                # Habilitamos o deshabilitamos los botones correspondientes para el descanso
                self.btns_config_state(btn_next_round="normal")

                # Modificamos una etiqueta para indicar que estamos en tiempo de descanso
                self.label_actions.configure(text="Descanso")
                self.btn_pause_resume.configure(text="Iniciar Round")

                if self.finished_combat:
                    self.label_actions.configure(text="Fin del combate")
                    self.btns_config_state(btn_finish_combat="normal")
                else:
                    # Corremos el temporizador del descanso
                    self.label_actions.configure(text="Descanso")
                    self.update_rest_timer()
    
    def update_rest_timer(self):
        if self.rest_time > 0:
            minutes, seconds = divmod(self.rest_time, 60)
            self.label_time.configure(text=f"{minutes}:{seconds:02d}")
            self.rest_time -= 1
            self.after(1000, self.update_rest_timer)
        else:
            # Reseteamos el tiempo de descanso
            self.rest_time = self.init_rest_time

            # Resetamos los valores para reiniciar el round
            self.reset_round_points()

            # Habilitamos o deshabilitamos los botones correspondientes para reiniciar el combate
            self.btns_config_state(entry_command="normal", btn_pause_resume="normal", btn_edit_score="normal", btn_finish_round="normal", btn_finish_combat="normal")

            # Modificamos una etiqueta para indicar que estamos en tiempo de descanso
            self.label_actions.configure(text="Esperando")
            self.btn_pause_resume.configure(text="Iniciar Round")

            self.update_labels()

    def apply_config(self):
        try:
            time_min, time_seg = self.entry_combat_time.get().split(":")
            rest_time_min, rest_time_seg = self.entry_restTime.get().split(":")
            keyshi_time_min, keyshi_time_seg = self.entry_keyshiTime.get().split(":")
    
            # Obtener valores de los entrys y configurar valores del sistema
            self.blue_name = self.entry_blue_name.get() if self.entry_blue_name.get() != "" else "Chung"
            self.red_name = self.entry_red_name.get() if self.entry_red_name.get() != "" else "Hong"
            self.init_combat_time = int(time_min)*60 + int(time_seg)
            self.init_rest_time = int(rest_time_min)*60 + int(rest_time_seg)
            self.init_keyshi_time = int(keyshi_time_min)*60 + int(keyshi_time_seg)
            self.gamjeon_limit = int(self.entry_gamjeon_limit.get())
            self.points_diff = int(self.entry_points_diff.get())

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
            new_min, new_seg = self.new_time_entry.get().split(":")
            self.combat_time = int(new_min)*60 + int(new_seg)
            self.blue_points = int(self.entry_blue_points.get())
            self.red_points = int(self.entry_red_points.get())
            self.blue_gamjeoms = int(self.entry_blue_gamjeons.get())
            self.red_gamjeoms = int(self.entry_red_gamjeons.get())

            # Actualizar las etiquetas correspondientes
            self.update_labels()

            # Cerramos la ventana
            self.edit_score_window.destroy()
        except Exception as e:
            print(e)
    
    def get_winner_round(self, required_winner=False):
        if required_winner:
            if self.blue_points == self.red_points:
                # STK => Spinning Turning Kicks 
                stk_blue = self.blue_points_list.count(4) + self.blue_points_list.count(5)
                stk_red = self.red_points_list.count(4) + self.red_points_list.count(5)
                
                # HK => Head Kicks
                hk_blue = self.blue_points_list.count(3)
                hk_red = self.red_points_list.count(3)
                
                # TK => Trunk Kicks
                tk_blue = self.blue_points_list.count(2)
                tk_red = self.red_points_list.count(2)

                # P => Punches
                p_blue = self.blue_points_list.count(1) - self.blue_gamjeoms
                p_red = self.red_points_list.count(1) - self.red_gamjeoms
                
                if stk_blue == stk_red:
                    if hk_blue == hk_red:
                        if tk_blue == tk_red:
                            if p_blue == p_red:
                                if self.blue_gamjeoms == self.red_gamjeoms:
                                    print("Empate")
                                    self.compare_points(self.blue_points, self.red_points)
                                else:
                                    self.compare_points(self.red_gamjeoms, self.blue_gamjeoms)
                            else:
                                self.compare_points(p_blue, p_red)
                        else:
                            self.compare_points(tk_blue, tk_red)
                    else:
                        self.compare_points(hk_blue, hk_red)
                else:
                    self.compare_points(stk_blue, stk_red)
            else:
                self.compare_points(self.blue_points, self.red_points)
        else:
            # Verificamos si un jugador ganó por superioridad de puntos
            if abs(self.blue_points - self.red_points) > self.points_diff:
                self.compare_points(self.blue_points, self.red_points)

            # Verificamos si alguien sobrepasó el límite de gamjeons
            elif max(self.blue_gamjeoms, self.red_gamjeoms) > self.gamjeom_limit:
                self.compare_points(self.red_gamjeoms, self.blue_gamjeoms)

            else:
                print("Todavia no hay ganador")

    def compare_points(self, points_blue, points_red):
        if points_blue > points_red:
            self.blue_name += "*" 
            self.blue_won_rounds += 1
            print("Ganador Azul")
            
        elif points_red > points_blue:
            self.red_name += "*" 
            self.red_won_rounds += 1
            print("Ganador Rojo")

        
        if max(self.blue_won_rounds, self.red_won_rounds) == 2:
            self.blue_name = self.blue_name[:len(self.blue_name)-self.blue_won_rounds]
            self.red_name = self.red_name[:len(self.red_name)-self.red_won_rounds]
            self.finished_combat = True
        
            if self.blue_won_rounds == 2:
                self.red_frame.configure(fg_color="#2C2C2C")
            if self.red_won_rounds == 2:
                self.blue_frame.configure(fg_color="#2C2C2C")
        
        else:
            self.round += 1

    def reset_round_points(self):
        self.blue_points = 0
        self.red_points = 0

        self.blue_gamjeoms = 0
        self.red_gamjeoms = 0

        self.blue_points_list.clear()
        self.red_points_list.clear()

    def btns_config_state(self, btn_config="disabled", btn_pause_resume="disabled", btn_edit_score="disabled", btn_keyshi="disabled", btn_finish_round="disabled", btn_finish_combat="disabled", btn_next_round="disabled", entry_command="disabled"):
        self.command_entry.configure(state=entry_command)
        self.btn_configuration.configure(state=btn_config)
        self.btn_pause_resume.configure(state=btn_pause_resume)
        self.btn_edit_score.configure(state=btn_edit_score)
        self.btn_keyshi.configure(state=btn_keyshi)
        self.btn_finish_round.configure(state=btn_finish_round)
        self.btn_finish_combat.configure(state=btn_finish_combat)
        self.btn_next_round.configure(state=btn_next_round)

    def update_labels(self):
        # Actualizar etiquetas de los temporizadores
        self.label_time.configure(text=f"{self.combat_time//60}:{self.combat_time%60:02d}")
        self.label_keyshi_time.configure(text=f"{self.init_keyshi_time//60}:{self.init_keyshi_time%60:02d}")

        self.label_num_round.configure(text=f"R{self.round}")

        # Actualizamos los nombres de los jugadores
        self.blue_name_label.configure(text=self.blue_name)
        self.red_name_label.configure(text=self.red_name)

        # Actualizamos sus puntajes
        self.blue_points_label.configure(text=self.blue_points)
        self.red_points_label.configure(text=self.red_points)

        # Actualizamos las amonestaciones
        self.blue_gamjeon_label.configure(text=self.blue_gamjeoms)
        self.red_gamjeon_label.configure(text=self.red_gamjeoms)
        return
    
if __name__ == "__main__":
    app = TaekwondoScoreboard()
    app.mainloop()
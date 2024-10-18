from tkinter import *
from tkinter import messagebox as mb
import random
import string

# Main programme

# constants
main_bg_colour = 'grey50'
secondary_bg_colour = 'grey90'

font_family = 'Calibri'
title_font = (font_family, 60, 'bold')
large_font = (font_family, 40)
medium_font = (font_family, 30)
small_font = (font_family, 20)

choices = ["rock","paper","scissors"]

# Creating the initial window
class Win():
    def __init__(self):
        self.win = Tk()
        self.win.title('RPS')
        # self.win.resizable(0,0)
        self.win.geometry('960x540')
        self.win.configure(bg=main_bg_colour)

        self.menu_frame()

        self.validate_username = self.win.register(self.username_check)
        self.validate_numbers = self.win.register(self.numbers_check)

    # validates input for an entered username
    def username_check(self, char):
        valid_chars = string.ascii_letters + string.digits

        if len(char) > 1:
            for i in char:
                if i not in char or i not in valid_chars:
                    return False
                
            return True

        return char in valid_chars
    
    # validates input to allow numbers only
    def numbers_check(self, char):
        valid_chars = string.digits

        if len(char) > 1:
            for i in char:
                if i not in char or i not in valid_chars:
                    return False
                
            return True

        return char in valid_chars

    # Creates menu frame
    def menu_frame(self):
        self.menu = Frame(self.win, width=920, height=500, bg=secondary_bg_colour)
        self.menu.grid(padx=20, pady=20)
        self.menu.grid_propagate(0)

        Frame(self.menu, width=920, bg=secondary_bg_colour).grid(row=0, column=0) # sets width and centers widgets
        
        Label(self.menu, text='Rock Paper Scissors', font=title_font, bg=secondary_bg_colour).grid(pady=90) # Title
        Button(self.menu,
                text='Play', font=large_font,
                width=10, bg='green3', activebackground='green4',
                border=False, cursor='mouse',
                command=self.create_play_frame).grid() # Play button

    def create_play_frame(self):
        self.menu.destroy()
        self.play_frame()

    # Create frame to select gamemode and more...
    def play_frame(self):
        self.play = Frame(self.win, width=920, height=500, bg=secondary_bg_colour)
        self.play.grid(padx=20, pady=20)
        self.play.grid_propagate(0)

        Frame(self.play, width=920, bg=secondary_bg_colour).grid(row=0, column=0) # sets width and centers widgets

        Label(self.play, text='Play', font=title_font, bg=secondary_bg_colour).grid(pady=5)
        
        Label(self.play, text='Player 1 username:', font=small_font, bg=secondary_bg_colour).grid()
        username1_entry = Entry(self.play, validate='key', validatecommand=(self.validate_username, '%S'))
        username1_entry.grid()
        
        Label(self.play, text='Player 2 username (singleplayer only):', font=small_font, bg=secondary_bg_colour).grid()
        username2_entry = Entry(self.play, validate='key', validatecommand=(self.validate_username, '%S'))
        username2_entry.grid()

        Label(self.play, text='Enter number of rounds (0 or blank for infinite):', font=small_font, bg=secondary_bg_colour).grid()
        rounds_entry = Entry(self.play, validate='key', validatecommand=(self.validate_numbers, '%S'))
        rounds_entry.grid()

        # Single player button
        Button(self.play,
                text='Singleplayer', font=small_font,
                bg='green3', activebackground='green4',
                border=False, cursor='mouse', width=15,
                command=lambda: self.create_singleplayer_frame(username1_entry.get(), username2_entry.get(), rounds_entry.get())).grid(pady=5)

        # Computer mode button
        Button(self.play,
                text='Against Computer', font=small_font,
                bg='green3', activebackground='green4',
                border=False, cursor='mouse', width=15,
                command=lambda: self.create_computer_frame(username1_entry.get(), rounds_entry.get())).grid(pady=5)

        # Back to menu button
        Button(self.play,
                text='Back to menu', font=small_font,
                bg='red', fg='white', activebackground='red4', activeforeground='white',
                border=False, cursor='X_cursor', width=15,
                command=self.back_to_menu).grid(pady=5)

    # to main menu
    def back_to_menu(self):
        self.play.destroy()
        self.menu_frame()

    # validation and creating singleplayer mode
    def create_singleplayer_frame(self, username1, username2, rounds):
        if len(username1) < 1 or len(username1) > 10:
            mb.showerror('Username 1', 'Usernames must be between 1 and 10 characters.')
            return

        elif len(username2) < 1 or len(username2) > 10:
            mb.showerror('Username 2', 'Usernames must be between 1 and 10 characters.')
            return

        elif rounds == "":
            rounds = "Infinite"
        
        elif (int(rounds) + 0) == 0:
            rounds = "Infinite"

        elif int(rounds) > 999:
            rounds = "999"
        
        self.play.destroy()
        self.singleplayer_frame(username1, username2, rounds)

    # validation and creating versus computer mode
    def create_computer_frame(self, username, rounds):

        if len(username) < 1 or len(username) > 10:
            mb.showerror('Username', 'Usernames must be between 1 and 10 characters.')
            return

        elif rounds == "":
            rounds = "Infinite"
        
        elif (int(rounds) + 0) == 0:
            rounds = "Infinite"

        elif int(rounds) > 999:
            rounds = "999"

        self.play.destroy()
        self.computer_frame(username, rounds)

    # Singleplayer game mode
    def singleplayer_frame(self, username1, username2, rounds):
        self.game = Frame(self.win, width=920, height=500, bg=secondary_bg_colour)
        self.game.grid(padx=20, pady=20)
        self.game.grid_propagate(0)

        self.username1 = username1
        self.username2 = username2
        self.rounds = rounds
        self.player1_score = 0
        self.player2_score = 0
        self.player1_turn = True

        Frame(self.game, width=920, bg=secondary_bg_colour).grid(row=0, column=0, columnspan=3) # sets width and centers widgets

        Label(self.game, text='Singleplayer', bg=secondary_bg_colour, font=title_font).grid(row=1, column=0, columnspan=3)

        # image paths and resizing images
        self.rock_image_path = PhotoImage(file='assets/rock.png')
        self.rock_image = self.rock_image_path.subsample(5, 5)
        self.paper_image_path = PhotoImage(file='assets/paper.png')
        self.paper_image = self.paper_image_path.subsample(5, 5)
        self.scissors_image_path = PhotoImage(file='assets/scissors.png')
        self.scissors_image = self.scissors_image_path.subsample(5, 5)

        Button(self.game, image=self.rock_image, cursor='mouse', command=lambda: self.rps_singleplayer("rock")).grid(row=2, column=0) # rock
        Button(self.game, image=self.paper_image, cursor='mouse', command=lambda: self.rps_singleplayer("paper")).grid(row=2, column=1) # paper
        Button(self.game, image=self.scissors_image, cursor='mouse', command=lambda: self.rps_singleplayer("scissors")).grid(row=2, column=2) #scissors

        Frame(self.game, width=920, bg=main_bg_colour).grid(row=3, column=0, columnspan=3, pady=10) # seperater line
        
        self.player1_label = Label(self.game, text=f'{self.username1}:\n{self.player1_score}', bg=secondary_bg_colour, font=medium_font)
        self.player1_label.grid(row=4, column=0)

        self.player2_label = Label(self.game, text=f'{self.username2}:\n{self.player2_score}', bg=secondary_bg_colour, font=medium_font)
        self.player2_label.grid(row=4, column=1)
        
        self.rounds_label = Label(self.game, text=f'Rounds:\n{self.rounds}', bg=secondary_bg_colour, font=medium_font)
        self.rounds_label.grid(row=4, column=2)

        Button(self.game,
            text='Exit', font=small_font,
            bg='red', fg='white', activebackground='red4', activeforeground='white',
            border=False, cursor='X_cursor', width=15,
            command=self.exit_game).grid(row=5, column=2)
        
        self.player_turn_label = Label(self.game, text=f"{self.username1}'s turn.", bg='green3', font=small_font)
        self.player_turn_label.grid(row=5, column=0)

    # Rock paper scissors singleplayer logic
    def rps_singleplayer(self, choice):
        if self.player1_turn:
            self.player1_turn = False
            self.choice1 = choice
            self.player_turn_label.config(text=f"{self.username2}'s turn.")
            return
        
        else:
            self.player1_turn = True
            self.player_turn_label.config(text=f"{self.username1}'s turn.")
        
            if choice == self.choice1:
                mb.showinfo(f"{self.choice1}", "Draw")
                return
            
            elif (choice == "rock" and self.choice1 == "paper") or (choice == "scissors" and self.choice1 == "rock") or (choice == "paper" and self.choice1 == "scissors"):
                self.player1_score += 1
                mb.showinfo(f"{self.username1}", f"{self.username1} WINS!")
            
            else:
                self.player2_score += 1
                mb.showinfo(f"{self.username2}", f"{self.username2} WINS!")

        self.player1_label.configure(text=f"{self.username1}:\n{self.player1_score}")
        self.player2_label.configure(text=f"{self.username2}:\n{self.player2_score}")

        if self.rounds == "Infinite":
            pass
        else:
            self.rounds = int(self.rounds) -1
            self.rounds_label.configure(text=f"Rounds:\n{self.rounds}")
            if self.rounds < 1:
                self.zero_round_singleplayer()

    # Against computer game mode
    def computer_frame(self, username, rounds):
        self.rounds = rounds
        self.username = username
        self.player_score = 0
        self.computer_score = 0

        self.game = Frame(self.win, width=920, height=500, bg=secondary_bg_colour)
        self.game.grid(padx=20, pady=20)
        self.game.grid_propagate(0)

        Frame(self.game, width=920, bg=secondary_bg_colour).grid(row=0, column=0, columnspan=3) # sets width and centers widgets

        Label(self.game, text='Computer mode', bg=secondary_bg_colour, font=title_font).grid(row=1, column=0, columnspan=3)

        self.rock_image_path = PhotoImage(file='assets/rock.png')
        self.rock_image = self.rock_image_path.subsample(5, 5)
        self.paper_image_path = PhotoImage(file='assets/paper.png')
        self.paper_image = self.paper_image_path.subsample(5, 5)
        self.scissors_image_path = PhotoImage(file='assets/scissors.png')
        self.scissors_image = self.scissors_image_path.subsample(5, 5)

        Button(self.game, image=self.rock_image, cursor='mouse', command=lambda:self.rps_computer("rock")).grid(row=2, column=0)
        Button(self.game, image=self.paper_image, cursor='mouse', command=lambda:self.rps_computer("paper")).grid(row=2, column=1)
        Button(self.game, image=self.scissors_image, cursor='mouse', command=lambda:self.rps_computer("scissors")).grid(row=2, column=2)

        Frame(self.game, width=920, bg=main_bg_colour).grid(row=3, column=0, columnspan=3, pady=10) # seperater line
        
        self.player_label = Label(self.game, text=f'{username}:\n{self.player_score}', bg=secondary_bg_colour, font=medium_font) # player 1 score
        self.player_label.grid(row=4, column=0)

        self.computer_label = Label(self.game, text=f'RPS Master:\n{self.computer_score}', bg=secondary_bg_colour, font=medium_font) # player 2 score
        self.computer_label.grid(row=4, column=1)
        
        self.rounds_label = Label(self.game, text=f'Rounds:\n{self.rounds}', bg=secondary_bg_colour, font=medium_font) # rounds remaining
        self.rounds_label.grid(row=4, column=2)

        Button(self.game,
            text='Exit', font=small_font,
            bg='red', fg='white', activebackground='red4', activeforeground='white',
            border=False, cursor='X_cursor', width=15,
            command=self.exit_game).grid(row=5, column=1)

    # Rock paper scissors computer mode logic
    def rps_computer(self, choice):
        computer_choice = random.choice(choices)
        if choice == computer_choice:
            mb.showinfo(f"{computer_choice}", "Draw")
            return

        elif (choice == "rock" and computer_choice == "scissors") or (choice == "scissors" and computer_choice == "paper") or (choice == "paper" and computer_choice == "rock"):
            mb.showinfo(f"{computer_choice}", "You Win!")
            self.player_score += 1

        else:
            mb.showinfo(f"{computer_choice}", "You Lose :(")
            self.computer_score += 1

        self.player_label.configure(text=f"{self.username}:\n{self.player_score}")
        self.computer_label.configure(text=f"RPS Master:\n{self.computer_score}")

        if self.rounds == "Infinite":
            pass
        else:
            self.rounds = int(self.rounds) -1
            self.rounds_label.configure(text=f"Rounds:\n{self.rounds}")
            if self.rounds < 1:
                self.zero_round_computer()

    # if rounds reach 0
    def zero_round_computer(self):
        mb.showinfo("No more rounds", f"Final score\n{self.username}: {self.player_score}\nRPS Master: {self.computer_score}")
        self.game.destroy()
        self.play_frame()

    def zero_round_singleplayer(self):
        mb.showinfo("No more rounds", f"Final score\n{self.username1}: {self.player1_score}\n{self.username2}: {self.player2_score}")
        self.game.destroy()
        self.play_frame()

    # leave game
    def exit_game(self):
        yes_or_no = mb.askyesno("Exit game", "Are you sure you want to exit?")

        if yes_or_no:
            self.game.destroy()
            self.play_frame()

# Creates the window and a mainloop
w = Win()
w.win.mainloop()

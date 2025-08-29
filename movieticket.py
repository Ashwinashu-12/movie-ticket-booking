import tkinter as tk
from tkinter import ttk, messagebox
import json

class MovieBookingSystem:
    def _init_(self, root):
        self.root = root
        self.root.title("Movie Ticket Booking System")
        self.root.geometry("800x600")
        
        # Movie data
        self.movies = {
            "INCEPTION": 90,
            "INTERSTELLAR": 0,
            "PULP FICTION": 75,
            "THE DARK KNIGHT": 50,
            "THE SHAWSHANK REDEMPTION": 90
        }
        
        # Selected movie and seats
        self.selected_movie = tk.StringVar()
        self.selected_seats = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Movie selection
        ttk.Label(main_frame, text="Select Movie:", font=('Arial', 12, 'bold')).grid(row=0, column=0, pady=10)
        movie_combo = ttk.Combobox(main_frame, textvariable=self.selected_movie, values=list(self.movies.keys()), state='readonly')
        movie_combo.grid(row=0, column=1, pady=10)
        movie_combo.bind('<<ComboboxSelected>>', self.update_seat_display)
        
        # Seats frame
        self.seats_frame = ttk.LabelFrame(main_frame, text="Select Seats", padding="10")
        self.seats_frame.grid(row=1, column=0, columnspan=2, pady=10)
        
        # Book button
        self.book_button = ttk.Button(main_frame, text="Book Tickets", command=self.book_tickets)
        self.book_button.grid(row=2, column=0, columnspan=2, pady=10)
        
        # Status label
        self.status_label = ttk.Label(main_frame, text="", font=('Arial', 10))
        self.status_label.grid(row=3, column=0, columnspan=2, pady=5)
        
    def create_seat_layout(self):
        # Clear previous seat layout
        for widget in self.seats_frame.winfo_children():
            widget.destroy()
        
        movie = self.selected_movie.get()
        available_seats = self.movies[movie]
        
        # Create seat grid (10 seats per row)
        total_rows = (available_seats + 9) // 10
        for row in range(total_rows):
            for col in range(10):
                seat_num = row * 10 + col + 1
                if seat_num <= available_seats:
                    btn = ttk.Button(self.seats_frame, 
                                   text=f"{seat_num}",
                                   width=5,
                                   command=lambda s=seat_num: self.toggle_seat(s))
                    btn.grid(row=row, column=col, padx=2, pady=2)
                    
        # Screen representation
        screen_label = ttk.Label(self.seats_frame, text="SCREEN THIS WAY", font=('Arial', 10, 'bold'))
        screen_label.grid(row=total_rows + 1, column=0, columnspan=10, pady=10)
        
    def toggle_seat(self, seat_num):
        if seat_num in self.selected_seats:
            self.selected_seats.remove(seat_num)
            self.seats_frame.winfo_children()[seat_num-1].configure(style='TButton')
        else:
            self.selected_seats.append(seat_num)
            style = ttk.Style()
            style.configure('Selected.TButton', background='green')
            self.seats_frame.winfo_children()[seat_num-1].configure(style='Selected.TButton')
            
        self.update_status()
        
    def update_status(self):
        self.status_label.configure(text=f"Selected Seats: {sorted(self.selected_seats)}")
        
    def update_seat_display(self, event=None):
        movie = self.selected_movie.get()
        if movie:
            if self.movies[movie] == 0:
                messagebox.showwarning("Sold Out", "Sorry, this movie is sold out!")
                self.selected_movie.set("")
                return
                
            self.selected_seats = []
            self.create_seat_layout()
            self.status_label.configure(text="")
            
    def book_tickets(self):
        if not self.selected_movie.get():
            messagebox.showwarning("Warning", "Please select a movie first!")
            return
            
        if not self.selected_seats:
            messagebox.showwarning("Warning", "Please select at least one seat!")
            return
            
        movie = self.selected_movie.get()
        seats = sorted(self.selected_seats)
        
        # Confirm booking
        confirm = messagebox.askyesno("Confirm Booking", 
                                    f"Book {len(seats)} seat(s) for {movie}?\nSeats: {seats}")
        
        if confirm:
            # Update available seats
            self.movies[movie] -= len(seats)
            messagebox.showinfo("Success", 
                              f"Booking successful!\nMovie: {movie}\nSeats: {seats}")
            
            # Reset selection
            self.selected_seats = []
            self.selected_movie.set("")
            self.status_label.configure(text="")
            
            # Clear seat layout
            for widget in self.seats_frame.winfo_children():
                widget.destroy()

def main():
    root = tk.Tk()
    app = MovieBookingSystem(root)
    root.mainloop()

if _name_ == "_main_":
    main()
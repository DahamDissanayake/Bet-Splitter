import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
from datetime import datetime
import json
import os

class BetSplitterApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DAMA Bet Splitter")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')
        
        # Remove tkinter icon
        self.root.iconbitmap()
        
        # Data storage
        self.current_session = None
        self.bettors = []
        self.bets = []
        self.total_pool = 0
        
        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('Title.TLabel', font=('Arial', 16, 'bold'))
        self.style.configure('Header.TLabel', font=('Arial', 12, 'bold'))
        
        self.create_main_menu()
        
    def create_main_menu(self):
        """Create the main menu interface"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = ttk.Label(main_frame, text="DAMA Bet Splitter", style='Title.TLabel')
        title_label.pack(pady=(0, 20))
        
        # GitHub link
        link_label = ttk.Label(main_frame, text="https://github.com/DahamDissanayake/Bet-Splitter", 
                              foreground="blue", cursor="hand2")
        link_label.pack(pady=(0, 30))
        
        # New Session button
        new_session_btn = ttk.Button(main_frame, text="Start New Betting Session", 
                                   command=self.create_new_session, width=25)
        new_session_btn.pack(pady=10)
        
        # Load Session button
        load_session_btn = ttk.Button(main_frame, text="Load Previous Session", 
                                    command=self.load_session, width=25)
        load_session_btn.pack(pady=10)
        
        # Copyright
        copyright_label = ttk.Label(main_frame, text="© 2025 DAMA - All Rights Reserved")
        copyright_label.pack(side=tk.BOTTOM, pady=(20, 0))
        
    def create_new_session(self):
        """Create a new betting session"""
        # Get session details
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        event_name = simpledialog.askstring("Betting Event", "Enter the betting event name:")
        
        if not event_name:
            return
            
        self.current_session = {
            'date': date,
            'event': event_name,
            'bettors': [],
            'bets': [],
            'total_pool': 0
        }
        
        self.bettors = []
        self.bets = []
        self.total_pool = 0
        
        self.create_bettors_page()
        
    def create_bettors_page(self):
        """Create the page for adding bettors"""
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text=f"Session: {self.current_session['event']}", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        date_label = ttk.Label(header_frame, text=f"Date: {self.current_session['date']}")
        date_label.pack(side=tk.RIGHT)
        
        # Add bettor section
        add_frame = ttk.LabelFrame(main_frame, text="Add Bettor", padding="10")
        add_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(add_frame, text="Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.name_entry = ttk.Entry(add_frame, width=20)
        self.name_entry.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(add_frame, text="Stake:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.stake_entry = ttk.Entry(add_frame, width=15)
        self.stake_entry.grid(row=0, column=3, padx=(0, 20))
        
        add_btn = ttk.Button(add_frame, text="Add Bettor", command=self.add_bettor)
        add_btn.grid(row=0, column=4)
        
        # Bettors list
        list_frame = ttk.LabelFrame(main_frame, text="Current Bettors", padding="10")
        list_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Treeview for bettors
        columns = ('Name', 'Stake', 'Percentage')
        self.bettors_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=8)
        
        for col in columns:
            self.bettors_tree.heading(col, text=col)
            self.bettors_tree.column(col, width=150)
            
        self.bettors_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.bettors_tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bettors_tree.configure(yscrollcommand=scrollbar.set)
        
        # Total pool display
        self.pool_label = ttk.Label(main_frame, text="Total Pool: $0.00", style='Header.TLabel')
        self.pool_label.pack(pady=10)
        
        # Navigation buttons
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X)
        
        back_btn = ttk.Button(nav_frame, text="Back to Main", command=self.create_main_menu)
        back_btn.pack(side=tk.LEFT)
        
        next_btn = ttk.Button(nav_frame, text="Start Betting", command=self.create_betting_page)
        next_btn.pack(side=tk.RIGHT)
        
    def add_bettor(self):
        """Add a bettor to the list"""
        name = self.name_entry.get().strip()
        try:
            stake = float(self.stake_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter a valid stake amount")
            return
            
        if not name:
            messagebox.showerror("Error", "Please enter a name")
            return
            
        if stake <= 0:
            messagebox.showerror("Error", "Stake must be greater than 0")
            return
            
        # Check if name already exists
        for bettor in self.bettors:
            if bettor['name'].lower() == name.lower():
                messagebox.showerror("Error", "Bettor name already exists")
                return
                
        # Add bettor
        bettor = {'name': name, 'stake': stake}
        self.bettors.append(bettor)
        self.total_pool += stake
        
        # Update display
        self.update_bettors_display()
        
        # Clear entries
        self.name_entry.delete(0, tk.END)
        self.stake_entry.delete(0, tk.END)
        
    def update_bettors_display(self):
        """Update the bettors display"""
        # Clear tree
        for item in self.bettors_tree.get_children():
            self.bettors_tree.delete(item)
            
        # Add bettors
        for bettor in self.bettors:
            percentage = (bettor['stake'] / self.total_pool * 100) if self.total_pool > 0 else 0
            self.bettors_tree.insert('', tk.END, values=(
                bettor['name'], 
                f"${bettor['stake']:.2f}", 
                f"{percentage:.1f}%"
            ))
            
        # Update pool label
        self.pool_label.config(text=f"Total Pool: ${self.total_pool:.2f}")
        
    def create_betting_page(self):
        """Create the betting page"""
        if not self.bettors:
            messagebox.showerror("Error", "Please add at least one bettor first")
            return
            
        # Clear the window
        for widget in self.root.winfo_children():
            widget.destroy()
            
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Header
        header_frame = ttk.Frame(main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Betting Interface", style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        pool_label = ttk.Label(header_frame, text=f"Available Pool: ${self.total_pool:.2f}", 
                              style='Header.TLabel')
        pool_label.pack(side=tk.RIGHT)
        
        # Add bet section
        add_bet_frame = ttk.LabelFrame(main_frame, text="Add New Bet", padding="10")
        add_bet_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Bet details
        details_frame = ttk.Frame(add_bet_frame)
        details_frame.pack(fill=tk.X)
        
        ttk.Label(details_frame, text="Bet Name:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10))
        self.bet_name_entry = ttk.Entry(details_frame, width=20)
        self.bet_name_entry.grid(row=0, column=1, padx=(0, 20))
        
        ttk.Label(details_frame, text="Bet:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10))
        self.bet_desc_entry = ttk.Entry(details_frame, width=25)
        self.bet_desc_entry.grid(row=0, column=3, padx=(0, 20))
        
        ttk.Label(details_frame, text="Odds:").grid(row=1, column=0, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.odds_entry = ttk.Entry(details_frame, width=10)
        self.odds_entry.grid(row=1, column=1, padx=(0, 20), pady=(10, 0))
        
        ttk.Label(details_frame, text="Stake:").grid(row=1, column=2, sticky=tk.W, padx=(0, 10), pady=(10, 0))
        self.bet_stake_entry = ttk.Entry(details_frame, width=10)
        self.bet_stake_entry.grid(row=1, column=3, padx=(0, 20), pady=(10, 0))
        
        add_bet_btn = ttk.Button(details_frame, text="Add Bet", command=self.add_bet)
        add_bet_btn.grid(row=1, column=4, pady=(10, 0))
        
        # Bets list
        bets_frame = ttk.LabelFrame(main_frame, text="Current Bets", padding="10")
        bets_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Treeview for bets
        bet_columns = ('Name', 'Bet', 'Odds', 'Stake', 'Potential Payout', 'Status')
        self.bets_tree = ttk.Treeview(bets_frame, columns=bet_columns, show='headings', height=8)
        
        for col in bet_columns:
            self.bets_tree.heading(col, text=col)
            self.bets_tree.column(col, width=120)
            
        self.bets_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Scrollbar for bets
        bet_scrollbar = ttk.Scrollbar(bets_frame, orient=tk.VERTICAL, command=self.bets_tree.yview)
        bet_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.bets_tree.configure(yscrollcommand=bet_scrollbar.set)
        
        # Bet result buttons
        result_frame = ttk.Frame(bets_frame)
        result_frame.pack(fill=tk.X, pady=(10, 0))
        
        ttk.Button(result_frame, text="Mark as Won", command=self.mark_won).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(result_frame, text="Mark as Lost", command=self.mark_lost).pack(side=tk.LEFT)
        
        # Navigation and action buttons
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X)
        
        back_btn = ttk.Button(nav_frame, text="Back to Bettors", command=self.create_bettors_page)
        back_btn.pack(side=tk.LEFT)
        
        calculate_btn = ttk.Button(nav_frame, text="Calculate Results", command=self.calculate_results)
        calculate_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        save_btn = ttk.Button(nav_frame, text="Save Session", command=self.save_session)
        save_btn.pack(side=tk.RIGHT)
        
    def add_bet(self):
        """Add a new bet"""
        try:
            name = self.bet_name_entry.get().strip()
            bet_desc = self.bet_desc_entry.get().strip()
            odds = float(self.odds_entry.get())
            stake = float(self.bet_stake_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Please enter valid odds and stake values")
            return
            
        if not name or not bet_desc:
            messagebox.showerror("Error", "Please fill in all fields")
            return
            
        if stake <= 0 or odds <= 0:
            messagebox.showerror("Error", "Odds and stake must be greater than 0")
            return
            
        # Calculate remaining pool
        used_stake = sum(bet['stake'] for bet in self.bets if bet['status'] != 'Lost')
        available = self.total_pool - used_stake
        
        if stake > available:
            messagebox.showerror("Error", f"Not enough funds. Available: ${available:.2f}")
            return
            
        # Add bet
        bet = {
            'name': name,
            'description': bet_desc,
            'odds': odds,
            'stake': stake,
            'potential_payout': stake * odds,
            'status': 'Pending'
        }
        
        self.bets.append(bet)
        self.update_bets_display()
        
        # Clear entries
        self.bet_name_entry.delete(0, tk.END)
        self.bet_desc_entry.delete(0, tk.END)
        self.odds_entry.delete(0, tk.END)
        self.bet_stake_entry.delete(0, tk.END)
        
    def update_bets_display(self):
        """Update the bets display"""
        # Clear tree
        for item in self.bets_tree.get_children():
            self.bets_tree.delete(item)
            
        # Add bets
        for bet in self.bets:
            self.bets_tree.insert('', tk.END, values=(
                bet['name'],
                bet['description'],
                f"{bet['odds']:.2f}",
                f"${bet['stake']:.2f}",
                f"${bet['potential_payout']:.2f}",
                bet['status']
            ))
            
    def mark_won(self):
        """Mark selected bet as won"""
        selection = self.bets_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Please select a bet to mark as won")
            return
            
        item = selection[0]
        index = self.bets_tree.index(item)
        self.bets[index]['status'] = 'Won'
        self.update_bets_display()
        
    def mark_lost(self):
        """Mark selected bet as lost"""
        selection = self.bets_tree.selection()
        if not selection:
            messagebox.showinfo("Info", "Please select a bet to mark as lost")
            return
            
        item = selection[0]
        index = self.bets_tree.index(item)
        self.bets[index]['status'] = 'Lost'
        self.update_bets_display()
        
    def calculate_results(self):
        """Calculate and display final results"""
        if not self.bets:
            messagebox.showinfo("Info", "No bets to calculate")
            return
            
        # Calculate totals
        total_stake = sum(bet['stake'] for bet in self.bets)
        total_won = sum(bet['potential_payout'] for bet in self.bets if bet['status'] == 'Won')
        total_lost = sum(bet['stake'] for bet in self.bets if bet['status'] == 'Lost')
        total_profit = total_won - total_stake
        
        # Create results window
        results_window = tk.Toplevel(self.root)
        results_window.title("Betting Results")
        results_window.geometry("600x500")
        results_window.configure(bg='#f0f0f0')
        
        main_frame = ttk.Frame(results_window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Results summary
        summary_frame = ttk.LabelFrame(main_frame, text="Session Summary", padding="15")
        summary_frame.pack(fill=tk.X, pady=(0, 20))
        
        ttk.Label(summary_frame, text=f"Total Stakes: ${total_stake:.2f}", font=('Arial', 11)).pack(anchor=tk.W)
        ttk.Label(summary_frame, text=f"Total Winnings: ${total_won:.2f}", font=('Arial', 11)).pack(anchor=tk.W)
        ttk.Label(summary_frame, text=f"Total Losses: ${total_lost:.2f}", font=('Arial', 11)).pack(anchor=tk.W)
        ttk.Label(summary_frame, text=f"Net Profit/Loss: ${total_profit:.2f}", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        
        # Payout distribution
        payout_frame = ttk.LabelFrame(main_frame, text="Payout Distribution", padding="15")
        payout_frame.pack(fill=tk.BOTH, expand=True)
        
        # Calculate each bettor's share
        final_amount = self.total_pool + total_profit
        
        # Treeview for payouts
        payout_columns = ('Bettor', 'Initial Stake', 'Percentage', 'Final Payout', 'Profit/Loss')
        payout_tree = ttk.Treeview(payout_frame, columns=payout_columns, show='headings', height=8)
        
        for col in payout_columns:
            payout_tree.heading(col, text=col)
            payout_tree.column(col, width=110)
            
        payout_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add payout data
        for bettor in self.bettors:
            percentage = bettor['stake'] / self.total_pool
            final_payout = final_amount * percentage
            profit_loss = final_payout - bettor['stake']
            
            payout_tree.insert('', tk.END, values=(
                bettor['name'],
                f"${bettor['stake']:.2f}",
                f"{percentage*100:.1f}%",
                f"${final_payout:.2f}",
                f"${profit_loss:.2f}"
            ))
            
    def save_session(self):
        """Save the current session to a JSON file"""
        if not self.current_session:
            messagebox.showinfo("Info", "No session to save")
            return
            
        # Update session data
        self.current_session['bettors'] = self.bettors
        self.current_session['bets'] = self.bets
        self.current_session['total_pool'] = self.total_pool
        
        # Generate filename
        event_name = self.current_session['event'].replace(' ', '_')
        date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"betting_session_{event_name}_{date_str}.json"
        
        try:
            with open(filename, 'w') as f:
                json.dump(self.current_session, f, indent=2)
            messagebox.showinfo("Success", f"Session saved as {filename}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save session: {str(e)}")
            
    def load_session(self):
        """Load a previous session"""
        # This is a simplified version - in a full app you'd want a file dialog
        filename = simpledialog.askstring("Load Session", "Enter the session filename:")
        if not filename:
            return
            
        try:
            with open(filename, 'r') as f:
                self.current_session = json.load(f)
                
            self.bettors = self.current_session.get('bettors', [])
            self.bets = self.current_session.get('bets', [])
            self.total_pool = self.current_session.get('total_pool', 0)
            
            self.create_betting_page()
            messagebox.showinfo("Success", "Session loaded successfully")
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session: {str(e)}")

def main():
    root = tk.Tk()
    app = BetSplitterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
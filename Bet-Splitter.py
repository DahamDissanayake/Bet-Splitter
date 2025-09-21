import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, filedialog
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
        
        title_label = ttk.Label(header_frame, text=f"Session: {self.current_session['event'] if self.current_session else 'New Session'}", 
                               style='Title.TLabel')
        title_label.pack(side=tk.LEFT)
        
        date_label = ttk.Label(header_frame, text=f"Date: {self.current_session['date'] if self.current_session else datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
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
        self.pool_label = ttk.Label(main_frame, text="Total Pool: LKR 0.00", style='Header.TLabel')
        self.pool_label.pack(pady=10)
        
        # Navigation buttons
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X)
        
        back_btn = ttk.Button(nav_frame, text="Back to Main", command=self.create_main_menu)
        back_btn.pack(side=tk.LEFT)
        
        next_btn = ttk.Button(nav_frame, text="Start Betting", command=self.create_betting_page)
        next_btn.pack(side=tk.RIGHT)
        
        # Update display with existing data
        if self.bettors:
            self.update_bettors_display()
        
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
                f"LKR {bettor['stake']:.2f}", 
                f"{percentage:.1f}%"
            ))
            
        # Update pool label
        self.pool_label.config(text=f"Total Pool: LKR {self.total_pool:.2f}")
        
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
        
        pool_label = ttk.Label(header_frame, text=f"Available Pool: LKR {self.get_available_pool():.2f}", 
                              style='Header.TLabel')
        pool_label.pack(side=tk.RIGHT)
        self.pool_display_label = pool_label  # Store reference for updates
        
        # Add bet section - FIXED: Made more compact
        add_bet_frame = ttk.LabelFrame(main_frame, text="Add New Bet", padding="10")
        add_bet_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Bet details in a more compact layout
        details_frame = ttk.Frame(add_bet_frame)
        details_frame.pack(fill=tk.X)
        
        # First row
        row1_frame = ttk.Frame(details_frame)
        row1_frame.pack(fill=tk.X, pady=(0, 5))
        
        ttk.Label(row1_frame, text="Bet Name:").pack(side=tk.LEFT, padx=(0, 5))
        self.bet_name_entry = ttk.Entry(row1_frame, width=15)
        self.bet_name_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(row1_frame, text="Bet:").pack(side=tk.LEFT, padx=(0, 5))
        self.bet_desc_entry = ttk.Entry(row1_frame, width=20)
        self.bet_desc_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(row1_frame, text="Odds:").pack(side=tk.LEFT, padx=(0, 5))
        self.odds_entry = ttk.Entry(row1_frame, width=8)
        self.odds_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        ttk.Label(row1_frame, text="Stake:").pack(side=tk.LEFT, padx=(0, 5))
        self.bet_stake_entry = ttk.Entry(row1_frame, width=8)
        self.bet_stake_entry.pack(side=tk.LEFT, padx=(0, 15))
        
        add_bet_btn = ttk.Button(row1_frame, text="Add Bet", command=self.add_bet)
        add_bet_btn.pack(side=tk.LEFT)
        
        # Bets list - FIXED: Better space allocation and scrolling
        bets_frame = ttk.LabelFrame(main_frame, text="Current Bets", padding="10")
        bets_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Create a frame for the treeview and scrollbar
        tree_container = ttk.Frame(bets_frame)
        tree_container.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Treeview for bets with better column sizing
        bet_columns = ('Name', 'Bet', 'Odds', 'Stake', 'Potential Payout', 'Status')
        self.bets_tree = ttk.Treeview(tree_container, columns=bet_columns, show='headings')
        
        # Better column configuration for visibility
        column_widths = {'Name': 100, 'Bet': 150, 'Odds': 60, 'Stake': 80, 'Potential Payout': 100, 'Status': 70}
        for col in bet_columns:
            self.bets_tree.heading(col, text=col)
            self.bets_tree.column(col, width=column_widths[col], minwidth=50)
        
        # Add scrollbars
        v_scrollbar = ttk.Scrollbar(tree_container, orient=tk.VERTICAL, command=self.bets_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_container, orient=tk.HORIZONTAL, command=self.bets_tree.xview)
        
        self.bets_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Pack treeview and scrollbars
        self.bets_tree.grid(row=0, column=0, sticky='nsew')
        v_scrollbar.grid(row=0, column=1, sticky='ns')
        h_scrollbar.grid(row=1, column=0, sticky='ew')
        
        # Configure grid weights
        tree_container.grid_rowconfigure(0, weight=1)
        tree_container.grid_columnconfigure(0, weight=1)
        
        # Bet management buttons - ENHANCED
        management_frame = ttk.Frame(bets_frame)
        management_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Left side - Bet status buttons
        status_frame = ttk.LabelFrame(management_frame, text="Quick Status Change", padding="5")
        status_frame.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        ttk.Button(status_frame, text="Mark as Won", command=self.mark_won).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(status_frame, text="Mark as Lost", command=self.mark_lost).pack(side=tk.LEFT, padx=(0, 5))
        
        # Right side - Management buttons
        actions_frame = ttk.LabelFrame(management_frame, text="Bet Management", padding="5")
        actions_frame.pack(side=tk.RIGHT, padx=(10, 0))
        
        ttk.Button(actions_frame, text="Set All Results", command=self.set_bet_results).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(actions_frame, text="Delete Selected", command=self.delete_bet).pack(side=tk.LEFT)
        
        # Navigation and action buttons
        nav_frame = ttk.Frame(main_frame)
        nav_frame.pack(fill=tk.X)
        
        back_btn = ttk.Button(nav_frame, text="Back to Bettors", command=self.create_bettors_page)
        back_btn.pack(side=tk.LEFT)
        
        calculate_btn = ttk.Button(nav_frame, text="Calculate Results", command=self.calculate_results)
        calculate_btn.pack(side=tk.RIGHT, padx=(10, 0))
        
        save_btn = ttk.Button(nav_frame, text="Save Session", command=self.save_session)
        save_btn.pack(side=tk.RIGHT)
        
        # Update displays with existing data
        if self.bets:
            self.update_bets_display()
        self.update_pool_display()
        
    def get_available_pool(self):
        """Calculate available pool amount"""
        used_stake = sum(bet['stake'] for bet in self.bets)
        return self.total_pool - used_stake
    
    def update_pool_display(self):
        """Update the available pool display"""
        if hasattr(self, 'pool_display_label'):
            available = self.get_available_pool()
            self.pool_display_label.config(text=f"Available Pool: LKR {available:.2f}")
    
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
        available = self.get_available_pool()
        
        if stake > available:
            messagebox.showerror("Error", f"Not enough funds. Available: LKR {available:.2f}")
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
        self.update_pool_display()  # Update available pool display
        
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
                f"LKR {bet['stake']:.2f}",
                f"LKR {bet['potential_payout']:.2f}",
                bet['status']
            ))
    
    def delete_bet(self):
        """Delete selected bet - FIXED IMPLEMENTATION"""
        selection = self.bets_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a bet from the list to delete")
            return
            
        # Get the selected item
        selected_item = selection[0]
        
        # Get bet details for confirmation
        bet_values = self.bets_tree.item(selected_item, 'values')
        bet_name = bet_values[0]
        bet_stake = bet_values[3]
        
        # Confirm deletion
        if messagebox.askyesno("Confirm Deletion", 
                              f"Are you sure you want to delete this bet?\n\n"
                              f"Bet: {bet_name}\n"
                              f"Stake: {bet_stake}\n\n"
                              f"This stake will be returned to the available pool."):
            
            # Find the index of the selected item
            all_items = self.bets_tree.get_children()
            index = all_items.index(selected_item)
            
            # Remove from data
            deleted_bet = self.bets.pop(index)
            
            # Update displays
            self.update_bets_display()
            self.update_pool_display()
            
            messagebox.showinfo("Bet Deleted", 
                               f"Bet '{deleted_bet['name']}' has been deleted.\n"
                               f"LKR {deleted_bet['stake']:.2f} returned to available pool.")
    
    def mark_won(self):
        """Mark selected bet as won - FIXED IMPLEMENTATION"""
        selection = self.bets_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a bet from the list to mark as won")
            return
            
        # Get the selected item
        selected_item = selection[0]
        
        # Find the index of the selected item
        all_items = self.bets_tree.get_children()
        index = all_items.index(selected_item)
        
        # Update status
        old_status = self.bets[index]['status']
        self.bets[index]['status'] = 'Won'
        
        # Update display
        self.update_bets_display()
        
        bet_name = self.bets[index]['name']
        messagebox.showinfo("Status Updated", f"Bet '{bet_name}' marked as Won")
        
    def mark_lost(self):
        """Mark selected bet as lost - FIXED IMPLEMENTATION"""
        selection = self.bets_tree.selection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a bet from the list to mark as lost")
            return
            
        # Get the selected item
        selected_item = selection[0]
        
        # Find the index of the selected item
        all_items = self.bets_tree.get_children()
        index = all_items.index(selected_item)
        
        # Update status
        old_status = self.bets[index]['status']
        self.bets[index]['status'] = 'Lost'
        
        # Update display
        self.update_bets_display()
        
        bet_name = self.bets[index]['name']
        messagebox.showinfo("Status Updated", f"Bet '{bet_name}' marked as Lost")
    
    def set_bet_results(self):
        """Set results for all bets before calculating final results - REDESIGNED"""
        if not self.bets:
            messagebox.showinfo("Info", "No bets to set results for")
            return
            
        # Create bet results window
        results_window = tk.Toplevel(self.root)
        results_window.title("Set Bet Results")
        results_window.geometry("900x600")
        results_window.configure(bg='#f0f0f0')
        results_window.grab_set()  # Make window modal
        results_window.resizable(True, True)
        
        # Main container with padding
        main_container = ttk.Frame(results_window, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header section
        header_frame = ttk.Frame(main_container)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(header_frame, text="Set Results for All Bets", 
                               font=('Arial', 16, 'bold'), foreground='#2c3e50')
        title_label.pack(anchor=tk.W)
        
        info_label = ttk.Label(header_frame, 
                              text="Select the outcome for each bet. You can change these results later if needed.",
                              font=('Arial', 10), foreground='#7f8c8d')
        info_label.pack(anchor=tk.W, pady=(5, 0))
        
        # Statistics bar
        stats_frame = ttk.LabelFrame(main_container, text="Current Statistics", padding="15")
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        stats_inner = ttk.Frame(stats_frame)
        stats_inner.pack(fill=tk.X)
        
        total_bets = len(self.bets)
        total_stake = sum(bet['stake'] for bet in self.bets)
        pending_bets = len([bet for bet in self.bets if bet['status'] == 'Pending'])
        
        ttk.Label(stats_inner, text=f"Total Bets: {total_bets}", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 30))
        ttk.Label(stats_inner, text=f"Total Stake: LKR {total_stake:.2f}", font=('Arial', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 30))
        ttk.Label(stats_inner, text=f"Pending: {pending_bets}", font=('Arial', 10, 'bold'), foreground='#e74c3c').pack(side=tk.LEFT)
        
        # Main content area with scrollbar
        content_frame = ttk.LabelFrame(main_container, text="Bet Results", padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 20))
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(content_frame, bg='white')
        v_scrollbar = ttk.Scrollbar(content_frame, orient="vertical", command=canvas.yview)
        h_scrollbar = ttk.Scrollbar(content_frame, orient="horizontal", command=canvas.xview)
        scrollable_frame = ttk.Frame(canvas)
        
        # Configure scrolling
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Store result variables
        self.result_vars = []
        
        # Create header row
        header_row = ttk.Frame(scrollable_frame)
        header_row.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        ttk.Label(header_row, text="Bet Name", font=('Arial', 10, 'bold'), width=15).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(header_row, text="Description", font=('Arial', 10, 'bold'), width=20).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(header_row, text="Odds", font=('Arial', 10, 'bold'), width=8).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(header_row, text="Stake", font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Label(header_row, text="Potential Win", font=('Arial', 10, 'bold'), width=12).pack(side=tk.LEFT, padx=(0, 20))
        ttk.Label(header_row, text="Result", font=('Arial', 10, 'bold'), width=15).pack(side=tk.LEFT)
        
        # Add separator
        separator = ttk.Separator(scrollable_frame, orient='horizontal')
        separator.pack(fill=tk.X, padx=5, pady=(0, 10))
        
        # Create result controls for each bet
        for i, bet in enumerate(self.bets):
            # Main bet frame with alternating colors
            bet_frame = ttk.Frame(scrollable_frame)
            bet_frame.pack(fill=tk.X, padx=5, pady=2)
            
            # Bet details in columns
            ttk.Label(bet_frame, text=bet['name'][:15], width=15, 
                     font=('Arial', 9, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Label(bet_frame, text=bet['description'][:20], width=20).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Label(bet_frame, text=f"{bet['odds']:.2f}", width=8).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Label(bet_frame, text=f"LKR {bet['stake']:.2f}", width=12).pack(side=tk.LEFT, padx=(0, 10))
            ttk.Label(bet_frame, text=f"LKR {bet['potential_payout']:.2f}", width=12, 
                     foreground='#27ae60').pack(side=tk.LEFT, padx=(0, 20))
            
            # Result selection with better styling
            result_var = tk.StringVar(value=bet['status'] if bet['status'] != 'Pending' else 'Won')
            self.result_vars.append(result_var)
            
            result_frame = ttk.Frame(bet_frame)
            result_frame.pack(side=tk.LEFT)
            
            # Custom styled radio buttons
            won_rb = ttk.Radiobutton(result_frame, text="Won", variable=result_var, 
                                   value="Won", style="Success.TRadiobutton")
            won_rb.pack(side=tk.LEFT, padx=(0, 15))
            
            lost_rb = ttk.Radiobutton(result_frame, text="Lost", variable=result_var, 
                                    value="Lost", style="Danger.TRadiobutton")
            lost_rb.pack(side=tk.LEFT)
            
            # Add subtle separator between bets
            if i < len(self.bets) - 1:
                ttk.Separator(scrollable_frame, orient='horizontal').pack(fill=tk.X, padx=20, pady=5)
        
        # Pack scrollbars and canvas
        canvas.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Action buttons with better styling
        button_frame = ttk.Frame(main_container)
        button_frame.pack(fill=tk.X, pady=(10, 0))
        
        # Left side - utility buttons
        left_buttons = ttk.Frame(button_frame)
        left_buttons.pack(side=tk.LEFT)
        
        ttk.Button(left_buttons, text="Reset All to Won", 
                  command=lambda: self.set_all_results("Won")).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(left_buttons, text="Reset All to Lost", 
                  command=lambda: self.set_all_results("Lost")).pack(side=tk.LEFT)
        
        # Right side - main action buttons
        right_buttons = ttk.Frame(button_frame)
        right_buttons.pack(side=tk.RIGHT)
        
        cancel_btn = ttk.Button(right_buttons, text="Cancel", command=results_window.destroy)
        cancel_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        apply_btn = ttk.Button(right_buttons, text="Apply Results", 
                              command=lambda: self.apply_bet_results(results_window))
        apply_btn.pack(side=tk.LEFT)
        
        # Configure custom styles
        style = ttk.Style()
        style.configure("Success.TRadiobutton", foreground='#27ae60')
        style.configure("Danger.TRadiobutton", foreground='#e74c3c')
        
        # Bind mouse wheel scrolling
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", on_mousewheel)
    
    def set_all_results(self, result):
        """Set all bets to the same result"""
        for var in self.result_vars:
            var.set(result)
        messagebox.showinfo("Updated", f"All bets set to '{result}'")
    
    def apply_bet_results(self, window):
        """Apply the bet results and close the window"""
        for i, result_var in enumerate(self.result_vars):
            self.bets[i]['status'] = result_var.get()
        
        self.update_bets_display()
        window.destroy()
        messagebox.showinfo("Success", "Bet results have been updated!")
        
    def calculate_results(self):
        """Calculate and display final results"""
        if not self.bets:
            messagebox.showinfo("Info", "No bets to calculate")
            return
            
        # Check if all bets have results
        pending_bets = [bet for bet in self.bets if bet['status'] == 'Pending']
        if pending_bets:
            response = messagebox.askyesno("Pending Bets", 
                                         f"There are {len(pending_bets)} bets with pending results. "
                                         "Do you want to set results for all bets first?")
            if response:
                self.set_bet_results()
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
        
        ttk.Label(summary_frame, text=f"Total Stakes: LKR {total_stake:.2f}", font=('Arial', 11)).pack(anchor=tk.W)
        ttk.Label(summary_frame, text=f"Total Winnings: LKR {total_won:.2f}", font=('Arial', 11)).pack(anchor=tk.W)
        ttk.Label(summary_frame, text=f"Total Losses: LKR {total_lost:.2f}", font=('Arial', 11)).pack(anchor=tk.W)
        ttk.Label(summary_frame, text=f"Net Profit/Loss: LKR {total_profit:.2f}", 
                 font=('Arial', 12, 'bold')).pack(anchor=tk.W)
        
        # Payout distribution
        payout_frame = ttk.LabelFrame(main_frame, text="Payout Distribution", padding="15")
        payout_frame.pack(fill=tk.BOTH, expand=True)
        
        # Calculate each bettor's share INCLUDING LEFTOVER MONEY
        leftover_money = self.get_available_pool()  # Money not used in bets
        final_amount = self.total_pool + total_profit  # Original pool + profit/loss
        
        # Show leftover money info
        if leftover_money > 0:
            leftover_frame = ttk.Frame(payout_frame)
            leftover_frame.pack(fill=tk.X, pady=(0, 10))
            
            ttk.Label(leftover_frame, 
                     text=f"Leftover Money (not used in bets): LKR {leftover_money:.2f} - This will be distributed proportionally",
                     font=('Arial', 10, 'bold'), foreground='#2980b9').pack(anchor=tk.W)
        
        # Treeview for payouts
        payout_columns = ('Bettor', 'Initial Stake', 'Percentage', 'Share of Winnings', 'Share of Leftover', 'Final Payout', 'Net Profit/Loss')
        payout_tree = ttk.Treeview(payout_frame, columns=payout_columns, show='headings', height=8)
        
        for col in payout_columns:
            payout_tree.heading(col, text=col)
            if col in ['Initial Stake', 'Share of Winnings', 'Share of Leftover', 'Final Payout', 'Net Profit/Loss']:
                payout_tree.column(col, width=100)
            else:
                payout_tree.column(col, width=80)
            
        payout_tree.pack(fill=tk.BOTH, expand=True)
        
        # Add payout data with leftover money calculation
        for bettor in self.bettors:
            percentage = bettor['stake'] / self.total_pool
            
            # Share of winnings/losses (excluding leftover)
            share_of_winnings = (self.total_pool + total_profit - leftover_money) * percentage
            
            # Share of leftover money
            share_of_leftover = leftover_money * percentage
            
            # Final payout = initial stake portion of winnings + leftover share
            final_payout = share_of_winnings + share_of_leftover
            
            # Net profit/loss compared to initial stake
            net_profit_loss = final_payout - bettor['stake']
            
            payout_tree.insert('', tk.END, values=(
                bettor['name'],
                f"LKR {bettor['stake']:.2f}",
                f"{percentage*100:.1f}%",
                f"LKR {share_of_winnings:.2f}",
                f"LKR {share_of_leftover:.2f}",
                f"LKR {final_payout:.2f}",
                f"LKR {net_profit_loss:.2f}"
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
        """Load a previous session - FIXED: Added file dialog"""
        # Get the directory where the Python file is located
        current_dir = os.path.dirname(os.path.abspath(__file__))
        
        # Open file dialog to select JSON file
        filename = filedialog.askopenfilename(
            title="Select Betting Session File",
            initialdir=current_dir,
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")],
            defaultextension=".json"
        )
        
        if not filename:
            return
            
        try:
            with open(filename, 'r') as f:
                self.current_session = json.load(f)
                
            self.bettors = self.current_session.get('bettors', [])
            self.bets = self.current_session.get('bets', [])
            self.total_pool = self.current_session.get('total_pool', 0)
            
            # Go directly to betting page if there are bets, otherwise go to bettors page
            if self.bets:
                self.create_betting_page()
            else:
                self.create_bettors_page()
                
            messagebox.showinfo("Success", f"Session '{self.current_session.get('event', 'Unknown')}' loaded successfully")
            
        except FileNotFoundError:
            messagebox.showerror("Error", "File not found")
        except json.JSONDecodeError:
            messagebox.showerror("Error", "Invalid JSON file format")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load session: {str(e)}")

def main():
    root = tk.Tk()
    app = BetSplitterApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
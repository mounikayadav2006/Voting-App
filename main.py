# ---------------------- main.py (Final Step) ----------------------
import tkinter as tk
from tkinter import messagebox
import sqlite3
import datetime
import winsound

# ---------------------- Admin Password ----------------------
ADMIN_PASSWORD = "admin123" #This is a function named logout.
 #It needs a window (like voting screen or admin screen) to be passed into it.

# ---------------------- Logout Function ----------------------
def logout(current_window):
    current_window.destroy()
    root = tk.Tk()
    app = Login(root)
    root.mainloop()
    #	Keeps the new window running until you exit again.

# ---------------------- Count Voters ----------------------
def count_voters():
    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM voters")
    total = cursor.fetchone()[0] #Without [0], you will get a tuple, not a number
    cursor.execute("SELECT COUNT(*) FROM voters WHERE has_voted = 1")
    voted = cursor.fetchone()[0]
    conn.close()
    return total, voted, total - voted

# ---------------------- Voting Screen ----------------------

def open_vote_screen(voter_id, voter_name):
    win = tk.Tk()
    tk.Label(win, text="🗳️ Secure Voting System", font=("Segoe UI", 26, "bold"), bg="#62a043", fg="white").pack(fill="x")
    win.title("Vote Now")
    win.geometry("900x600")
    win.configure(bg="#e8f5e9")

    tk.Label(win, text=f"Welcome {voter_name}, Cast Your Vote", font=("Segoe UI", 22, "bold"), bg="#e8f5e9").pack(pady=20)
    frame = tk.Frame(win, bg="#e8f5e9")#	Container to group widgets (Radio buttons are grouped inside the frame)
    frame.pack()

    conn = sqlite3.connect("voting.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM candidates")
    candidates = cursor.fetchall()#all tuples together
    conn.close()

    selected = tk.StringVar() # tkinter provides StringVar, which connects the GUI to a variable.-->selected
  # updations
    def submit_vote():
        choice = selected.get()#getting from user and assigning to choice
        if not choice:
            messagebox.showwarning("Select", "Please select a candidate")#select is title
            return

        conn = sqlite3.connect("voting.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, party FROM candidates WHERE candidate_id = ?", (choice,))
        row = cursor.fetchone()
        candidate_name, party = row[0], row[1]
        cursor.execute("UPDATE voters SET has_voted = 1 WHERE voter_id = ?", (voter_id,))
        #voter_id: is the unique ID of the current voter who is logged in
        cursor.execute("INSERT INTO votes (voter_id, candidate, party) VALUES (?, ?, ?)", (voter_id, candidate_name, party))
        conn.commit()
        conn.close()

        winsound.Beep(1000, 300)

        messagebox.showinfo("Vote Recorded", f"✅ Your vote for {candidate_name} has been successfully recorded!")

        def show_slip():
            slip = tk.Toplevel()
            slip.title("Confirmation Slip")
            slip.geometry("400x300")
            slip.config(bg="#f0f4c3")

            tk.Label(slip, text="----- Confirmation Slip -----", font=("Courier", 16, "bold"), bg="#f0f4c3").pack(pady=5)

            # tk.Label(slip, text="Voting Completed ✅", font=("Segoe UI", 20, "bold"), bg="#f0f4c3").pack(pady=10)
            tk.Label(slip, text=f"Voter Name: {voter_name}", font=("Segoe UI", 16), bg="#f0f4c3").pack(pady=5)
            tk.Label(slip, text=f"Voted for: {candidate_name}", font=("Segoe UI", 16), bg="#f0f4c3").pack(pady=5)
            tk.Label(slip, text=f"Time: {datetime.datetime.now().strftime('%H:%M:%S')}\nDate: {datetime.datetime.now().strftime('%d-%m-%Y')}",
                      font=("Segoe UI", 14), bg="#f0f4c3").pack(pady=10)

            def close_all():
                slip.destroy()
                win.destroy()

            tk.Button(slip, text="Close", command=close_all, font=("Segoe UI", 14), bg="#aed581").pack(pady=10)

        show_slip()
    for idx, c in enumerate(candidates):
          tk.Radiobutton(frame, text=f"{c[1]} ({c[2]})", variable=selected, value=c[0],
                   font=("Segoe UI", 16), bg="#c8e6c9", indicatoron=0,
                   width=25, padx=10, pady=10).grid(row=idx//2, column=idx%2, padx=20, pady=10)

    # for c in candidates:
    #     tk.Radiobutton(frame, text=f"{c[1]} ({c[2]})", variable=selected, value=c[0],
    #                    font=("Segoe UI", 16), bg="#c8e6c9", indicatoron=0,
    #                    width=25, padx=10, pady=10).pack(pady=10)
        
        #These radio buttons appear visually in the Tkinter window.

        # Now, the user (voter) uses the mouse to click on one of them.

        #That click stores the value (candidate ID) inside selected
        
        
        #When user selects that radio button, selected gets the value c[0] (the candidate ID).
        #It removes the circular dot, and makes it look like a button that you can click-->indicatoron

    tk.Button(win, text="Submit Vote", command=submit_vote, font=("Segoe UI", 16), bg="#4caf50", fg="white").pack(pady=20)
    
    # 🔁 Add Logout button here
    tk.Button(win, text="Logout", command=lambda: logout(win), font=("Segoe UI", 14), bg="orange", fg="white").pack(pady=10)
  #lambda: logout(win) → Create a function to run only when clicked.
    win.mainloop()

# ---------------------- Admin View ----------------------
def show_results():
    def verify():
        if pwd.get() != ADMIN_PASSWORD:
            messagebox.showerror("Error", "Incorrect password")
            return
        win = tk.Toplevel()
        win.title("Voting Results")
        win.geometry("500x400")
        win.configure(bg="#fffde7")
        conn = sqlite3.connect("voting.db")
        cursor = conn.cursor()
        cursor.execute("SELECT candidate, COUNT(*) FROM votes GROUP BY candidate")
        result = cursor.fetchall()
        conn.close()

        for r in result:
            tk.Label(win, text=f"{r[0]} — {r[1]} votes", font=("Segoe UI", 16), bg="#fffde7").pack(pady=5)
        
        # 🔁 Add Logout button in admin results
        tk.Button(win, text="Logout", command=lambda: logout(win), font=("Segoe UI", 14), bg="orange", fg="white").pack(pady=20)

    win = tk.Toplevel()
    win.title("Admin Login")
    win.geometry("300x200")
    win.configure(bg="#fce4ec")
    tk.Label(win, text="Enter Admin Password", font=("Segoe UI", 16), bg="#fce4ec").pack(pady=10)
    pwd = tk.Entry(win, show="*", font=("Segoe UI", 14), width=20)
    pwd.pack()
    tk.Button(win, text="Submit", command=verify, font=("Segoe UI", 14), bg="#ec407a", fg="white").pack(pady=10)

# ---------------------- Login Page ----------------------
class Login:
    def __init__(self, root):
        self.root = root#This line saves the window (root) so you can use it inside the class later.
        self.root.title("Voter Login")
        self.root.attributes('-fullscreen', True)
        self.root.configure(bg="#e3f2fd")
        def confirm_exit():

         if messagebox.askyesno("Exit", "Are you sure you want to exit?"):
           root.destroy()

       

        exit_btn = tk.Button(root, text="Exit", command=root.destroy, font=("Segoe UI", 14), bg="red", fg="white")
        exit_btn.place(x=10, y=10)

        tk.Label(root, text="Secure Voter Login", font=("Segoe UI", 30, "bold"), bg="#e3f2fd", fg="#0d47a1").pack(pady=30)

        frame = tk.Frame(root, bg="#e3f2fd")
        frame.pack()
        #A Frame is like a box inside the window.

        #You can put buttons, labels, entries, etc. inside that box.

        left = tk.Frame(frame, bg="#e3f2fd")
        left.grid(row=0, column=0, padx=80) #.grid() method in Tkinter places widgets using a row-column table layout 

        right = tk.Frame(frame, bg="#e3f2fd")
        right.grid(row=0, column=1, padx=80)

        tk.Label(left, text="Voter ID", font=("Segoe UI", 16), bg="#e3f2fd").pack(pady=10)
        self.voter_id = tk.Entry(left, font=("Segoe UI", 16))#We store the box in a variable so that we can get the value
        self.voter_id.pack()

        tk.Label(left, text="Password", font=("Segoe UI", 16), bg="#e3f2fd").pack(pady=10)
        self.password = tk.Entry(left, show="*", font=("Segoe UI", 16))
        self.password.pack()

        tk.Button(left, text="Login", command=self.validate, font=("Segoe UI", 16), bg="#2196f3", fg="white", width=15).pack(pady=20)

        total, voted, not_voted = count_voters()
        tk.Label(right, text=f"Registered Voters: {total}", font=("Segoe UI", 16), bg="#e3f2fd").pack(pady=5)
        tk.Label(right, text=f"Voted: {voted}", font=("Segoe UI", 16), bg="#e3f2fd").pack(pady=5)
        tk.Label(right, text=f"Not Voted: {not_voted}", font=("Segoe UI", 16), bg="#e3f2fd").pack(pady=5)

        tk.Button(root, text="Admin Results", command=show_results, font=("Segoe UI", 14), bg="#8e24aa", fg="white").pack(pady=20)
    
        
    def validate(self):
        vid = self.voter_id.get()
        pwd = self.password.get()
        conn = sqlite3.connect("voting.db")
        cursor = conn.cursor()
        cursor.execute("SELECT name, password, has_voted FROM voters WHERE voter_id = ?", (vid,))
        row = cursor.fetchone()
        conn.close()
        if not row:
            messagebox.showerror("Error", "Voter ID not found")
        elif pwd != row[1]:
            messagebox.showerror("Error", "Wrong password")
        elif row[2] == 1:
            messagebox.showinfo("Already Voted", "You have already voted")
        else:
            self.root.destroy()
            open_vote_screen(vid, row[0])


# ---------------------- Start App ----------------------


root = tk.Tk()# Create the main Tkinter window
app = Login(root)# ✅ Create Login object ; login is class
root.mainloop()# Start the GUI loop
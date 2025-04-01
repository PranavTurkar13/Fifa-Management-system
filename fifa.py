from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from pymongo import MongoClient
import bcrypt


root = Tk()
root.title("FIFA Manager Login")
root.geometry("1100x800")  


bg_image = Image.open("C:/Users/HP/Downloads/fifa-background-33aoa324hzdl8opy.jpg")
bg_image = bg_image.resize((1100, 800), Image.Resampling.LANCZOS)  
bg_photo = ImageTk.PhotoImage(bg_image)

# Set background image
background_label = Label(root, image=bg_photo)
background_label.place(relwidth=1, relheight=1)

# Variables
username_var = StringVar()
password_var = StringVar()
role_var = StringVar()
user_role = None
manager_budget = 1000000 
purchased_players = [] 


client = MongoClient("mongodb://localhost:27017/")
db = client['fifa_database']
players_collection = db['players']
users_collection = db['users']


def signup():
    username = username_var.get()
    password = password_var.get()
    role = role_var.get()

    if username and password and role:
        if users_collection.find_one({"username": username}):
            messagebox.showerror("Error", "Username already exists!")
        else:
            hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_data = {"username": username, "password": hashed_pw, "role": role}
            users_collection.insert_one(user_data)
            messagebox.showinfo("Success", f"Sign up successful as {role}!")
            clear_fields()
            show_login()
    else:
        messagebox.showerror("Error", "Please fill all fields")


def login():
    global user_role
    username = username_var.get()
    password = password_var.get()

    if username and password:
        user = users_collection.find_one({"username": username})
        if user:
            if bcrypt.checkpw(password.encode('utf-8'), user['password']):
                user_role = user['role']
                messagebox.showinfo("Success", f"Welcome {username}! You are logged in as {user_role}")
                clear_fields()
                show_dashboard(user_role)
            else:
                messagebox.showerror("Error", "Incorrect password!")
        else:
            messagebox.showerror("Error", "Username not found!")
    else:
        messagebox.showerror("Error", "Please fill all fields")


def clear_fields():
    username_var.set("")
    password_var.set("")
    role_var.set("")


def show_login():
    signup_frame.pack_forget()
    dashboard_frame.pack_forget()
    login_frame.pack()


def show_signup():
    login_frame.pack_forget()
    signup_frame.pack()


def show_dashboard(role):
    login_frame.pack_forget()
    signup_frame.pack_forget()
    dashboard_frame.pack()

    if role == "player":
        player_dashboard()
    elif role == "manager":
        manager_dashboard()
    elif role == "admin":
        admin_dashboard()


def back_to_home():
    dashboard_frame.pack_forget()
    show_login()


def clear_frame():
    for widget in dashboard_frame.winfo_children():
        widget.destroy()

# Player Dashboard - Enter details
def player_dashboard():
    clear_frame()

    Label(dashboard_frame, text="Player Dashboard", font=("Arial", 30), bg="#ffffff", fg="#007BFF").pack(pady=20)

    # Player details form with larger input fields
    Label(dashboard_frame, text="Name", font=("Arial", 18), bg="#ffffff").pack()
    name_entry = Entry(dashboard_frame, font=("Arial", 18), width=30)
    name_entry.pack(pady=10)

    Label(dashboard_frame, text="Goals", font=("Arial", 18), bg="#ffffff").pack()
    goals_entry = Entry(dashboard_frame, font=("Arial", 18), width=30)
    goals_entry.pack(pady=10)

    Label(dashboard_frame, text="Assists", font=("Arial", 18), bg="#ffffff").pack()
    assists_entry = Entry(dashboard_frame, font=("Arial", 18), width=30)
    assists_entry.pack(pady=10)

    Label(dashboard_frame, text="Club", font=("Arial", 18), bg="#ffffff").pack()
    club_entry = Entry(dashboard_frame, font=("Arial", 18), width=30)
    club_entry.pack(pady=10)

    Label(dashboard_frame, text="Country", font=("Arial", 18), bg="#ffffff").pack()
    country_entry = Entry(dashboard_frame, font=("Arial", 18), width=30)
    country_entry.pack(pady=10)

    Label(dashboard_frame, text="Age", font=("Arial", 18), bg="#ffffff").pack()
    age_entry = Entry(dashboard_frame, font=("Arial", 18), width=30)
    age_entry.pack(pady=10)

    Label(dashboard_frame, text="Achievements", font=("Arial", 18), bg="#ffffff").pack()
    achievements_entry = Entry(dashboard_frame, font=("Arial", 18), width=30)
    achievements_entry.pack(pady=10)

    # Submit button with larger font
    Button(dashboard_frame, text="Submit", command=lambda: submit_player_data(
        name_entry.get(),
        goals_entry.get(),
        assists_entry.get(),
        club_entry.get(),
        country_entry.get(),
        age_entry.get(),
        achievements_entry.get()
    ), bg="#28a745", fg="white", font=("Arial", 18), width=15).pack(pady=20)

    Button(dashboard_frame, text="Back", command=back_to_home, bg="#007BFF", fg="white", font=("Arial", 18), width=15).pack(pady=10)

# Function to handle player data submission
def submit_player_data(name, goals, assists, club, country, age, achievements):
    if name and goals and assists and club and country and age and achievements:
        player_data = {
            "name": name,
            "goals": goals,
            "assists": assists,
            "club": club,
            "country": country,
            "age": age,
            "achievements": achievements,
            "price": 0,  # Default price
            "rank": "Unranked"  # Default rank
        }
        players_collection.insert_one(player_data)
        messagebox.showinfo("Success", "Player data submitted successfully!")
        show_player_info(player_data)
    else:
        messagebox.showerror("Error", "Please fill all fields!")

# Show the player's submitted information
def show_player_info(player_data):
    clear_frame()

    Label(dashboard_frame, text="Your Information", font=("Arial", 30), bg="#ffffff").pack(pady=20)

    for key, value in player_data.items():
        Label(dashboard_frame, text=f"{key.capitalize()}: {value}", font=("Arial", 18), bg="#ffffff").pack(pady=5)

    Button(dashboard_frame, text="Back", command=back_to_home, bg="#007BFF", fg="white", font=("Arial", 18), width=15).pack(pady=10)

# Manager Dashboard - Buy players and view purchased players
def manager_dashboard():
    clear_frame()

    Label(dashboard_frame, text="Manager Dashboard", font=("Arial", 30), bg="#ffffff", fg="#28a745").pack(pady=20)
    Label(dashboard_frame, text=f"Budget: ${manager_budget}", font=("Arial", 24), bg="#ffffff").pack(pady=10)

    # Get player details for purchasing
    players = players_collection.find()

    Label(dashboard_frame, text="Select Player to Buy", font=("Arial", 18), bg="#ffffff").pack(pady=20)
    player_listbox = Listbox(dashboard_frame, font=("Arial", 18), width=50, height=10)
    for player in players:
        player_listbox.insert(END, f"{player['name']} - Price: {player.get('price', 'Not Set')}")
    player_listbox.pack(pady=10)

    Button(dashboard_frame, text="Buy Player", command=lambda: buy_player(player_listbox.get(ACTIVE)), bg="#28a745", fg="white", font=("Arial", 18), width=20).pack(pady=10)

    # View Purchased Players button
    Button(dashboard_frame, text="View Purchased Players", command=view_purchased_players, bg="#17a2b8", fg="white", font=("Arial", 18), width=20).pack(pady=10)

    # Show Player Info button
    Button(dashboard_frame, text="Show Player Info", command=lambda: show_selected_player_info(player_listbox.get(ACTIVE)), bg="#007BFF", fg="white", font=("Arial", 18), width=20).pack(pady=10)

    Button(dashboard_frame, text="Back", command=back_to_home, bg="#007BFF", fg="white", font=("Arial", 18), width=15).pack(pady=10)

# Buy player function
def buy_player(player_info):
    global manager_budget, purchased_players
    player_name = player_info.split(" - ")[0]
    player = players_collection.find_one({"name": player_name})

    if player:
        price = player.get('price', 0)
        if manager_budget >= price:
            purchased_players.append(player)
            manager_budget -= price
            messagebox.showinfo("Success", f"You bought {player_name}!")
        else:
            messagebox.showerror("Error", "Not enough budget!")
    else:
        messagebox.showerror("Error", "Player not found!")

# View purchased players
def view_purchased_players():
    clear_frame()
    Label(dashboard_frame, text="Purchased Players", font=("Arial", 30), bg="#ffffff").pack(pady=20)

    if purchased_players:
        for player in purchased_players:
            Label(dashboard_frame, text=f"{player['name']} - Price: {player.get('price', 'Not Set')}", font=("Arial", 18), bg="#ffffff").pack(pady=5)
    else:
        Label(dashboard_frame, text="No players purchased yet!", font=("Arial", 18), bg="#ffffff").pack(pady=5)

    Button(dashboard_frame, text="Back", command=back_to_home, bg="#007BFF", fg="white", font=("Arial", 18), width=15).pack(pady=10)

# Admin Dashboard - View, delete, set price, and set rank for players
def admin_dashboard():
    clear_frame()

    Label(dashboard_frame, text="Admin Dashboard", font=("Arial", 30), bg="#ffffff", fg="#dc3545").pack(pady=20)

    # Display players for admin
    players = players_collection.find()
    
    Label(dashboard_frame, text="Manage Players", font=("Arial", 18), bg="#ffffff").pack(pady=20)
    player_listbox = Listbox(dashboard_frame, font=("Arial", 18), width=50, height=10)
    for player in players:
        player_listbox.insert(END, f"{player['name']} - Price: {player.get('price', 'Not Set')} - Rank: {player.get('rank', 'Unranked')}")

    player_listbox.pack(pady=10)

    Button(dashboard_frame, text="Delete Player", command=lambda: delete_player(player_listbox.get(ACTIVE)), bg="#dc3545", fg="white", font=("Arial", 18), width=20).pack(pady=10)

    # Price and Rank setting
    price_entry = Entry(dashboard_frame, font=("Arial", 18), width=30)
    price_entry.pack(pady=5)
    price_entry.insert(0, "Set Price")

    rank_entry = Entry(dashboard_frame, font=("Arial", 18), width=30)
    rank_entry.pack(pady=5)
    rank_entry.insert(0, "Set Rank")

    Button(dashboard_frame, text="Set Price", command=lambda: set_price(player_listbox.get(ACTIVE), price_entry.get()), bg="#28a745", fg="white", font=("Arial", 18), width=20).pack(pady=10)
    Button(dashboard_frame, text="Set Rank", command=lambda: set_rank(player_listbox.get(ACTIVE), rank_entry.get()), bg="#28a745", fg="white", font=("Arial", 18), width=20).pack(pady=10)

    Button(dashboard_frame, text="Back", command=back_to_home, bg="#007BFF", fg="white", font=("Arial", 18), width=15).pack(pady=10)

# Delete player function
def delete_player(player_info):
    player_name = player_info.split(" - ")[0]
    result = players_collection.delete_one({"name": player_name})

    if result.deleted_count > 0:
        messagebox.showinfo("Success", f"Player {player_name} deleted successfully!")
        admin_dashboard()  # Refresh the admin dashboard
    else:
        messagebox.showerror("Error", "Player not found!")

# Set player price function
def set_price(player_info, price):
    player_name = player_info.split(" - ")[0]
    try:
        price = float(price)
        if price < 0:
            raise ValueError("Price cannot be negative.")

        players_collection.update_one({"name": player_name}, {"$set": {"price": price}})
        messagebox.showinfo("Success", f"Price for {player_name} set to ${price:.2f}!")
    except ValueError as e:
        messagebox.showerror("Error", f"Invalid price: {e}")

# Set player rank function
def set_rank(player_info, rank):
    player_name = player_info.split(" - ")[0]
    if rank:
        players_collection.update_one({"name": player_name}, {"$set": {"rank": rank}})
        messagebox.showinfo("Success", f"Rank for {player_name} set to {rank}!")
    else:
        messagebox.showerror("Error", "Rank cannot be empty!")

# Show player details in a new window
def show_selected_player_info(player_info):
    player_name = player_info.split(" - ")[0]
    player = players_collection.find_one({"name": player_name})

    if player:
        player_info_window = Toplevel(root)
        player_info_window.title(player_name)
        player_info_window.geometry("400x400")

        Label(player_info_window, text="Player Information", font=("Arial", 20)).pack(pady=10)

        for key, value in player.items():
            Label(player_info_window, text=f"{key.capitalize()}: {value}").pack(pady=5)

        Button(player_info_window, text="Close", command=player_info_window.destroy).pack(pady=20)
    else:
        messagebox.showerror("Error", "Player not found!")

# Frames for login and signup
login_frame = Frame(root, bg="#ffffff")
signup_frame = Frame(root, bg="#ffffff")
dashboard_frame = Frame(root, bg="#ffffff")

# Login UI
Label(login_frame, text="Login", font=("Arial", 40), bg="#ffffff").pack(pady=20)
Label(login_frame, text="Username", font=("Arial", 18), bg="#ffffff").pack()
Entry(login_frame, textvariable=username_var, font=("Arial", 18)).pack(pady=10)
Label(login_frame, text="Password", font=("Arial", 18), bg="#ffffff").pack()
Entry(login_frame, textvariable=password_var, font=("Arial", 18), show='*').pack(pady=10)

Button(login_frame, text="Login", command=login, bg="#007BFF", fg="white", font=("Arial", 18), width=15).pack(pady=20)
Button(login_frame, text="Go to Signup", command=show_signup, bg="#28a745", fg="white", font=("Arial", 18), width=15).pack(pady=10)

# Signup UI
Label(signup_frame, text="Signup", font=("Arial", 40), bg="#ffffff").pack(pady=20)
Label(signup_frame, text="Username", font=("Arial", 18), bg="#ffffff").pack()
Entry(signup_frame, textvariable=username_var, font=("Arial", 18)).pack(pady=10)
Label(signup_frame, text="Password", font=("Arial", 18), bg="#ffffff").pack()
Entry(signup_frame, textvariable=password_var, font=("Arial", 18), show='*').pack(pady=10)
Label(signup_frame, text="Role", font=("Arial", 18), bg="#ffffff").pack()
role_dropdown = OptionMenu(signup_frame, role_var, "player", "manager", "admin")
role_dropdown.config(font=("Arial", 18))
role_dropdown.pack(pady=10)

Button(signup_frame, text="Signup", command=signup, bg="#28a745", fg="white", font=("Arial", 18), width=15).pack(pady=20)
Button(signup_frame, text="Back to Login", command=show_login, bg="#007BFF", fg="white", font=("Arial", 18), width=15).pack(pady=10)

# Start with the login interface
show_login()

# Start the application
root.mainloop()

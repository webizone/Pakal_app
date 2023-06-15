from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
    
    # Import additional modules
from flask import request

# Update the registration route
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        # Insert the user data into the database
        conn = sqlite3.connect('travel_agent.db')
        c = conn.cursor()
        c.execute("INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
                  (name, email, password))
        conn.commit()
        conn.close()

        return "Registration successful! You can now <a href='/'>login</a>."

    return render_template('index.html')

# Remove the existing route for the home page
@app.route('/')
def home():
    return render_template('login.html')


# Update the login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        # Check if the user exists in the database
        conn = sqlite3.connect('travel_agent.db')
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE email=? AND password=?",
                  (email, password))
        user = c.fetchone()
        conn.close()

        if user:
            session['user'] = {
                'id': user[0],
                'name': user[1],
                'email': user[2]
            }
            return redirect('/dashboard')

        return "Invalid email or password. <a href='/'>Try again</a>."

    return render_template('index.html')

# Create a route for the dashboard page
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return f"Welcome, {session['user']['name']}! This is your dashboard."
    else:
        return redirect('/')

# Create a route for logout
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/')


# Update the dashboard route to show the profile page
@app.route('/dashboard')
def dashboard():
    if 'user' in session:
        return render_template('profile.html', user=session['user'])
    else:
        return redirect('/')

# Create a route for updating the user profile
@app.route('/update_profile', methods=['POST'])
def update_profile():
    if 'user' in session:
        name = request.form['name']

        # Update the user's name in the database
        conn = sqlite3.connect('travel_agent.db')
        c = conn.cursor()
        c.execute("UPDATE users SET name=? WHERE id=?", (name, session['user']['id']))
        conn.commit()
        conn.close()

        # Update the name in the session
        session['user']['name'] = name

        return redirect('/dashboard')

    return redirect('/')


# Create a route for hotel search
@app.route('/search', methods=['POST'])
def hotel_search():
    if 'user' in session:
        location = request.form['location']

        # Perform hotel search logic
        # This is where you would connect to an API or perform database queries to fetch hotel data based on the location provided

        # For demonstration purposes, let's assume we have a list of hotels
        hotels = [
            {'name': 'Hotel A', 'location': 'Location A'},
            {'name': 'Hotel B', 'location': 'Location B'},
            {'name': 'Hotel C', 'location': 'Location C'}
        ]

        return render_template('hotel_search_results.html', location=location, hotels=hotels)
    else:
        return redirect('/')
    
    
    @app.route('/search', methods=['POST'])
def hotel_search():
    if 'user' in session:
        location = request.form['location']
        # Perform hotel search logic

        # For demonstration purposes, let's assume we have a list of hotels
        hotels = [
            {'name': 'Hotel A', 'location': 'Location A', 'description': 'This is Hotel A'},
            {'name': 'Hotel B', 'location': 'Location B', 'description': 'This is Hotel B'},
            {'name': 'Hotel C', 'location': 'Location C', 'description': 'This is Hotel C'}
        ]

        return render_template('hotel_search_results.html', location=location, hotels=hotels)
    else:
        return redirect('/')
    
    
    @app.route('/hotel/<hotel_name>/book', methods=['GET', 'POST'])
def book_hotel(hotel_name):
    if 'user' in session:
        if request.method == 'POST':
            # Retrieve booking details from the form
            check_in_date = request.form['check_in_date']
            check_out_date = request.form['check_out_date']
            num_guests = request.form['num_guests']

            # Perform booking process logic
            # This is where you would typically store the booking details in a database or connect to a booking API

            return f"Successfully booked {hotel_name} for {num_guests} guests from {check_in_date} to {check_out_date}!"

        return render_template('hotel_booking.html', hotel_name=hotel_name)
    else:
        return redirect('/')
    
    @app.route('/dashboard')
def dashboard():
    if 'user' in session:
        # Retrieve the user's past bookings from the database or any other data source
        # For demonstration purposes, let's assume we have a list of past bookings for the user
        past_bookings = [
            {'hotel': 'Hotel A', 'check_in_date': '2023-06-01', 'check_out_date': '2023-06-03'},
            {'hotel': 'Hotel B', 'check_in_date': '2023-06-05', 'check_out_date': '2023-06-07'}
        ]

        return render_template('dashboard.html', past_bookings=past_bookings)
    else:
        return redirect('/')

    
    
   









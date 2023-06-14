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



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


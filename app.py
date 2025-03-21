from flask import Flask, jsonify, redirect, request, render_template
import mysql.connector

app = Flask(__name__)

# Handle registration form submission
@app.route('/api/register', methods=['POST'])
def register_form():
    data = request.form

    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="raas@2006",
        database="blood_buddy"
    )

    cursor = connection.cursor()

    try:
        query = "INSERT INTO Registration (username, email, password, user_type) VALUES (%s, %s, %s, %s)"
        values = (data['username'], data['email'], data['password'], data['user_type'])
        cursor.execute(query, values)
        connection.commit()

        if int(data['user_type']) == 1:
            return redirect(url_for('index', user_type=1))
        else:
            return redirect(url_for('index2', user_type=2))

    except Exception as e:
        print(f"Error: {e}")
        connection.rollback()
    finally:
        connection.close()

# Home pages based on user type
@app.route('/index/<int:user_type>')
def index(user_type):
    return render_template(f'index{user_type}.html')

@app.route('/index2/<int:user_type>')
def index2(user_type):
    return render_template(f'index2{user_type}.html')

# Add this route to render the Register.html file
@app.route('/Register.html')
def register_html():
    return render_template('Register.html', html_safe=True)

if __name__ == '__main__':
    app.run(debug=True, port=5500)
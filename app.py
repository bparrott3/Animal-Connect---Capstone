from flask import Flask, render_template
from db_conn import get_db_connection
import mysql.connector

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# @app.route('/browse', methods=['GET'])
# def database():
#     db = get_db_connection()
#     if db is not None:
#         cursor = db.cursor()
#         # Example query: SELECT * FROM your_table;
#         cursor.execute("SELECT * FROM Users")
#         rows = cursor.fetchall()
#         cursor.close()
#         db.close()
#         return str(rows)  # Convert the result to a string to display it
#     else:
#         return "Failed to connect to the database."
# def browse_page():
#     return render_template('browse.html')

@app.route('/animal_profiles', methods=['GET'])
def animal_profiles():
    conn = get_db_connection()  # Get database connection
    cursor = conn.cursor(dictionary=True)  # Use dictionary cursor to directly get results as dictionaries
    
    query = "SELECT * FROM Animal_Profiles"
    cursor.execute(query)
    
    profiles = cursor.fetchall()  # Fetch all rows from the query result
    
    cursor.close()
    conn.close()
    
    return render_template('animal_profiles.html', profiles=profiles)

@app.route('/insert_animal_profiles', methods=['GET', 'POST'])
def insert_animal_profiles():
    connection = get_db_connection()
    cursor = connection.cursor()
    
    query = """
    INSERT INTO Animal_Profiles (type, breed, disposition, image, description) VALUES
        ('Dog', 'Golden Retriever', 'Good with children', 'https://shorturl.at/itRT7', 'Friendly and devoted, great for families.'),
        ('Cat', 'Siamese', 'Good with other animals', 'https://example.com/images/cat1.jpg', 'Energetic and playful, enjoys companionship.'),
        ('Dog', 'Beagle', 'Animal must be leashed at all times', 'https://example.com/images/dog2.jpg', 'Curious and merry, possesses a keen sense of smell.'),
        ('Cat', 'Persian', 'Good with children', 'https://example.com/images/cat2.jpg', 'Calm and affectionate, loves to be pampered.'),
        ('Dog', 'Border Collie', 'Good with other animals', 'https://example.com/images/dog3.jpg', 'Intelligent and energetic, needs lots of exercise.'),
        ('Cat', 'Maine Coon', 'Good with children', 'https://example.com/images/cat3.jpg', 'Gentle giant, friendly and playful.'),
        ('Dog', 'French Bulldog', 'Good with other animals', 'https://example.com/images/dog4.jpg', 'Adaptable and playful, makes a great companion.'),
        ('Other', 'Rabbit', 'Good with children', 'https://example.com/images/rabbit1.jpg', 'Quiet and affectionate, requires gentle handling.'),
        ('Dog', 'Labrador Retriever', 'Good with children', 'https://example.com/images/dog5.jpg', 'Friendly and outgoing, great for active families.'),
        ('Cat', 'Bengal', 'Animal must be leashed at all times', 'https://example.com/images/cat4.jpg', 'Energetic and requires plenty of playtime.');

    """
    
    try:
        cursor.execute(query)
        connection.commit()
        return "Animal profiles inserted successfully."
    except mysql.connector.Error as err:
        return f"Failed to insert animal profiles: {err}"
    finally:
        cursor.close()
        connection.close()


if __name__ == '__main__':
    app.run(debug=True)

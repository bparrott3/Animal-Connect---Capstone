from flask import Flask, render_template, request, redirect, url_for
from db_conn import get_db_connection
import mysql.connector

app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# @app.route('/shelter', methods=['GET'])
# def shelter():
#     return render_template('shelter.html')

@app.route('/shelter/<int:shelter_id>', methods=['GET'])
def shelter(shelter_id):
    # You can now use shelter_id to fetch data specific to this shelter from your database
    # For example:
    conn = get_db_connection()
    
    # Assuming conn is your MySQL connection object and shelter_id is defined
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries
    query = 'SELECT * FROM Shelters WHERE id = %s'
    cursor.execute(query, (shelter_id,))
    # Fetch one result
    shelter_data = cursor.fetchone()
    cursor.close()
    
    # Assuming conn is your MySQL connection object and shelter_id is defined
    cursor = conn.cursor(dictionary=True)  # Use dictionary=True to get results as dictionaries
    pet_id = shelter_data['profile_id']
    query = 'SELECT * FROM Animal_Profiles WHERE shelter_id = %s'
    cursor.execute(query, (shelter_id,))
    # Fetch all results
    pet_profiles = cursor.fetchall()
    cursor.close()

    conn.close()

    # Assuming shelter_data is a dictionary with the shelter's information, you can pass it to the template
    return render_template('shelter.html', shelter_data=shelter_data, pet_profiles=pet_profiles)
    # If you have data to pass to the template, use: return render_template('shelter.html', shelter_data=shelter_data)

@app.route('/<int:shelter_id>/add_profile.html', methods=['GET'])
def add_profile(shelter_id):
    return render_template('add_profile.html', shelter_id=shelter_id)

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

# @app.route('/insert_animal_profiles', methods=['GET', 'POST'])
# def insert_animal_profiles():
#     connection = get_db_connection()
#     cursor = connection.cursor()
    
#     query = """
#     INSERT INTO Animal_Profiles (type, breed, disposition, image, description) VALUES
#         ('Dog', 'Golden Retriever', 'Good with children', 'https://shorturl.at/itRT7', 'Friendly and devoted, great for families.'),
#         ('Cat', 'Siamese', 'Good with other animals', 'https://example.com/images/cat1.jpg', 'Energetic and playful, enjoys companionship.'),
#         ('Dog', 'Beagle', 'Animal must be leashed at all times', 'https://example.com/images/dog2.jpg', 'Curious and merry, possesses a keen sense of smell.'),
#         ('Cat', 'Persian', 'Good with children', 'https://example.com/images/cat2.jpg', 'Calm and affectionate, loves to be pampered.'),
#         ('Dog', 'Border Collie', 'Good with other animals', 'https://example.com/images/dog3.jpg', 'Intelligent and energetic, needs lots of exercise.'),
#         ('Cat', 'Maine Coon', 'Good with children', 'https://example.com/images/cat3.jpg', 'Gentle giant, friendly and playful.'),
#         ('Dog', 'French Bulldog', 'Good with other animals', 'https://example.com/images/dog4.jpg', 'Adaptable and playful, makes a great companion.'),
#         ('Other', 'Rabbit', 'Good with children', 'https://example.com/images/rabbit1.jpg', 'Quiet and affectionate, requires gentle handling.'),
#         ('Dog', 'Labrador Retriever', 'Good with children', 'https://example.com/images/dog5.jpg', 'Friendly and outgoing, great for active families.'),
#         ('Cat', 'Bengal', 'Animal must be leashed at all times', 'https://example.com/images/cat4.jpg', 'Energetic and requires plenty of playtime.');

#     """
    
#     try:
#         cursor.execute(query)
#         connection.commit()
#         return "Animal profiles inserted successfully."
#     except mysql.connector.Error as err:
#         return f"Failed to insert animal profiles: {err}"
#     finally:
#         cursor.close()
#         connection.close()

@app.route('/insert_animal_profiles', methods=['POST', 'GET'])
def insert_animal_profile():
    # Get form data
    shelter_id = request.form['shelter_id']
    animal_type = request.form['type']
    breed = request.form['breed']
    disposition = request.form.getlist('disposition')  # Assuming disposition is a list of checkboxes
    availability = request.form['availability']
    description = request.form['description']
    image_url = request.form['image']
    
    # Convert disposition list to a string if needed
    disposition_str = ', '.join(disposition)

    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # SQL Insert Query
    insert_query = '''
        INSERT INTO Animal_Profiles (shelter_id, type, breed, disposition, availability, description, image)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    '''
    cursor.execute(insert_query, (shelter_id, animal_type, breed, disposition_str, availability, description, image_url))
        
    # Commit the transaction
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()
    
    # Redirect or respond as needed, e.g., back to the profiles page or a success message
    return redirect(url_for('shelter', shelter_id = shelter_id))  # Adjust the redirection as per your app's flow

# Ensure you have a function or route for 'some_function_name' to redirect to, or adjust as needed.


if __name__ == '__main__':
    app.run(debug=True)

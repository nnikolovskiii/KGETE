import mysql.connector
import random

def generate_light_hex_colors(num_colors=300):
    colors = set()  # Use a set to store unique colors

    while len(colors) < num_colors:
        # Generate light tones by keeping the RGB values higher
        red = random.randint(180, 255)
        green = random.randint(180, 255)
        blue = random.randint(180, 255)

        # Convert to hex and format as #RRGGBB
        hex_color = f'#{red:02X}{green:02X}{blue:02X}'

        # Add the color to the set (automatically handles uniqueness)
        colors.add(hex_color)

    return list(colors)  # Convert the set to a list for indexing


# Database connection details
db_config = {
    'user': 'admin',
    'password': 'ogan123',
    'host': '127.0.0.1',
    'port': 3308,
    'database': 'finki_rasporedi',
}

# Establishing the connection
conn = mysql.connector.connect(**db_config)

# Creating a cursor object
cursor = conn.cursor()

# Query to select all entities from the lectures table
query = "SELECT * FROM subjects"

# Executing the query
cursor.execute(query)

# Fetching all rows from the lectures table
lectures = cursor.fetchall()

# Generate light hex colors equal to the number of lectures
hex_colors = generate_light_hex_colors(len(lectures))

# Update the HexColor column for each lecture
for i, lecture in enumerate(lectures):
    lecture_id = lecture[0]  # Assuming the first column is the lecture ID
    update_query = "UPDATE subjects SET HexColor = %s WHERE id = %s"
    cursor.execute(update_query, (hex_colors[i], lecture_id))

# Commit the changes to the database
conn.commit()

# Closing the cursor and connection
cursor.close()
conn.close()

print("HexColor column updated successfully.")

RGB Color Dataset with Nearest Named Colors
📂 Overview
This project generates a dataset of RGB values (Red, Green, Blue) and maps each RGB color to its closest named color based on the CSS3 color names.

The dataset is saved as a .csv file and includes:

R – Red component (0–255)

G – Green component (0–255)

B – Blue component (0–255)

NearestColor – Closest named color (e.g., skyblue, red, darkgreen)

⚙️ Requirements
Python 3.6 or higher

webcolors library

Install dependencies:

bash
Copy
Edit
pip install webcolors
🧪 Sample Dataset
If you don't need all 16 million color combinations, you can generate a smaller dataset using a step size (e.g., every 32nd value). This produces a file with 512 color entries.

🖥️ How to Generate the Dataset
🔹 Step 1: Create a Python File
Save the following code as generate_rgb_named_dataset.py:

python
Copy
Edit
import webcolors
import csv

def closest_color(requested_color):
    min_distance = float('inf')
    closest_name = None
    for name, hex_val in webcolors.CSS3_NAMES_TO_HEX.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(hex_val)
        distance = (r_c - requested_color[0]) ** 2 + (g_c - requested_color[1]) ** 2 + (b_c - requested_color[2]) ** 2
        if distance < min_distance:
            min_distance = distance
            closest_name = name
    return closest_name

# Change `step = 1` for full dataset (16M rows) or increase for smaller file
step = 32
output_file = 'rgb_named_dataset.csv'

with open(output_file, 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['R', 'G', 'B', 'NearestColor'])
    for r in range(0, 256, step):
        for g in range(0, 256, step):
            for b in range(0, 256, step):
                name = closest_color((r, g, b))
                writer.writerow([r, g, b, name])
🔹 Step 2: Run the Script
In the terminal, run:

bash
Copy
Edit
python generate_rgb_named_dataset.py
This will create a file named rgb_named_dataset.csv in the same directory.

📊 Sample Output (CSV)
python-repl
Copy
Edit
R,G,B,NearestColor
0,0,0,black
0,0,32,navy
0,0,64,navy
...
💡 Notes
Full dataset with step = 1 will have 16,777,216 rows and take a long time to generate.

The nearest color is computed by comparing Euclidean distance in RGB space to known CSS3 colors.

📄 License
This dataset and script are free to use for personal or educational purposes. Attribution is appreciated but not required.


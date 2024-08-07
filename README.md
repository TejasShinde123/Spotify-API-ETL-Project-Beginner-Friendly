# Spotify-API-ETL-Project-Beginner-Friendly
Project Description: ETL Pipeline for Spotify Data using Apache Spark This project involves building an ETL (Extract, Transform, Load) pipeline to process song data obtained from the Spotify API using Apache Spark. This ETL pipeline facilitates the efficient extraction, transformation, and loading of Spotify song data, leveraging Apache Spark
Merge JSON Files from Folder

Overview

This script merges multiple JSON files from a specified folder into a single DataFrame, performs transformations, and saves the result as a cleaned JSON file.

Requirements

- Python 3.x
- PySpark 3.x
- JSON files in the specified folder

Usage

1. Update the folder_path variable with the path to your JSON files.
2. Run the script using python (link unavailable).
3. The cleaned JSON file will be saved to the specified output_path.

Script Explanation

1. Initializes a Spark session.
2. Defines the directory containing JSON files.
3. Gets a list of all JSON files in the directory.
4. Reads and merges JSON files into a single DataFrame.
5. Performs transformations to select and rename columns.
6. Creates a temporary view for SQL queries.
7. Runs a SQL SELECT query to get the song_name column.
8. Shows the result of the SQL SELECT query.
9. Collects the DataFrame as a list of dictionaries.
10. Converts the list of dictionaries to JSON format.
11. Saves the JSON data to a file.
12. Stops the Spark session.
13. Manually cleans up Spark temporary directories.

Note

- Make sure to update the folder_path and output_path variables with your actual file paths.
- This script assumes that the JSON files have a consistent structure. If the structure varies, you 

import os
import shutil
from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import json

# Initialize Spark session
spark = SparkSession.builder \
    .appName("Merge JSON Files from Folder") \
    .getOrCreate()

# Define the directory containing JSON files
folder_path = r"/your_actual_path/artist_songs"
# Get list of all JSON files in the directory
file_paths = [os.path.join(folder_path, file) for file in os.listdir(folder_path) if file.endswith('.json')]

# Read and merge JSON files into a single DataFrame
dfs = [spark.read \
            .option("inferSchema", "true") \
            .option("multiLine", "true") \
            .json(file_path) for file_path in file_paths]

# Union all DataFrames
df = dfs[0]
for other_df in dfs[1:]:
    df = df.union(other_df)

# Perform any necessary transformations
df_name = df.select(
    col("name").alias("song_name"),
    col("album.name").alias("album_name"),
    col("id").alias("song_id"),
    col("popularity"),
    col("type"),
    col("uri"),
    col("album.release_date").alias("album_release_date"),
    col("album.release_date_precision").alias("album_release_date_precision"),
    col("album.artists.name").alias("artist_names"),
    col("album.artists.type").alias("artist_type"),
    col("album.artists.id").alias("artist_ids")
)

# Create a temporary view for SQL queries
df_name.createOrReplaceTempView("merged_songs_view")

# Run a SQL SELECT query to get only the song_name column
result_df = spark.sql("SELECT * FROM merged_songs_view")

# Show the result of the SQL SELECT query
result_df.show(n=100, truncate=False)


# Collect DataFrame as a list of dictionaries
data = result_df.collect()

data_list = [row.asDict() for row in data]

# Convert list of dictionaries to JSON format
json_data = json.dumps(data_list, indent=4)

# Save JSON data to a file
output_path = r"/your_actual_path/artist_songs"
with open(output_path, 'w') as file:
    file.write(json_data)

# Stop the Spark session
spark.stop()

# Manually clean up Spark temporary directories
temp_dir = r"/your_actual_path/artist_songs"
if os.path.exists(temp_dir):
    try:
        shutil.rmtree(temp_dir)
    except Exception as e:
        print(f"Error while deleting Spark temp dir: {e}")

import streamlit as st
import sqlite3
from googleapiclient.discovery import build
import pandas as pd
import isodate

# Function to create tables
def create_tables(conn):
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Channel (
            Channel_Id TEXT PRIMARY KEY,
            Channel_Name TEXT,
            Subscription_Count INTEGER,
            Channel_Views INTEGER,
            Channel_Description TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Video (
            Video_Id TEXT PRIMARY KEY,
            Video_Name TEXT,
            Channel_Id TEXT,
            Published_At TEXT,
            View_Count INTEGER,
            Like_Count INTEGER,
            Dislike_Count INTEGER,
            Comment_Count INTEGER,
            Duration TEXT,
            FOREIGN KEY(Channel_Id) REFERENCES Channel(Channel_Id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Comment (
            Comment_Id TEXT PRIMARY KEY,
            Video_Id TEXT,
            Comment_Text TEXT,
            Author_Name TEXT,
            Published_At TEXT,
            FOREIGN KEY(Video_Id) REFERENCES Video(Video_Id)
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Playlist (
            Playlist_Id TEXT PRIMARY KEY,
            Channel_Id TEXT,
            Playlist_Name TEXT,
            Video_Count INTEGER,
            FOREIGN KEY(Channel_Id) REFERENCES Channel(Channel_Id)
        )
    """)
    conn.commit()

# Function to insert channel data
def insert_channel_data(conn, channel_data):
    cursor = conn.cursor()
    cursor.execute("""
        INSERT OR REPLACE INTO Channel (Channel_Id, Channel_Name, Subscription_Count, Channel_Views, Channel_Description)
        VALUES (?, ?, ?, ?, ?)
    """, (channel_data['Channel_Id'], channel_data['Channel_Name'], channel_data['Subscription_Count'], channel_data['Channel_Views'], channel_data['Channel_Description']))
    conn.commit()

# Function to insert videos data
def insert_videos_data(conn, videos):
    cursor = conn.cursor()
    for video in videos:
        cursor.execute("""
            INSERT OR REPLACE INTO Video (Video_Id, Video_Name, Channel_Id, Published_At, View_Count, Like_Count, Dislike_Count, Comment_Count, Duration)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (video['Video_Id'], video['Video_Name'], video['Channel_Id'], video['Published_At'], video['View_Count'], video['Like_Count'], video['Dislike_Count'], video['Comment_Count'], video['Duration']))
    conn.commit()

# Function to insert comments data
def insert_comments_data(conn, comments):
    cursor = conn.cursor()
    for comment in comments:
        cursor.execute("""
            INSERT OR REPLACE INTO Comment (Comment_Id, Video_Id, Comment_Text, Author_Name, Published_At)
            VALUES (?, ?, ?, ?, ?)
        """, (comment['Comment_Id'], comment['Video_Id'], comment['Comment_Text'], comment['Author_Name'], comment['Published_At']))
    conn.commit()

# Function to insert playlists data
def insert_playlists_data(conn, playlists):
    cursor = conn.cursor()
    for playlist in playlists:
        cursor.execute("""
            INSERT OR REPLACE INTO Playlist (Playlist_Id, Channel_Id, Playlist_Name, Video_Count)
            VALUES (?, ?, ?, ?)
        """, (playlist['Playlist_Id'], playlist['Channel_Id'], playlist['Playlist_Name'], playlist['Video_Count']))
    conn.commit()

# Function to fetch channel data from YouTube API
def fetch_channel_data(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.channels().list(
        part="snippet,statistics",
        id=channel_id
    )
    response = request.execute()

    if 'items' in response and len(response['items']) > 0:
        item = response['items'][0]
        channel_data = {
            'Channel_Id': item['id'],
            'Channel_Name': item['snippet']['title'],
            'Subscription_Count': item['statistics'].get('subscriberCount', 0),
            'Channel_Views': item['statistics'].get('viewCount', 0),
            'Channel_Description': item['snippet'].get('description', ''),
        }
        return channel_data
    else:
        st.error("Channel not found.")
        return None

# Function to fetch videos data from YouTube API
def fetch_videos_data(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    videos = []

    next_page_token = None
    while True:
        request = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            type="video",
            maxResults=50,  # Maximum allowed value for maxResults
            pageToken=next_page_token
        )
        response = request.execute()

        if 'items' in response:
            for item in response['items']:
                video_id = item['id']['videoId']
                video_details = youtube.videos().list(
                    part="snippet,statistics,contentDetails",
                    id=video_id
                ).execute()

                video_data = video_details['items'][0]
                videos.append({
                    'Video_Id': video_data['id'],
                    'Video_Name': video_data['snippet']['title'],
                    'Channel_Id': video_data['snippet']['channelId'],
                    'Published_At': video_data['snippet']['publishedAt'],
                    'View_Count': video_data['statistics'].get('viewCount', 0),
                    'Like_Count': video_data['statistics'].get('likeCount', 0),
                    'Dislike_Count': video_data['statistics'].get('dislikeCount', 0),
                    'Comment_Count': video_data['statistics'].get('commentCount', 0),
                    'Duration': video_data['contentDetails']['duration'],
                })

        # Get the next page token
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break  # Exit the loop if there are no more pages

    return videos


# Function to fetch comments data for a video from YouTube API
def fetch_comments_data(video_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    comments = []

    next_page_token = None
    while True:
        request = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            maxResults=100,  # Maximum allowed value for maxResults in comments
            pageToken=next_page_token
        )
        response = request.execute()

        if 'items' in response:
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']
                comments.append({
                    'Comment_Id': item['id'],
                    'Video_Id': video_id,
                    'Comment_Text': comment['textDisplay'],
                    'Author_Name': comment['authorDisplayName'],
                    'Published_At': comment['publishedAt']
                })

        # Get the next page token
        next_page_token = response.get('nextPageToken')
        if not next_page_token:
            break  # Exit the loop if there are no more pages

    return comments

# Function to fetch playlists data from YouTube API
def fetch_playlists_data(channel_id, api_key):
    youtube = build('youtube', 'v3', developerKey=api_key)
    request = youtube.playlists().list(
        part="snippet,contentDetails",
        channelId=channel_id
    )
    response = request.execute()
    playlists = []

    if 'items' in response:
        for item in response['items']:
            playlists.append({
                'Playlist_Id': item['id'],
                'Channel_Id': item['snippet']['channelId'],
                'Playlist_Name': item['snippet']['title'],
                'Video_Count': item['contentDetails']['itemCount'],
            })

    return playlists

# Function to get channel names from the database
def get_channel_names(conn):
    cursor = conn.cursor()
    cursor.execute("SELECT Channel_Name FROM Channel")
    return [row[0] for row in cursor.fetchall()]

# Function to query videos and channels from SQLite database
def query_videos_and_channels(conn, query_type):
    cursor = conn.cursor()
    queries = {
        1: """
            SELECT Video.Video_Name, Channel.Channel_Name
            FROM Video
            INNER JOIN Channel ON Video.Channel_Id = Channel.Channel_Id;
        """,
        2: """
            SELECT Channel.Channel_Name, COUNT(Video.Video_Id) AS Number_of_Videos
            FROM Video
            INNER JOIN Channel ON Video.Channel_Id = Channel.Channel_Id
            GROUP BY Channel.Channel_Id
            ORDER BY COUNT(Video.Video_Id) DESC;
        """,
        3: """
            SELECT Video.Video_Name, Channel.Channel_Name, Video.View_Count
            FROM Video
            INNER JOIN Channel ON Video.Channel_Id = Channel.Channel_Id
            ORDER BY Video.View_Count DESC
            LIMIT 10;
        """,
        4: """
            SELECT Video.Video_Name, COUNT(Comment.Comment_Id)
            FROM Video
            LEFT JOIN Comment ON Video.Video_Id = Comment.Video_Id
            GROUP BY Video.Video_Id
            ORDER BY COUNT(Comment.Comment_Id) DESC;
        """,
        5: """
            SELECT Video.Video_Name, Channel.Channel_Name, Video.Like_Count
            FROM Video
            INNER JOIN Channel ON Video.Channel_Id = Channel.Channel_Id
            ORDER BY Video.Like_Count DESC;
        """,
        6: """
            SELECT Video.Video_Name, Video.Like_Count, Video.Dislike_Count
            FROM Video;
        """,
        7: """
            SELECT Channel.Channel_Name, SUM(Video.View_Count)
            FROM Video
            INNER JOIN Channel ON Video.Channel_Id = Channel.Channel_Id
            GROUP BY Channel.Channel_Id;
        """,
        8: """
            SELECT Channel.Channel_Name, COUNT(Video.Video_Id)
            FROM Video
            INNER JOIN Channel ON Video.Channel_Id = Channel.Channel_Id
            WHERE strftime('%Y', Video.Published_At) = '2022'
            GROUP BY Channel.Channel_Name;
        """,
        9: """
            SELECT Channel.Channel_Name, AVG(
                COALESCE(
                    (CAST(SUBSTR(Video.Duration, INSTR(Video.Duration, 'H') - 1, 1) AS INTEGER)), 0) * 3600 +  -- Hours to seconds
                COALESCE(
                    (CAST(SUBSTR(Video.Duration, INSTR(Video.Duration, 'M') - 1, 1) AS INTEGER)), 0) * 60 +    -- Minutes to seconds
                COALESCE(
                    (CAST(SUBSTR(Video.Duration, INSTR(Video.Duration, 'S') - 1, 1) AS INTEGER)), 0)           -- Seconds
            ) AS "Avg Duration"
            FROM Video
            INNER JOIN Channel ON Video.Channel_Id = Channel.Channel_Id
            GROUP BY Channel.Channel_Name;
        """,
        10: """
            SELECT Video.Video_Name, Channel.Channel_Name, Video.Comment_Count
            FROM Video
            INNER JOIN Channel ON Video.Channel_Id = Channel.Channel_Id
            ORDER BY Video.Comment_Count DESC
            LIMIT 1;
        """
    }

    cursor.execute(queries[query_type])
    return cursor.fetchall()

# Function to fetch channel ID from the database using channel name
def fetch_channel_id_from_name(conn, channel_name):
    cursor = conn.cursor()
    cursor.execute("SELECT Channel_Id FROM Channel WHERE Channel_Name = ?", (channel_name,))
    result = cursor.fetchone()
    return result[0] if result else None

def parse_duration(duration):
    """Parse ISO 8601 duration format to total seconds."""
    parsed_duration = isodate.parse_duration(duration)
    return int(parsed_duration.total_seconds())

# Function to automatically update database with new videos
def update_database_with_new_videos(conn, api_key):
    cursor = conn.cursor()

    # Get all channel IDs from the database
    cursor.execute("SELECT Channel_Id FROM Channel")
    channel_ids = [row[0] for row in cursor.fetchall()]

    for channel_id in channel_ids:
        # Fetch current videos for the channel
        existing_videos = set()
        cursor.execute("SELECT Video_Id FROM Video WHERE Channel_Id = ?", (channel_id,))
        existing_videos.update(row[0] for row in cursor.fetchall())

        # Fetch new videos from YouTube API
        new_videos = fetch_videos_data(channel_id, api_key)
        new_video_ids = set(video['Video_Id'] for video in new_videos)

        # Identify newly uploaded videos
        newly_uploaded_videos = new_video_ids - existing_videos
        if newly_uploaded_videos:
            # Insert new videos and their comments into the database
            for video in new_videos:
                if video['Video_Id'] in newly_uploaded_videos:
                    insert_videos_data(conn, [video])

                    comments = fetch_comments_data(video['Video_Id'], api_key)
                    insert_comments_data(conn, comments)

    conn.commit()

# Main Streamlit Application
def main():
    st.set_page_config(page_title="YouTube Data Harvesting and Warehousing", page_icon="📹", layout="wide")

    # Create or connect to SQLite database
    db_path = 'channel_database.db'
    conn = sqlite3.connect(db_path, check_same_thread=False)
    create_tables(conn)

    # Initialize session_state to store channel names and fetched channel data
    if 'channel_names' not in st.session_state:
        st.session_state.channel_names = get_channel_names(conn)
    if 'fetched_channel_data' not in st.session_state:
        st.session_state.fetched_channel_data = {}

    api_key = "AIzaSyDvmMKdabwHSyOBJPCDwIg8BOxtXvhP_zk"

    if 'database_updated' not in st.session_state:
        # Run the update function if it hasn't been run yet
        update_database_with_new_videos(conn, api_key)
        st.session_state.database_updated = True

    # Sidebar for navigation
    page = st.sidebar.radio("", ["Data Harvesting", "Data Warehousing", "Query Data"])

    # Page 1: Data Harvesting
    if page == "Data Harvesting":
        st.header(':red[Data Harvesting]', divider='red')

        user_input_ID = st.text_input("Enter the Channel ID")
        if user_input_ID and st.button("SCRAP"):
            # Fetch channel data from YouTube API
            channel_data = fetch_channel_data(user_input_ID, api_key)
            if channel_data:
                # Store fetched data in session state
                st.session_state.fetched_channel_data[channel_data['Channel_Name']] = channel_data

                # Display channel details
                st.write("**Channel Name:**", channel_data['Channel_Name'])
                st.write("**Channel ID:**", channel_data['Channel_Id'])
                st.write("**Subscription Count:**", channel_data['Subscription_Count'])
                st.write("**Channel Views:**", channel_data['Channel_Views'])
                st.write("**Channel Description:**", channel_data['Channel_Description'])

                # Add the channel name to the list for the second page
                if channel_data['Channel_Name'] not in st.session_state.channel_names:
                    st.session_state.channel_names.append(channel_data['Channel_Name'])

                st.success("Channel Data Fetched Successfully!")

    # Page 2: Data Warehousing
    elif page == "Data Warehousing":
        st.header(':red[Data Warehousing]', divider='red')

        if st.session_state.channel_names:
            selected_channel = st.selectbox("Select a Channel Name", st.session_state.channel_names)
        
            if st.button("TO SQL"):
                # Check if channel data is available in session state
                if selected_channel in st.session_state.fetched_channel_data:
                    channel_data = st.session_state.fetched_channel_data[selected_channel]

                    cursor = conn.cursor()
                    cursor.execute("SELECT * FROM Channel WHERE Channel_Id = ?", (channel_data['Channel_Id'],))
                    if cursor.fetchone():
                        st.warning("Data Already Exists in SQL")
                    else:
                        insert_channel_data(conn, channel_data)

                        videos = fetch_videos_data(channel_data['Channel_Id'], api_key)
                        insert_videos_data(conn, videos)

                        for video in videos:
                            comments = fetch_comments_data(video['Video_Id'], api_key)
                            insert_comments_data(conn, comments)

                        playlists = fetch_playlists_data(channel_data['Channel_Id'], api_key)
                        insert_playlists_data(conn, playlists)

                        st.success(f"Data inserted in SQL")
                else:
                    st.warning(f"Channel {selected_channel} data is not available in session or missing channel ID.")

        else:
            selected_channel = st.selectbox("Select a Channel Name", [""])

    # Page 3: Query Data
    elif page == "Query Data":
        st.header(':red[Query Data]', divider='red')

        query_type = st.selectbox("Select any Question", [
            "1. What are the names of all the videos and their corresponding channels?",
            "2. Which channels have the most number of videos, and how many videos do they have?",
            "3. What are the top 10 most viewed videos and their respective channels?",
            "4. How many comments were made on each video, and what are their corresponding video names?",
            "5. Which videos have the highest number of likes, and what are their corresponding channel names?",
            "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?",
            "7. What is the total number of views for each channel, and what are their corresponding channel names?",
            "8. What are the names of all the channels that have published videos in the year 2022?",
            "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?",
            "10. Which videos have the highest number of comments, and what are their corresponding channel names?"
        ])

        query_map = {
        "1. What are the names of all the videos and their corresponding channels?": {
            'headers': ["Video Title", "Channel Name"],
            'query_type': 1
        },
        "2. Which channels have the most number of videos, and how many videos do they have?": {
            'headers': ["Channel Name", "Video Count"],
            'query_type': 2
        },
        "3. What are the top 10 most viewed videos and their respective channels?": {
            'headers': ["Video Title", "Channel Name", "View Count"],
            'query_type': 3
        },
        "4. How many comments were made on each video, and what are their corresponding video names?": {
            'headers': ["Video Title", "Comment Count"],
            'query_type': 4
        },
        "5. Which videos have the highest number of likes, and what are their corresponding channel names?": {
            'headers': ["Video Title", "Channel Name", "Like Count"],
            'query_type': 5
        },
        "6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?": {
            'headers': ["Video Title", "Like Count", "Dislike Count"],
            'query_type': 6
        },
        "7. What is the total number of views for each channel, and what are their corresponding channel names?": {
            'headers': ["Channel Name", "View Count"],
            'query_type': 7
        },
        "8. What are the names of all the channels that have published videos in the year 2022?": {
            'headers': ["Channel Name", "Video Count"],
            'query_type': 8
        },
        "9. What is the average duration of all videos in each channel, and what are their corresponding channel names?": {
            'headers': ["Channel Name", "Avg Duration"],
            'query_type': 9
        },
        "10. Which videos have the highest number of comments, and what are their corresponding channel names?": {
            'headers': ["Video Title", "Channel Name", "Comment Count"],
            'query_type': 10
        }
        }

        selected_query = query_map.get(query_type)
        if selected_query:
            result = query_videos_and_channels(conn, selected_query['query_type'])
            if result:
                st.table(pd.DataFrame(result, columns=selected_query['headers']))

if __name__ == "__main__":
    main()

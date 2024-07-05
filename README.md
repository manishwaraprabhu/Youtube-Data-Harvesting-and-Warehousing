# Youtube-Data-Harvesting-and-Warehousing
This project aims to develop a user-friendly Streamlit application that utilizes the Youtube Data API to extract information on a YouTube channel, stores it in an SQL database. It provides a streamlined process for data harvesting and warehousing, leveraging a user-friendly Streamlit interface.
I have installed VSCode to start the project and installed necessary packages and created a new environment to work on this project.
To begin, I have taken reference from a session conducted by GUVI. So I have started extracting a Youtube Channel's data like it's Channel Name, Subscribers Count, View Count, Channel Description, and the Playlist ID from what I have learned from the session.
Following that, I have retrieved the information of a video like Video Name, Video Description, Tags, PublishedAt, View Count, Like Count, Dislike Count, Favorite Count, Comment Count, Thumbnail, Duration and Caption Status. And Comment data like Comment ID, Comment Text, Comment Author and the Comment Published At. Similarly, Playlist Name and Playlist ID.
Now, I have created a SQL database named "channel_database.db".
I have created four tables named Channel, Video, Comment, and Playlist with necessary parameters using four separate sql files and integrated all the tables in my SQL database.
I have executed four seperate codes to fill the tables in my SQL database to check if all the parameters in all the tables are filled after I extract the data.
Now that I have tested if the parameters in all my SQL tables are filled as my API Key works fine to extract data and store it in the database, I have moved on to the main streamlit application code.
I have understood how the API Key works and all my tables in my database are well interlinked and well structured, I have started coding and built the streamlit application successfully matching all my project requirements.
So, the project required building a streamlit 

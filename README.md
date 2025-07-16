# 📺 YouTube Data Harvesting and Warehousing using SQL and Streamlit

This project is a full-stack Streamlit web application that utilizes the **YouTube Data API v3** to extract, warehouse, and analyze information from YouTube channels. The project showcases an end-to-end data pipeline—from data harvesting to querying—implemented using **Python**, **Streamlit**, and **SQL (SQLite/MySQL/PostgreSQL)**.

It provides a seamless and interactive UI for users to input a YouTube Channel ID, extract all relevant metadata and analytics, store the data into a structured SQL database, and perform complex SQL queries with visual output—all within a single dashboard.

---

## ✅ Key Features

- 📥 Input a YouTube **Channel ID** and retrieve:
  - Channel metadata (name, subscribers, views, description, etc.)
  - Video details (title, description, likes, comments, duration, etc.)
  - Comment data for each video
  - Playlist data

- 🗃️ Store extracted data from up to **10 different YouTube channels** in a local data lake

- 💾 Insert channel data into a **SQL database** (MySQL or PostgreSQL compatible)

- 📊 Perform **10 predefined SQL queries** to retrieve insights from stored data

- 🌐 Built with **Streamlit** and organized across three pages:
  - **Data Harvesting**
  - **Data Warehousing**
  - **Query Data**

---

## 🛠️ Tools & Technologies Used

- Python
- Streamlit
- YouTube Data API v3
- SQLite / MySQL / PostgreSQL
- SQLAlchemy
- Pandas
- DB Browser (SQLite)

---

## 🧠 Problem Statement

The goal of this project is to build an intuitive Streamlit app that allows users to:
1. Fetch channel-level and video-level data from YouTube using its Data API.
2. Store the extracted data into a structured SQL database.
3. Perform analytical SQL queries to gain insights from the data.
4. Display the results interactively within the Streamlit interface.

---

## 🧩 Project Approach

1. **Environment Setup**:  
   Created a virtual environment in VSCode and installed the necessary packages.

2. **YouTube Data Extraction**:  
   Using the YouTube Data API and Python, extracted key metadata from a channel including:
   - Channel Info
   - Video Details (IDs, names, stats)
   - Comments for each video
   - Playlists

3. **SQL Database Design**:  
   - Designed a normalized database schema using four tables: `Channel`, `Video`, `Comment`, and `Playlist`.
   - Created these tables using `.sql` files.
   - Used SQLite to test data storage and structure.

4. **Data Insertion & Testing**:  
   - Executed separate Python scripts to fill each table.
   - Verified all entries using DB Browser (SQLite) to ensure data consistency.

5. **Streamlit Application Development**:  
   Developed a 3-page Streamlit app:
   - **Data Harvesting**: Enter a Channel ID → click `SCRAP` → fetch and display channel data.
   - **Data Warehousing**: Select a channel name from a dropdown → click `TO SQL` → insert into SQL.
     - If data already exists: displays `"Data Already Exists in SQL"`
     - If successful: displays `"Data Inserted in SQL"`
   - **Query Data**: Interface to select and run 10 SQL queries and display results in tabular form.

6. **Streamlit UI Enhancements**:  
   - Used Streamlit widgets like dropdowns, buttons, and table displays.
   - Referred to official [Streamlit documentation](https://docs.streamlit.io/) for layout and interaction patterns.

---

## 🗄️ Sample Data Structure (Extracted from API)

```json
"Channel_Name": {
  "Channel_Name": "Example Channel",
  "Channel_Id": "UC1234567890",
  "Subscription_Count": 10000,
  "Channel_Views": 1000000,
  "Channel_Description": "This is an example channel.",
  "Playlist_Id": "PL1234567890"
},
"Video_Id_1": {
  "Video_Id": "V1234567890",
  "Video_Name": "Example Video 1",
  "PublishedAt": "2022-01-01T00:00:00Z",
  "View_Count": 1000,
  "Like_Count": 100,
  "Comment_Count": 20,
  "Duration": "00:05:00",
  "Comments": {
    "Comment_Id_1": {
      "Comment_Id": "C1234567890",
      "Comment_Text": "This is a comment.",
      "Comment_Author": "Example User"
    }
  }
}
```

---

## 🔍 SQL Queries Implemented

1. What are the names of all the videos and their corresponding channels?  
2. Which channels have the most number of videos, and how many videos do they have?  
3. What are the top 10 most viewed videos and their respective channels?  
4. How many comments were made on each video, and what are their corresponding video names?  
5. Which videos have the highest number of likes, and what are their corresponding channel names?  
6. What is the total number of likes and dislikes for each video, and what are their corresponding video names?  
7. What is the total number of views for each channel, and what are their corresponding channel names?  
8. What are the names of all the channels that have published videos in the year 2022?  
9. What is the average duration of all videos in each channel, and what are their corresponding channel names?  
10. Which videos have the highest number of comments, and what are their corresponding channel names?  

All query outputs are displayed dynamically within the Streamlit interface using data tables.

---

## 📌 Final Outcome

The final product is a fully functional **Streamlit dashboard** that allows for:
- Real-time YouTube data extraction
- Seamless SQL data warehousing
- Interactive querying and insights generation

It demonstrates practical applications of **API integration**, **data engineering**, **SQL querying**, and **dashboard development**—and is ideal for showcasing in data science or backend portfolio.

---

## 📚 References

- [YouTube Data API Documentation](https://developers.google.com/youtube/v3/getting-started)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [SQLite Browser](https://sqlitebrowser.org/)

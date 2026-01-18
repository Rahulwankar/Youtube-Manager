import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import ObjectId
from bson.errors import InvalidId

load_dotenv()
mongo_uri = os.getenv("MongoDb")

try:
    client = MongoClient(mongo_uri)
    db = client["ytmanager"]
    video_collection = db["videos"]
except Exception as e:
    print("Error connecting to MongoDB:", e)
    exit()

def list_videos():
    videos = video_collection.find()
    for video in videos:
        print(f"ID: {video['_id']}, Name: {video['name']}, Time: {video['time']}")

def add_video(name, time):
    result = video_collection.insert_one({"name": name, "time": time})
    print(f"Video '{name}' added successfully with ID: {result.inserted_id}")

def update_video(video_id, name, time):
    try:
        result = video_collection.update_one(
            {"_id": ObjectId(video_id)},
            {"$set": {"name": name, "time": time}}
        )
        if result.matched_count == 0:
            print("No video found with this ID.")
        else:
            print("Video updated successfully.")
    except InvalidId:
        print("Invalid video ID format.")

def delete_video(video_id):
    try:
        result = video_collection.delete_one({"_id": ObjectId(video_id)})
        if result.deleted_count == 0:
            print("No video found with this ID.")
        else:
            print("Video deleted successfully.")
    except InvalidId:
        print("Invalid video ID format.")

def search_videos(keyword):
    videos = video_collection.find({"name": {"$regex": keyword, "$options": "i"}})
    found = False
    for video in videos:
        print(f"ID: {video['_id']}, Name: {video['name']}, Time: {video['time']}")
        found = True
    if not found:
        print("No videos found matching that keyword.")

def main():
    while True:
        print("\nYouTube Manager App")
        print("1. List all Videos")
        print("2. Add a new Video")
        print("3. Update a Video")
        print("4. Delete a Video")
        print("5. Search Videos")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == '1':
            list_videos()
        elif choice == '2':
            name = input("Enter video name: ").strip()
            time = input("Enter video time: ").strip()
            add_video(name, time)
        elif choice == '3':
            video_id = input("Enter a video ID to update: ").strip()
            name = input("Enter updated video name: ").strip()
            time = input("Enter updated video time: ").strip()
            update_video(video_id, name, time)
        elif choice == '4':
            video_id = input("Enter a video ID to delete: ").strip()
            delete_video(video_id)
        elif choice == '5':
            keyword = input("Enter keyword to search: ").strip()
            search_videos(keyword)
        elif choice == '6':
            print("Exiting the application.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()

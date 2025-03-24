# 🐘 WildGuard - Elephant Detection and Alert System 🚀

## 📌 Description
**WildGuard** is a real-time elephant detection system that uses **YOLOv3** and **OpenCV** to detect elephants and trigger alerts to prevent human-wildlife conflicts. It plays an **🚨 alarm sound** and sends **📩 SMS notifications** to nearby authorities when an elephant is detected.

## ✨ Features
✅ **Real-time elephant detection** using **YOLOv3**  
✅ **🔊 Plays an alert sound** when an elephant is detected  
✅ **🗂 Logs detections** in a MySQL database  
✅ **📡 Sends SMS notifications** using Twilio  
✅ Simple and efficient **🖥 OpenCV-based implementation**  

## 🛠 Installation
Follow these steps to set up and run **WildGuard** on your system:

### 1️⃣ Clone the Repository 🏗
```sh
git clone https://github.com/AruvasagaChithan/WildGuard.git
cd WildGuard
```

### 2️⃣ Install Dependencies 📦
Ensure you have **Python** installed, then install the required packages:
```sh
pip install -r requirements.txt
```

### 3️⃣ Download YOLOv3 Model Files 🎯
Due to file size restrictions, download the necessary **YOLOv3** files manually:
🔗 **YOLOv3 Weights:** [Download Here](https://pjreddie.com/media/files/yolov3.weights)  
🔗 **YOLOv3 Config:** [Download Here](https://github.com/pjreddie/darknet/blob/master/cfg/yolov3.cfg)  
🔗 **COCO Names File:** [Download Here](https://github.com/pjreddie/darknet/blob/master/data/coco.names)  

📂 Place these files inside the **project directory**.

### 4️⃣ Set Up MySQL Database 🗄
Create a **MySQL database** and **table** for storing detections:
```sql
CREATE DATABASE wildguard_db;
USE wildguard_db;
CREATE TABLE detections (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME NOT NULL,
    info TEXT NOT NULL
);
```
✅ Ensure **MySQL** is running and update the **database connection details** in the script if needed.

### 5️⃣ Configure Twilio for SMS Alerts 📲
1. **Sign up** on [Twilio](https://www.twilio.com/)  
2. Get your **🔑 Account SID** and **🔒 Auth Token**  
3. Replace the placeholders in `wildguard.py`:
   ```python
   account_sid = "YOUR_ACCOUNT_SSID"
   auth_token = "YOUR_AUTH_TOKEN"
   ```
4. Replace the **📞 Twilio phone number** and **📲 recipient number** in the script.

### 6️⃣ Run WildGuard 🚀
To start the system, simply run:
```sh
python wildguard.py
```
Press **⏹ Q** to stop detection.

## 🎯 Usage
- The system will start **detecting elephants** in real-time.  
- If an **elephant is detected**:  
  - **🔊 An alarm sound** will be played.  
  - **📂 The detection will be logged** in the database.  
  - **📩 An SMS alert will be sent** to the authorities.

## 👨‍💻 Author
**Aruvasaga Chithan**  
🔗 [GitHub Profile](https://github.com/aruvasaga-chithan)  
🔗 [LinkedIn Profile](https://www.linkedin.com/in/aruvasaga-chithan)

## 📜 License
This project is licensed under the **MIT License**.

# SC-Solace-Pubsub-Messaging-App
A full-stack messaging application using Solace PubSub+ with React frontend and Flask backend

**Author:** Sanchit Chavan   
---

## 📌 **Project Overview**
A **real-time messaging system** using **Solace PubSub+** with persistent queues, built with:
- 🐍 **Backend:** Flask-based APIs for message publishing & receiving.  
- ⚙️ **Messaging Protocol:** Solace SMF with TLS encryption.  
- 💻 **Frontend:** React app with live message display & tooltips showing timestamps.  

---

## ⚙️ **Tech Stack**
- **Languages:** Python, JavaScript  
- **Frameworks:** Flask, React  
- **Messaging:** Solace PubSub+ with TLS  
- **Deployment:** Flask APIs & Netlify frontend  

---

## 🔥 **Message Flow**
1️⃣ **Publisher:**  
- Sends messages to the Solace topic via a REST API.  
- Secure TLS connection ensures encrypted traffic.  

2️⃣ **Solace Broker:**  
- Routes messages to a **persistent queue**.  
- Ensures guaranteed delivery.  

3️⃣ **Receiver:**  
- Subscribes to the queue & retrieves messages asynchronously.  
- Updates timestamps & stores messages in memory.  

4️⃣ **Frontend:**  
- React app displays messages in real-time.  
- Tooltips reveal `Sent at` & `Received at` timestamps on hover.  

---

## 🚀 **How to Run Locally**
### 🔥 **Backend (Flask)**  
1. **Install dependencies:**  
```bash
pip install -r requirements.txt

python Publisher_Queue.py   # Port 5001  
python Receiver_Queue.py    # Port 5002  

cd queue-react  
npm install  

npm start

```


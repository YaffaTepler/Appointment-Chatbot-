# Appointment Chatbot

**Interface:**  
Web-based chat UI.

**Functionality:**  
Allow users to schedule a doctor’s appointment. Server-side logic includes:

- Checking availability against business hours and working days
- Preventing double bookings by querying Google Calendar
- Automatically adding confirmed slots to the designated Google Calendar

---

## 🛠️ Installation

```bash
git clone https://github.com/YaffaTepler/Appointment-Chatbot-.git
cd Appointment-Chatbot-
```
Copy credentials.json to Appointment-Chatbot- folder

## 🚀 Build & Run
```bash
docker build -t chatbot .
docker run -d -p 8000:8000 chatbot
```
You will get a container ID like this:

```bash
f42f57664e3bf842ea2e92723e4d8141daa4d48fc4301e40cb913523c4d364d0
```
Now open your browser and navigate to:

http://localhost:8000
### ✅ Notes
Make sure Docker is installed and running.

Port 8000 should be free before launching the container.

The app is expected to run on localhost unless deployed differently
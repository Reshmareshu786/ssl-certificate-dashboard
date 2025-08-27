# 🔐 SSL Certificate Dashboard

A simple **React + Azure Function** dashboard to check SSL certificate details (Valid From, Valid To, Days Remaining) for one or multiple domains in real-time.

---

## 🚀 Features
- Check SSL certificate details for one or multiple domains (comma-separated)
- Real-time response from Azure Function endpoint
- Color-coded status indicators:
  - 🟢 Green → Valid (> 30 days)
  - 🟠 Orange → Near Expiry (≤ 30 days)
  - 🔴 Red → Expired
- Clean and responsive UI

---

## 🛠️ Tech Stack
- **Frontend:** React, Axios, CSS
- **Backend:** Azure Function (Python)
- **Deployment:** Azure Function App

---

## 📂 Project Structure
ssl-certificate/
│
├── cert_checker/ # Azure Function backend
│ ├── get_cert/ # Python function for SSL validation
│ ├── host.json
│ ├── requirements.txt
│ └── ...
│
└── dashboard-ui/ # React frontend
├── public/
├── src/
│ ├── App.js # Main React UI logic
│ ├── App.css # Styling
│ └── index.js
└── package.json


---

## ⚙️ Setup Instructions

### **1️⃣ Clone the Repository**
```bash
git clone https://github.com/<your-username>/ssl-certificate-dashboard.git
cd ssl-certificate
```

### 2️⃣ Backend - Azure Function
Install Azure Functions Core Tools
```bash 
npm install -g azure-functions-core-tools@4 --unsafe-perm true
```

Navigate to your Azure Function folder
```
cd cert_checker
```

Deploy to Azure Function App
```
func azure functionapp publish sslcert-checker --python
```

Replace sslcert-checker with your actual Function App name if different.

3️⃣ Frontend - React App
Install dependencies
```
cd dashboard-ui
npm install
```

Run development server
```
npm start
```


Visit the app in your browser:
http://localhost:3000

4️⃣ Update API Endpoint

Edit dashboard-ui/src/App.js and update your API endpoint:
const res = await axios.get(
  `https://sslcert-checker.azurewebsites.net/api/get_cert?domain=${domain}`
);

5️⃣ Build and Deploy Frontend

For production build:
```
npm run build
```

Then deploy the build/ folder to:
Azure Static Web Apps
Vercel
Netlify
Any hosting provider

🧪 Example Usage
Single domain:
google.com

Multiple domains:
google.com,youtube.com


Sample JSON Response:
```Json
[
  {
    "domain": "google.com",
    "cn": "*.google.com",
    "valid_from": "2025-07-07 08:35:54",
    "valid_to": "2025-09-29 08:35:53",
    "days_remaining": 32
  },
  {
    "domain": "youtube.com",
    "cn": "*.google.com",
    "valid_from": "2025-07-07 08:34:03",
    "valid_to": "2025-09-29 08:34:02",
    "days_remaining": 32
  }
]
```
🌐 Deployment

Deploy backend with:
```bash
cd cert_checker
func azure functionapp publish sslcert-checker --python
```

Deploy frontend with:
```bash
cd dashboard-ui
npm run build
```

# 🚀 HOSTING GUIDE - Deploy Your Application

## 📱 **Hosting Options for Jury Presentation**

---

## 🏠 **OPTION 1: Local Network Hosting (Recommended for Jury)**

**Best for:** In-person presentations, local demos

### **Step 1: Find Your Local IP Address**

**Windows:**
```bash
ipconfig
```
Look for "IPv4 Address" - something like `192.168.1.x`

**Example Output:**
```
IPv4 Address: 192.168.1.105
```

---

### **Step 2: Update Backend to Accept Network Connections**

Edit `backend/main.py`:

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

**Run backend:**
```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000
```

---

### **Step 3: Update Web App API Configuration**

Edit `web/src/config.js`:

```javascript
// Replace localhost with your IP address
export const API_BASE_URL = 'http://192.168.1.105:8000';
```

**Run web app:**
```bash
cd web
npm run dev -- --host
```

The web app will be accessible at: `http://192.168.1.105:3000`

---

### **Step 4: Update Mobile App Configuration**

Edit `mobile/config.js`:

```javascript
// Use your computer's IP address
export const API_BASE_URL = 'http://192.168.1.105:8000';
```

**Run mobile app:**
```bash
cd mobile
npm start
```

Then scan QR code with Expo Go app on phone, OR
Access via browser: `http://192.168.1.105:8082`

---

### **Step 5: Share with Jury**

**Give jury members these URLs:**
- **Web App:** `http://192.168.1.105:3000`
- **Mobile App (browser):** `http://192.168.1.105:8082`
- **API Docs:** `http://192.168.1.105:8000/docs`

**Requirements:**
- ✅ All devices on same WiFi network
- ✅ Firewall allows connections (see troubleshooting below)
- ✅ Your computer stays on during presentation

---

## ☁️ **OPTION 2: Cloud Deployment (Free)**

**Best for:** Remote presentations, persistent access

### **A. Backend - Deploy to Render.com (Free)**

1. **Create account:** https://render.com
2. **Connect GitHub repository**
3. **Create Web Service:**
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn main:app --host 0.0.0.0 --port $PORT`
   - Environment: Python 3

You'll get a URL like: `https://skill-assign.onrender.com`

---

### **B. Web App - Deploy to Vercel (Free)**

1. **Create account:** https://vercel.com
2. **Connect GitHub repository**
3. **Deploy web folder**

You'll get a URL like: `https://skill-assign.vercel.app`

**Update web/src/config.js:**
```javascript
export const API_BASE_URL = 'https://skill-assign.onrender.com';
```

---

### **C. Mobile App - Expo Publish**

```bash
cd mobile
npx expo publish
```

Share the Expo link with jury to open in Expo Go app.

---

## 🖥️ **OPTION 3: Single Machine Demo**

**Best for:** Presenting from your own laptop

### **Setup:**

1. **Start all servers on your laptop:**
```bash
# Terminal 1 - Backend
cd backend
.\run.bat

# Terminal 2 - Web
cd web
npm run dev

# Terminal 3 - Mobile
cd mobile
npm start
```

2. **Open on your laptop:**
   - Web: http://localhost:3000
   - Mobile: http://localhost:8082

3. **Screen share or project to jury**

---

## 🔥 **QUICK SETUP FOR LOCAL NETWORK**

### **Windows Firewall Configuration:**

```bash
# Allow Python through firewall
netsh advfirewall firewall add rule name="Python" dir=in action=allow program="C:\Python\python.exe" enable=yes

# Allow Node through firewall
netsh advfirewall firewall add rule name="Node" dir=in action=allow program="C:\Program Files\nodejs\node.exe" enable=yes
```

Or use Windows Defender Firewall GUI:
1. Windows Security → Firewall & network protection
2. Allow an app through firewall
3. Check Node.js and Python

---

## 📋 **PRE-PRESENTATION CHECKLIST**

### **For Local Network Hosting:**

- [ ] Find your IP address
- [ ] Update all config files with your IP
- [ ] Test from another device on same WiFi
- [ ] Configure firewall rules
- [ ] Prepare URLs to share
- [ ] Keep laptop plugged in
- [ ] Disable sleep mode

### **For Cloud Hosting:**

- [ ] Deploy backend to Render
- [ ] Deploy web app to Vercel
- [ ] Update API URLs
- [ ] Test all features online
- [ ] Prepare URLs to share
- [ ] Have backup (local) ready

---

## 🧪 **TEST YOUR HOSTING**

### **From Another Device:**

1. **Connect to same WiFi**
2. **Open browser**
3. **Try:** `http://YOUR_IP:3000`
4. **Test:**
   - Can you see Dashboard?
   - Can you assign roles?
   - Does mobile app load?

---

## 🆘 **TROUBLESHOOTING**

### **Issue: Cannot connect from other devices**

**Solution:**
1. Check firewall settings
2. Ensure same WiFi network
3. Try `0.0.0.0` as host instead of `localhost`
4. Restart backend with `--host 0.0.0.0`

### **Issue: CORS errors**

**Solution - Edit backend/main.py:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Already set
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

### **Issue: Mobile app not connecting**

**Solution:**
1. Update `mobile/config.js` with correct IP
2. Restart Expo dev server
3. Clear Expo cache: `npx expo start -c`

### **Issue: Backend crashes on network access**

**Solution:**
```bash
# Run with explicit host
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

---

## 🎯 **RECOMMENDED SETUP FOR JURY PRESENTATION**

### **Option A: All Local (Most Reliable)**

```
Your Laptop (192.168.1.105)
├── Backend: :8000
├── Web: :3000
└── Mobile: :8082

Jury's Devices (same WiFi)
└── Access: http://192.168.1.105:3000
```

**Pros:**
- ✅ Fast
- ✅ No internet required
- ✅ Full control
- ✅ No deployment complexity

**Cons:**
- ❌ Same network required
- ❌ Your laptop must stay on

---

### **Option B: Cloud + Local Mobile**

```
Cloud
├── Backend: https://skill-assign.onrender.com
└── Web: https://skill-assign.vercel.app

Your Laptop
└── Mobile: :8082 (or Expo publish)

Jury
└── Access from anywhere!
```

**Pros:**
- ✅ Accessible from anywhere
- ✅ Professional URLs
- ✅ Persistent deployment

**Cons:**
- ❌ Requires internet
- ❌ Setup time
- ❌ Free tier limitations

---

## 🚀 **FASTEST SETUP (5 MINUTES)**

### **For In-Person Jury Demo:**

1. **Get your IP:**
   ```bash
   ipconfig
   ```

2. **Update mobile/config.js:**
   ```javascript
   export const API_BASE_URL = 'http://YOUR_IP:8000';
   ```

3. **Start everything:**
   ```bash
   # Backend
   cd backend
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload

   # Web (new terminal)
   cd web
   npm run dev -- --host

   # Mobile (new terminal)
   cd mobile
   npm start
   ```

4. **Share URLs with jury:**
   - Web: `http://YOUR_IP:3000`
   - Mobile: `http://YOUR_IP:8082`

**Done! 🎉**

---

## 📱 **MOBILE APP ACCESS OPTIONS**

### **1. Browser Access (Easiest)**
```
http://YOUR_IP:8082
```
Works on any smartphone browser!

### **2. Expo Go App**
1. Jury installs Expo Go
2. Scans QR code from your terminal
3. App loads in Expo Go

### **3. Expo Publish (Best)**
```bash
cd mobile
npx expo publish
```
Generates permanent link - no local server needed!

---

## 🎬 **DEMO DAY SETUP**

### **30 Minutes Before:**

1. ✅ Test all URLs
2. ✅ Populate demo data
3. ✅ Clear browser cache
4. ✅ Disable sleep mode
5. ✅ Keep laptop plugged in
6. ✅ Connect to presentation WiFi
7. ✅ Get new IP if network changed
8. ✅ Share URLs with jury

### **During Presentation:**

1. ✅ Keep terminals visible (shows live system)
2. ✅ Monitor for errors
3. ✅ Have backup screenshots
4. ✅ Test on your device first

---

## 💾 **BACKUP PLAN**

**If hosting fails:**

1. **Screen share your localhost**
2. **Use recorded demo video**
3. **Show screenshots with live code**
4. **API docs as proof of concept**

---

## 🎉 **RECOMMENDED: Local Network + Backup Cloud**

**Primary:** Local network hosting (fast, reliable)
**Backup:** Screenshots + API docs
**Bonus:** Cloud deployment link (shows production-ready)

---

**You're ready to host! Pick the option that works best for your jury setup! 🚀**

**Quick Start:** Use Option 1 (Local Network) for in-person presentations!

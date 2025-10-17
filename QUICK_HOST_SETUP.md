# ⚡ QUICK HOSTING SETUP

## 🎯 **For Jury Presentation - 5 Minutes**

---

## 📋 **OPTION A: Automatic Setup (Recommended)**

### **Step 1: Run the setup script**

```bash
.\setup_network_hosting.bat
```

This will:
- ✅ Find your IP address
- ✅ Show what to update
- ✅ Start all servers

---

## 🖐️ **OPTION B: Manual Setup**

### **Step 1: Get Your IP Address**

```bash
ipconfig
```

Look for `IPv4 Address`: **192.168.1.xxx**

Example: `192.168.1.105`

---

### **Step 2: Update Mobile Config**

Edit `mobile/config.js`:

```javascript
// Replace YOUR_IP with your actual IP
export const API_BASE_URL = 'http://192.168.1.105:8000';
```

---

### **Step 3: Start Backend (Network Mode)**

```bash
cd backend
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
```

✅ Backend running on: `http://192.168.1.105:8000`

---

### **Step 4: Start Web App (Network Mode)**

```bash
cd web
npm run dev -- --host
```

✅ Web running on: `http://192.168.1.105:3000`

---

### **Step 5: Start Mobile App**

```bash
cd mobile
npm start
```

✅ Mobile running on: `http://192.168.1.105:8082`

---

## 📱 **SHARE WITH JURY**

Give them these URLs (replace with YOUR IP):

```
Web App:    http://192.168.1.105:3000
Mobile App: http://192.168.1.105:8082
API Docs:   http://192.168.1.105:8000/docs
```

**Important:** All devices must be on the **SAME WiFi network**!

---

## 🔥 **TROUBLESHOOTING**

### **Can't connect from other devices?**

**Fix 1: Windows Firewall**
```bash
# Run as Administrator
netsh advfirewall firewall add rule name="Node" dir=in action=allow program="C:\Program Files\nodejs\node.exe" enable=yes
netsh advfirewall firewall add rule name="Python" dir=in action=allow program="C:\Python\python.exe" enable=yes
```

**Fix 2: Check if servers are listening**
```bash
netstat -an | findstr "3000 8000 8082"
```

Should see: `0.0.0.0:8000`, `0.0.0.0:3000`, etc.

---

## ✅ **VERIFICATION**

### **Test from another device:**

1. Connect to **same WiFi**
2. Open browser
3. Go to: `http://YOUR_IP:3000`
4. Should see Dashboard!

---

## 🎬 **PRESENTATION CHECKLIST**

Before jury arrives:

- [ ] Get your IP address
- [ ] Update mobile/config.js
- [ ] Start all 3 servers
- [ ] Test from phone/another laptop
- [ ] Keep laptop plugged in
- [ ] Disable sleep mode
- [ ] Have URLs ready to share

---

## 💡 **PRO TIPS**

1. **Print this URL** for jury:
   ```
   http://YOUR_IP:3000
   ```

2. **Keep terminals visible** during demo
   - Shows it's a real live system
   - Jury can see API logs

3. **Have backup plan**:
   - Screenshots ready
   - Can always show on your screen

4. **Test 10 minutes before**:
   - WiFi might change
   - IP might be different

---

## 🚀 **FASTEST METHOD**

```bash
# 1. Get IP
ipconfig

# 2. Update mobile/config.js (use your IP)
# export const API_BASE_URL = 'http://192.168.1.105:8000';

# 3. Start everything (3 separate terminals)
cd backend && uvicorn main:app --host 0.0.0.0 --port 8000
cd web && npm run dev -- --host  
cd mobile && npm start

# 4. Share: http://YOUR_IP:3000
```

**Done! 🎉**

---

## 📸 **FOR SCREENSHOTS**

If hosting fails, have these ready:
1. Dashboard with roles
2. ML recommendations dialog
3. Mobile app with tasks
4. Assignment status updates
5. API documentation

---

**You're ready! Good luck with your presentation! 🚀**

# 🚀 TVS Skill Assignment System - Quick Reference

## 📊 Dataset Summary

| Category | Count | Details |
|----------|-------|---------|
| **Workers** | 20 | Realistic TVS manufacturing workforce |
| **Roles** | 19 | All TVS manufacturing functions covered |
| **Skills** | 60+ | Automotive-specific technical skills |
| **Assignments** | 18 | Historical data for ML training |

---

## 👥 Worker Categories

### Shop Floor (10 workers)
1. Assembly Operator
2. Welder
3. Paint Shop Operator
4. Quality Inspector
5. CNC Operator
6. Electronics Technician
7. Maintenance Technician
8. Fit & Finish Specialist
9. Shift Supervisor
10. Packing Staff

### Engineering (9 workers)
11. Powertrain Engineer
12. Supplier Quality Engineer
13. Process Planning Engineer
14. Design Engineer
15. Tooling Engineer
16. Production Planner
17. Safety Officer
18. Logistics Staff
19. EEE Design Engineer

### Entry Level (1 worker)
20. Entry Level Technician

---

## 🎯 Role Categories

### Shop Floor Roles (8)
- Assembly Operator / Technician
- Welder
- Painter / Paint Shop Operator
- CNC Operator / Machinist
- Quality Inspector / Quality Engineer
- Maintenance Technician / Mechanic
- Fit & Finish Specialist
- Electrical / Electronics Technician

### Engineering Roles (6)
- Process Planning Engineer
- Design Engineer (Chassis / Parts)
- Engine / Powertrain Engineer
- Supplier Quality Assurance Engineer
- Tooling / Jig & Fixture Engineer
- Electrical / EEE Design Engineer

### Management & Support (5)
- Shift Supervisor / Team Lead
- Production Planner / Line Balancing Engineer
- Safety & Environment Officer
- Logistics / Material Handling Staff
- Packing / Dispatch Staff

---

## 🔑 Key Skills by Function

### Welding & Joining
- TIG Welding, MIG Welding, Spot Welding
- Frame Welding, Blueprint Reading

### Machining
- CNC Programming, CNC Operation
- CAM Software, Precision Machining, Tool Setting

### Quality Control
- Quality Inspection, CMM Operation
- Gauge Calibration, ISO Standards, Documentation

### Electrical/Electronics
- Electrical Wiring, ECU Assembly
- Sensor Installation, Harness Routing
- PCB Design, Circuit Design, CAN Bus

### Design & Engineering
- CAD Design, CATIA, Chassis Design
- FEA Basics, GD&T
- Process Design, Capacity Planning

### Maintenance
- Hydraulic Systems, Pneumatic Systems
- Preventive Maintenance, Breakdown Maintenance
- PLC Basics

### Production Management
- Team Leadership, Line Supervision
- Production Scheduling, Line Balancing
- ERP Systems, Throughput Optimization

---

## 📈 Performance Metrics

### Top Performers (90%+)
- Karthik Iyer (Maintenance) - 95%
- Priya Sharma (Welder) - 92%
- Sanjay Rao (Process Planning) - 93%
- Suresh Pillai (EEE Design) - 90%

### High Workload (45+ hours/week)
- Amit Patel - 48h/week (Paint Shop)
- Anjali Desai - 46h/week (Electronics)
- Sanjay Rao - 45h/week (Process Planning)

### Entry Level (<2 years experience)
- Pooja Sharma - 1.0 year
- Amit Patel - 1.0 year
- Neha Gupta - 1.5 years
- Lakshmi Iyer - 2.0 years

---

## 🎯 Role Difficulty Levels

### Easy (4-5/10)
- Packing / Dispatch Staff
- Assembly Operator
- Fit & Finish Specialist
- Logistics / Material Handling

### Medium (6-7/10)
- Painter / Paint Shop Operator
- Quality Inspector
- Safety & Environment Officer
- Maintenance Technician
- Electrical Technician
- Shift Supervisor
- Supplier Quality Engineer

### Hard (8-9/10)
- CNC Operator / Machinist
- Process Planning Engineer
- Production Planner
- Tooling Engineer

### Very Hard (9/10)
- Design Engineer
- Engine / Powertrain Engineer
- Electrical / EEE Design Engineer

---

## 🚀 Quick Start Commands

### Start Backend
```bash
cd backend
.\venv\Scripts\activate
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Start Web App
```bash
cd web
npm run dev
```

### Reinitialize Database
```bash
cd backend
.\venv\Scripts\activate
Remove-Item -Force skill_assign.db
python init_db.py
```

---

## 📊 API Endpoints

### Worker Management
- `GET /worker/all` - Get all workers
- `POST /worker/add` - Add new worker
- `PUT /worker/{id}` - Update worker
- `DELETE /worker/{id}` - Delete worker

### Role Management
- `GET /role/all` - Get all roles
- `GET /role/{id}/description` - Get role details
- `POST /role/add` - Add new role

### ML Predictions
- `POST /predict-fit` - Get worker recommendations for role
- `POST /train-model` - Train ML model with assignment data

### Analytics
- `GET /analytics/overview` - Get overall analytics
- `GET /analytics/skill-gap` - Get skill gap analysis

### Assignments
- `POST /assignment/create` - Create assignment
- `PUT /assignment/{id}/feedback` - Add feedback
- `GET /assignment/all` - Get all assignments

---

## 🎨 Color Coding

### Hours/Week
- 🟢 **Green**: <45 hours (Healthy)
- 🟡 **Yellow**: 45-50 hours (Warning)
- 🔴 **Red**: 50+ hours (Overworked)

### Fit Score
- 🟢 **Green**: >70% (Good fit)
- 🟡 **Yellow**: 50-70% (Moderate fit)
- 🔴 **Red**: <50% (Poor fit)

### Training Priority
- 🔴 **High**: High performers with capacity
- 🟡 **Medium**: Good potential workers
- 🔵 **Low**: Focus on current role first

---

## 📱 Access Points

- **Web Dashboard**: http://localhost:3000
- **API Documentation**: http://localhost:8000/docs
- **Backend Health**: http://localhost:8000/health

---

## 💡 Pro Tips

1. **Train the model** after every 10 assignments for better accuracy
2. **Monitor hours/week** to prevent worker burnout
3. **Check skill gap analysis** monthly for training planning
4. **Use role descriptions** to make informed assignments
5. **Provide detailed feedback** to improve ML recommendations

---

## 🎯 Success Metrics

### Assignment Accuracy
- Target: 85%+ successful assignments
- Current: Baseline being established

### Worker Utilization
- Target: 40-45 hours/week average
- Alert: >48 hours/week

### Skill Coverage
- Target: 3+ workers per critical skill
- Monitor: Skills with <2 workers

### Training Effectiveness
- Target: 90%+ completion rate
- Measure: Skill acquisition within 3 months

---

**Ready for TVS Manufacturing Deployment! 🏭**

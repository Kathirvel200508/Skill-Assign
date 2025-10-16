"""
Initialize database with sample workers and roles
"""
from sqlalchemy.orm import Session
from database import SessionLocal, engine
import models

def init_sample_data():
    """Initialize database with sample data"""
    models.Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(models.Worker).count() > 0:
            print("Database already contains data. Skipping initialization.")
            return
        
        # Sample workers - TVS Manufacturing Unit
        workers = [
            models.Worker(
                name="Rajesh Kumar",
                age=28,
                experience=3.5,
                skills=["assembly", "torque_tools", "quality_inspection", "two_wheeler_assembly"],
                hours_per_day=8.0,
                hours_per_week=42,
                fatigue_level=0.2,
                performance_score=0.85,
                current_role="Assembly Operator"
            ),
            models.Worker(
                name="Priya Sharma",
                age=35,
                experience=7.2,
                skills=["tig_welding", "mig_welding", "spot_welding", "frame_welding", "blueprint_reading"],
                hours_per_day=7.5,
                hours_per_week=38,
                fatigue_level=0.1,
                performance_score=0.92,
                current_role="Welder"
            ),
            models.Worker(
                name="Amit Patel",
                age=22,
                experience=1.0,
                skills=["spray_painting", "powder_coating", "surface_preparation", "color_matching"],
                hours_per_day=8.5,
                hours_per_week=48,
                fatigue_level=0.5,
                performance_score=0.65
            ),
            models.Worker(
                name="Sunita Reddy",
                age=45,
                experience=12.0,
                skills=["quality_inspection", "cmm_operation", "gauge_calibration", "iso_standards", "documentation"],
                hours_per_day=8.0,
                hours_per_week=40,
                fatigue_level=0.3,
                performance_score=0.88,
                current_role="Quality Inspector"
            ),
            models.Worker(
                name="Vikram Singh",
                age=30,
                experience=5.0,
                skills=["cnc_programming", "cnc_operation", "cam_software", "precision_machining", "tool_setting"],
                hours_per_day=8.0,
                hours_per_week=44,
                fatigue_level=0.2,
                performance_score=0.88,
                current_role="CNC Operator"
            ),
            models.Worker(
                name="Anjali Desai",
                age=26,
                experience=2.5,
                skills=["electrical_wiring", "ecu_assembly", "sensor_installation", "harness_routing", "multimeter_testing"],
                hours_per_day=8.0,
                hours_per_week=46,
                fatigue_level=0.4,
                performance_score=0.72
            ),
            models.Worker(
                name="Karthik Iyer",
                age=38,
                experience=9.0,
                skills=["hydraulic_systems", "pneumatic_systems", "preventive_maintenance", "breakdown_maintenance", "plc_basics"],
                hours_per_day=7.5,
                hours_per_week=40,
                fatigue_level=0.2,
                performance_score=0.95,
                current_role="Maintenance Technician"
            ),
            models.Worker(
                name="Neha Gupta",
                age=24,
                experience=1.5,
                skills=["surface_finishing", "buffing", "polishing", "cosmetic_inspection", "paint_touch_up"],
                hours_per_day=8.0,
                hours_per_week=42,
                fatigue_level=0.3,
                performance_score=0.68
            ),
            models.Worker(
                name="Ravi Menon",
                age=32,
                experience=6.0,
                skills=["team_leadership", "line_supervision", "production_monitoring", "5s_implementation", "problem_solving"],
                hours_per_day=8.0,
                hours_per_week=44,
                fatigue_level=0.2,
                performance_score=0.82,
                current_role="Shift Supervisor"
            ),
            models.Worker(
                name="Deepa Nair",
                age=29,
                experience=4.0,
                skills=["packaging", "dispatch_preparation", "inventory_management", "forklift_operation", "documentation"],
                hours_per_day=8.0,
                hours_per_week=40,
                fatigue_level=0.3,
                performance_score=0.79
            ),
            models.Worker(
                name="Arjun Krishnan",
                age=33,
                experience=8.0,
                skills=["engine_assembly", "powertrain_testing", "dynamometer_operation", "performance_analysis", "durability_testing"],
                hours_per_day=8.0,
                hours_per_week=42,
                fatigue_level=0.25,
                performance_score=0.89
            ),
            models.Worker(
                name="Meera Joshi",
                age=27,
                experience=3.0,
                skills=["supplier_audit", "ppap_review", "incoming_inspection", "vendor_coordination", "quality_documentation"],
                hours_per_day=8.0,
                hours_per_week=40,
                fatigue_level=0.2,
                performance_score=0.81
            ),
            models.Worker(
                name="Sanjay Rao",
                age=41,
                experience=15.0,
                skills=["process_design", "capacity_planning", "layout_optimization", "lean_manufacturing", "value_stream_mapping"],
                hours_per_day=8.0,
                hours_per_week=45,
                fatigue_level=0.3,
                performance_score=0.93
            ),
            models.Worker(
                name="Lakshmi Iyer",
                age=25,
                experience=2.0,
                skills=["cad_design", "catia", "chassis_design", "fea_basics", "gd_and_t"],
                hours_per_day=8.0,
                hours_per_week=42,
                fatigue_level=0.25,
                performance_score=0.76
            ),
            models.Worker(
                name="Ramesh Babu",
                age=36,
                experience=10.0,
                skills=["jig_design", "fixture_design", "tool_maintenance", "autocad", "manufacturing_processes"],
                hours_per_day=8.0,
                hours_per_week=44,
                fatigue_level=0.28,
                performance_score=0.87
            ),
            models.Worker(
                name="Kavita Menon",
                age=31,
                experience=5.5,
                skills=["production_scheduling", "line_balancing", "erp_systems", "throughput_optimization", "bottleneck_analysis"],
                hours_per_day=8.0,
                hours_per_week=43,
                fatigue_level=0.27,
                performance_score=0.84
            ),
            models.Worker(
                name="Anil Kumar",
                age=28,
                experience=4.0,
                skills=["safety_audits", "ppe_management", "hazard_identification", "emergency_response", "iso_45001"],
                hours_per_day=8.0,
                hours_per_week=40,
                fatigue_level=0.22,
                performance_score=0.80
            ),
            models.Worker(
                name="Divya Reddy",
                age=26,
                experience=2.5,
                skills=["material_handling", "warehouse_management", "inventory_control", "kanban_systems", "sap_basics"],
                hours_per_day=8.0,
                hours_per_week=42,
                fatigue_level=0.26,
                performance_score=0.74
            ),
            models.Worker(
                name="Suresh Pillai",
                age=34,
                experience=7.0,
                skills=["pcb_design", "circuit_design", "ecu_programming", "can_bus", "embedded_systems"],
                hours_per_day=8.0,
                hours_per_week=44,
                fatigue_level=0.29,
                performance_score=0.90
            ),
            models.Worker(
                name="Pooja Sharma",
                age=23,
                experience=1.0,
                skills=["assembly", "hand_tools", "basic_quality_check", "safety_protocols"],
                hours_per_day=8.0,
                hours_per_week=40,
                fatigue_level=0.24,
                performance_score=0.70
            )
        ]
        
        # Sample roles - TVS Manufacturing Unit
        roles = [
            models.Role(
                name="Assembly Operator / Technician",
                description="Assemble two-wheeler components including engine, chassis, and body parts on production line",
                required_skills=["assembly", "torque_tools", "quality_inspection", "two_wheeler_assembly"],
                difficulty_level=0.5,
                typical_tasks=["Assemble engine and chassis components", "Use torque wrenches and pneumatic tools", "Perform inline quality checks", "Follow assembly sequence and work instructions"],
                success_criteria="Meet takt time with zero critical defects and 100% first-time-right assembly"
            ),
            models.Role(
                name="Welder",
                description="Perform TIG, MIG, and spot welding on motorcycle frames and structural components",
                required_skills=["tig_welding", "mig_welding", "spot_welding", "frame_welding", "blueprint_reading"],
                difficulty_level=0.7,
                typical_tasks=["Weld chassis frames and sub-assemblies", "Read and interpret welding blueprints", "Inspect weld quality visually and with gauges", "Maintain welding equipment and consumables"],
                success_criteria="Zero weld failures in testing, <0.5% rework rate, maintain safety standards"
            ),
            models.Role(
                name="Painter / Paint Shop Operator",
                description="Apply paint and coating to motorcycle parts ensuring quality finish and appearance",
                required_skills=["spray_painting", "powder_coating", "surface_preparation", "color_matching"],
                difficulty_level=0.6,
                typical_tasks=["Prepare surfaces for painting", "Apply primer, base coat, and clear coat", "Match colors to specifications", "Inspect finish quality and address defects"],
                success_criteria="Achieve A-grade finish on 95%+ parts, minimize paint wastage"
            ),
            models.Role(
                name="CNC Operator / Machinist",
                description="Operate CNC machines to manufacture precision engine and transmission components",
                required_skills=["cnc_programming", "cnc_operation", "cam_software", "precision_machining", "tool_setting"],
                difficulty_level=0.8,
                typical_tasks=["Set up and operate CNC lathes and mills", "Load CNC programs and verify tool offsets", "Inspect parts with micrometers and gauges", "Perform tool changes and machine maintenance"],
                success_criteria="Maintain dimensional accuracy within ±0.01mm, 98%+ machine uptime"
            ),
            models.Role(
                name="Quality Inspector / Quality Engineer",
                description="Inspect incoming materials, in-process components, and finished vehicles for quality compliance",
                required_skills=["quality_inspection", "cmm_operation", "gauge_calibration", "iso_standards", "documentation"],
                difficulty_level=0.6,
                typical_tasks=["Perform dimensional inspection using CMM and gauges", "Conduct first-off and last-off inspections", "Document quality data and generate reports", "Coordinate with production on non-conformances"],
                success_criteria="Catch 98%+ defects before customer, maintain ISO/TS compliance"
            ),
            models.Role(
                name="Maintenance Technician / Mechanic",
                description="Perform preventive and breakdown maintenance on production equipment and machinery",
                required_skills=["hydraulic_systems", "pneumatic_systems", "preventive_maintenance", "breakdown_maintenance", "plc_basics"],
                difficulty_level=0.7,
                typical_tasks=["Execute preventive maintenance schedules", "Troubleshoot and repair hydraulic/pneumatic systems", "Respond to production line breakdowns", "Maintain spare parts inventory"],
                success_criteria="Achieve 95%+ equipment uptime, reduce MTTR by 20%"
            ),
            models.Role(
                name="Fit & Finish Specialist",
                description="Ensure cosmetic quality and surface finish of visible motorcycle parts meet aesthetic standards",
                required_skills=["surface_finishing", "buffing", "polishing", "cosmetic_inspection", "paint_touch_up"],
                difficulty_level=0.5,
                typical_tasks=["Inspect painted and chrome parts for defects", "Perform buffing and polishing operations", "Touch up minor paint defects", "Ensure gap and flush alignment"],
                success_criteria="Zero cosmetic defects reaching customer, 98%+ A-grade finish"
            ),
            models.Role(
                name="Electrical / Electronics Technician",
                description="Assemble and test electrical harnesses, ECUs, sensors, and lighting systems",
                required_skills=["electrical_wiring", "ecu_assembly", "sensor_installation", "harness_routing", "multimeter_testing"],
                difficulty_level=0.7,
                typical_tasks=["Route and connect wiring harnesses", "Install ECUs, sensors, and switches", "Test electrical systems with multimeter", "Diagnose and fix electrical faults"],
                success_criteria="Zero electrical failures in end-of-line testing, proper harness routing"
            ),
            models.Role(
                name="Process Planning Engineer",
                description="Design manufacturing processes, plan capacity, and optimize factory layout for efficiency",
                required_skills=["process_design", "capacity_planning", "layout_optimization", "lean_manufacturing", "value_stream_mapping"],
                difficulty_level=0.8,
                typical_tasks=["Design process flows and work instructions", "Calculate line capacity and takt time", "Optimize factory layout for material flow", "Implement lean manufacturing principles"],
                success_criteria="Achieve 85%+ OEE, reduce cycle time by 15%, eliminate waste"
            ),
            models.Role(
                name="Design Engineer (Chassis / Parts)",
                description="Design motorcycle chassis, body panels, and mechanical components using CAD software",
                required_skills=["cad_design", "catia", "chassis_design", "fea_basics", "gd_and_t"],
                difficulty_level=0.9,
                typical_tasks=["Create 3D CAD models of chassis and parts", "Perform FEA analysis for strength validation", "Generate engineering drawings with GD&T", "Collaborate with manufacturing on DFM"],
                success_criteria="Meet design validation targets, ensure manufacturability"
            ),
            models.Role(
                name="Engine / Powertrain Engineer",
                description="Design, test, and validate engine and transmission systems for performance and durability",
                required_skills=["engine_assembly", "powertrain_testing", "dynamometer_operation", "performance_analysis", "durability_testing"],
                difficulty_level=0.9,
                typical_tasks=["Conduct engine performance testing on dyno", "Analyze power, torque, and emissions data", "Perform durability and endurance testing", "Optimize engine calibration parameters"],
                success_criteria="Meet power/torque targets, pass emission norms, 100k km durability"
            ),
            models.Role(
                name="Supplier Quality Assurance Engineer",
                description="Ensure quality of parts from suppliers through audits, PPAP, and incoming inspection",
                required_skills=["supplier_audit", "ppap_review", "incoming_inspection", "vendor_coordination", "quality_documentation"],
                difficulty_level=0.7,
                typical_tasks=["Conduct supplier quality audits", "Review and approve PPAP submissions", "Perform incoming material inspection", "Coordinate with vendors on quality issues"],
                success_criteria="Achieve 99%+ incoming quality, reduce supplier rejections"
            ),
            models.Role(
                name="Tooling / Jig & Fixture Engineer",
                description="Design and maintain jigs, fixtures, and tooling for manufacturing operations",
                required_skills=["jig_design", "fixture_design", "tool_maintenance", "autocad", "manufacturing_processes"],
                difficulty_level=0.8,
                typical_tasks=["Design welding jigs and assembly fixtures", "Create tool drawings in AutoCAD", "Maintain and repair existing tooling", "Optimize tool design for ease of use"],
                success_criteria="Reduce setup time by 30%, ensure tool accuracy and repeatability"
            ),
            models.Role(
                name="Shift Supervisor / Team Lead",
                description="Lead production team, monitor line performance, and ensure targets are met during shift",
                required_skills=["team_leadership", "line_supervision", "production_monitoring", "5s_implementation", "problem_solving"],
                difficulty_level=0.7,
                typical_tasks=["Supervise 20-30 operators on production line", "Monitor hourly production vs targets", "Implement 5S and kaizen activities", "Resolve production issues and bottlenecks"],
                success_criteria="Meet shift production targets, maintain team morale and safety"
            ),
            models.Role(
                name="Production Planner / Line Balancing Engineer",
                description="Schedule production, balance assembly lines, and optimize throughput",
                required_skills=["production_scheduling", "line_balancing", "erp_systems", "throughput_optimization", "bottleneck_analysis"],
                difficulty_level=0.8,
                typical_tasks=["Create daily/weekly production schedules", "Balance workload across assembly stations", "Analyze bottlenecks and optimize flow", "Coordinate with logistics on material availability"],
                success_criteria="Achieve 90%+ schedule adherence, minimize line imbalance"
            ),
            models.Role(
                name="Safety & Environment Officer",
                description="Ensure workplace safety, manage PPE, and maintain environmental compliance",
                required_skills=["safety_audits", "ppe_management", "hazard_identification", "emergency_response", "iso_45001"],
                difficulty_level=0.6,
                typical_tasks=["Conduct safety audits and risk assessments", "Ensure PPE availability and usage", "Investigate accidents and near-misses", "Maintain ISO 45001 and environmental compliance"],
                success_criteria="Zero lost-time accidents, 100% PPE compliance, pass audits"
            ),
            models.Role(
                name="Logistics / Material Handling Staff",
                description="Manage material flow, supply parts to production line, and maintain warehouse inventory",
                required_skills=["material_handling", "warehouse_management", "inventory_control", "kanban_systems", "sap_basics"],
                difficulty_level=0.5,
                typical_tasks=["Supply parts to production line using kanban", "Manage warehouse inventory and stock levels", "Operate forklifts and material handling equipment", "Update inventory in SAP/ERP system"],
                success_criteria="Zero line stoppages due to material shortage, 99%+ inventory accuracy"
            ),
            models.Role(
                name="Packing / Dispatch Staff",
                description="Pack finished motorcycles and prepare them for shipment to dealers",
                required_skills=["packaging", "dispatch_preparation", "inventory_management", "forklift_operation", "documentation"],
                difficulty_level=0.4,
                typical_tasks=["Pack motorcycles with protective materials", "Prepare dispatch documentation and labels", "Load vehicles onto transport trucks", "Maintain dispatch records and inventory"],
                success_criteria="Zero damage during transit, 100% on-time dispatch"
            ),
            models.Role(
                name="Electrical / EEE Design Engineer",
                description="Design electronic control units, wiring harnesses, and embedded systems for motorcycles",
                required_skills=["pcb_design", "circuit_design", "ecu_programming", "can_bus", "embedded_systems"],
                difficulty_level=0.9,
                typical_tasks=["Design PCBs for ECUs and control modules", "Develop embedded software for vehicle systems", "Design CAN bus communication architecture", "Test and validate electronic systems"],
                success_criteria="Meet functional safety standards, pass EMC/EMI testing"
            )
        ]
        
        # Add to database
        for worker in workers:
            db.add(worker)
        
        for role in roles:
            db.add(role)
        
        db.commit()
        
        print(f"✅ Successfully added {len(workers)} workers and {len(roles)} roles to the database")
        
        # Create some sample assignments for training
        assignments = [
            models.Assignment(worker_id=1, role_id=1, fit_score=0.88, success=True, feedback="Excellent assembly skills"),
            models.Assignment(worker_id=2, role_id=2, fit_score=0.95, success=True, feedback="Perfect weld quality"),
            models.Assignment(worker_id=3, role_id=3, fit_score=0.70, success=True, feedback="Good painting but needs speed improvement"),
            models.Assignment(worker_id=4, role_id=5, fit_score=0.90, success=True, feedback="Thorough quality inspection"),
            models.Assignment(worker_id=5, role_id=4, fit_score=0.92, success=True, feedback="Expert CNC operation"),
            models.Assignment(worker_id=6, role_id=8, fit_score=0.75, success=True, feedback="Good electrical work"),
            models.Assignment(worker_id=7, role_id=6, fit_score=0.93, success=True, feedback="Excellent maintenance skills"),
            models.Assignment(worker_id=8, role_id=7, fit_score=0.72, success=True, feedback="Good finishing work"),
            models.Assignment(worker_id=9, role_id=14, fit_score=0.85, success=True, feedback="Strong leadership"),
            models.Assignment(worker_id=10, role_id=18, fit_score=0.82, success=True, feedback="Efficient packing"),
            models.Assignment(worker_id=11, role_id=11, fit_score=0.91, success=True, feedback="Excellent engine testing"),
            models.Assignment(worker_id=12, role_id=12, fit_score=0.83, success=True, feedback="Good supplier coordination"),
            models.Assignment(worker_id=13, role_id=9, fit_score=0.94, success=True, feedback="Outstanding process planning"),
            models.Assignment(worker_id=14, role_id=10, fit_score=0.78, success=True, feedback="Good CAD skills, needs more experience"),
            models.Assignment(worker_id=15, role_id=13, fit_score=0.89, success=True, feedback="Excellent tooling design"),
            models.Assignment(worker_id=1, role_id=2, fit_score=0.45, success=False, feedback="Lacks welding certification"),
            models.Assignment(worker_id=3, role_id=4, fit_score=0.35, success=False, feedback="No CNC experience"),
            models.Assignment(worker_id=20, role_id=1, fit_score=0.68, success=True, feedback="Entry level, learning well"),
        ]
        
        for assignment in assignments:
            db.add(assignment)
        
        db.commit()
        print(f"✅ Successfully added {len(assignments)} sample assignments for ML training")
        
    except Exception as e:
        print(f"❌ Error initializing database: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("Initializing database with sample data...")
    init_sample_data()

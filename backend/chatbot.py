"""
AI Chatbot using Hugging Face LLM (UserLM-8b)
Provides intelligent assistance to supervisors about workers, roles, and assignments
"""
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from typing import List, Dict
from sqlalchemy.orm import Session
import models

class SupervisorChatbot:
    def __init__(self):
        self.model_name = "microsoft/UserLM-8b"  # Advanced conversational model
        self.tokenizer = None
        self.model = None
        self.conversation_history = []
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
    def load_model(self):
        """Load the Hugging Face UserLM model"""
        try:
            print(f"[CHATBOT] Loading UserLM-8b model on {self.device}...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name, 
                trust_remote_code=True
            )
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                trust_remote_code=True
            ).to(self.device)
            print("[CHATBOT] ✅ UserLM model loaded successfully!")
            return True
        except Exception as e:
            print(f"[CHATBOT] ❌ Error loading model: {e}")
            print(f"[CHATBOT] Will use rule-based responses instead")
            return False
    
    def get_detailed_context_data(self, db: Session) -> str:
        """Get comprehensive system context with full descriptions"""
        try:
            # Get all data
            workers = db.query(models.Worker).all()
            roles = db.query(models.Role).all()
            assignments = db.query(models.Assignment).all()
            tasks = db.query(models.Task).all()
            
            # Worker statistics
            worker_count = len(workers)
            avg_performance = sum(w.performance_score for w in workers) / worker_count if workers else 0
            high_performers = [w for w in workers if w.performance_score > 0.85]
            low_fatigue = [w for w in workers if w.fatigue_level < 0.3]
            high_fatigue = [w for w in workers if w.fatigue_level >= 0.7]
            
            # Task statistics
            task_completed = sum(1 for t in tasks if t.status == 'completed')
            task_in_progress = sum(1 for t in tasks if t.status == 'in_progress')
            task_pending = sum(1 for t in tasks if t.status == 'pending')
            
            # Assignment statistics
            completed_assignments = [a for a in assignments if a.success == True]
            pending_assignments = [a for a in assignments if a.success is None]
            success_rate = (len(completed_assignments) / len(assignments) * 100) if assignments else 0
            
            # Build comprehensive context
            context = f"""WORKFORCE MANAGEMENT SYSTEM - COMPLETE DATA OVERVIEW

=== WORKERS DATABASE ({worker_count} Total) ===
- Average Performance Score: {avg_performance*100:.1f}%
- High Performers (>85%): {len(high_performers)} workers
- Low Fatigue Workers (<30%): {len(low_fatigue)} workers  
- High Fatigue Workers (≥70%): {len(high_fatigue)} workers

Top 5 Performers:
{chr(10).join([f"{i+1}. {w.name} - Performance: {w.performance_score*100:.0f}%, Experience: {w.experience} years, Fatigue: {w.fatigue_level*100:.0f}%, Skills: {len(w.skills)}" for i, w in enumerate(sorted(workers, key=lambda x: x.performance_score, reverse=True)[:5])])}

Workers by Fatigue Level:
- Low Fatigue (Ready for Work): {len(low_fatigue)} workers
- Medium Fatigue: {len([w for w in workers if 0.3 <= w.fatigue_level < 0.7])} workers
- High Fatigue (Need Rest): {len(high_fatigue)} workers

=== ROLES DATABASE ({len(roles)} Total) ===
Available roles with requirements:
{chr(10).join([f"- {r.name}: Difficulty {r.difficulty_level*10:.1f}/10, Required Skills: {', '.join(r.required_skills[:3])}" for r in roles[:5]])}
{'...' if len(roles) > 5 else ''}

=== TASKS STATUS ({len(tasks)} Total) ===
- Completed: {task_completed} tasks ({task_completed/len(tasks)*100:.0f}% if tasks else 0)
- In Progress: {task_in_progress} tasks  
- Pending: {task_pending} tasks

=== ASSIGNMENTS TRACKING ({len(assignments)} Total) ===
- Successful Assignments: {len(completed_assignments)}
- Pending Assignments: {len(pending_assignments)}
- Success Rate: {success_rate:.1f}%

Recent Successful Assignments:
{chr(10).join([f"- Worker {a.worker_id} → Role {a.role_id}, Fit Score: {a.fit_score*100:.0f}%" for a in completed_assignments[-3:]]) if completed_assignments else 'No recent assignments'}

=== SYSTEM CAPABILITIES ===
This is an AI-powered workforce management system that:
1. Uses ML algorithms to recommend best worker-role matches
2. Monitors worker health and fatigue in real-time
3. Tracks task completion and assignment success
4. Provides analytics on workforce performance
5. Automatically learns from assignment outcomes
6. Integrates with wearable devices for health data
7. Enables real-time task synchronization to mobile apps

You are an AI assistant with access to all this data. Answer questions about workers, roles, assignments, tasks, performance, health, and provide recommendations."""
            
            return context.strip()
        except Exception as e:
            return f"Error getting context: {e}"
    
    def generate_response(self, user_message: str, db: Session) -> str:
        """Generate chatbot response using UserLM-8b format"""
        
        # If model not loaded, use rule-based responses
        if self.model is None:
            return self._rule_based_response(user_message, db)
        
        try:
            # Get comprehensive system context with full descriptions
            context_data = self.get_detailed_context_data(db)
            
            # Create system message with full workforce data
            system_content = f"""{context_data}

You are an intelligent AI assistant for a workforce management system. You have access to complete data about workers, roles, assignments, tasks, and system performance. 

Your role is to:
1. Answer questions accurately based on the data provided
2. Provide insights and recommendations
3. Help supervisors make data-driven decisions
4. Explain trends and patterns in the workforce
5. Be helpful, professional, and concise

When answering questions, use the specific data provided above. Reference actual numbers, names, and statistics."""

            # Create conversation with chat template format
            messages = [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_message}
            ]
            
            # Apply chat template and convert to tensors
            inputs = self.tokenizer.apply_chat_template(
                messages, 
                return_tensors="pt"
            ).to(self.device)
            
            # Define end tokens
            end_token = "<|eot_id|>"
            end_token_id = self.tokenizer.encode(end_token, add_special_tokens=False)
            
            end_conv_token = "<|endconversation|>"
            end_conv_token_id = self.tokenizer.encode(end_conv_token, add_special_tokens=False)
            
            # Generate response with UserLM-8b settings
            with torch.no_grad():
                outputs = self.model.generate(
                    input_ids=inputs,
                    do_sample=True,
                    top_p=0.8,
                    temperature=1,
                    max_new_tokens=300,  # Increased for detailed responses
                    eos_token_id=end_token_id,
                    pad_token_id=self.tokenizer.eos_token_id,
                    bad_words_ids=[[token_id] for token_id in end_conv_token_id]
                )
            
            # Decode response
            response = self.tokenizer.decode(
                outputs[0][inputs.shape[1]:], 
                skip_special_tokens=True
            )
            
            return response.strip()
            
        except Exception as e:
            print(f"[CHATBOT] Error generating response with UserLM: {e}")
            print(f"[CHATBOT] Falling back to rule-based responses")
            return self._rule_based_response(user_message, db)
    
    def _rule_based_response(self, message: str, db: Session) -> str:
        """Rule-based fallback responses"""
        message_lower = message.lower()
        
        try:
            # Specific worker info (check for worker names FIRST - highest priority)
            workers = db.query(models.Worker).all()
            matched_worker = None
            for worker in workers:
                if worker.name.lower() in message_lower:
                    matched_worker = worker
                    break
            
            if matched_worker:
                response = f"📋 Profile: {matched_worker.name}\n\n"
                response += f"Performance Score: {matched_worker.performance_score*100:.0f}%\n"
                response += f"Experience: {matched_worker.experience} years\n"
                response += f"Fatigue Level: {matched_worker.fatigue_level*100:.0f}%\n"
                response += f"Hours/Week: {matched_worker.hours_per_week:.1f}\n\n"
                response += f"Skills ({len(matched_worker.skills)}):\n"
                for i, skill in enumerate(matched_worker.skills, 1):
                    response += f"  {i}. {skill}\n"
                
                # Add recommendation
                if matched_worker.fatigue_level < 0.3 and matched_worker.performance_score > 0.8:
                    response += f"\n✅ Status: Ready for demanding tasks"
                elif matched_worker.fatigue_level >= 0.7:
                    response += f"\n⚠️ Status: High fatigue - recommend rest or lighter tasks"
                else:
                    response += f"\n✓ Status: Available for standard assignments"
                
                return response
            
            # Health/Fatigue queries (check first before general worker queries)
            if any(word in message_lower for word in ['health', 'fatigue', 'tired', 'stress', 'low fatigue', 'high fatigue']):
                workers = db.query(models.Worker).all()
                low_fatigue = [w for w in workers if w.fatigue_level < 0.3]
                medium_fatigue = [w for w in workers if 0.3 <= w.fatigue_level < 0.7]
                high_fatigue = [w for w in workers if w.fatigue_level >= 0.7]
                
                if 'low' in message_lower:
                    response = f"Workers with Low Fatigue (<30%) - Ready for Work:\n\n"
                    for i, w in enumerate(low_fatigue[:10], 1):
                        response += f"{i}. {w.name} - Fatigue: {w.fatigue_level*100:.0f}%, Performance: {w.performance_score*100:.0f}%\n"
                    if len(low_fatigue) > 10:
                        response += f"\n...and {len(low_fatigue)-10} more workers"
                    response += f"\n\nTotal: {len(low_fatigue)} workers ready for demanding tasks"
                    return response
                elif 'high' in message_lower:
                    response = f"Workers with High Fatigue (≥70%) - Need Rest:\n\n"
                    if high_fatigue:
                        for i, w in enumerate(high_fatigue, 1):
                            response += f"{i}. {w.name} - Fatigue: {w.fatigue_level*100:.0f}%, Hours/week: {w.hours_per_week:.1f}\n"
                        response += f"\n⚠️ Recommendation: Assign lighter tasks or provide rest periods."
                    else:
                        response = "✅ Great news! No workers currently have high fatigue levels."
                    return response
                else:
                    return f"Worker Fatigue Status:\n- Low Fatigue: {len(low_fatigue)} workers\n- Medium Fatigue: {len(medium_fatigue)} workers\n- High Fatigue: {len(high_fatigue)} workers\n\n⚠️ Recommendation: Consider assigning lighter tasks to high-fatigue workers."
            
            # Skill-based queries (check for specific skills)
            elif any(word in message_lower for word in ['skill', 'iso', 'welding', 'cnc', 'quality', 'assembly', 'testing', 'inspection']):
                workers = db.query(models.Worker).all()
                
                # Extract skill query
                skill_query = None
                if 'iso' in message_lower:
                    skill_query = 'ISO Standards'
                elif 'welding' in message_lower:
                    skill_query = 'Welding'
                elif 'cnc' in message_lower:
                    skill_query = 'CNC'
                elif 'quality' in message_lower:
                    skill_query = 'Quality'
                elif 'assembly' in message_lower:
                    skill_query = 'Assembly'
                elif 'testing' in message_lower:
                    skill_query = 'Testing'
                
                if skill_query:
                    # Find workers with this skill (case-insensitive partial match)
                    matching_workers = [
                        w for w in workers 
                        if any(skill_query.lower() in skill.lower() for skill in w.skills)
                    ]
                    
                    if matching_workers:
                        response = f"Workers with {skill_query} skill: {len(matching_workers)} total\n\n"
                        for i, w in enumerate(matching_workers[:10], 1):
                            # Find the matching skills
                            matching_skills = [s for s in w.skills if skill_query.lower() in s.lower()]
                            response += f"{i}. {w.name}\n"
                            response += f"   Skills: {', '.join(matching_skills)}\n"
                            response += f"   Performance: {w.performance_score*100:.0f}%, Fatigue: {w.fatigue_level*100:.0f}%, Experience: {w.experience} years\n\n"
                        
                        if len(matching_workers) > 10:
                            response += f"...and {len(matching_workers)-10} more workers with {skill_query} skills"
                        
                        return response
                    else:
                        return f"No workers found with {skill_query} skill. Try asking about: Welding, CNC Operation, Quality Inspection, Assembly, Testing, ISO Standards, etc."
                else:
                    # General skill query
                    all_skills = {}
                    for worker in workers:
                        for skill in worker.skills:
                            all_skills[skill] = all_skills.get(skill, 0) + 1
                    
                    response = "Top Skills in Workforce:\n\n"
                    sorted_skills = sorted(all_skills.items(), key=lambda x: x[1], reverse=True)[:10]
                    for i, (skill, count) in enumerate(sorted_skills, 1):
                        response += f"{i}. {skill}: {count} workers\n"
                    
                    return response
            
            # Performance/Top Performers (check before general worker queries)
            elif any(phrase in message_lower for phrase in ['top perform', 'best perform', 'high perform', 'top worker']):
                workers = db.query(models.Worker).all()
                top_workers = sorted(workers, key=lambda w: w.performance_score, reverse=True)[:5]
                response = "Top Performing Workers:\n\n"
                for i, w in enumerate(top_workers, 1):
                    response += f"{i}. {w.name} - Performance: {w.performance_score*100:.0f}%, Fatigue: {w.fatigue_level*100:.0f}%, Experience: {w.experience} years\n"
                response += f"\nThese workers consistently exceed expectations and are ready for challenging assignments."
                return response
            
            # Worker queries
            elif any(word in message_lower for word in ['worker', 'workers', 'employee', 'employees']):
                workers = db.query(models.Worker).all()
                if 'how many' in message_lower or 'total' in message_lower:
                    return f"We currently have {len(workers)} workers in the system."
                elif 'available' in message_lower:
                    low_fatigue = [w for w in workers if w.fatigue_level < 0.3]
                    return f"{len(low_fatigue)} workers are available with low fatigue levels."
                else:
                    return f"We have {len(workers)} workers. I can help you find the best worker for a role, check availability, or view performance statistics."
            
            # Role queries
            elif any(word in message_lower for word in ['role', 'roles', 'position', 'positions']):
                roles = db.query(models.Role).all()
                if 'how many' in message_lower or 'total' in message_lower:
                    return f"We have {len(roles)} roles defined in the system."
                elif 'list' in message_lower:
                    response = "Available roles:\n"
                    for role in roles[:5]:
                        response += f"- {role.name}\n"
                    if len(roles) > 5:
                        response += f"...and {len(roles)-5} more"
                    return response
                else:
                    return f"We have {len(roles)} roles. Would you like to see the list or get recommendations for a specific role?"
            
            # Assignment queries
            elif any(word in message_lower for word in ['assignment', 'assignments', 'assigned']):
                assignments = db.query(models.Assignment).all()
                completed = sum(1 for a in assignments if a.success == True)
                pending = sum(1 for a in assignments if a.success is None)
                
                return f"Assignment Status:\n- Total: {len(assignments)}\n- Completed: {completed}\n- Pending: {pending}\n- Success Rate: {(completed/len(assignments)*100) if assignments else 0:.0f}%"
            
            # Task queries
            elif any(word in message_lower for word in ['task', 'tasks']):
                tasks = db.query(models.Task).all()
                completed = sum(1 for t in tasks if t.status == 'completed')
                in_progress = sum(1 for t in tasks if t.status == 'in_progress')
                pending = sum(1 for t in tasks if t.status == 'pending')
                
                return f"Task Status:\n- Total: {len(tasks)}\n- Completed: {completed}\n- In Progress: {in_progress}\n- Pending: {pending}"
            
            # Performance queries
            elif 'performance' in message_lower:
                workers = db.query(models.Worker).all()
                avg_performance = sum(w.performance_score for w in workers) / len(workers) if workers else 0
                high_performers = sum(1 for w in workers if w.performance_score > 0.8)
                
                return f"Performance Overview:\n- Average Performance: {avg_performance*100:.0f}%\n- High Performers (>80%): {high_performers}\n- Total Workers: {len(workers)}"
            
            # Recommendation queries
            elif any(word in message_lower for word in ['recommend', 'suggestion', 'best fit', 'assign']):
                return "I can help you find the best workers for any role! Please:\n1. Go to Dashboard\n2. Click 'Find Best Workers' on a role card\n3. The ML algorithm will show top recommendations based on skills, performance, and fatigue levels."
            
            # Help queries
            elif any(word in message_lower for word in ['help', 'what can you', 'how do']):
                return """I'm your AI assistant! I can help you with:

📊 **Data Queries:**
- Ask about workers, roles, assignments, or tasks
- Get performance statistics
- Check worker availability and fatigue levels

🎯 **Recommendations:**
- Find best workers for roles
- Identify training needs
- Optimize assignments

💡 **Examples:**
- "How many workers do we have?"
- "Who are the top performers?"
- "What's the assignment success rate?"
- "Show me workers with low fatigue"

Just ask me anything about your workforce!"""
            
            # Default response
            else:
                return "I can help you with information about workers, roles, assignments, and tasks. Try asking:\n\n- 'How many workers do we have?'\n- 'Who are the top performers?'\n- 'Show me workers with low fatigue'\n- 'What's the assignment success rate?'\n- 'Show me task status'\n\nWhat would you like to know?"
                
        except Exception as e:
            return f"I encountered an error: {e}. Please try asking about workers, roles, assignments, or tasks."

# Global chatbot instance
chatbot = SupervisorChatbot()

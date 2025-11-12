"""
Medical Triage Workflow Guide - Core Logic

⚠️ DISCLAIMER: This is a simplified demonstration for educational purposes.
Real medical systems require clinical expertise, regulatory approval, and
extensive validation. This is NOT production medical software.

This demonstrates the "Tool-as-Guide" pattern where the guide (not the AI)
controls the workflow through a state machine, ensuring protocol compliance.
"""

import uuid
from typing import Dict, Optional, List
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class TriageLevel(Enum):
    """Standard emergency triage levels"""
    IMMEDIATE = "Level 1 - Immediate (Life-threatening)"
    EMERGENCY = "Level 2 - Emergency (10 min)"
    URGENT = "Level 3 - Urgent (30 min)"
    SEMI_URGENT = "Level 4 - Semi-urgent (60 min)"
    NON_URGENT = "Level 5 - Non-urgent (120 min)"


@dataclass
class TriageSession:
    """Represents a triage session in progress"""
    session_id: str
    state: str = "START"
    
    # Red flag screening
    red_flags_checked: bool = False
    has_red_flags: bool = False
    red_flag_details: List[str] = field(default_factory=list)
    
    # Chief complaint
    chief_complaint: Optional[str] = None
    
    # Patient history
    medical_history: Dict = field(default_factory=dict)
    
    # Vital signs
    vitals: Dict = field(default_factory=dict)
    vitals_critical: bool = False
    
    # Assessment
    severity_score: int = 0
    triage_level: Optional[TriageLevel] = None
    recommendation: Optional[str] = None
    
    # Audit trail
    protocol_steps: List[Dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.now)
    
    def add_step(self, step: str, data: Dict):
        """Add a step to the audit trail"""
        self.protocol_steps.append({
            "step": step,
            "timestamp": datetime.now().isoformat(),
            "data": data
        })
    
    def to_dict(self) -> dict:
        """Convert session to dictionary"""
        return {
            "session_id": self.session_id,
            "state": self.state,
            "triage_level": self.triage_level.value if self.triage_level else None,
            "recommendation": self.recommendation,
            "protocol_steps": self.protocol_steps
        }


class MedicalTriageGuide:
    """
    Workflow guide for medical triage.
    
    This implements the "Tool-as-Guide" pattern:
    - The guide controls the workflow (WHAT to do)
    - The agent/LLM handles execution (HOW to do it)
    - Protocol compliance is enforced by the guide
    """
    
    # Red flag symptoms (require immediate escalation)
    RED_FLAGS = [
        "severe chest pain",
        "difficulty breathing",
        "loss of consciousness",
        "severe bleeding",
        "signs of stroke",
        "severe allergic reaction",
        "poisoning",
        "severe head injury"
    ]
    
    def __init__(self):
        self.sessions: Dict[str, TriageSession] = {}
    
    def start_triage(self) -> dict:
        """
        Start a new triage session.
        
        Returns instructions for the agent on what to do first.
        """
        session_id = str(uuid.uuid4())[:8]
        session = TriageSession(session_id=session_id, state="RED_FLAG_SCREENING")
        self.sessions[session_id] = session
        
        session.add_step("triage_started", {"session_id": session_id})
        
        return {
            "status": "in_progress",
            "session_id": session_id,
            "task": "screen_red_flags",
            "instructions_for_agent": (
                "CRITICAL: Before anything else, screen for emergency symptoms. This is mandatory protocol."
            ),
            "prompt": (
                "Before we begin, I need to ask about any immediate concerns:\n\n"
                "Are you experiencing any of the following RIGHT NOW:\n"
                "- Severe chest pain or pressure\n"
                "- Difficulty breathing or shortness of breath\n"
                "- Loss of consciousness or fainting\n"
                "- Severe bleeding\n"
                "- Signs of stroke (face drooping, arm weakness, speech difficulty)\n"
                "- Severe allergic reaction (swelling, difficulty swallowing)\n\n"
                "Please answer yes or no, and describe any symptoms."
            ),
            "required_data": ["symptoms_present", "symptom_details"],
            "protocol": "Emergency Department Triage Protocol - Red Flag Screening (Mandatory)"
        }
    
    def continue_triage(self, session_id: str, agent_report: dict) -> dict:
        """
        Process agent's report and provide next instructions.
        
        The agent reports back what it learned/did. The guide validates
        and decides the next step in the protocol.
        
        Args:
            session_id: The triage session ID
            agent_report: What the agent discovered/executed
                - For red flags: {"symptoms_detected": [...], "patient_statement": "..."}
                - For vitals: {"vitals": {...}, "critical_values": [...]}
                - etc.
        """
        if session_id not in self.sessions:
            return {
                "status": "error",
                "message": f"Session {session_id} not found. Please start a new triage."
            }
        
        session = self.sessions[session_id]
        
        # State machine - protocol enforcement
        if session.state == "RED_FLAG_SCREENING":
            return self._handle_red_flag_screening(session, agent_report)
        
        elif session.state == "CHIEF_COMPLAINT":
            return self._handle_chief_complaint(session, agent_report)
        
        elif session.state == "MEDICAL_HISTORY":
            return self._handle_medical_history(session, agent_report)
        
        elif session.state == "VITAL_SIGNS":
            return self._handle_vital_signs(session, agent_report)
        
        elif session.state == "SEVERITY_ASSESSMENT":
            return self._handle_severity_assessment(session, agent_report)
        
        elif session.state == "SAVE_RECORD":
            return self._handle_save_record(session, agent_report)
        
        else:
            return {
                "status": "error",
                "message": f"Unknown state: {session.state}"
            }
    
    def _handle_red_flag_screening(self, session: TriageSession, report: dict) -> dict:
        """Handle red flag screening results"""
        session.red_flags_checked = True
        
        # Get classification from agent's report
        classification = report.get("classification", {})
        symptoms = report.get("symptoms_detected", [])
        
        # Protocol: Check if agent's classifier flagged this as emergency
        requires_emergency = classification.get("requires_emergency_protocol", False)
        detected_red_flags = classification.get("critical_symptoms", [])
        
        session.add_step("red_flag_screening", {
            "symptoms_detected": symptoms,
            "severity": classification.get("severity", "unknown"),
            "red_flags": detected_red_flags
        })
        
        # EMERGENCY PROTOCOL - if classifier identified critical symptoms, escalate immediately
        if requires_emergency:
            session.has_red_flags = True
            session.red_flag_details = detected_red_flags
            session.state = "EMERGENCY_ESCALATION"
            session.triage_level = TriageLevel.IMMEDIATE
            session.recommendation = "IMMEDIATE EMERGENCY CARE REQUIRED"
            
            # Log the decision in audit trail
            session.add_step("emergency_escalation_activated", {
                "decision": "EMERGENCY_ESCALATION",
                "triage_level": TriageLevel.IMMEDIATE.value,
                "red_flags": detected_red_flags,
                "reason": "Critical symptoms detected by classifier"
            })
            
            # Move to record saving state
            session.state = "SAVE_RECORD"
            
            return {
                "status": "emergency_save_required",
                "session_id": session.session_id,
                "decision": "EMERGENCY_ESCALATION",
                "triage_level": TriageLevel.IMMEDIATE.value,
                "red_flags_detected": detected_red_flags,
                "task": "save_triage_record",
                "instructions_for_agent": (
                    "Emergency triage completed. Save the triage record to patient file before final response."
                ),
                "triage_data": {
                    "patient_id": report.get("medical_history", {}).get("patient_id", "P001"),
                    "complaint": report.get("patient_statement", ""),
                    "severity": classification.get("severity", "critical"),
                    "triage_level": TriageLevel.IMMEDIATE.value,
                    "red_flags": detected_red_flags
                },
                "protocol": "Emergency Escalation Protocol - Record Saving",
                "audit_trail": session.protocol_steps,
                "emergency_message": (
                    "🚨 EMERGENCY: Based on your symptoms, you need immediate medical attention.\n\n"
                    "Please do ONE of the following RIGHT NOW:\n"
                    "1. Call 911 (or your local emergency number)\n"
                    "2. Go to the nearest Emergency Department\n"
                    "3. If with someone, have them drive you to the ER\n\n"
                    "Do NOT wait. Do NOT drive yourself if symptoms worsen."
                )
            }
        
        # No red flags - continue with standard protocol
        session.state = "CHIEF_COMPLAINT"
        session.add_step("red_flag_screening_passed", {"result": "no_red_flags"})
        
        return {
            "status": "in_progress",
            "session_id": session.session_id,
            "task": "gather_chief_complaint",
            "instructions_for_agent": (
                "Red flag screening passed. Now gather the chief complaint. "
                "Ask the patient what brought them in today."
            ),
            "prompt": "Thank you. Now, what brings you in today? What is the main issue you're experiencing?",
            "required_data": ["chief_complaint", "symptom_description"],
            "protocol": "Standard Triage - Chief Complaint"
        }
    
    def _handle_chief_complaint(self, session: TriageSession, report: dict) -> dict:
        """Handle chief complaint gathering"""
        session.chief_complaint = report.get("chief_complaint", "")
        session.add_step("chief_complaint_gathered", report)
        
        session.state = "MEDICAL_HISTORY"
        
        return {
            "status": "in_progress",
            "session_id": session.session_id,
            "task": "check_medical_history",
            "instructions_for_agent": (
                "Use available tools to check patient's medical history. "
                "Look for: chronic conditions, medications, allergies, previous similar episodes. "
                "This helps assess risk factors."
            ),
            "prompt": "I'm checking your medical history. Do you have any chronic conditions, take any medications, or have any allergies I should know about?",
            "required_data": ["medical_history", "medications", "allergies"],
            "protocol": "Standard Triage - Medical History Review"
        }
    
    def _handle_medical_history(self, session: TriageSession, report: dict) -> dict:
        """Handle medical history check"""
        session.medical_history = report.get("medical_history", {})
        session.add_step("medical_history_checked", report)
        
        # Check if history increases urgency
        high_risk_conditions = report.get("high_risk_conditions", [])
        if high_risk_conditions:
            session.severity_score += 2
        
        session.state = "VITAL_SIGNS"
        
        return {
            "status": "in_progress",
            "session_id": session.session_id,
            "task": "get_vital_signs",
            "instructions_for_agent": (
                "MANDATORY: Obtain vital signs. Use available monitoring tools. "
                "Required: Blood pressure, heart rate, temperature, respiratory rate, oxygen saturation. "
                "Flag any critical values immediately."
            ),
            "prompt": "Now I need to check your vital signs. This is a required step for proper assessment.",
            "required_data": ["blood_pressure", "heart_rate", "temperature", "respiratory_rate", "oxygen_saturation"],
            "protocol": "Standard Triage - Vital Signs (Mandatory)"
        }
    
    def _handle_vital_signs(self, session: TriageSession, report: dict) -> dict:
        """Handle vital signs assessment"""
        vitals = report.get("vitals", {})
        critical_values = report.get("critical_values", [])
        
        session.vitals = vitals
        session.vitals_critical = len(critical_values) > 0
        session.add_step("vital_signs_obtained", {
            "vitals": vitals,
            "critical_values": critical_values
        })
        
        # Assess severity based on vitals
        if critical_values:
            session.severity_score += 3
        
        session.state = "SEVERITY_ASSESSMENT"
        
        return {
            "status": "in_progress",
            "session_id": session.session_id,
            "task": "assess_severity",
            "instructions_for_agent": (
                "All required data collected. Now assess overall severity and determine "
                "appropriate triage level and care recommendation."
            ),
            "data_for_assessment": {
                "red_flags": session.red_flag_details,
                "chief_complaint": session.chief_complaint,
                "medical_history": session.medical_history,
                "vitals": session.vitals,
                "severity_score": session.severity_score
            },
            "protocol": "Final Triage Assessment"
        }
    
    def _handle_severity_assessment(self, session: TriageSession, report: dict) -> dict:
        """Handle final severity assessment and recommendation"""
        # Use severity score to determine triage level
        if session.severity_score >= 5 or session.vitals_critical:
            session.triage_level = TriageLevel.EMERGENCY
            session.recommendation = "Emergency Department - within 10 minutes"
        elif session.severity_score >= 3:
            session.triage_level = TriageLevel.URGENT
            session.recommendation = "Urgent Care or ED - within 30 minutes"
        elif session.severity_score >= 2:
            session.triage_level = TriageLevel.SEMI_URGENT
            session.recommendation = "Urgent Care - within 60 minutes"
        else:
            session.triage_level = TriageLevel.NON_URGENT
            session.recommendation = "Primary care or telehealth - within 24 hours"
        
        session.add_step("triage_completed", {
            "triage_level": session.triage_level.value,
            "recommendation": session.recommendation
        })
        
        session.state = "COMPLETE"
        
        return {
            "status": "complete",
            "session_id": session.session_id,
            "triage_level": session.triage_level.value,
            "recommendation": session.recommendation,
            "message": self._generate_final_message(session),
            "protocol_compliance": {
                "all_steps_completed": True,
                "red_flags_screened": session.red_flags_checked,
                "vitals_obtained": bool(session.vitals),
                "history_reviewed": bool(session.medical_history)
            },
            "audit_trail": session.protocol_steps
        }
    
    def _handle_save_record(self, session: TriageSession, report: dict) -> dict:
        """Handle saving triage record to patient file"""
        # Log that record was saved
        session.add_step("triage_record_saved", {
            "record_id": report.get("record_id"),
            "status": report.get("status")
        })
        
        # Complete the emergency escalation
        session.state = "COMPLETE"
        
        return {
            "status": "emergency",
            "session_id": session.session_id,
            "decision": "EMERGENCY_ESCALATION",
            "triage_level": session.triage_level.value,
            "red_flags_detected": session.red_flag_details,
            "task": "emergency_response",
            "instructions_for_agent": (
                "Triage record saved. Emergency protocol complete."
            ),
            "message": (
                "🚨 EMERGENCY: Based on your symptoms, you need immediate medical attention.\n\n"
                "Please do ONE of the following RIGHT NOW:\n"
                "1. Call 911 (or your local emergency number)\n"
                "2. Go to the nearest Emergency Department\n"
                "3. If with someone, have them drive you to the ER\n\n"
                "Do NOT wait. Do NOT drive yourself if symptoms worsen."
            ),
            "protocol": "Emergency Escalation Protocol - Complete",
            "audit_trail": session.protocol_steps
        }
    
    def _generate_final_message(self, session: TriageSession) -> str:
        """Generate final triage message"""
        return f"""
TRIAGE ASSESSMENT COMPLETE

Triage Level: {session.triage_level.value}
Recommendation: {session.recommendation}

Based on:
- Symptoms: {session.chief_complaint}
- Vital signs: {'Critical values detected' if session.vitals_critical else 'Within normal limits'}
- Medical history: {'Risk factors present' if session.medical_history.get('high_risk') else 'Reviewed'}

Next Steps:
{self._get_next_steps(session.triage_level)}

⚠️ If symptoms worsen or new severe symptoms develop, seek emergency care immediately.

Protocol Compliance: All required steps completed ✓
        """.strip()
    
    def _get_next_steps(self, level: TriageLevel) -> str:
        """Get next steps based on triage level"""
        if level == TriageLevel.IMMEDIATE:
            return "Call 911 or go to Emergency Department IMMEDIATELY"
        elif level == TriageLevel.EMERGENCY:
            return "Go to Emergency Department within 10 minutes"
        elif level == TriageLevel.URGENT:
            return "Visit Urgent Care or ED within 30 minutes"
        elif level == TriageLevel.SEMI_URGENT:
            return "Visit Urgent Care within 1 hour"
        else:
            return "Schedule appointment with primary care or use telehealth within 24 hours"
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get current session state"""
        if session_id in self.sessions:
            return self.sessions[session_id].to_dict()
        return None
    
    def cancel_session(self, session_id: str) -> dict:
        """Cancel a triage session"""
        if session_id in self.sessions:
            del self.sessions[session_id]
            return {
                "status": "cancelled",
                "message": "Triage session cancelled."
            }
        return {
            "status": "error",
            "message": f"Session {session_id} not found."
        }



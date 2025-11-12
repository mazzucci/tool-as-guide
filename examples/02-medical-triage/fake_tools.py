"""
Fake Medical Tools for Demo

⚠️ DISCLAIMER: These are mock tools for demonstration purposes only.
They return simulated data and should NEVER be used for real medical decisions.

These tools simulate what a real medical system might have:
- Patient medical records database
- Vital signs monitoring system
- Allergy database
- etc.
"""

from typing import Dict, List, Optional
import random


class SymptomClassifier:
    """
    Simulates an AI-powered symptom classification system.
    
    In a real system, this could be:
    - A trained ML model
    - A rule-based expert system
    - Integration with clinical decision support tools
    
    This tool contains domain knowledge about symptom severity.
    """
    
    # High-risk symptoms that require immediate attention
    CRITICAL_SYMPTOMS = [
        "chest pain", "crushing chest pain", "severe chest pain",
        "difficulty breathing", "shortness of breath", "cannot breathe",
        "severe bleeding", "uncontrolled bleeding",
        "altered consciousness", "confusion", "unresponsive",
        "severe head injury", "stroke symptoms",
        "severe abdominal pain", "suspected heart attack"
    ]
    
    # Moderate symptoms requiring prompt evaluation
    MODERATE_SYMPTOMS = [
        "persistent cough", "fever", "vomiting",
        "moderate pain", "dizziness", "weakness",
        "rash", "swelling"
    ]
    
    def classify_symptoms(self, patient_statement: str, medical_history: Dict) -> Dict:
        """
        Classify symptom severity based on patient statement and history.
        
        Returns:
            Dict with classification results including:
            - severity: "critical", "moderate", "low"
            - red_flags: List of detected red flags
            - risk_factors: Additional risk factors from history
            - recommendation: Clinical recommendation
        """
        statement_lower = patient_statement.lower()
        
        # Check for critical symptoms
        detected_critical = []
        for symptom in self.CRITICAL_SYMPTOMS:
            if symptom in statement_lower:
                detected_critical.append(symptom)
        
        # Check for moderate symptoms
        detected_moderate = []
        for symptom in self.MODERATE_SYMPTOMS:
            if symptom in statement_lower:
                detected_moderate.append(symptom)
        
        # Assess risk based on medical history
        risk_factors = []
        if medical_history.get("high_risk"):
            risk_factors.append("high-risk medical history")
        if medical_history.get("cardiac_history"):
            risk_factors.append("cardiac history")
        if medical_history.get("chronic_conditions"):
            risk_factors.extend(medical_history["chronic_conditions"])
        
        # Determine overall severity
        if detected_critical:
            severity = "critical"
            recommendation = "immediate_emergency_care"
        elif detected_moderate and risk_factors:
            severity = "moderate-high"
            recommendation = "urgent_evaluation"
        elif detected_moderate:
            severity = "moderate"
            recommendation = "prompt_evaluation"
        else:
            severity = "low"
            recommendation = "routine_assessment"
        
        return {
            "severity": severity,
            "critical_symptoms": detected_critical,
            "moderate_symptoms": detected_moderate,
            "risk_factors": risk_factors,
            "recommendation": recommendation,
            "requires_emergency_protocol": len(detected_critical) > 0
        }


class MedicalDatabase:
    """
    Simulates a medical records database.
    
    In a real system, this would query actual patient records,
    medical history, previous diagnoses, etc.
    """
    
    # Simulated patient database
    PATIENTS = {
        "P001": {
            "name": "Test Patient",
            "age": 55,
            "conditions": ["hypertension", "high cholesterol"],
            "cardiac_history": True,
            "previous_mi": False,
            "medications": ["lisinopril", "atorvastatin"],
            "allergies": ["penicillin"],
            "last_visit": "2024-09-15"
        },
        "P002": {
            "name": "Test Patient 2",
            "age": 32,
            "conditions": [],
            "cardiac_history": False,
            "previous_mi": False,
            "medications": [],
            "allergies": [],
            "last_visit": "2024-10-01"
        }
    }
    
    def check_conditions(self, symptoms: str) -> Dict:
        """
        Check if patient has conditions related to symptoms.
        
        In demo, returns simulated data. In real system,
        would query actual database.
        """
        # Simple simulation based on symptoms
        if any(word in symptoms.lower() for word in ["chest", "pain", "cardiac", "heart"]):
            # High-risk patient
            return {
                "patient_id": "P001",
                "chronic_conditions": ["hypertension", "high cholesterol"],
                "cardiac_history": True,
                "previous_mi": False,
                "risk_factors": ["age > 50", "hypertension", "family history"],
                "high_risk": True
            }
        else:
            # Lower-risk patient
            return {
                "patient_id": "P002",
                "chronic_conditions": [],
                "cardiac_history": False,
                "previous_mi": False,
                "risk_factors": [],
                "high_risk": False
            }
    
    def check_allergies(self, patient_id: str = "P001") -> List[str]:
        """Check patient allergies"""
        patient = self.PATIENTS.get(patient_id, {})
        return patient.get("allergies", [])
    
    def get_medications(self, patient_id: str = "P001") -> List[str]:
        """Get current medications"""
        patient = self.PATIENTS.get(patient_id, {})
        return patient.get("medications", [])
    
    def save_triage_record(self, patient_id: str, triage_data: Dict) -> Dict:
        """
        Save triage encounter to patient's medical record.
        
        In a real system, this would write to the database.
        For demo, we just simulate success.
        """
        return {
            "status": "saved",
            "patient_id": patient_id,
            "record_id": f"TRIAGE-{random.randint(1000, 9999)}",
            "saved_data": {
                "complaint": triage_data.get("complaint"),
                "severity": triage_data.get("severity"),
                "triage_level": triage_data.get("triage_level"),
                "red_flags": triage_data.get("red_flags", [])
            },
            "message": "Triage record saved to patient file"
        }


class VitalsMonitor:
    """
    Simulates a vital signs monitoring system.
    
    In a real system, this would interface with actual monitoring
    equipment (BP cuff, pulse oximeter, thermometer, etc.)
    """
    
    def get_vitals(self, patient_id: str = "P001", scenario: str = "normal") -> Dict:
        """
        Get patient vital signs.
        
        Args:
            patient_id: Patient identifier
            scenario: "normal", "elevated", or "critical" for demo purposes
        
        Returns:
            Dict with vital signs
        """
        if scenario == "critical":
            # Critical vitals (emergency)
            return {
                "blood_pressure": {
                    "systolic": 180,
                    "diastolic": 110,
                    "unit": "mmHg",
                    "status": "CRITICAL"
                },
                "heart_rate": {
                    "bpm": 120,
                    "unit": "bpm",
                    "status": "CRITICAL"
                },
                "respiratory_rate": {
                    "rate": 28,
                    "unit": "breaths/min",
                    "status": "ELEVATED"
                },
                "temperature": {
                    "value": 98.6,
                    "unit": "°F",
                    "status": "NORMAL"
                },
                "oxygen_saturation": {
                    "value": 92,
                    "unit": "%",
                    "status": "LOW"
                },
                "timestamp": "2024-11-11T16:30:00Z"
            }
        
        elif scenario == "elevated":
            # Elevated but not critical
            return {
                "blood_pressure": {
                    "systolic": 145,
                    "diastolic": 92,
                    "unit": "mmHg",
                    "status": "ELEVATED"
                },
                "heart_rate": {
                    "bpm": 95,
                    "unit": "bpm",
                    "status": "NORMAL"
                },
                "respiratory_rate": {
                    "rate": 18,
                    "unit": "breaths/min",
                    "status": "NORMAL"
                },
                "temperature": {
                    "value": 99.2,
                    "unit": "°F",
                    "status": "SLIGHTLY_ELEVATED"
                },
                "oxygen_saturation": {
                    "value": 96,
                    "unit": "%",
                    "status": "NORMAL"
                },
                "timestamp": "2024-11-11T16:30:00Z"
            }
        
        else:  # normal
            return {
                "blood_pressure": {
                    "systolic": 120,
                    "diastolic": 80,
                    "unit": "mmHg",
                    "status": "NORMAL"
                },
                "heart_rate": {
                    "bpm": 72,
                    "unit": "bpm",
                    "status": "NORMAL"
                },
                "respiratory_rate": {
                    "rate": 16,
                    "unit": "breaths/min",
                    "status": "NORMAL"
                },
                "temperature": {
                    "value": 98.6,
                    "unit": "°F",
                    "status": "NORMAL"
                },
                "oxygen_saturation": {
                    "value": 98,
                    "unit": "%",
                    "status": "NORMAL"
                },
                "timestamp": "2024-11-11T16:30:00Z"
            }
    
    def assess_vitals(self, vitals: Dict) -> List[str]:
        """
        Assess vitals and return list of critical findings.
        
        This is what the agent would do - analyze the data.
        """
        critical_findings = []
        
        # Check BP
        bp = vitals.get("blood_pressure", {})
        if bp.get("status") == "CRITICAL":
            critical_findings.append("Severely elevated blood pressure")
        
        # Check HR
        hr = vitals.get("heart_rate", {})
        if hr.get("status") == "CRITICAL":
            critical_findings.append("Tachycardia (elevated heart rate)")
        
        # Check O2
        o2 = vitals.get("oxygen_saturation", {})
        if o2.get("status") == "LOW":
            critical_findings.append("Low oxygen saturation")
        
        return critical_findings


class PatientInterviewSimulator:
    """
    Simulates patient responses for demo purposes.
    
    In a real system, this would be actual patient interaction
    (chat interface, voice, etc.)
    """
    
    SCENARIOS = {
        "chest_pain_emergency": {
            "initial": "I have severe chest pain that started 30 minutes ago",
            "red_flags": "Yes, severe chest pain and some difficulty breathing",
            "complaint": "Crushing chest pain, radiating to left arm",
            "history": "I have high blood pressure and high cholesterol"
        },
        "minor_issue": {
            "initial": "I have a mild headache for the past 2 hours",
            "red_flags": "No, none of those symptoms",
            "complaint": "Just a headache, nothing severe",
            "history": "No chronic conditions, generally healthy"
        }
    }
    
    def get_response(self, scenario: str, question_type: str) -> str:
        """Get simulated patient response"""
        scenario_data = self.SCENARIOS.get(scenario, self.SCENARIOS["minor_issue"])
        return scenario_data.get(question_type, "I don't know")


# Convenience function for demos
def get_demo_scenario(scenario_type: str = "emergency"):
    """
    Get a complete demo scenario with consistent data.
    
    Args:
        scenario_type: "emergency" or "normal"
    
    Returns:
        Dict with all simulated data for the scenario
    """
    if scenario_type == "emergency":
        return {
            "patient_response": "I have severe chest pain that started 30 minutes ago",
            "db_data": MedicalDatabase().check_conditions("chest pain"),
            "vitals": VitalsMonitor().get_vitals(scenario="critical"),
            "scenario_name": "Cardiac Emergency"
        }
    else:
        return {
            "patient_response": "I have a mild headache",
            "db_data": MedicalDatabase().check_conditions("headache"),
            "vitals": VitalsMonitor().get_vitals(scenario="normal"),
            "scenario_name": "Minor Complaint"
        }


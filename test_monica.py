"""
Test script for Monica Voice Agent with Twilio
Run this to test the voice interview system
"""
import requests
import time
import os
from dotenv import load_dotenv

load_dotenv()

API_BASE = "http://localhost:8000/api/v1/monica"

def test_voice_interview():
    """Test the complete voice interview flow"""
    
    print("=" * 60)
    print("Monica Voice Interview Test")
    print("=" * 60)
    
    # Get your phone number
    phone = input("\nEnter your phone number (format: +1234567890): ").strip()
    if not phone.startswith("+"):
        print("❌ Phone number must start with + and country code")
        return
    
    name = input("Enter candidate name: ").strip() or "Test Candidate"
    
    print(f"\n📞 Starting voice interview for {name}...")
    
    # Start the call
    try:
        response = requests.post(
            f"{API_BASE}/start-call",
            json={
                "candidate_name": name,
                "candidate_phone": phone,
                "position": "software_engineer"
            },
            timeout=30
        )
        
        if response.status_code != 200:
            print(f"❌ Error: {response.status_code}")
            print(response.text)
            return
        
        data = response.json()
        
        if not data.get("success"):
            print(f"❌ Failed to start call: {data.get('error')}")
            return
        
        session_id = data["session_id"]
        call_sid = data.get("call_sid")
        
        print(f"✅ Call initiated successfully!")
        print(f"   Session ID: {session_id}")
        print(f"   Call SID: {call_sid}")
        print(f"\n📱 You should receive a call shortly...")
        print(f"   Answer the call and respond to Monica's questions")
        
        # Monitor the interview progress
        print(f"\n⏳ Monitoring interview progress...")
        
        for i in range(30):  # Check for 5 minutes max
            time.sleep(10)
            
            status_response = requests.get(f"{API_BASE}/status/{session_id}")
            if status_response.status_code == 200:
                status = status_response.json()
                if status.get("success"):
                    progress = status.get("progress", 0)
                    current_q = status.get("current_question", 0)
                    total_q = status.get("total_questions", 0)
                    interview_status = status.get("status", "unknown")
                    
                    print(f"   Progress: {progress:.0f}% - Question {current_q}/{total_q} - Status: {interview_status}")
                    
                    if interview_status == "completed":
                        print(f"\n✅ Interview completed!")
                        break
        
        # Get the final report
        print(f"\n📊 Fetching interview report...")
        time.sleep(2)
        
        report_response = requests.get(f"{API_BASE}/report/{session_id}")
        if report_response.status_code == 200:
            report = report_response.json()
            if report.get("success"):
                print(f"\n" + "=" * 60)
                print(f"INTERVIEW REPORT")
                print(f"=" * 60)
                print(f"Session ID: {report['session_id']}")
                print(f"Overall Score: {report['overall_score']}")
                print(f"\nStrengths:")
                for s in report['strengths']:
                    print(f"  • {s}")
                print(f"\nConcerns:")
                for c in report.get('concerns', []):
                    print(f"  • {c}")
                print(f"\nSummary:")
                print(f"  {report['summary']}")
                print(f"\nTranscript:")
                for idx, text in enumerate(report['transcript'], 1):
                    print(f"  {idx}. {text}")
                print(f"=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("❌ Error: Could not connect to the API")
        print("   Make sure the server is running on http://localhost:8000")
    except Exception as e:
        print(f"❌ Error: {e}")


if __name__ == "__main__":
    test_voice_interview()

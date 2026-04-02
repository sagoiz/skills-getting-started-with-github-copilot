import pytest
from fastapi.testclient import TestClient
import sys
from pathlib import Path

# Add src directory to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import app, activities


@pytest.fixture
def client():
    """Create a test client for the FastAPI app"""
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    """Reset activities to initial state before each test"""
    # Store original state
    original_state = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Practice basketball skills and compete in games",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["alex@mergington.edu"]
        },
        "Soccer Club": {
            "description": "Train for soccer matches and improve fitness",
            "schedule": "Mondays and Wednesdays, 3:00 PM - 4:30 PM",
            "max_participants": 22,
            "participants": ["liam@mergington.edu"]
        },
        "Art Club": {
            "description": "Explore various art forms and create masterpieces",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 10,
            "participants": ["ava@mergington.edu"]
        },
        "Drama Club": {
            "description": "Act in plays and improve public speaking",
            "schedule": "Fridays, 4:00 PM - 6:00 PM",
            "max_participants": 18,
            "participants": ["mia@mergington.edu"]
        },
        "Debate Club": {
            "description": "Engage in debates and develop critical thinking",
            "schedule": "Mondays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["noah@mergington.edu"]
        },
        "Science Club": {
            "description": "Conduct experiments and learn about science",
            "schedule": "Thursdays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["isabella@mergington.edu"]
        }
    }
    
    # Clear and repopulate activities
    activities.clear()
    activities.update(original_state)
    yield


@pytest.fixture
def sample_email():
    """Provide a sample email for testing"""
    return "michael@mergington.edu"


@pytest.fixture
def sample_activity():
    """Provide a sample activity name"""
    return "Chess Club"


@pytest.fixture
def new_email():
    """Provide a new email not in the system"""
    return "newstudent@mergington.edu"
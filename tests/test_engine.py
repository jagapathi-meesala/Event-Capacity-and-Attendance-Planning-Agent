import unittest
from core.engine import estimate_attendance, generate_report

class EventPlanningTests(unittest.TestCase):
    def sample(self, registrations=100, rate=0.8, capacity=100):
        return {"event":{"name":"Campus Workshop","registrations":registrations,"expected_attendance_rate":rate},
                "venue":{"name":"Main Hall","approved_capacity":capacity}}
    def test_estimate(self):
        result = estimate_attendance(self.sample())
        self.assertEqual(result["attendance_estimate"], 80)
        self.assertEqual(result["status"], "within_capacity")
    def test_capacity_exceeded(self):
        self.assertEqual(estimate_attendance(self.sample(200, 0.8, 100))["status"], "capacity_exceeded")
    def test_at_capacity(self):
        self.assertEqual(estimate_attendance(self.sample(100, 1.0, 100))["status"], "at_capacity")
    def test_zero_registrations(self):
        self.assertEqual(estimate_attendance(self.sample(0, 0.5, 100))["attendance_estimate"], 0)
    def test_invalid_root(self):
        self.assertEqual(estimate_attendance([])["status"], "needs_input_correction")
    def test_invalid_rate(self):
        self.assertTrue(estimate_attendance(self.sample(100, 1.2, 100))["validation_issues"])
    def test_negative_registrations(self):
        self.assertTrue(estimate_attendance(self.sample(-1, 0.5, 100))["validation_issues"])
    def test_invalid_capacity(self):
        self.assertTrue(estimate_attendance(self.sample(10, 0.5, 0))["validation_issues"])
    def test_human_review_always_required(self):
        self.assertTrue(estimate_attendance(self.sample())["human_review_required"])
    def test_report_agent_name(self):
        self.assertEqual(generate_report(self.sample())["agent"], "event-capacity-attendance-planning-agent")

if __name__ == "__main__":
    unittest.main()

"""
Policy Compliance Agent
-----------------------
A simple rule-based agent that evaluates synthetic employee
security activity against predefined company policies.

Features:
1. Generates synthetic employee data
2. Evaluates multiple compliance rules
3. Assigns COMPLIANT / NON-COMPLIANT / REVIEW REQUIRED
4. Calculates compliance score
5. Provides recommendations
6. Generates a summary report
"""

import random


# ============================================================
# 1. POLICY DEFINITIONS
# ============================================================

POLICIES = {
    "MFA": {
        "description": "Multi-Factor Authentication must be enabled."
    },
    "PASSWORD": {
        "description": "Password must not be older than 60 days."
    },
    "FAILED_LOGIN": {
        "description": "More than 5 failed login attempts requires investigation."
    },
    "DEVICE": {
        "description": "Employee must use an approved device."
    },
    "LOCATION": {
        "description": "Login from an unknown location requires review."
    }
}


# ============================================================
# 2. SYNTHETIC DATA GENERATION
# ============================================================

def generate_synthetic_data(number_of_employees=10):
    """
    Generates fake employee security activity.
    """

    locations = ["India", "USA", "UK", "Singapore", "Unknown"]

    employees = []

    for i in range(1, number_of_employees + 1):

        employee = {
            "employee_id": f"EMP{i:03d}",
            "name": f"Employee_{i}",
            "mfa_enabled": random.choice([True, True, True, False]),
            "password_age": random.randint(10, 100),
            "failed_logins": random.randint(0, 10),
            "approved_device": random.choice(
                [True, True, True, False]
            ),
            "login_location": random.choice(locations)
        }

        employees.append(employee)

    return employees


# ============================================================
# 3. POLICY COMPLIANCE AGENT
# ============================================================

class PolicyComplianceAgent:

    def __init__(self):
        self.total_employees = 0
        self.compliant = 0
        self.non_compliant = 0
        self.review_required = 0

    # --------------------------------------------------------
    # MFA RULE
    # --------------------------------------------------------

    def check_mfa(self, employee):

        if employee["mfa_enabled"]:
            return True, None

        return False, "MFA is disabled."

    # --------------------------------------------------------
    # PASSWORD RULE
    # --------------------------------------------------------

    def check_password(self, employee):

        if employee["password_age"] <= 60:
            return True, None

        return False, (
            f"Password is {employee['password_age']} days old. "
            "Maximum allowed is 60 days."
        )

    # --------------------------------------------------------
    # FAILED LOGIN RULE
    # --------------------------------------------------------

    def check_failed_logins(self, employee):

        if employee["failed_logins"] <= 5:
            return True, None

        return False, (
            f"{employee['failed_logins']} failed login attempts detected. "
            "Investigation is required."
        )

    # --------------------------------------------------------
    # DEVICE RULE
    # --------------------------------------------------------

    def check_device(self, employee):

        if employee["approved_device"]:
            return True, None

        return False, "Unapproved device detected."

    # --------------------------------------------------------
    # LOCATION RULE
    # --------------------------------------------------------

    def check_location(self, employee):

        if employee["login_location"] != "Unknown":
            return True, None

        return False, "Login originated from an unknown location."

    # ========================================================
    # EVALUATE EMPLOYEE
    # ========================================================

    def evaluate_employee(self, employee):

        violations = []
        review_reasons = []

        # Check MFA
        passed, reason = self.check_mfa(employee)

        if not passed:
            violations.append(reason)

        # Check password
        passed, reason = self.check_password(employee)

        if not passed:
            violations.append(reason)

        # Check failed login attempts
        passed, reason = self.check_failed_logins(employee)

        if not passed:
            review_reasons.append(reason)

        # Check device
        passed, reason = self.check_device(employee)

        if not passed:
            violations.append(reason)

        # Check location
        passed, reason = self.check_location(employee)

        if not passed:
            review_reasons.append(reason)

        # ----------------------------------------------------
        # Determine final status
        # ----------------------------------------------------

        if violations:

            status = "NON-COMPLIANT"

        elif review_reasons:

            status = "REVIEW REQUIRED"

        else:

            status = "COMPLIANT"

        # ----------------------------------------------------
        # Calculate compliance score
        # ----------------------------------------------------

        total_rules = 5
        failed_rules = len(violations) + len(review_reasons)

        score = ((total_rules - failed_rules) / total_rules) * 100

        # ----------------------------------------------------
        # Recommendations
        # ----------------------------------------------------

        recommendations = []

        for violation in violations:

            if "MFA" in violation:
                recommendations.append(
                    "Enable Multi-Factor Authentication."
                )

            if "Password" in violation:
                recommendations.append(
                    "Force the employee to change the password."
                )

            if "Unapproved device" in violation:
                recommendations.append(
                    "Block the unapproved device and use an approved device."
                )

        for reason in review_reasons:

            if "failed login" in reason:
                recommendations.append(
                    "Investigate failed login attempts and check for brute-force activity."
                )

            if "unknown location" in reason:
                recommendations.append(
                    "Verify the employee's location and investigate the login."
                )

        return {
            "employee_id": employee["employee_id"],
            "name": employee["name"],
            "status": status,
            "score": score,
            "violations": violations,
            "review_reasons": review_reasons,
            "recommendations": recommendations
        }

    # ========================================================
    # RUN AGENT
    # ========================================================

    def run(self, employees):

        self.total_employees = len(employees)

        results = []

        for employee in employees:

            result = self.evaluate_employee(employee)

            results.append(result)

            if result["status"] == "COMPLIANT":
                self.compliant += 1

            elif result["status"] == "NON-COMPLIANT":
                self.non_compliant += 1

            elif result["status"] == "REVIEW REQUIRED":
                self.review_required += 1

        return results

    # ========================================================
    # DISPLAY REPORT
    # ========================================================

    def display_report(self, employees, results):

        print("\n")
        print("=" * 70)
        print("           POLICY COMPLIANCE AGENT")
        print("=" * 70)

        print("\nPOLICIES BEING CHECKED:")
        print("-" * 70)

        for name, policy in POLICIES.items():

            print(f"{name}: {policy['description']}")

        print("\n")
        print("=" * 70)
        print("              EMPLOYEE COMPLIANCE REPORT")
        print("=" * 70)

        for employee, result in zip(employees, results):

            print("\nEmployee ID :", result["employee_id"])
            print("Name        :", result["name"])

            print("MFA         :", 
                  "Enabled" if employee["mfa_enabled"] else "Disabled")

            print("Password Age:",
                  f"{employee['password_age']} days")

            print("Failed Login:",
                  employee["failed_logins"])

            print("Device      :",
                  "Approved" if employee["approved_device"]
                  else "Unapproved")

            print("Location    :",
                  employee["login_location"])

            print("Compliance Score:",
                  f"{result['score']:.2f}%")

            print("Status:",
                  result["status"])

            if result["violations"]:

                print("\nPolicy Violations:")

                for violation in result["violations"]:
                    print("  -", violation)

            if result["review_reasons"]:

                print("\nReview Required:")

                for reason in result["review_reasons"]:
                    print("  -", reason)

            if result["recommendations"]:

                print("\nRecommended Actions:")

                for recommendation in result["recommendations"]:
                    print("  -", recommendation)

            print("-" * 70)

        # ====================================================
        # SUMMARY
        # ====================================================

        print("\n")
        print("=" * 70)
        print("                    SUMMARY")
        print("=" * 70)

        print("Total Employees :", self.total_employees)
        print("Compliant       :", self.compliant)
        print("Non-Compliant   :", self.non_compliant)
        print("Review Required :", self.review_required)

        if self.total_employees > 0:

            compliance_rate = (
                self.compliant / self.total_employees
            ) * 100

            print(
                f"Overall Compliance Rate: {compliance_rate:.2f}%"
            )

        print("=" * 70)


# ============================================================
# 4. MAIN PROGRAM
# ============================================================

def main():

    print("\nStarting Policy Compliance Agent...")

    # Generate synthetic data
    employees = generate_synthetic_data(10)

    # Create agent
    agent = PolicyComplianceAgent()

    # Run compliance evaluation
    results = agent.run(employees)

    # Display final report
    agent.display_report(employees, results)


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()
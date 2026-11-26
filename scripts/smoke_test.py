import argparse
import json
import os
import sys
import time
from datetime import datetime, timezone
import requests


def wait_for_health(base_url, timeout=60, interval=3):
    """Poll /health until the service reports healthy or timeout expires."""
    deadline = time.time() + timeout
    last_error = "No response received"
    while time.time() < deadline:
        try:
            resp = requests.get(f"{base_url}/health", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                if data.get("status") == "healthy" and data.get("database") == "connected":
                    return True, data
                last_error = f"Unexpected payload: {data}"
            else:
                last_error = f"HTTP {resp.status_code}"
        except Exception as exc:
            last_error = str(exc)
        time.sleep(interval)
    return False, {"error": last_error}


def run_smoke_tests(base_url, username, password, report_path):
    results = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "target_url": base_url,
        "checks": [],
        "verdict": "FAILED",
    }

    # Check 1: /health endpoint & DB connectivity
    health_ok, health_payload = wait_for_health(base_url)
    results["checks"].append({
        "name": "GET /health (Service & MySQL Connectivity)",
        "passed": health_ok,
        "details": health_payload,
    })
    if not health_ok:
        save_report(results, report_path)
        return False

    session = requests.Session()

    # Check 2: Public login page renders
    try:
        login_get = session.get(f"{base_url}/auth/login", timeout=10)
        login_page_ok = login_get.status_code == 200 and "ISGS" in login_get.text
        results["checks"].append({
            "name": "GET /auth/login (Public UI Render)",
            "passed": login_page_ok,
            "status_code": login_get.status_code,
        })
        if not login_page_ok:
            save_report(results, report_path)
            return False
    except Exception as exc:
        results["checks"].append({"name": "GET /auth/login", "passed": False, "error": str(exc)})
        save_report(results, report_path)
        return False

    # Check 3: Admin authentication & protected dashboard access
    try:
        login_post = session.post(
            f"{base_url}/auth/login",
            data={"username": username, "password": password},
            allow_redirects=True,
            timeout=10,
        )
        dashboard_ok = (
            login_post.status_code == 200
            and "Tableau de Bord" in login_post.text
        )
        results["checks"].append({
            "name": "POST /auth/login -> GET / (Authenticated Dashboard)",
            "passed": dashboard_ok,
            "status_code": login_post.status_code,
        })
        if not dashboard_ok:
            save_report(results, report_path)
            return False
    except Exception as exc:
        results["checks"].append({"name": "POST /auth/login", "passed": False, "error": str(exc)})
        save_report(results, report_path)
        return False

    # Check 4: Protected Students module query against MySQL
    try:
        students_resp = session.get(f"{base_url}/students/", timeout=10)
        students_ok = students_resp.status_code == 200 and "STD-2026-001" in students_resp.text
        results["checks"].append({
            "name": "GET /students/ (Authenticated MySQL Read)",
            "passed": students_ok,
            "status_code": students_resp.status_code,
        })
        if not students_ok:
            save_report(results, report_path)
            return False
    except Exception as exc:
        results["checks"].append({"name": "GET /students/", "passed": False, "error": str(exc)})
        save_report(results, report_path)
        return False

    results["verdict"] = "PASSED"
    save_report(results, report_path)
    return True


def save_report(results, report_path):
    os.makedirs(os.path.dirname(report_path), exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Automated Smoke Test Suite")
    parser.add_argument("--url", default="http://localhost:5000", help="Base URL of running app")
    parser.add_argument("--username", default="admin", help="Login username")
    parser.add_argument("--password", default="admin123", help="Login password")
    parser.add_argument("--report", default="artifacts/smoke_test_report.json", help="Output report path")
    args = parser.parse_args()

    print(f"=== Running Smoke Tests against {args.url} ===")
    success = run_smoke_tests(args.url, args.username, args.password, args.report)

    for check in json.load(open(args.report, encoding="utf-8"))["checks"]:
        status_label = "PASSED" if check["passed"] else "FAILED"
        print(f"[{status_label}] {check['name']}")

    if success:
        print("\nSMOKE TEST SUITE RESULT: PASSED")
        sys.exit(0)
    else:
        print("\nSMOKE TEST SUITE RESULT: FAILED")
        sys.exit(1)
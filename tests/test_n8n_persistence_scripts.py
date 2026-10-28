#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite: test_n8n_persistence_scripts.py
Empirical Verification Test Suite for Milestone 5 (R5: n8n Windows Service Persistence & Control Scripts)
Healing Touch Egypt (هيلينج تاتش مصر)

Verifies:
1. File Existence & Layout Compliance (scripts/run_n8n_silent.vbs, start_n8n.bat, stop_n8n.bat, status_n8n.bat, scripts/setup_n8n_service.bat)
2. CRLF Line Ending Compliance for Windows Batch & VBScript
3. Script Syntax, Configuration Constants & Safety Directives
4. Live Subprocess Execution of status_n8n.bat (Exit Code 0, Healthy output, PID extraction)
5. Scheduled Task Configuration via schtasks query (HealingTouch_n8n_Service)
6. Live Health Endpoint Response (http://localhost:5678/healthz -> HTTP 200 {"status":"ok"})
"""

import os
import re
import subprocess
import unittest
import urllib.request
import json
from pathlib import Path

ROOT_DIR = Path(r"c:\followUPSHEET\healing_touch")
SCRIPTS_DIR = ROOT_DIR / "scripts"

VBS_RUNNER = SCRIPTS_DIR / "run_n8n_silent.vbs"
START_BAT = ROOT_DIR / "start_n8n.bat"
STOP_BAT = ROOT_DIR / "stop_n8n.bat"
STATUS_BAT = ROOT_DIR / "status_n8n.bat"
SETUP_BAT = SCRIPTS_DIR / "setup_n8n_service.bat"


class TestN8nPersistenceScripts(unittest.TestCase):
    """Rigorous verification suite for n8n Windows Service persistence and control scripts."""

    def test_01_all_persistence_files_exist(self):
        """Verify that all 5 persistence and control files exist in expected project paths."""
        expected_files = [
            (VBS_RUNNER, "Silent VBScript Background Runner"),
            (START_BAT, "n8n Service Start Batch Script"),
            (STOP_BAT, "n8n Service Stop Batch Script"),
            (STATUS_BAT, "n8n Service Status Batch Script"),
            (SETUP_BAT, "n8n Scheduled Task Setup Script"),
        ]
        for path, description in expected_files:
            self.assertTrue(path.is_file(), f"Missing required persistence file ({description}): {path}")
            self.assertGreater(path.stat().st_size, 100, f"File {path.name} is suspiciously small: {path.stat().st_size} bytes")

    def test_02_crlf_line_endings_compliance(self):
        """Verify that all Windows batch and VBScript files have proper CRLF (\\r\\n) line endings."""
        files_to_check = [VBS_RUNNER, START_BAT, STOP_BAT, STATUS_BAT, SETUP_BAT]
        for path in files_to_check:
            raw = path.read_bytes()
            self.assertIn(b"\r\n", raw, f"File {path.name} must contain Windows CRLF line endings")
            # Ensure no lone LF without preceding CR
            lone_lf_count = len(re.findall(b"(?<!\r)\n", raw))
            self.assertEqual(lone_lf_count, 0, f"File {path.name} contains {lone_lf_count} lone LF characters which can break cmd.exe parser")

    def test_03_run_n8n_silent_vbs_structure(self):
        """Verify run_n8n_silent.vbs configuration, hidden execution, and environment variables."""
        content = VBS_RUNNER.read_text(encoding="utf-8")
        self.assertIn("WshShell.Run", content, "VBScript must invoke WshShell.Run")
        self.assertIn(", 0, False", content, "VBScript must specify WindowStyle 0 (hidden) and WaitOnReturn False")
        self.assertIn("N8N_PORT", content, "VBScript must configure N8N_PORT")
        self.assertIn("5678", content, "VBScript must specify port 5678")
        self.assertIn("Africa/Cairo", content, "VBScript must configure GENERIC_TIMEZONE to Africa/Cairo")
        self.assertIn("npx", content, "VBScript must execute npx")
        self.assertIn("n8n start", content, "VBScript must execute n8n start")

    def test_04_start_n8n_bat_structure(self):
        """Verify start_n8n.bat checks port 5678, invokes silent runner, and polls /healthz."""
        content = START_BAT.read_text(encoding="utf-8")
        self.assertIn("5678", content, "start_n8n.bat must reference port 5678")
        self.assertIn("run_n8n_silent.vbs", content, "start_n8n.bat must invoke run_n8n_silent.vbs")
        self.assertIn("healthz", content, "start_n8n.bat must check healthz endpoint")
        self.assertIn("200", content, "start_n8n.bat must verify HTTP 200 OK")
        self.assertIn("wscript", content.lower(), "start_n8n.bat must use wscript to launch VBScript")

    def test_05_stop_n8n_bat_structure(self):
        """Verify stop_n8n.bat finds listening PID on 5678 and terminates process tree."""
        content = STOP_BAT.read_text(encoding="utf-8")
        self.assertIn("5678", content, "stop_n8n.bat must reference port 5678")
        self.assertIn("taskkill", content.lower(), "stop_n8n.bat must use taskkill to terminate process tree")
        self.assertIn("LISTENING", content, "stop_n8n.bat must inspect LISTENING sockets")

    def test_06_status_n8n_bat_structure(self):
        """Verify status_n8n.bat queries healthz, displays PID, and exits with proper status codes."""
        content = STATUS_BAT.read_text(encoding="utf-8")
        self.assertIn("5678", content, "status_n8n.bat must reference port 5678")
        self.assertIn("healthz", content, "status_n8n.bat must query healthz")
        self.assertIn("curl.exe", content, "status_n8n.bat must use curl.exe")
        self.assertIn("exit /b 0", content, "status_n8n.bat must exit 0 on healthy status")
        self.assertIn("exit /b 1", content, "status_n8n.bat must exit 1 on stopped status")

    def test_07_setup_n8n_service_bat_structure(self):
        """Verify setup_n8n_service.bat configures Windows Scheduled Task HealingTouch_n8n_Service."""
        content = SETUP_BAT.read_text(encoding="utf-8")
        self.assertIn("HealingTouch_n8n_Service", content, "setup_n8n_service.bat must register HealingTouch_n8n_Service")
        self.assertIn("schtasks", content, "setup_n8n_service.bat must invoke schtasks")
        self.assertIn("ONLOGON", content, "setup_n8n_service.bat must trigger on user logon")
        self.assertIn("run_n8n_silent.vbs", content, "setup_n8n_service.bat must target run_n8n_silent.vbs")

    def test_08_live_healthz_endpoint(self):
        """Directly test http://localhost:5678/healthz over HTTP to ensure n8n responds with HTTP 200 ok."""
        req = urllib.request.Request("http://localhost:5678/healthz", headers={"User-Agent": "HealingTouch-Auditor/1.0"})
        with urllib.request.urlopen(req, timeout=5) as response:
            self.assertEqual(response.status, 200, f"Expected HTTP 200 but received {response.status}")
            data = json.loads(response.read().decode("utf-8"))
            self.assertEqual(data.get("status"), "ok", f"Expected {{'status': 'ok'}} but got {data}")

    def test_09_live_status_n8n_execution(self):
        """Execute status_n8n.bat directly in cmd and verify exit code 0 and healthy output."""
        res = subprocess.run(
            ["cmd.exe", "/c", str(STATUS_BAT)],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            timeout=15
        )
        self.assertEqual(res.returncode, 0, f"status_n8n.bat returned code {res.returncode}. Output:\n{res.stdout}\n{res.stderr}")
        self.assertIn("ONLINE [HEALTHY]", res.stdout, "status_n8n.bat output should contain 'ONLINE [HEALTHY]'")
        self.assertIn("200 OK", res.stdout, "status_n8n.bat output should contain '200 OK'")
        self.assertIn("5678", res.stdout, "status_n8n.bat output should contain port '5678'")
        self.assertIn("Process PID:", res.stdout, "status_n8n.bat output should display process PID")

    def test_10_live_scheduled_task_registered(self):
        """Execute setup_n8n_service.bat /query and confirm HealingTouch_n8n_Service task exists."""
        res = subprocess.run(
            ["cmd.exe", "/c", str(SETUP_BAT), "/query"],
            cwd=str(ROOT_DIR),
            capture_output=True,
            text=True,
            timeout=10
        )
        self.assertEqual(res.returncode, 0, f"setup_n8n_service.bat /query returned code {res.returncode}. Output:\n{res.stdout}\n{res.stderr}")
        self.assertIn("HealingTouch_n8n_Service", res.stdout, "Task HealingTouch_n8n_Service must be listed in schtasks output")


if __name__ == "__main__":
    unittest.main()

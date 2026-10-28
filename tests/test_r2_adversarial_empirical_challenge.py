#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
test_r2_adversarial_empirical_challenge.py
Adversarial Empirical Challenge Suite for Round 2 Remediations
Healing Touch Egypt n8n Workflows
"""

import json
import os
import subprocess
import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(r"c:\followUPSHEET\healing_touch")
WORKFLOWS_DIR = ROOT_DIR / "n8n_workflows"

def execute_js_node(js_code: str, input_json: dict) -> dict:
    """Executes n8n Code node JavaScript via Node.js."""
    wrapper = """
    const readline = require('readline');
    let inputData = '';
    const rl = readline.createInterface({ input: process.stdin, output: process.stdout, terminal: false });
    rl.on('line', (line) => { inputData += line; });
    rl.on('close', () => {
        const $input = {
            first: () => ({ json: JSON.parse(inputData) })
        };
        const $now = {
            toISO: () => new Date().toISOString()
        };
        try {
            const result = (function() {
                %s
            })();
            console.log(JSON.stringify({ success: true, result }));
        } catch (err) {
            console.log(JSON.stringify({ success: false, error: err.message }));
        }
    });
    """ % js_code

    proc = subprocess.run(
        ["node", "-e", wrapper],
        input=json.dumps(input_json),
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if proc.returncode != 0:
        raise RuntimeError(f"Node execution error: {proc.stderr}")
    return json.loads(proc.stdout)


class TestR2AdversarialPhoneNormalization(unittest.TestCase):
    """Adversarial testing of phone normalization in whatsapp_sheets_crm.json."""

    @classmethod
    def setUpClass(cls):
        sys.stdout.reconfigure(encoding="utf-8")
        wf_path = WORKFLOWS_DIR / "whatsapp_sheets_crm.json"
        with open(wf_path, "r", encoding="utf-8") as f:
            wf = json.load(f)
        val_node = next(n for n in wf["nodes"] if n["name"] == "Validate & Normalize Patient Lead")
        cls.js_code = val_node["parameters"]["jsCode"]

    def _validate(self, name: str, phone: str):
        payload = {"patient_name": name, "patient_phone": phone}
        res = execute_js_node(self.js_code, payload)
        self.assertTrue(res["success"], f"Execution failed: {res.get('error')}")
        return res["result"][0]["json"]

    def test_all_egyptian_notations_accepted(self):
        cases = [
            ("أحمد محمود", "01012345678", "201012345678", "Local 010"),
            ("فاطمة علي", "01198765432", "201198765432", "Local 011"),
            ("مريم حسن", "01255554444", "201255554444", "Local 012"),
            ("هدى إبراهيم", "01511223344", "201511223344", "Local 015"),
            ("سارة أحمد", "+201012345678", "201012345678", "International +20"),
            ("نور خليل", "+20 10 1234 5678", "201012345678", "Intl +20 with spaces"),
            ("رنا توفيق", "+20-10-1234-5678", "201012345678", "Intl +20 with dashes"),
            ("منى الشريف", "00201012345678", "201012345678", "Intl 0020"),
            ("ياسمين كمال", "0020-10-1234-5678", "201012345678", "Intl 0020 with dashes"),
            ("دينا سامي", "201012345678", "201012345678", "Intl 20 12-digit"),
            ("إيمان ناصر", "20-10-1234-5678", "201012345678", "Intl 20 with dashes"),
            ("زينب مصطفى", "٠١٠١٢٣٤٥٦٧٨", "201012345678", "Eastern Arabic 010"),
            ("هند عادل", "٠١١٩٨٧٦٥٤٣٢", "201198765432", "Eastern Arabic 011"),
            ("أميرة خالد", "٠١٢٥٥٥٥٤٤٤٤", "201255554444", "Eastern Arabic 012"),
            ("دعاء سمير", "٠١٥١١٢٢٣٣٤٤", "201511223344", "Eastern Arabic 015"),
            ("آية سعيد", "٠١٠-١٢٣٤-٥٦٧٨", "201012345678", "Eastern Arabic with dashes"),
            ("شيرين فريد", "٠١٠ ١٢٣٤ ٥٦٧٨", "201012345678", "Eastern Arabic with spaces"),
            ("بسمة عمر", "(٠١٠) ١٢٣٤٥٦٧٨", "201012345678", "Eastern Arabic with parens"),
            ("نهال جودة", "+٢٠١٠١٢٣٤٥٦٧٨", "201012345678", "Eastern Arabic with +20"),
            ("ولاء كرم", "٠٠٢٠١٠١٢٣٤٥٦٧٨", "201012345678", "Eastern Arabic with 0020"),
            ("لبنى طارق", "٢٠١٠١٢٣٤٥٦٧٨", "201012345678", "Eastern Arabic with 20"),
            ("مها صلاح", "+2001012345678", "201012345678", "Plus 20 followed by 010 (13 digits)"),
        ]
        for name, phone, expected_norm, desc in cases:
            out = self._validate(name, phone)
            self.assertTrue(out["is_valid"], f"Failed to accept valid lead: {desc} ({phone})")
            self.assertEqual(out["normalized_phone"], expected_norm, f"Incorrect normalization for {desc}")
            self.assertIsNone(out["validation_error"])

    def test_invalid_rejections_and_security(self):
        invalid_cases = [
            ("مريضة تجريبية", "01312345678", "Invalid prefix 013"),
            ("مريضة تجريبية", "+201312345678", "Invalid prefix +2013"),
            ("مريضة تجريبية", "01412345678", "Invalid prefix 014"),
            ("مريضة تجريبية", "01612345678", "Invalid prefix 016"),
            ("مريضة تجريبية", "01712345678", "Invalid prefix 017"),
            ("مريضة تجريبية", "01812345678", "Invalid prefix 018"),
            ("مريضة تجريبية", "01912345678", "Invalid prefix 019"),
            ("مريضة تجريبية", "0223456789", "Cairo landline 02"),
            ("مريضة تجريبية", "+20223456789", "Cairo landline +202"),
            ("مريضة تجريبية", "035432109", "Alex landline 03"),
            ("مريضة تجريبية", "+120101234567", "US number starting with +1"),
            ("مريضة تجريبية", "+966501234567", "Saudi number +966"),
            ("مريضة تجريبية", "0101234567", "10 digits (too short)"),
            ("مريضة تجريبية", "010123456789", "12 digits (too long)"),
            ("مريضة تجريبية", "010abcdefgh", "Alphanumeric letters"),
            ("مريضة تجريبية", "<script>alert('xss')</script>", "XSS script"),
            ("مريضة تجريبية", "01012345678; DROP TABLE Leads;", "SQL injection"),
            ("مريضة تجريبية", "", "Empty phone string"),
            ("A", "01012345678", "Name single ASCII char"),
            ("أ", "01012345678", "Name single Arabic char"),
            ("   ", "01012345678", "Name whitespace only"),
        ]
        for name, phone, desc in invalid_cases:
            out = self._validate(name, phone)
            self.assertFalse(out["is_valid"], f"Security failure: accepted invalid input in {desc}: {phone}")
            self.assertIsNotNone(out["validation_error"])


class TestR2AdversarialInstagramPollingBoundedness(unittest.TestCase):
    """Adversarial testing of Instagram container polling loop boundedness."""

    @classmethod
    def setUpClass(cls):
        sys.stdout.reconfigure(encoding="utf-8")
        wf_path = WORKFLOWS_DIR / "omnichannel_cross_post.json"
        with open(wf_path, "r", encoding="utf-8") as f:
            cls.wf = json.load(f)
        cls.nodes_by_name = {n["name"]: n for n in cls.wf["nodes"]}
        cls.conns = cls.wf["connections"]

        counter_node = cls.nodes_by_name["IG Polling Loop · Increment Counter"]
        cls.counter_js = counter_node["parameters"]["jsCode"]

        err_node = cls.nodes_by_name["Format Instagram Error Result"]
        cls.err_js = err_node["parameters"]["jsCode"]

    def test_loop_boundedness_state_machine(self):
        """Emulate the polling loop state machine and verify it terminates at <= 10 iterations."""
        state = {"status_code": "IN_PROGRESS", "poll_count": 0}
        iteration = 0
        max_loop_guard = 15

        while iteration < max_loop_guard:
            iteration += 1
            res = execute_js_node(self.counter_js, state)
            self.assertTrue(res["success"])
            state = res["result"][0]["json"]

            # Simulate IF condition
            has_retries = state["has_retries_left"]
            if not has_retries:
                # Loop terminated
                break

        # Verification: Must terminate at exactly poll_count == 10
        self.assertEqual(state["poll_count"], 10)
        self.assertFalse(state["has_retries_left"])
        self.assertIn("10 attempts", state["error_message"])

        # Format error node
        err_res = execute_js_node(self.err_js, state)
        self.assertTrue(err_res["success"])
        err_out = err_res["result"][0]["json"]
        self.assertEqual(err_out["platform"], "instagram")
        self.assertFalse(err_out["success"])
        self.assertEqual(err_out["status"], "TIMED_OUT")
        self.assertEqual(err_out["poll_count"], 10)

    def test_terminal_error_exit_immediate(self):
        """Verify that ERROR or EXPIRED exits immediately on iteration 1 without looping."""
        for term_code in ["ERROR", "EXPIRED"]:
            state = {"status_code": term_code, "poll_count": 0}
            res = execute_js_node(self.counter_js, state)
            self.assertTrue(res["success"])
            out = res["result"][0]["json"]

            self.assertEqual(out["poll_count"], 1)
            self.assertTrue(out["is_terminal_error"])
            self.assertFalse(out["has_retries_left"], f"Must not retry on terminal status: {term_code}")
            self.assertIn("terminal status", out["error_message"])

            err_res = execute_js_node(self.err_js, out)
            self.assertTrue(err_res["success"])
            err_out = err_res["result"][0]["json"]
            self.assertEqual(err_out["status"], "FAILED")
            self.assertFalse(err_out["success"])

    def test_graph_connections_for_polling_loop(self):
        """Verify connection topology ensures boundedness."""
        # 1. Is IG Container Ready? -> false routes to counter
        if_conns = self.conns["Is IG Container Ready?"]["main"]
        self.assertEqual(if_conns[1][0]["node"], "IG Polling Loop · Increment Counter")

        # 2. Counter routes to IF Attempts Left?
        counter_conns = self.conns["IG Polling Loop · Increment Counter"]["main"][0]
        self.assertEqual(counter_conns[0]["node"], "IG Polling · Attempts Left?")

        # 3. IF Attempts Left? Output 0 (True) routes to delay; Output 1 (False) routes to Format Instagram Error Result
        attempts_conns = self.conns["IG Polling · Attempts Left?"]["main"]
        self.assertEqual(attempts_conns[0][0]["node"], "Container Polling Retry Delay")
        self.assertEqual(attempts_conns[1][0]["node"], "Format Instagram Error Result")

        # 4. Error Result routes to Merge node
        err_conns = self.conns["Format Instagram Error Result"]["main"][0]
        self.assertEqual(err_conns[0]["node"], "Merge Omnichannel Results")


class TestR2AdversarialMultiBranchFanIn(unittest.TestCase):
    """Adversarial testing of 4-branch fan-in and synchronization via Merge node."""

    @classmethod
    def setUpClass(cls):
        sys.stdout.reconfigure(encoding="utf-8")
        wf_path = WORKFLOWS_DIR / "omnichannel_cross_post.json"
        with open(wf_path, "r", encoding="utf-8") as f:
            cls.wf = json.load(f)
        cls.nodes_by_name = {n["name"]: n for n in cls.wf["nodes"]}
        cls.conns = cls.wf["connections"]

    def test_merge_node_configuration_and_connections(self):
        merge_node = self.nodes_by_name.get("Merge Omnichannel Results")
        self.assertIsNotNone(merge_node, "Merge Omnichannel Results node must exist")
        self.assertEqual(merge_node["type"], "n8n-nodes-base.merge")

        # Trace reverse connections to Merge node
        incoming_to_merge = []
        for src, conn_data in self.conns.items():
            for group in conn_data.get("main", []):
                for target in group:
                    if target.get("node") == "Merge Omnichannel Results":
                        incoming_to_merge.append(src)

        expected_sources = {
            "Format Facebook Result",
            "Format Instagram Result",
            "Format Instagram Error Result",
            "Format YouTube Result",
            "Format TikTok Result"
        }
        self.assertEqual(set(incoming_to_merge), expected_sources)

        # Merge node connects solely to Aggregate Omnichannel Results
        merge_outgoing = [t["node"] for t in self.conns["Merge Omnichannel Results"]["main"][0]]
        self.assertEqual(merge_outgoing, ["Aggregate Omnichannel Results"])

        # Aggregate Omnichannel Results incoming is solely Merge Omnichannel Results
        agg_incoming = []
        for src, conn_data in self.conns.items():
            for group in conn_data.get("main", []):
                for target in group:
                    if target.get("node") == "Aggregate Omnichannel Results":
                        agg_incoming.append(src)
        self.assertEqual(agg_incoming, ["Merge Omnichannel Results"])


if __name__ == "__main__":
    unittest.main(verbosity=2)

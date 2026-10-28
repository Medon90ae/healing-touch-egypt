#!/usr/bin/env python3
"""
Test Suite: validate_n8n_workflows.py
Automated validation of n8n production workflows for Healing Touch Egypt.

Validates:
1. JSON Parseability & file existence
2. Top-level n8n schema compliance (name, nodes, connections, settings, meta)
3. Node uniqueness (unique IDs and unique node names per workflow)
4. Connection graph integrity (source and target nodes exist, valid main output arrays)
5. Valid recognized n8n node types and versions
6. Domain-specific requirements:
   - omnichannel_cross_post.json:
       * Webhook trigger from Python
       * Parallel fanout to FB, IG, YouTube, TikTok
       * Facebook retryOnFail with exponential backoff
       * Instagram Reels 2-step media container polling loop with wait
       * YouTube Shorts publishing
       * TikTok pack staging and staff alert
       * Promo code HT10 references
   - ai_content_factory_hitl.json:
       * Multi-trigger intake (Schedule, Webhook, RSS)
       * LLM Arabic copy generation with healthcare compliance & zero meta-jargon
       * Telegram interactive approval gate with inline buttons [✅ نشر فوري] / [❌ إلغاء]
       * Conditional routing to post-approval dispatch vs cancellation archive
   - whatsapp_sheets_crm.json:
       * Webhook intake from wa.html
       * Egyptian phone regex validation (^01[0125][0-9]{8}$) and 201XXXXXXXXX normalization
       * Google Sheets append to tab gid=513215731
       * 3x retry loop with exponential backoff wait
       * Instant Telegram staff alert & WhatsApp alert with HT10 promo code
       * Webhook responses: 200 OK and 400 Bad Request
"""

import json
import os
import re
import sys
import unittest

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKFLOWS_DIR = os.path.join(ROOT_DIR, "n8n_workflows")

EXPECTED_FILES = [
    "omnichannel_cross_post.json",
    "ai_content_factory_hitl.json",
    "whatsapp_sheets_crm.json"
]


class TestN8nWorkflows(unittest.TestCase):
    workflows = {}

    @classmethod
    def setUpClass(cls):
        sys.stdout.reconfigure(encoding="utf-8")
        if not os.path.isdir(WORKFLOWS_DIR):
            raise FileNotFoundError(f"Workflows directory not found: {WORKFLOWS_DIR}")
        for filename in EXPECTED_FILES:
            filepath = os.path.join(WORKFLOWS_DIR, filename)
            if not os.path.isfile(filepath):
                raise FileNotFoundError(f"Missing required workflow file: {filepath}")
            with open(filepath, "r", encoding="utf-8") as f:
                cls.workflows[filename] = json.load(f)

    def test_01_all_workflow_files_exist_and_parse(self):
        """Verify all 3 workflow files exist and parse as valid JSON dictionaries."""
        self.assertEqual(len(self.workflows), 3)
        for fname in EXPECTED_FILES:
            self.assertIn(fname, self.workflows)
            self.assertIsInstance(self.workflows[fname], dict)

    def test_02_top_level_n8n_schema(self):
        """Verify top-level n8n schema keys: name, nodes, connections, settings, meta."""
        required_keys = {"name", "nodes", "connections", "settings", "meta"}
        for fname, wf in self.workflows.items():
            for key in required_keys:
                self.assertIn(key, wf, f"Workflow {fname} missing required top-level key: {key}")
            self.assertIsInstance(wf["name"], str)
            self.assertTrue(len(wf["name"]) > 5)
            self.assertIsInstance(wf["nodes"], list)
            self.assertGreaterEqual(len(wf["nodes"]), 5, f"Workflow {fname} has too few nodes ({len(wf['nodes'])})")
            self.assertIsInstance(wf["connections"], dict)
            self.assertIsInstance(wf["settings"], dict)
            self.assertIsInstance(wf["meta"], dict)

    def test_03_node_uniqueness_and_attributes(self):
        """Verify node ID and name uniqueness, plus standard node attributes."""
        for fname, wf in self.workflows.items():
            seen_ids = set()
            seen_names = set()
            for node in wf["nodes"]:
                nid = node.get("id")
                name = node.get("name")
                ntype = node.get("type")
                pos = node.get("position")
                v = node.get("typeVersion")

                self.assertIsNotNone(nid, f"Node missing 'id' in {fname}: {node}")
                self.assertNotIn(nid, seen_ids, f"Duplicate node id '{nid}' in {fname}")
                seen_ids.add(nid)

                self.assertIsNotNone(name, f"Node missing 'name' in {fname}: {node}")
                self.assertNotIn(name, seen_names, f"Duplicate node name '{name}' in {fname}")
                seen_names.add(name)

                self.assertIsInstance(ntype, str, f"Node '{name}' missing valid 'type' in {fname}")
                self.assertTrue(
                    ntype.startswith("n8n-nodes-base.") or ntype.startswith("@n8n/"),
                    f"Unrecognized node type '{ntype}' in {fname} (node: {name})"
                )

                self.assertIsInstance(pos, list, f"Node '{name}' missing position array in {fname}")
                self.assertEqual(len(pos), 2, f"Node '{name}' position must have [x, y] in {fname}")
                self.assertIsInstance(v, (int, float), f"Node '{name}' missing valid typeVersion in {fname}")

    def test_04_valid_connections_graph(self):
        """Verify connection graph integrity: all sources and targets must exist."""
        for fname, wf in self.workflows.items():
            node_names = {n["name"] for n in wf["nodes"]}
            connections = wf["connections"]

            for source_name, conn_data in connections.items():
                self.assertIn(
                    source_name, node_names,
                    f"Connection source '{source_name}' does not exist in nodes of {fname}"
                )
                self.assertIn("main", conn_data, f"Connection for '{source_name}' missing 'main' output list in {fname}")
                self.assertIsInstance(conn_data["main"], list)

                for output_group in conn_data["main"]:
                    self.assertIsInstance(output_group, list)
                    for target in output_group:
                        target_name = target.get("node")
                        target_type = target.get("type")
                        target_idx = target.get("index")

                        self.assertIn(
                            target_name, node_names,
                            f"Connection target '{target_name}' referenced by '{source_name}' not found in {fname}"
                        )
                        self.assertEqual(target_type, "main")
                        self.assertIsInstance(target_idx, int)
                        self.assertGreaterEqual(target_idx, 0)

    def test_05_omnichannel_cross_post_specifics(self):
        """Verify Omnichannel Cross-Posting workflow functional architecture."""
        wf = self.workflows["omnichannel_cross_post.json"]
        nodes_by_name = {n["name"]: n for n in wf["nodes"]}
        node_types = {n["type"] for n in wf["nodes"]}

        # 1. Webhook trigger from Python
        self.assertIn("Python Webhook Intake", nodes_by_name)
        webhook_node = nodes_by_name["Python Webhook Intake"]
        self.assertEqual(webhook_node["type"], "n8n-nodes-base.webhook")
        self.assertEqual(webhook_node["parameters"].get("httpMethod"), "POST")
        self.assertEqual(webhook_node["parameters"].get("path"), "publish-post")

        # 2. Parallel fanout from payload preparation
        prep_conns = wf["connections"].get("Validate & Format Payloads", {}).get("main", [[]])[0]
        self.assertGreaterEqual(len(prep_conns), 4, "Validate node must fan out to at least 4 parallel platform branches")
        target_platform_nodes = {c["node"] for c in prep_conns}
        self.assertIn("Publish Facebook Photo Post", target_platform_nodes)
        self.assertIn("Create Instagram Media Container", target_platform_nodes)
        self.assertIn("Publish YouTube Shorts", target_platform_nodes)
        self.assertIn("Stage TikTok Assets & Package", target_platform_nodes)

        # 3. Facebook retryOnFail and backoff
        fb_node = nodes_by_name["Publish Facebook Photo Post"]
        self.assertTrue(fb_node.get("retryOnFail"), "Facebook node must have retryOnFail: True")
        self.assertGreaterEqual(fb_node.get("maxTries", 0), 3, "Facebook node must have maxTries >= 3")
        self.assertGreaterEqual(fb_node.get("waitBetweenTries", 0), 1000, "Facebook node must have backoff wait")

        # 4. Instagram Reels 2-step media container polling loop with bounded counter & terminal error handling
        self.assertIn("Create Instagram Media Container", nodes_by_name)
        self.assertIn("Wait For Container Processing", nodes_by_name)
        self.assertIn("Check Container Processing Status", nodes_by_name)
        self.assertIn("Is IG Container Ready?", nodes_by_name)
        self.assertIn("IG Polling Loop · Increment Counter", nodes_by_name)
        self.assertIn("IG Polling · Attempts Left?", nodes_by_name)
        self.assertIn("Format Instagram Error Result", nodes_by_name)
        self.assertIn("Container Polling Retry Delay", nodes_by_name)
        self.assertIn("Publish Instagram Container", nodes_by_name)
        self.assertIn("Merge Omnichannel Results", nodes_by_name)

        ig_container = nodes_by_name["Create Instagram Media Container"]
        ig_params = str(ig_container.get("parameters", {}))
        self.assertIn("REELS", ig_params)

        ig_wait = nodes_by_name["Wait For Container Processing"]
        self.assertEqual(ig_wait["type"], "n8n-nodes-base.wait")

        ig_if = nodes_by_name["Is IG Container Ready?"]
        self.assertEqual(ig_if["type"], "n8n-nodes-base.if")

        # Check loopback connection: Output 1 (False) routes to bounded counter
        ig_if_conns = wf["connections"]["Is IG Container Ready?"]["main"]
        self.assertGreaterEqual(len(ig_if_conns), 2, "Is IG Container Ready? must have 2 outputs (True/False)")
        self.assertEqual(ig_if_conns[0][0]["node"], "Publish Instagram Container")
        self.assertEqual(ig_if_conns[1][0]["node"], "IG Polling Loop · Increment Counter")

        # Check counter routes to attempts left check
        counter_conns = wf["connections"]["IG Polling Loop · Increment Counter"]["main"][0]
        self.assertEqual(counter_conns[0]["node"], "IG Polling · Attempts Left?")

        # Check attempts left: True routes to delay wait, False routes to terminal error result
        attempts_conns = wf["connections"]["IG Polling · Attempts Left?"]["main"]
        self.assertEqual(attempts_conns[0][0]["node"], "Container Polling Retry Delay")
        self.assertEqual(attempts_conns[1][0]["node"], "Format Instagram Error Result")

        delay_conns = wf["connections"]["Container Polling Retry Delay"]["main"][0]
        self.assertEqual(delay_conns[0]["node"], "Check Container Processing Status", "Polling delay must loop back")

        # Check Merge node synchronizes all branches before Aggregate
        merge_node = nodes_by_name["Merge Omnichannel Results"]
        self.assertEqual(merge_node["type"], "n8n-nodes-base.merge")
        merge_conns = wf["connections"]["Merge Omnichannel Results"]["main"][0]
        self.assertEqual(merge_conns[0]["node"], "Aggregate Omnichannel Results")

        # 5. YouTube Shorts
        yt_node = nodes_by_name["Publish YouTube Shorts"]
        self.assertTrue(yt_node.get("retryOnFail"))
        yt_body = str(yt_node.get("parameters", {}))
        self.assertIn("Shorts", yt_body)

        # 6. TikTok pack staging & Telegram notification
        tt_stage = nodes_by_name["Stage TikTok Assets & Package"]
        self.assertIn("tiktok", str(tt_stage.get("parameters", {})).lower())
        self.assertIn("Notify Staff of TikTok Pack", nodes_by_name)
        tt_notify = nodes_by_name["Notify Staff of TikTok Pack"]
        self.assertEqual(tt_notify["type"], "n8n-nodes-base.telegram")

        # 7. Promo code HT10 & Webhook response
        full_json_str = json.dumps(wf, ensure_ascii=False)
        self.assertIn("HT10", full_json_str)
        self.assertIn("Respond to Python Webhook", nodes_by_name)
        resp_node = nodes_by_name["Respond to Python Webhook"]
        self.assertEqual(resp_node["type"], "n8n-nodes-base.respondToWebhook")

    def test_06_ai_content_factory_hitl_specifics(self):
        """Verify AI Content Factory with Human-in-the-Loop review workflow."""
        wf = self.workflows["ai_content_factory_hitl.json"]
        nodes_by_name = {n["name"]: n for n in wf["nodes"]}
        full_json_str = json.dumps(wf, ensure_ascii=False)

        # 1. Triggers: Schedule, Webhook, RSS
        self.assertIn("Daily Morning Schedule Trigger", nodes_by_name)
        self.assertEqual(nodes_by_name["Daily Morning Schedule Trigger"]["type"], "n8n-nodes-base.scheduleTrigger")
        self.assertIn("Manual Webhook Intake Trigger", nodes_by_name)
        self.assertEqual(nodes_by_name["Manual Webhook Intake Trigger"]["type"], "n8n-nodes-base.webhook")
        self.assertIn("PubMed Medical Research RSS Intake", nodes_by_name)
        self.assertEqual(nodes_by_name["PubMed Medical Research RSS Intake"]["type"], "n8n-nodes-base.rssFeedRead")

        # 2. LLM Arabic Copy Generation Node & Compliance
        self.assertIn("LLM Arabic Clinical Copy Generator", nodes_by_name)
        llm_node = nodes_by_name["LLM Arabic Clinical Copy Generator"]
        llm_body = str(llm_node.get("parameters", {}))
        self.assertIn("أخصائية العناية بالتعافي", llm_body)
        self.assertIn("HT10", llm_body)
        self.assertIn("المرحلة 1", llm_body)  # Listed in prohibition rules in system prompt

        # 3. Telegram Interactive Approval Gate with [✅ نشر فوري] / [❌ إلغاء]
        self.assertIn("Telegram Interactive Approval Gate", nodes_by_name)
        tg_node = nodes_by_name["Telegram Interactive Approval Gate"]
        self.assertEqual(tg_node["type"], "n8n-nodes-base.telegram")
        self.assertEqual(tg_node["parameters"].get("operation"), "sendAndWait")

        approval_opts = tg_node["parameters"].get("approvalOptions", {}).get("values", {})
        self.assertEqual(approval_opts.get("approvalType"), "double")
        self.assertEqual(approval_opts.get("approveLabel"), "✅ نشر فوري")
        self.assertEqual(approval_opts.get("disapproveLabel"), "❌ إلغاء")

        # 4. Decision Branching & Post-Approval Dispatch
        self.assertIn("Check Approval Decision", nodes_by_name)
        check_node = nodes_by_name["Check Approval Decision"]
        self.assertEqual(check_node["type"], "n8n-nodes-base.if")

        if_conns = wf["connections"]["Check Approval Decision"]["main"]
        self.assertGreaterEqual(len(if_conns), 2)
        # Approved output 0
        self.assertEqual(if_conns[0][0]["node"], "Telegram Notify Approval Confirmed")
        self.assertIn("Dispatch to Omnichannel Publisher Webhook", nodes_by_name)
        dispatch_node = nodes_by_name["Dispatch to Omnichannel Publisher Webhook"]
        self.assertEqual(dispatch_node["type"], "n8n-nodes-base.httpRequest")
        self.assertEqual(dispatch_node["parameters"].get("method"), "POST")

        # Rejected output 1
        self.assertEqual(if_conns[1][0]["node"], "Telegram Notify Cancellation")
        self.assertIn("Archive Cancelled Draft", nodes_by_name)

    def test_07_whatsapp_sheets_crm_specifics(self):
        """Verify WhatsApp & Google Sheets CRM workflow."""
        wf = self.workflows["whatsapp_sheets_crm.json"]
        nodes_by_name = {n["name"]: n for n in wf["nodes"]}
        full_json_str = json.dumps(wf, ensure_ascii=False)

        # 1. Webhook Intake
        self.assertIn("Consultation Lead Webhook Intake", nodes_by_name)
        wh = nodes_by_name["Consultation Lead Webhook Intake"]
        self.assertEqual(wh["type"], "n8n-nodes-base.webhook")
        self.assertEqual(wh["parameters"].get("path"), "lead-capture")

        # 2. Egyptian Phone Regex Validation & Normalization
        self.assertIn("Validate & Normalize Patient Lead", nodes_by_name)
        val_node = nodes_by_name["Validate & Normalize Patient Lead"]
        val_code = val_node["parameters"].get("jsCode", "")
        self.assertIn("01[0125][0-9]{8}", val_code, "Must validate Egyptian phone pattern 01[0125]xxxxxxxx")
        self.assertIn("20", val_code, "Must normalize Egyptian phone to 201xxxxxxxxx")
        self.assertIn("HT10", val_code)

        # 3. Validation Routing & 400 Bad Request
        self.assertIn("Is Lead Valid?", nodes_by_name)
        self.assertIn("Respond 400 · Invalid Lead Data", nodes_by_name)
        resp_400 = nodes_by_name["Respond 400 · Invalid Lead Data"]
        self.assertEqual(resp_400["parameters"]["options"]["responseCode"], 400)

        # 4. Google Sheets Tab gid=513215731 Append
        self.assertIn("Append Lead to Google Sheets Tab 513215731", nodes_by_name)
        sheets_node = nodes_by_name["Append Lead to Google Sheets Tab 513215731"]
        self.assertEqual(sheets_node["type"], "n8n-nodes-base.googleSheets")
        self.assertEqual(sheets_node["parameters"].get("operation"), "append")
        self.assertEqual(sheets_node["parameters"]["documentId"]["value"], "12yAqzm-pSykfv7nRlvgocAHmwIYD_NPxqcNxrRKzA8k")
        self.assertEqual(sheets_node["parameters"]["sheetName"]["value"], "gid=513215731")
        self.assertEqual(sheets_node.get("onError"), "continueErrorOutput")

        # 5. 3x Retry Loop with Exponential Backoff
        self.assertIn("CRM Retry Loop · Increment Counter", nodes_by_name)
        self.assertIn("CRM Retry Loop · Attempts Left?", nodes_by_name)
        self.assertIn("CRM Retry Loop · Exponential Backoff Wait", nodes_by_name)
        self.assertIn("Log CRM Write Failure & Escalate", nodes_by_name)

        wait_node = nodes_by_name["CRM Retry Loop · Exponential Backoff Wait"]
        self.assertEqual(wait_node["type"], "n8n-nodes-base.wait")

        # Verify loopback to sheets append
        backoff_conn = wf["connections"]["CRM Retry Loop · Exponential Backoff Wait"]["main"][0][0]
        self.assertEqual(
            backoff_conn["node"],
            "Append Lead to Google Sheets Tab 513215731",
            "Backoff wait must loop back to Google Sheets append node"
        )

        # 6. Instant Telegram & WhatsApp Staff Alert
        self.assertIn("Send Instant Telegram Staff Alert", nodes_by_name)
        tg_alert = nodes_by_name["Send Instant Telegram Staff Alert"]
        self.assertEqual(tg_alert["type"], "n8n-nodes-base.telegram")
        tg_text = tg_alert["parameters"].get("text", "")
        self.assertIn("HT10", tg_text)
        self.assertIn("patient_name", tg_text)
        self.assertIn("patient_phone", tg_text)

        self.assertIn("Send WhatsApp Staff Notification", nodes_by_name)
        wa_alert = nodes_by_name["Send WhatsApp Staff Notification"]
        self.assertEqual(wa_alert["type"], "n8n-nodes-base.whatsApp")
        self.assertEqual(wa_alert["parameters"].get("recipientPhoneNumber"), "201155803307")

        # 7. 200 OK Webhook Response
        self.assertIn("Respond 200 · Lead Registered", nodes_by_name)
        resp_200 = nodes_by_name["Respond 200 · Lead Registered"]
        self.assertEqual(resp_200["parameters"]["options"]["responseCode"], 200)


def main():
    print("=" * 70)
    print("Healing Touch Egypt - n8n Workflow Validation Test Suite")
    print("=" * 70)
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestN8nWorkflows)
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    if result.wasSuccessful():
        print("\nAll n8n workflow validation tests passed successfully (exit code 0).")
        sys.exit(0)
    else:
        print(f"\nValidation failed with {len(result.failures)} failures and {len(result.errors)} errors.")
        sys.exit(1)


if __name__ == "__main__":
    main()

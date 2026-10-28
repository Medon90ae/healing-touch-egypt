#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite: test_n8n_adversarial_verification.py
Challenger 2 Empirical Adversarial Test Suite for Healing Touch Egypt n8n Workflows

Verifies:
1. HTTP Node Retry Configurations (retryOnFail, maxTries >= 3, waitBetweenTries >= 2000ms)
2. V8 Heap Limit Compliance (Zero binary video buffering, URL passing architecture)
3. Instagram 2-Step Container Polling Loop (Container -> Wait -> Status Check -> IF -> Loopback / Publish)
4. Graph Connection & Topology Integrity (Zero broken edges, valid multi-output mappings)
5. Interface Contract Compatibility (Payload schema alignment with Python pipeline & wa.html)
6. Healthcare Compliance & Arabic Copy Purity (Negative prompt enforcement + fallback purity)
7. Architectural and Quickstart Reports (Technical depth, formulas, and contract specifications)
"""

import json
import os
import re
import sys
import unittest
from pathlib import Path

ROOT_DIR = Path(r"c:\followUPSHEET\healing_touch")
WORKFLOWS_DIR = ROOT_DIR / "n8n_workflows"
REPORTS_DIR = ROOT_DIR / "docs" / "reports"

WORKFLOW_FILES = [
    "omnichannel_cross_post.json",
    "ai_content_factory_hitl.json",
    "whatsapp_sheets_crm.json"
]

FORBIDDEN_MARKETING_TERMS = [
    'طمأنة المريض',
    'المرحلة 1',
    'المرحلة 2',
    'الإقناع النفسي',
    'Persuasion Triggers',
    'Social Hook',
    'استراتيجية الانتشار',
    'E-E-A-T',
    'محرك التريند',
    'أسلوب الفضول',
    'أسلوب المقارنة الصادمة',
    'كسر المعتقدات الخاطئة',
    'تحويل القلق إلى خطوة',
]


class TestN8nAdversarialVerification(unittest.TestCase):
    workflows = {}

    @classmethod
    def setUpClass(cls):
        sys.stdout.reconfigure(encoding="utf-8")
        for filename in WORKFLOW_FILES:
            filepath = WORKFLOWS_DIR / filename
            if not filepath.is_file():
                raise FileNotFoundError(f"Missing required workflow file: {filepath}")
            with open(filepath, "r", encoding="utf-8") as f:
                cls.workflows[filename] = json.load(f)

    # =========================================================================
    # Test Group 1: HTTP Request Retry Configurations & Backoff Policies
    # =========================================================================

    def test_01_http_request_nodes_retry_policies(self):
        """
        Adversarially verify that every httpRequest node has:
        - retryOnFail == True
        - maxTries >= 3
        - waitBetweenTries >= 2000 (ms)
        to withstand Meta Graph API HTTP 429 rate limits and Google cold starts.
        """
        total_http_nodes = 0
        for wfname, wf in self.workflows.items():
            for node in wf.get("nodes", []):
                ntype = node.get("type", "")
                if "httprequest" in ntype.lower():
                    total_http_nodes += 1
                    node_name = node.get("name")
                    retry = node.get("retryOnFail")
                    max_tries = node.get("maxTries")
                    wait_time = node.get("waitBetweenTries")

                    # Check inside parameters.options fallback if applicable
                    opts = node.get("parameters", {}).get("options", {})
                    if retry is None:
                        retry = opts.get("retryOnFail")
                    if max_tries is None:
                        max_tries = opts.get("maxTries")
                    if wait_time is None:
                        wait_time = opts.get("waitBetweenTries")

                    self.assertTrue(
                        retry is True,
                        f"HTTP node '{node_name}' in {wfname} missing 'retryOnFail: true'. Found: {retry}"
                    )
                    self.assertIsNotNone(
                        max_tries,
                        f"HTTP node '{node_name}' in {wfname} missing 'maxTries'"
                    )
                    self.assertGreaterEqual(
                        max_tries,
                        3,
                        f"HTTP node '{node_name}' in {wfname} has maxTries={max_tries} (must be >= 3)"
                    )
                    self.assertIsNotNone(
                        wait_time,
                        f"HTTP node '{node_name}' in {wfname} missing 'waitBetweenTries'"
                    )
                    self.assertGreaterEqual(
                        wait_time,
                        2000,
                        f"HTTP node '{node_name}' in {wfname} has waitBetweenTries={wait_time}ms (must be >= 2000ms for backoff)"
                    )

        self.assertGreaterEqual(total_http_nodes, 7, f"Expected at least 7 HTTP nodes across workflows, found {total_http_nodes}")

    def test_02_crm_resilience_and_retry_mechanisms(self):
        """
        Verify that CRM and Google Sheets writes have explicit retry & backoff protection
        against Google Sheets API quotas and cold starts.
        """
        crm_wf = self.workflows["whatsapp_sheets_crm.json"]
        nodes_by_name = {n["name"]: n for n in crm_wf["nodes"]}
        
        # Verify Google Sheets node has continueErrorOutput configured
        sheets_node = nodes_by_name.get("Append Lead to Google Sheets Tab 513215731")
        self.assertIsNotNone(sheets_node, "Missing Google Sheets node in CRM workflow")
        self.assertEqual(
            sheets_node.get("onError"),
            "continueErrorOutput",
            "Google Sheets node must specify onError: continueErrorOutput to route failures to retry loop"
        )
        
        # Verify retry counter code node
        retry_inc_node = nodes_by_name.get("CRM Retry Loop · Increment Counter")
        self.assertIsNotNone(retry_inc_node, "Missing CRM Retry Loop Increment node")
        inc_code = retry_inc_node.get("parameters", {}).get("jsCode", "")
        self.assertIn("max_retries = 3", inc_code, "CRM retry loop must enforce max_retries = 3")
        self.assertIn("attempt <= max_retries", inc_code, "CRM retry loop must evaluate retry exhaustion")

        # Verify exponential backoff wait node in CRM loop
        wait_node = nodes_by_name.get("CRM Retry Loop · Exponential Backoff Wait")
        self.assertIsNotNone(wait_node, "Missing CRM backoff wait node")
        self.assertGreaterEqual(wait_node.get("parameters", {}).get("amount", 0), 5, "CRM backoff wait must be >= 5 seconds")

        # Verify WhatsApp alert node has retryOnFail
        wa_node = nodes_by_name.get("Send WhatsApp Staff Notification")
        self.assertIsNotNone(wa_node, "Missing WhatsApp notification node")
        self.assertTrue(wa_node.get("retryOnFail"), "WhatsApp node must have retryOnFail: true")
        self.assertGreaterEqual(wa_node.get("maxTries", 0), 3, "WhatsApp node maxTries must be >= 3")

    # =========================================================================
    # Test Group 2: V8 Heap Limits Compliance (Media Flow Architecture)
    # =========================================================================

    def test_03_zero_binary_video_buffering_in_n8n_memory(self):
        """
        Adversarially verify that NO node attempts to buffer raw binary video data,
        preventing Node.js V8 1.4GB heap Out-of-Memory crashes.
        """
        for wfname, wf in self.workflows.items():
            for node in wf.get("nodes", []):
                node_name = node.get("name")
                ntype = node.get("type", "")
                params = node.get("parameters", {})
                
                # Check for direct file download to memory
                self.assertNotEqual(
                    params.get("responseFormat"),
                    "file",
                    f"Forbidden binary buffering: Node '{node_name}' in {wfname} sets responseFormat=file"
                )
                
                # Check for binaryPropertyName usage for videos
                self.assertNotIn(
                    "binaryPropertyName",
                    params,
                    f"Node '{node_name}' in {wfname} uses binaryPropertyName, risking V8 heap OOM"
                )

                # Check for readBinaryFile nodes
                self.assertNotIn(
                    "readbinary",
                    ntype.lower(),
                    f"Forbidden binary node '{node_name}' ({ntype}) in {wfname}"
                )

    def test_04_url_passing_media_architecture(self):
        """
        Verify that large media is dispatched strictly via public URLs or external paths.
        """
        omni_wf = self.workflows["omnichannel_cross_post.json"]
        nodes_by_name = {n["name"]: n for n in omni_wf["nodes"]}

        # Instagram Video Container must pass video_url parameter
        ig_node = nodes_by_name.get("Create Instagram Media Container")
        self.assertIsNotNone(ig_node)
        body_params = ig_node.get("parameters", {}).get("bodyParameters", {}).get("parameters", [])
        param_dict = {p.get("name"): p.get("value") for p in body_params}
        self.assertEqual(param_dict.get("media_type"), "REELS")
        self.assertIn("video_url", param_dict, "Instagram container must receive video_url (URL string, not binary)")
        self.assertIn("$json.media_video_url", param_dict["video_url"])

        # Facebook Photo must pass url parameter
        fb_node = nodes_by_name.get("Publish Facebook Photo Post")
        self.assertIsNotNone(fb_node)
        fb_params = {p.get("name"): p.get("value") for p in fb_node.get("parameters", {}).get("bodyParameters", {}).get("parameters", [])}
        self.assertIn("url", fb_params, "Facebook photo node must receive url string")
        self.assertIn("$json.media_image_url", fb_params["url"])

        # TikTok Staging must pass file path reference and deep link, not binary upload
        tiktok_node = nodes_by_name.get("Stage TikTok Assets & Package")
        self.assertIsNotNone(tiktok_node)
        tiktok_code = tiktok_node.get("parameters", {}).get("jsCode", "")
        self.assertIn("video_file: payload.video_vertical_path", tiktok_code)
        self.assertIn("upload_url", tiktok_code)

    # =========================================================================
    # Test Group 3: Instagram 2-Step Container Polling Loop
    # =========================================================================

    def test_05_instagram_two_step_container_polling_loop(self):
        """
        Verify the complete state machine and polling cycle for Instagram media container:
        1. Container Creation: POST /media -> outputs to Wait node
        2. Wait node: delays initial query by >= 15 seconds
        3. Status Check node: GET container_id?fields=status_code,status
        4. IF node: checks status_code == 'FINISHED'
        5. True Branch: connects to Publish Instagram Container
        6. False Branch: connects to Retry Delay Wait node (>= 10s)
        7. Retry Delay Wait node: connects back to Status Check node (authentic graph cycle)
        """
        omni_wf = self.workflows["omnichannel_cross_post.json"]
        nodes_by_name = {n["name"]: n for n in omni_wf["nodes"]}
        conns = omni_wf["connections"]

        # Step 1: Container Creation
        c_create = nodes_by_name.get("Create Instagram Media Container")
        self.assertIsNotNone(c_create)
        create_targets = [t["node"] for t in conns.get("Create Instagram Media Container", {}).get("main", [[]])[0]]
        self.assertIn("Wait For Container Processing", create_targets)

        # Step 2: Initial Wait
        wait_1 = nodes_by_name.get("Wait For Container Processing")
        self.assertIsNotNone(wait_1)
        self.assertGreaterEqual(wait_1.get("parameters", {}).get("amount", 0), 15)
        wait_1_targets = [t["node"] for t in conns.get("Wait For Container Processing", {}).get("main", [[]])[0]]
        self.assertIn("Check Container Processing Status", wait_1_targets)

        # Step 3: Status Check
        status_check = nodes_by_name.get("Check Container Processing Status")
        self.assertIsNotNone(status_check)
        self.assertEqual(status_check.get("parameters", {}).get("method"), "GET")
        self.assertIn("status_code", status_check.get("parameters", {}).get("url", ""))
        status_targets = [t["node"] for t in conns.get("Check Container Processing Status", {}).get("main", [[]])[0]]
        self.assertIn("Is IG Container Ready?", status_targets)

        # Step 4: IF Node Condition
        if_node = nodes_by_name.get("Is IG Container Ready?")
        self.assertIsNotNone(if_node)
        cond_block = if_node.get("parameters", {}).get("conditions", {})
        conds = cond_block.get("conditions", [])
        self.assertGreaterEqual(len(conds), 1)
        self.assertIn("$json.status_code", conds[0].get("leftValue", ""))
        self.assertEqual(conds[0].get("rightValue"), "FINISHED")

        # Step 5: True Branch (Output 0) -> Publish
        if_conns = conns.get("Is IG Container Ready?", {}).get("main", [])
        self.assertGreaterEqual(len(if_conns), 2, "IF node must have 2 outputs (True and False)")
        true_targets = [t["node"] for t in if_conns[0]]
        self.assertIn("Publish Instagram Container", true_targets)

        # Step 6: False Branch (Output 1) -> Retry Delay
        false_targets = [t["node"] for t in if_conns[1]]
        self.assertIn("Container Polling Retry Delay", false_targets)

        # Step 7: Retry Delay Wait -> Loop Back to Status Check
        wait_2 = nodes_by_name.get("Container Polling Retry Delay")
        self.assertIsNotNone(wait_2)
        self.assertGreaterEqual(wait_2.get("parameters", {}).get("amount", 0), 10)
        wait_2_targets = [t["node"] for t in conns.get("Container Polling Retry Delay", {}).get("main", [[]])[0]]
        self.assertIn("Check Container Processing Status", wait_2_targets, "Retry Delay must loop back to Status Check node")

    # =========================================================================
    # Test Group 4: Connection Graph Topology & Uniqueness
    # =========================================================================

    def test_06_connection_graph_integrity_and_node_uniqueness(self):
        """
        Verify that every connection points to an existing node,
        and that all node IDs and node names are strictly unique across each workflow.
        """
        for wfname, wf in self.workflows.items():
            nodes = wf.get("nodes", [])
            node_ids = set()
            node_names = set()
            for n in nodes:
                nid = n.get("id")
                name = n.get("name")
                self.assertNotIn(nid, node_ids, f"Duplicate node ID '{nid}' in {wfname}")
                self.assertNotIn(name, node_names, f"Duplicate node name '{name}' in {wfname}")
                node_ids.add(nid)
                node_names.add(name)

            connections = wf.get("connections", {})
            for src_name, conn_data in connections.items():
                self.assertIn(src_name, node_names, f"Connection source '{src_name}' does not exist in nodes of {wfname}")
                main_outputs = conn_data.get("main", [])
                for out_idx, target_list in enumerate(main_outputs):
                    for target in target_list:
                        tgt_name = target.get("node")
                        self.assertIn(tgt_name, node_names, f"Connection target '{tgt_name}' (from '{src_name}') not found in {wfname}")

    # =========================================================================
    # Test Group 5: Healthcare Compliance & Copy Purity
    # =========================================================================

    def test_07_healthcare_compliance_and_copy_purity_in_workflows(self):
        """
        Verify that:
        1. Workflow prompt negative constraints explicitly forbid marketing jargon.
        2. Post-LLM regex scrubber actively strips forbidden marketing terms.
        3. Default fallback Arabic copy is 100% free from forbidden terms.
        4. Egyptian healthcare regulations are honored (no claims of 'طبيبة' or 'الدكتورة').
        """
        ai_wf = self.workflows["ai_content_factory_hitl.json"]
        nodes_by_name = {n["name"]: n for n in ai_wf["nodes"]}

        # 1. Check LLM system prompt negative constraints
        llm_node = nodes_by_name.get("LLM Arabic Clinical Copy Generator")
        self.assertIsNotNone(llm_node)
        prompt_body = llm_node.get("parameters", {}).get("jsonBody", "")
        self.assertIn("أخصائية العناية بالتعافي", prompt_body)
        self.assertIn("منع بات لجميع مصطلحات التسويق الداخلي", prompt_body)

        # 2. Check regex sanitization code node
        clean_node = nodes_by_name.get("Parse & Format Copy Variants")
        self.assertIsNotNone(clean_node)
        clean_code = clean_node.get("parameters", {}).get("jsCode", "")
        self.assertIn(".replace(/المرحلة\\s*[12]/g", clean_code)
        self.assertIn(".replace(/طمأنة المريض/g", clean_code)
        self.assertIn(".replace(/Persuasion Triggers/gi", clean_code)
        self.assertIn(".replace(/Social Hook/gi", clean_code)
        self.assertIn(".replace(/E-E-A-T/gi", clean_code)

        # 3. Extract the fallback cleanText string and verify zero forbidden terms
        clean_text_match = re.search(r'cleanText\s*=\s*`([^`]+)`', clean_code)
        self.assertTrue(clean_text_match, "Could not extract fallback cleanText from Sanitizer node")
        fallback_text = clean_text_match.group(1)
        for term in FORBIDDEN_MARKETING_TERMS:
            self.assertNotIn(term, fallback_text, f"Forbidden term '{term}' leaked into fallback copy")

        # 4. Check Egyptian regulation compliance in fallback copy
        self.assertNotIn("طبيبة", fallback_text)
        self.assertNotIn("الدكتورة", fallback_text)
        self.assertIn("أخصائية العناية بالتعافي", fallback_text)

    # =========================================================================
    # Test Group 6: Verification of Architectural and Quickstart Reports
    # =========================================================================

    def test_08_reports_and_documentation_alignment(self):
        """
        Verify all 4 required reports exist, are comprehensive (>5000 bytes),
        and accurately document the 5 technical axes, hybrid contracts, and setup steps.
        """
        expected_reports = [
            "n8n_architectural_study.md",
            "n8n_curated_templates_catalog.md",
            "n8n_hybrid_architecture.md",
            "n8n_quickstart_guide.md"
        ]
        for rname in expected_reports:
            rpath = REPORTS_DIR / rname
            self.assertTrue(rpath.is_file(), f"Missing report: {rpath}")
            size = rpath.stat().st_size
            self.assertGreater(size, 5000, f"Report {rname} is too small ({size} bytes)")
            
            with open(rpath, "r", encoding="utf-8") as f:
                content = f.read()
            self.assertIn("Healing Touch Egypt", content)

        # Specific report validations:
        # 1. Architectural study must detail 5 axes and V8 1.4GB heap limit
        with open(REPORTS_DIR / "n8n_architectural_study.md", "r", encoding="utf-8") as f:
            study = f.read()
        self.assertIn("1.4 GB", study)
        self.assertIn("V8", study)
        self.assertIn("FFmpeg", study)
        self.assertIn("retry", study.lower())

        # 2. Hybrid architecture must document webhook contracts and HT10 promo code
        with open(REPORTS_DIR / "n8n_hybrid_architecture.md", "r", encoding="utf-8") as f:
            hybrid = f.read()
        self.assertIn("HT10", hybrid)
        self.assertIn("POST /webhook/publish-post", hybrid)
        self.assertIn("POST /webhook/lead-capture", hybrid)

        # 3. Quickstart guide must warn about deprecated Desktop app and provide npx/Docker
        with open(REPORTS_DIR / "n8n_quickstart_guide.md", "r", encoding="utf-8") as f:
            quickstart = f.read()
        self.assertIn("npx n8n", quickstart)
        self.assertIn("docker", quickstart.lower())
        self.assertIn("deprecated", quickstart.lower())


if __name__ == "__main__":
    unittest.main(verbosity=2)

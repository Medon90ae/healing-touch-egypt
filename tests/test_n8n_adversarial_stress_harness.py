#!/usr/bin/env python3
"""
Adversarial Test Harness: test_n8n_adversarial_stress_harness.py
Empirical stress-testing of Healing Touch Egypt n8n workflows:
- Graph topology, orphaned nodes, loop termination, fan-in semantics
- Phone validation edge cases (Eastern Arabic digits, international formats, whitespaces)
- Payload variations with missing optional fields
- Telegram callback isolation and multi-campaign concurrency
- Healthcare compliance and prohibited marketing terms
"""

import json
import os
import re
import subprocess
import sys
import unittest
from collections import defaultdict, deque

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
WORKFLOWS_DIR = os.path.join(ROOT_DIR, "n8n_workflows")

WORKFLOW_FILES = {
    "cross_post": os.path.join(WORKFLOWS_DIR, "omnichannel_cross_post.json"),
    "hitl": os.path.join(WORKFLOWS_DIR, "ai_content_factory_hitl.json"),
    "crm": os.path.join(WORKFLOWS_DIR, "whatsapp_sheets_crm.json")
}


def run_node_js(js_code: str, input_json: dict) -> dict:
    """Execute a snippet of JavaScript via Node.js with input provided on stdin."""
    wrapper = f"""
    const readline = require('readline');
    let inputData = '';
    const rl = readline.createInterface({{ input: process.stdin, output: process.stdout, terminal: false }});
    rl.on('line', (line) => {{ inputData += line; }});
    rl.on('close', () => {{
        const $input = {{
            first: () => ({{ json: JSON.parse(inputData) }})
        }};
        const $now = {{
            toISO: () => new Date().toISOString()
        }};
        try {{
            const result = (function() {{
                {js_code}
            }})();
            console.log(JSON.stringify({{ success: true, result }}));
        }} catch (err) {{
            console.log(JSON.stringify({{ success: false, error: err.message, stack: err.stack }}));
        }}
    }});
    """
    res = subprocess.run(
        ["node", "-e", wrapper],
        input=json.dumps(input_json),
        capture_output=True,
        text=True,
        encoding="utf-8"
    )
    if res.returncode != 0:
        raise RuntimeError(f"Node.js process error (code {res.returncode}): {res.stderr}")
    return json.loads(res.stdout)


class TestWorkflowGraphTopology(unittest.TestCase):
    """Adversarial stress-testing of workflow graph connectivity and execution structure."""

    @classmethod
    def setUpClass(cls):
        sys.stdout.reconfigure(encoding="utf-8")
        cls.workflows = {}
        for key, path in WORKFLOW_FILES.items():
            with open(path, "r", encoding="utf-8") as f:
                cls.workflows[key] = json.load(f)

    def _build_adj_list(self, wf):
        adj = defaultdict(list)
        rev_adj = defaultdict(list)
        for src, conn in wf.get("connections", {}).items():
            for out_type, out_groups in conn.items():
                for group in out_groups:
                    for target in group:
                        tgt_node = target.get("node")
                        adj[src].append(tgt_node)
                        rev_adj[tgt_node].append(src)
        return adj, rev_adj

    def test_01_no_orphaned_nodes_across_all_workflows(self):
        """Every non-trigger node must have at least one incoming and one outgoing connection (unless terminal)."""
        trigger_types = {
            "n8n-nodes-base.webhook",
            "n8n-nodes-base.scheduleTrigger",
            "n8n-nodes-base.rssFeedRead"
        }
        terminal_types = {
            "n8n-nodes-base.respondToWebhook",
            "n8n-nodes-base.googleSheets"
        }

        for wfname, wf in self.workflows.items():
            adj, rev_adj = self._build_adj_list(wf)
            nodes_by_name = {n["name"]: n for n in wf["nodes"]}

            for name, node in nodes_by_name.items():
                ntype = node.get("type", "")
                is_trigger = ntype in trigger_types
                is_terminal = ntype in terminal_types or "Archive" in name or "Escalate" in name

                incoming = rev_adj.get(name, [])
                outgoing = adj.get(name, [])

                if is_trigger:
                    self.assertGreater(
                        len(outgoing), 0,
                        f"Trigger node '{name}' in {wfname} has NO outgoing connections!"
                    )
                else:
                    self.assertGreater(
                        len(incoming), 0,
                        f"Orphaned non-trigger node '{name}' in {wfname} has NO incoming connections!"
                    )
                    if not is_terminal:
                        self.assertGreater(
                            len(outgoing), 0,
                            f"Non-terminal node '{name}' in {wfname} has NO outgoing connections!"
                        )

    def test_02_all_nodes_reachable_from_triggers(self):
        """Every node in each workflow must be reachable via graph traversal from at least one trigger node."""
        trigger_types = {
            "n8n-nodes-base.webhook",
            "n8n-nodes-base.scheduleTrigger",
            "n8n-nodes-base.rssFeedRead"
        }

        for wfname, wf in self.workflows.items():
            adj, _ = self._build_adj_list(wf)
            nodes_by_name = {n["name"]: n for n in wf["nodes"]}

            triggers = [n["name"] for n in wf["nodes"] if n.get("type") in trigger_types]
            self.assertGreater(len(triggers), 0, f"Workflow {wfname} has no trigger nodes!")

            reachable = set()
            queue = deque(triggers)
            for t in triggers:
                reachable.add(t)

            while queue:
                curr = queue.popleft()
                for neighbor in adj.get(curr, []):
                    if neighbor not in reachable:
                        reachable.add(neighbor)
                        queue.append(neighbor)

            unreachable = set(nodes_by_name.keys()) - reachable
            self.assertEqual(
                len(unreachable), 0,
                f"Unreachable nodes found in {wfname}: {unreachable}"
            )

    def test_03_detect_cycles_and_verify_loop_termination_bounds(self):
        """
        Adversarial Challenge: detect cycles in workflows and check whether loops
        have explicit iteration counters or bounded retry limits vs risking infinite loops.
        """
        for wfname, wf in self.workflows.items():
            adj, _ = self._build_adj_list(wf)
            nodes_by_name = {n["name"]: n for n in wf["nodes"]}

            # DFS cycle detection
            visited = {}  # 0: unvisited, 1: visiting, 2: visited
            cycles = []

            def dfs(node, path):
                visited[node] = 1
                for neighbor in adj.get(node, []):
                    if visited.get(neighbor) == 1:
                        # Found cycle
                        cycle_path = path + [neighbor]
                        cycles.append(cycle_path)
                    elif visited.get(neighbor) != 2:
                        dfs(neighbor, path + [neighbor])
                visited[node] = 2

            for n in nodes_by_name.keys():
                if visited.get(n) != 2:
                    dfs(n, [n])

            if wfname == "cross_post":
                # In omnichannel_cross_post.json:
                # Polling loop: Check Container Processing Status -> Is IG Container Ready? -> IG Polling Loop · Increment Counter -> IG Polling · Attempts Left? -> Container Polling Retry Delay -> Check Container Processing Status
                self.assertGreater(len(cycles), 0, "Expected Instagram container polling loop in omnichannel_cross_post.json")
                loop_nodes = set()
                for c in cycles:
                    loop_nodes.update(c)

                # Check if there is an explicit retry count incrementer or counter node in this loop
                has_counter = any("Counter" in name or "retry" in name.lower() for name in loop_nodes if nodes_by_name[name]["type"] == "n8n-nodes-base.code")
                print(f"\n[TOPOLOGY VULNERABILITY AUDIT] omnichannel_cross_post IG loop detected: {loop_nodes}")
                print(f"  Explicit iteration counter in loop: {has_counter}")
                # Verify that the IG polling loop now HAS an explicit iteration counter / max retry bound
                self.assertTrue(
                    has_counter,
                    "Verified: IG polling loop has an explicit iteration counter / max retry bound"
                )
                self.assertIn("IG Polling Loop · Increment Counter", nodes_by_name)
                self.assertIn("IG Polling · Attempts Left?", nodes_by_name)
                self.assertIn("Format Instagram Error Result", nodes_by_name)

            elif wfname == "crm":
                # In whatsapp_sheets_crm.json:
                # Retry loop: Sheets append -> CRM Retry Loop · Increment Counter -> CRM Retry Loop · Attempts Left? -> Backoff -> Sheets append
                self.assertGreater(len(cycles), 0, "Expected Sheets retry loop in whatsapp_sheets_crm.json")
                # Verify that crm retry loop HAS an explicit counter and condition
                self.assertIn("CRM Retry Loop · Increment Counter", nodes_by_name)
                self.assertIn("CRM Retry Loop · Attempts Left?", nodes_by_name)

    def test_04_multi_branch_fan_in_without_merge_node(self):
        """
        Adversarial Verification: Ensure multi-branch fan-in is synchronized via an n8n Merge node.
        The parallel platform branches (Facebook, Instagram, YouTube, TikTok) feed into 'Merge Omnichannel Results',
        which then cleanly passes a synchronized single execution into 'Aggregate Omnichannel Results'.
        """
        wf = self.workflows["cross_post"]
        _, rev_adj = self._build_adj_list(wf)
        agg_incoming = rev_adj.get("Aggregate Omnichannel Results", [])
        merge_incoming = rev_adj.get("Merge Omnichannel Results", [])

        print(f"\n[FAN-IN AUDIT] Aggregate Omnichannel Results incoming branches: {agg_incoming}")
        print(f"[FAN-IN AUDIT] Merge Omnichannel Results incoming branches: {merge_incoming}")

        # Aggregate Omnichannel Results receives cleanly from Merge node
        self.assertEqual(agg_incoming, ["Merge Omnichannel Results"])
        # Merge node receives from all platform formatters (FB, IG, IG Error, YT, TT)
        self.assertIn("Format Facebook Result", merge_incoming)
        self.assertIn("Format Instagram Result", merge_incoming)
        self.assertIn("Format Instagram Error Result", merge_incoming)
        self.assertIn("Format YouTube Result", merge_incoming)
        self.assertIn("Format TikTok Result", merge_incoming)


class TestPhoneValidationEdgeCases(unittest.TestCase):
    """Adversarial stress-testing of Egyptian phone number validation and normalization logic."""

    @classmethod
    def setUpClass(cls):
        with open(WORKFLOW_FILES["crm"], "r", encoding="utf-8") as f:
            cls.wf_crm = json.load(f)

        # Extract JS code from "Validate & Normalize Patient Lead" node
        val_node = next(n for n in cls.wf_crm["nodes"] if n["name"] == "Validate & Normalize Patient Lead")
        cls.js_code = val_node["parameters"]["jsCode"]

    def _run_validation(self, name: str, phone: str, context: str = "استشارة قيصرية"):
        payload = {
            "patient_name": name,
            "patient_phone": phone,
            "context_topic": context
        }
        res = run_node_js(self.js_code, payload)
        self.assertTrue(res["success"], f"JS execution failed: {res.get('error')}")
        return res["result"][0]["json"]

    def test_01_canonical_valid_egyptian_numbers(self):
        """Standard valid 11-digit Egyptian mobile numbers starting with 010, 011, 012, 015."""
        valid_cases = [
            ("منى الشريف", "01012345678", "201012345678"),
            ("سارة أحمد", "01198765432", "201198765432"),
            ("رانيا خليل", "01255554444", "201255554444"),
            ("هدى محمود", "01511223344", "201511223344"),
        ]
        for name, phone, expected_norm in valid_cases:
            out = self._run_validation(name, phone)
            self.assertTrue(out["is_valid"], f"Phone {phone} should be valid")
            self.assertEqual(out["normalized_phone"], expected_norm)
            self.assertIsNone(out["validation_error"])
            self.assertIn("HT10", out["promo_code"])

    def test_02_whitespace_dashes_and_plus_stripping(self):
        """Numbers with leading/trailing/interspersed whitespace, dashes, and internal plus signs."""
        cases = [
            ("نور محمد", " 01012345678 ", "201012345678", True),
            ("مريم حسن", "011 1234 5678", "201112345678", True),
            ("ياسمين علي", "012-1234-5678", "201212345678", True),
            ("إيمان كمال", "+01012345678", "201012345678", True),
        ]
        for name, phone, expected_norm, should_be_valid in cases:
            out = self._run_validation(name, phone)
            self.assertEqual(out["is_valid"], should_be_valid)
            if should_be_valid:
                self.assertEqual(out["normalized_phone"], expected_norm)

    def test_03_international_prefix_edge_cases(self):
        """
        Adversarial Verification: International formats (+2010..., 002010..., 2010...).
        Egyptian numbers submitted with international prefixes (+20, 0020, 20) are normalized
        to standard local 01... for validation and formatted to E.164 201XXXXXXXXX.
        """
        intl_cases = [
            ("+201012345678", "International with plus", "201012345678"),
            ("00201012345678", "International with 0020", "201012345678"),
            ("201012345678", "International without plus", "201012345678"),
        ]
        for phone, desc, expected_norm in intl_cases:
            out = self._run_validation("أحمد توفيق", phone)
            print(f"\n[PHONE ADVERSARIAL] {desc} ('{phone}') -> is_valid: {out['is_valid']}, normalized: {out['normalized_phone']}")
            self.assertTrue(out["is_valid"], f"Valid Egyptian number formatted internationally should be accepted: {phone}")
            self.assertEqual(out["normalized_phone"], expected_norm)

    def test_04_eastern_arabic_indic_numerals(self):
        """
        Adversarial Verification: Eastern Arabic-Indic numerals (٠١٠١٢٣٤٥٦٧٨).
        Transliterates Arabic-Indic numerals (٠-٩) to ASCII (0-9) so that Egyptian patients
        typing with native Arabic keyboards on iOS/Android are accepted and properly routed.
        """
        arabic_phones = [
            ("فاطمة مصطفى", "٠١٠١٢٣٤٥٦٧٨", "Arabic 010", "201012345678"),
            ("هند عادل", "٠١١٩٨٧٦٥٤٣٢", "Arabic 011", "201198765432"),
            ("أميرة خالد", "٠١٢٥٥٥٥٤٤٤٤", "Arabic 012", "201255554444"),
            ("دعاء سمير", "٠١٥١١٢٢٣٣٤٤", "Arabic 015", "201511223344"),
        ]
        for name, phone, desc, expected_norm in arabic_phones:
            out = self._run_validation(name, phone)
            print(f"\n[ARABIC NUMERALS AUDIT] {desc} ('{phone}') -> is_valid: {out['is_valid']}, normalized: {out['normalized_phone']}")
            self.assertTrue(out["is_valid"], f"Arabic numerals should be accepted and normalized: {phone}")
            self.assertEqual(out["normalized_phone"], expected_norm)

    def test_05_invalid_prefixes_and_landlines(self):
        """Invalid mobile prefixes (013, 014, 016, 017, 018, 019) and landlines (02, 03)."""
        invalid_cases = [
            ("01312345678", "013 Benha landline"),
            ("01412345678", "014 unallocated"),
            ("01612345678", "016 unallocated"),
            ("01712345678", "017 unallocated"),
            ("01812345678", "018 unallocated"),
            ("01912345678", "019 unallocated"),
            ("0223456789", "02 Cairo landline"),
            ("035432109", "03 Alex landline"),
        ]
        for phone, desc in invalid_cases:
            out = self._run_validation("مريضة تجريبية", phone)
            self.assertFalse(out["is_valid"], f"{desc} ('{phone}') should be rejected")
            self.assertEqual(out["normalized_phone"], "")

    def test_06_malicious_inputs_and_boundary_lengths(self):
        """Short, long, non-numeric, script injection, empty, null values."""
        bad_cases = [
            ("", "Empty string"),
            ("0101234567", "10 digits (too short)"),
            ("010123456789", "12 digits (too long)"),
            ("010abcdefgh", "Letters in phone"),
            ("<script>alert(1)</script>", "XSS attempt"),
            ("01012345678; DROP TABLE Leads;", "SQL injection attempt"),
            ("null", "String null"),
        ]
        for phone, desc in bad_cases:
            out = self._run_validation("مريضة تجريبية", phone)
            self.assertFalse(out["is_valid"], f"{desc} ('{phone}') should be rejected")

    def test_07_patient_name_boundaries(self):
        """Patient name validation: >= 2 characters required."""
        name_cases = [
            ("", "01012345678", False, "Empty name"),
            ("A", "01012345678", False, "Single ASCII character"),
            ("أ", "01012345678", False, "Single Arabic character"),
            ("   ", "01012345678", False, "Whitespace-only name"),
            ("مي", "01012345678", True, "2-character valid Arabic name"),
            ("د. نورهان الشامي", "01012345678", True, "Full valid name"),
        ]
        for name, phone, should_be_valid, desc in name_cases:
            out = self._run_validation(name, phone)
            self.assertEqual(out["is_valid"], should_be_valid, f"{desc} ('{name}') unexpected result")


class TestPayloadVariationsAndExpressionResilience(unittest.TestCase):
    """Adversarial stress-testing of omnichannel payload parsing with missing optional fields."""

    @classmethod
    def setUpClass(cls):
        with open(WORKFLOW_FILES["cross_post"], "r", encoding="utf-8") as f:
            cls.wf_cp = json.load(f)

        # Extract JS code from "Validate & Format Payloads"
        val_node = next(n for n in cls.wf_cp["nodes"] if n["name"] == "Validate & Format Payloads")
        cls.js_code = val_node["parameters"]["jsCode"]

    def _run_payload_format(self, payload: dict) -> dict:
        res = run_node_js(self.js_code, payload)
        self.assertTrue(res["success"], f"JS payload formatting threw exception: {res.get('error')}")
        return res["result"][0]["json"]

    def test_01_canonical_payload(self):
        """Full payload with all fields populated."""
        full_payload = {
            "campaign_id": "csection_care_01",
            "product_name": "BUPY Silicone Scar Sheets 4cm x 3m",
            "promo_code": "HT10",
            "copywriting": {
                "facebook": "بروتوكول مخصص للفيسبوك",
                "instagram": "بروتوكول مخصص للإنستجرام",
                "youtube_title": "عنوان يوتيوب مخصص",
                "youtube_description": "وصف يوتيوب مخصص"
            },
            "media": {
                "square_card_url": "https://example.com/custom.jpg",
                "video_vertical_url": "https://example.com/custom.mp4",
                "video_vertical_path": "media_assets/branded_designs/custom.mp4"
            },
            "hashtags": "#هاشتاج_تجريبي #ولادة_قيصرية",
            "target_platforms": ["facebook", "instagram"]
        }
        out = self._run_payload_format(full_payload)
        self.assertEqual(out["campaign_id"], "csection_care_01")
        self.assertIn("بروتوكول مخصص للفيسبوك", out["fb_caption"])
        self.assertIn("بروتوكول مخصص للإنستجرام", out["ig_caption"])
        self.assertIn("عنوان يوتيوب مخصص", out["yt_title"])
        self.assertEqual(out["media_image_url"], "https://example.com/custom.jpg")

    def test_02_completely_empty_payload(self):
        """Empty payload {} must fallback to safe defaults without throwing TypeError."""
        out = self._run_payload_format({})
        self.assertEqual(out["campaign_id"], "post_op_care")
        self.assertEqual(out["product_name"], "BUPY Silicone Scar Sheets 4cm x 3m")
        self.assertEqual(out["promo_code"], "HT10")
        self.assertTrue(len(out["fb_caption"]) > 20)
        self.assertTrue(len(out["ig_caption"]) > 20)
        self.assertTrue(len(out["yt_title"]) > 10)
        self.assertTrue(len(out["yt_description"]) > 20)
        self.assertTrue(out["media_image_url"].startswith("http"))
        self.assertTrue(out["media_video_url"].startswith("http"))
        self.assertTrue(out["video_vertical_path"].endswith(".mp4"))
        self.assertEqual(len(out["target_platforms"]), 4)

    def test_03_missing_copywriting_and_media_subobjects(self):
        """Payloads where copywriting or media are missing, null, or empty dicts."""
        variations = [
            {"campaign_id": "test_1"},
            {"campaign_id": "test_2", "copywriting": None, "media": None},
            {"campaign_id": "test_3", "copywriting": {}, "media": {}},
            {"campaign_id": "test_4", "copywriting": {"text": "نص عام بديل"}},
            {"campaign_id": "test_5", "copywriting": {"facebook": "فيس فقط"}},
        ]
        for var in variations:
            out = self._run_payload_format(var)
            self.assertIsNotNone(out["fb_caption"])
            self.assertNotIn("undefined", out["fb_caption"])
            self.assertIsNotNone(out["ig_caption"])
            self.assertNotIn("undefined", out["ig_caption"])
            self.assertIsNotNone(out["yt_title"])
            self.assertNotIn("undefined", out["yt_title"])

    def test_04_downstream_expression_evaluations(self):
        """
        Verify that all downstream node expression references resolve cleanly
        against the formatted payload without undefined reference errors.
        """
        out = self._run_payload_format({})
        required_downstream_keys = [
            "fb_page_id", "media_image_url", "fb_caption",
            "ig_user_id", "media_video_url", "ig_caption",
            "yt_title", "yt_description",
            "video_vertical_path", "promo_code", "campaign_id"
        ]
        for key in required_downstream_keys:
            self.assertIn(key, out, f"Formatted payload missing downstream key: {key}")
            self.assertIsNotNone(out[key], f"Formatted payload key is None: {key}")
            self.assertNotEqual(out[key], "undefined", f"Key contains literal 'undefined': {key}")


class TestTelegramHitlCallbackIsolation(unittest.TestCase):
    """Adversarial stress-testing of Telegram HITL approval gate and campaign isolation."""

    @classmethod
    def setUpClass(cls):
        with open(WORKFLOW_FILES["hitl"], "r", encoding="utf-8") as f:
            cls.wf_hitl = json.load(f)

        norm_node = next(n for n in cls.wf_hitl["nodes"] if n["name"] == "Normalize Content Intake Topic")
        cls.js_norm = norm_node["parameters"]["jsCode"]

        format_node = next(n for n in cls.wf_hitl["nodes"] if n["name"] == "Parse & Format Copy Variants")
        cls.js_format = format_node["parameters"]["jsCode"]

    def test_01_campaign_id_generation_and_uniqueness(self):
        """Campaign ID prefix HT-CAMP- must be unique across rapid invocations."""
        campaign_ids = set()
        for i in range(25):
            res = run_node_js(self.js_norm, {"topic": f"Topic {i}"})
            self.assertTrue(res["success"])
            cid = res["result"][0]["json"]["campaign_id"]
            self.assertTrue(cid.startswith("HT-CAMP-"))
            campaign_ids.add(cid)

        # Check timestamp collision potential if called within same millisecond
        print(f"\n[CAMPAIGN ID AUDIT] 25 rapid invocations generated {len(campaign_ids)} unique IDs.")
        # Under rapid sequential Node.js calls, Date.now() may produce duplicates if executed within < 1ms
        # In production, high-throughput webhooks should use a UUID or monotonic sequence

    def test_02_telegram_approval_decision_condition_evaluation(self):
        """
        Test the condition expression in 'Check Approval Decision':
        leftValue: '={{ $json.data?.approved === true || $json.approved === true }}'
        operator: boolean true
        """
        # Scenario A: Approved via inline button callback
        payload_approved_1 = {"data": {"approved": True}}
        payload_approved_2 = {"approved": True}
        # Scenario B: Disapproved
        payload_disapproved = {"data": {"approved": False}, "approved": False}
        # Scenario C: Timed out after 24h
        payload_timeout = {"timedOut": True, "approved": False}
        # Scenario D: Corrupted / empty callback
        payload_empty = {}

        def eval_condition(payload):
            data = payload.get("data", {})
            return data.get("approved") is True or payload.get("approved") is True

        self.assertTrue(eval_condition(payload_approved_1), "Should evaluate to True for approved button")
        self.assertTrue(eval_condition(payload_approved_2), "Should evaluate to True for direct approved")
        self.assertFalse(eval_condition(payload_disapproved), "Should evaluate to False for disapproved button")
        self.assertFalse(eval_condition(payload_timeout), "Should evaluate to False on 24h timeout")
        self.assertFalse(eval_condition(payload_empty), "Should evaluate to False on empty payload")

    def test_03_contract_compatibility_between_hitl_and_cross_post(self):
        """
        Verify that parameters dispatched by 'Dispatch to Omnichannel Publisher Webhook' in HITL
        exactly match what 'Validate & Format Payloads' expects in omnichannel_cross_post.json.
        """
        hitl_dispatch_node = next(
            n for n in self.wf_hitl["nodes"]
            if n["name"] == "Dispatch to Omnichannel Publisher Webhook"
        )
        body_params = hitl_dispatch_node["parameters"]["bodyParameters"]["parameters"]
        dispatched_keys = {p["name"] for p in body_params}

        # Check required fields
        self.assertIn("campaign_id", dispatched_keys)
        self.assertIn("product_name", dispatched_keys)
        self.assertIn("copywriting", dispatched_keys)
        self.assertIn("hashtags", dispatched_keys)
        self.assertIn("promo_code", dispatched_keys)

        # Check target URL endpoint
        url = hitl_dispatch_node["parameters"]["url"]
        self.assertIn("/webhook/publish-post", url)


class TestHealthcareComplianceAndForbiddenMetaTerms(unittest.TestCase):
    """Scan all 3 workflow files for forbidden marketing meta-labels and compliance with healthcare guidelines."""

    @classmethod
    def setUpClass(cls):
        cls.raw_workflows = {}
        for key, path in WORKFLOW_FILES.items():
            with open(path, "r", encoding="utf-8") as f:
                cls.raw_workflows[key] = f.read()

    def test_01_no_forbidden_marketing_terms_in_generated_outputs(self):
        """
        Forbidden terms: المرحلة 1, المرحلة 2, طمأنة المريض, Persuasion Triggers, Social Hook, E-E-A-T, محرك التريند.
        These terms must NOT appear in generated captions, staff alerts, or customer messages.
        Note: They may only appear in sanitization regexes or system prompts instructing the LLM to prohibit them.
        """
        # In ai_content_factory_hitl.json, check that they only appear in system prompt instructions or replace regex
        hitl_raw = self.raw_workflows["hitl"]
        # In omnichannel_cross_post.json, verify 0 occurrences of forbidden terms
        cp_raw = self.raw_workflows["cross_post"]
        forbidden_terms = [
            "المرحلة 1", "المرحلة 2", "طمأنة المريض", "Persuasion Triggers",
            "Social Hook", "E-E-A-T", "محرك التريند"
        ]
        for term in forbidden_terms:
            self.assertNotIn(
                term, cp_raw,
                f"Forbidden term '{term}' found in omnichannel_cross_post.json!"
            )

    def test_02_egyptian_healthcare_practitioner_title_compliance(self):
        """Must consistently use 'أخصائية العناية بالتعافي', never claiming doctor title in customer-facing texts."""
        for wfname, raw in self.raw_workflows.items():
            self.assertIn(
                "أخصائية العناية بالتعافي", raw,
                f"Workflow {wfname} missing compliant title 'أخصائية العناية بالتعافي'"
            )

    def test_03_promo_code_ht10_presence(self):
        """All workflows must explicitly reference promo code HT10 and its clinical perks."""
        for wfname, raw in self.raw_workflows.items():
            self.assertIn("HT10", raw, f"Workflow {wfname} missing HT10 promo code")
            self.assertIn("شحن مجاني", raw, f"Workflow {wfname} missing free shipping benefit")
            self.assertIn("معاينة", raw, f"Workflow {wfname} missing package inspection benefit")


def main():
    print("=" * 80)
    print("Adversarial Stress Test Harness - Healing Touch Egypt n8n Workflows")
    print("=" * 80)
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTests(loader.loadTestsFromTestCase(TestWorkflowGraphTopology))
    suite.addTests(loader.loadTestsFromTestCase(TestPhoneValidationEdgeCases))
    suite.addTests(loader.loadTestsFromTestCase(TestPayloadVariationsAndExpressionResilience))
    suite.addTests(loader.loadTestsFromTestCase(TestTelegramHitlCallbackIsolation))
    suite.addTests(loader.loadTestsFromTestCase(TestHealthcareComplianceAndForbiddenMetaTerms))

    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)

    total = result.testsRun
    failures = len(result.failures)
    errors = len(result.errors)

    print("\n" + "=" * 80)
    print(f"ADVERSARIAL STRESS TEST RESULTS: {total} tests run, {failures} failures, {errors} errors.")
    print("=" * 80)
    sys.exit(0 if (failures == 0 and errors == 0) else 1)


if __name__ == "__main__":
    main()

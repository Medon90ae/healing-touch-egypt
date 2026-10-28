#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Deep Adversarial Testing and Verification Suite for n8n Workflows
Healing Touch Egypt
Author: Challenger 2 (Empirical Adversary)
"""

import json
import os
import sys
from pathlib import Path

WORKFLOWS_DIR = Path(r"c:\followUPSHEET\healing_touch\n8n_workflows")

def run_deep_adversarial_suite():
    print("=" * 80)
    print("HEALING TOUCH EGYPT - ADVERSARIAL CHALLENGER 2 VERIFICATION SUITE")
    print("=" * 80)
    
    workflows = {}
    for f in WORKFLOWS_DIR.glob("*.json"):
        with open(f, "r", encoding="utf-8") as fp:
            workflows[f.name] = json.load(fp)
            
    # -------------------------------------------------------------
    # 1. Inspect ALL Nodes in ALL Workflows
    # -------------------------------------------------------------
    for wfname, wf in workflows.items():
        print(f"\n>>> WORKFLOW: {wfname} (Total Nodes: {len(wf.get('nodes', []))})")
        for node in wf.get("nodes", []):
            nid = node.get("id")
            nname = node.get("name")
            ntype = node.get("type")
            retry = node.get("retryOnFail")
            max_t = node.get("maxTries")
            wait_t = node.get("waitBetweenTries")
            print(f"  * Node [{nid}] '{nname}' | Type: {ntype}")
            if retry is not None or max_t is not None or wait_t is not None:
                print(f"      Retry Config: retryOnFail={retry}, maxTries={max_t}, waitBetweenTries={wait_t}")

    # -------------------------------------------------------------
    # 2. CHALLENGE 1: HTTP Request Retry Configurations
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("CHALLENGE 1: HTTP REQUEST RETRY CONFIGURATIONS (Exponential Backoff, maxTries >= 3)")
    print("=" * 80)
    
    http_nodes_found = []
    missing_retries = []
    low_tries = []
    missing_wait = []
    
    for wfname, wf in workflows.items():
        for node in wf.get("nodes", []):
            ntype = node.get("type", "")
            if "httprequest" in ntype.lower():
                http_nodes_found.append((wfname, node))
                retry = node.get("retryOnFail")
                max_t = node.get("maxTries")
                wait_t = node.get("waitBetweenTries")
                
                # Check options in parameters too
                opts = node.get("parameters", {}).get("options", {})
                if retry is None and "retryOnFail" in opts:
                    retry = opts["retryOnFail"]
                if max_t is None and "maxTries" in opts:
                    max_t = opts["maxTries"]
                if wait_t is None and "waitBetweenTries" in opts:
                    wait_t = opts["waitBetweenTries"]
                    
                if not retry:
                    missing_retries.append((wfname, node.get("name"), retry))
                if max_t is None or max_t < 3:
                    low_tries.append((wfname, node.get("name"), max_t))
                if wait_t is None or wait_t <= 0:
                    missing_wait.append((wfname, node.get("name"), wait_t))
                    
    print(f"Total HTTP Request Nodes Found Across All Workflows: {len(http_nodes_found)}")
    for wf, n in http_nodes_found:
        print(f"  - [{wf}] '{n.get('name')}' -> retryOnFail={n.get('retryOnFail')}, maxTries={n.get('maxTries')}, waitBetweenTries={n.get('waitBetweenTries')}")
        
    print(f"\nFailures / Deficiencies:")
    print(f"  Missing retryOnFail: {missing_retries}")
    print(f"  Max tries < 3:       {low_tries}")
    print(f"  Missing wait time:   {missing_wait}")
    
    # Check non-HTTP integration nodes (like Google Sheets, Telegram, WhatsApp)
    print("\nNon-HTTP Network Integration Nodes Retry Analysis:")
    for wfname, wf in workflows.items():
        for node in wf.get("nodes", []):
            ntype = node.get("type", "")
            if any(svc in ntype.lower() for svc in ["googlesheets", "telegram", "whatsapp", "gmail", "reddit"]):
                print(f"  - [{wfname}] '{node.get('name')}' ({ntype}) -> retryOnFail={node.get('retryOnFail')}, maxTries={node.get('maxTries')}, waitBetweenTries={node.get('waitBetweenTries')}")

    # -------------------------------------------------------------
    # 3. CHALLENGE 2: V8 Heap Limits Compliance (Media Flow Architecture)
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("CHALLENGE 2: V8 HEAP LIMIT COMPLIANCE (No Binary Video Buffering)")
    print("=" * 80)
    
    binary_violations = []
    for wfname, wf in workflows.items():
        for node in wf.get("nodes", []):
            raw = json.dumps(node)
            # check if node downloads binary data or handles raw binary video
            params = node.get("parameters", {})
            if params.get("responseFormat") == "file":
                binary_violations.append((wfname, node.get("name"), "responseFormat=file"))
            if "binaryPropertyName" in params:
                binary_violations.append((wfname, node.get("name"), f"binaryPropertyName={params.get('binaryPropertyName')}"))
            if "readBinaryFiles" in node.get("type", "").lower() or "readbinaryfile" in node.get("type", "").lower():
                binary_violations.append((wfname, node.get("name"), "ReadBinaryFile node"))
            # Check if video posting in omnichannel_cross_post uses public URL
            if "video" in node.get("name", "").lower() or "reel" in node.get("name", "").lower() or "shorts" in node.get("name", "").lower() or "instagram" in node.get("name", "").lower():
                body_params = params.get("bodyParameters", {}).get("parameters", [])
                for bp in body_params:
                    val = bp.get("value", "")
                    name = bp.get("name", "")
                    if "video" in name.lower() or "url" in name.lower():
                        print(f"  Video parameter in [{wfname} -> {node.get('name')}]: {name} = {val}")

    print(f"\nBinary Violations Found: {len(binary_violations)}")
    for bv in binary_violations:
        print(f"  VIOLATION: {bv}")
    if not binary_violations:
        print("  PASS: Zero binary video buffers or file downloads detected. All video publishing operates via URL passing / external orchestration.")

    # -------------------------------------------------------------
    # 4. CHALLENGE 3: Instagram 2-Step Polling Loop Deep Audit
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("CHALLENGE 3: INSTAGRAM 2-STEP POLLING LOOP & STATE MACHINE AUDIT")
    print("=" * 80)
    
    cross_wf = workflows.get("omnichannel_cross_post.json")
    if not cross_wf:
        print("ERROR: omnichannel_cross_post.json not found!")
        return

    cross_nodes = {n["name"]: n for n in cross_wf.get("nodes", [])}
    cross_conn = cross_wf.get("connections", {})
    
    print("\nTracing Instagram Branch Connection Path:")
    # Look for connections starting from parallel fanout or Instagram container
    ig_start_node = "Create Instagram Media Container"
    
    def trace_connections(current_node, visited=None, depth=0):
        if visited is None:
            visited = []
        indent = "  " * depth
        print(f"{indent}-> {current_node}")
        visited.append(current_node)
        conns = cross_conn.get(current_node, {}).get("main", [])
        for out_idx, target_list in enumerate(conns):
            for t in target_list:
                node_name = t.get("node")
                out_label = f"[out {out_idx}]"
                print(f"{indent}   {out_label} connected to: {node_name}")
                if node_name in visited:
                    print(f"{indent}   *** CYCLE DETECTED (Loop Back): {node_name} ***")
                else:
                    trace_connections(node_name, visited.copy(), depth + 1)

    trace_connections(ig_start_node)

    # Inspect the loop nodes
    print("\nInspecting IF node conditions and branching:")
    if_node = cross_nodes.get("Is IG Container Ready?")
    if if_node:
        print(f"  IF Node params: {json.dumps(if_node.get('parameters'), indent=4)}")
    
    wait_node_1 = cross_nodes.get("Wait For Container Processing")
    if wait_node_1:
        print(f"  Initial Wait node params: {json.dumps(wait_node_1.get('parameters'), indent=4)}")

    wait_node_2 = cross_nodes.get("Container Polling Retry Delay")
    if wait_node_2:
        print(f"  Retry Delay Wait node params: {json.dumps(wait_node_2.get('parameters'), indent=4)}")

    check_node = cross_nodes.get("Check Container Processing Status")
    if check_node:
        print(f"  Status Check node params: {json.dumps(check_node.get('parameters'), indent=4)}")

    # -------------------------------------------------------------
    # 5. CHALLENGE 4: Loop Safety & Deadlock Analysis
    # -------------------------------------------------------------
    print("\n" + "=" * 80)
    print("CHALLENGE 4: LOOP SAFETY, TIMEOUT, AND INFINITE LOOP RISK")
    print("=" * 80)
    
    # Check if the polling loop has a maximum iteration guard or timeout
    # Trace false branch of 'Is IG Container Ready?'
    false_branch_targets = cross_conn.get("Is IG Container Ready?", {}).get("main", [])
    print(f"'Is IG Container Ready?' outputs structure: {len(false_branch_targets)} outputs")
    for idx, targets in enumerate(false_branch_targets):
        output_name = "Output 0 (TRUE - Finished)" if idx == 0 else "Output 1 (FALSE - In Progress / Other)"
        print(f"  {output_name}: {[t.get('node') for t in targets]}")

if __name__ == "__main__":
    run_deep_adversarial_suite()

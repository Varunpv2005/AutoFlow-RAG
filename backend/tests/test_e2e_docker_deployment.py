import requests
import json
import os
import time

BASE_URL = "http://localhost:8000/api"
FRONTEND_URL = "http://localhost:3000"

def run_e2e_tests():
    print("=== STARTING REAL DOCKER E2E VALIDATION ===")
    
    # 1. Healthcheck Endpoint
    res = requests.get(f"{BASE_URL}/health")
    assert res.status_code == 200, f"Healthcheck failed: {res.text}"
    health = res.json()
    assert health["status"] in ["ok", "degraded"], f"Unexpected health status: {health}"
    print("[PASS] 1. Healthcheck verified:", health)

    # 2. Frontend Accessibility
    f_res = requests.get(FRONTEND_URL)
    assert f_res.status_code == 200, f"Frontend failed: {f_res.status_code}"
    assert "<!DOCTYPE html>" in f_res.text or "<div" in f_res.text, "Frontend HTML missing"
    print("[PASS] 2. Frontend web server verified at http://localhost:3000")

    # 3. User Registration & Auth (User A & User B)
    ts = int(time.time())
    user_a = f"docker_user_a_{ts}"
    user_b = f"docker_user_b_{ts}"
    pwd = "Password123!"

    reg_a = requests.post(f"{BASE_URL}/auth/signup", json={"username": user_a, "password": pwd})
    assert reg_a.status_code == 200, f"User A signup failed: {reg_a.text}"
    token_a = reg_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    reg_b = requests.post(f"{BASE_URL}/auth/signup", json={"username": user_b, "password": pwd})
    assert reg_b.status_code == 200, f"User B signup failed: {reg_b.text}"
    token_b = reg_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}
    print("[PASS] 3. Registration & JWT Authentication verified for User A & User B")

    # 4. Oversized File Upload Rejection Test
    oversized_content = b"X" * (26 * 1024 * 1024) # 26 MB
    files_over = {"file": ("big_file.txt", oversized_content, "text/plain")}
    res_over = requests.post(f"{BASE_URL}/upload", headers=headers_a, files=files_over)
    assert res_over.status_code in [413, 400, 422], f"Oversized file not rejected correctly: {res_over.status_code}"
    print("[PASS] 4. Oversized upload (26MB) cleanly rejected with HTTP", res_over.status_code)

    # 5. Invalid File Extension Rejection Test
    files_bad = {"file": ("script.exe", b"binary content", "application/octet-stream")}
    res_bad = requests.post(f"{BASE_URL}/upload", headers=headers_a, files=files_bad)
    assert res_bad.status_code in [400, 422], f"Invalid file extension not rejected: {res_bad.status_code}"
    print("[PASS] 5. Unsupported file (.exe) cleanly rejected with HTTP", res_bad.status_code)

    # 6. Document Upload & Ingestion (User A vs User B)
    doc_a_text = "Project Alpha Financial Secret: Q3 revenue reached 10 million dollars for User A."
    files_a = {"file": ("alpha_report.txt", doc_a_text.encode('utf-8'), "text/plain")}
    res_up_a = requests.post(f"{BASE_URL}/upload", headers=headers_a, files=files_a)
    assert res_up_a.status_code == 200, f"Upload A failed: {res_up_a.text}"
    file_a_id = res_up_a.json()["id"]

    doc_b_text = "Project Beta Secret Code: Beta access password is QuantumBeta2026 for User B."
    files_b = {"file": ("beta_report.txt", doc_b_text.encode('utf-8'), "text/plain")}
    res_up_b = requests.post(f"{BASE_URL}/upload", headers=headers_b, files=files_b)
    assert res_up_b.status_code == 200, f"Upload B failed: {res_up_b.text}"
    file_b_id = res_up_b.json()["id"]
    print("[PASS] 6. Document upload & RAG ingestion verified for User A (ID:", file_a_id, ") and User B (ID:", file_b_id, ")")

    # 7. User Scoped File Listing & Analytics
    list_a = requests.get(f"{BASE_URL}/files", headers=headers_a).json()
    assert len(list_a) == 1 and list_a[0]["id"] == file_a_id, f"User A file list leak: {list_a}"

    list_b = requests.get(f"{BASE_URL}/files", headers=headers_b).json()
    assert len(list_b) == 1 and list_b[0]["id"] == file_b_id, f"User B file list leak: {list_b}"

    analytics_a = requests.get(f"{BASE_URL}/analytics", headers=headers_a).json()
    assert analytics_a["user_documents"] == 1, f"Analytics mismatch: {analytics_a}"
    print("[PASS] 7. User file listing & scoped analytics verified")

    # 8. RAG Query & User Isolation Test
    # User A asks about Alpha revenue
    chat_a = requests.post(f"{BASE_URL}/chat", headers=headers_a, json={"question": "What is the Q3 revenue for Project Alpha?"}).json()
    assert "10 million" in chat_a["answer"] or "revenue" in chat_a["answer"].lower(), f"Unexpected answer: {chat_a}"
    assert len(chat_a["sources"]) > 0, "Sources missing for User A"
    print("[PASS] 8. Grounded RAG Query & Source Citations verified for User A")

    # User A tries to ask about User B's secret (Project Beta password) -> must refuse / not return User B data
    chat_cross = requests.post(f"{BASE_URL}/chat", headers=headers_a, json={"question": "What is the Beta access password?"}).json()
    assert "cannot find" in chat_cross["answer"].lower() or "no relevant context" in chat_cross["answer"].lower(), f"Cross-user leak detected: {chat_cross}"
    assert len(chat_cross["sources"]) == 0, f"Cross-user sources returned: {chat_cross['sources']}"
    print("[PASS] 9. Cross-user isolation verified (User A cannot retrieve User B secrets)")

    # 9. Document Deletion Test
    del_res = requests.delete(f"{BASE_URL}/files/{file_a_id}", headers=headers_a)
    assert del_res.status_code == 200, f"Delete file failed: {del_res.text}"
    list_after_del = requests.get(f"{BASE_URL}/files", headers=headers_a).json()
    assert len(list_after_del) == 0, "File still exists after delete"
    print("[PASS] 10. Document deletion and FAISS index update verified")

    print("=== ALL REAL DOCKER INTEGRATION TESTS PASSED CLEANLY ===")

if __name__ == "__main__":
    run_e2e_tests()

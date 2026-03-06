sessions = {}

def next_state(state: str, event: str) -> str:
    if state == "NEW":
        if event == "PAY_OK":
            return "PAID"
        elif event == "PAY_FAIL":
            return "CANCELLED"
    elif state == "PAID":
        if event == "DONE":
            return "DONE"
        elif event == "CANCEL":
            return "CANCELLED"
    return state

def create_session(session_id: str, ip: str) -> bool:
    sessions[session_id] = {
        "status": "NEW",
        "ip": ip,
        "attempts": 0
    }
    return True

def process_payment(amount: int) -> str:
    if amount >= 100:
        return "PAY_FAIL"
    return "PAY_OK"

def cancel_session(session_id: str) -> bool:
    if session_id not in sessions:
        return False
    
    sessions[session_id]["attempts"] += 1
    if sessions[session_id]["attempts"] < 3:
        return False
    
    sessions[session_id]["status"] = "CANCELLED"
    return True

def complete_session(session_id: str) -> str:
    return "DONE"

def process_order(session_id: str, ip: str, amount: int):
    create_session(session_id, ip)
    
    pay_result = process_payment(amount)
    new_status = next_state(sessions[session_id]["status"], pay_result)
    sessions[session_id]["status"] = new_status
    
    if new_status == "PAID":
        complete_result = complete_session(session_id)
        final_status = next_state(new_status, complete_result)
        sessions[session_id]["status"] = final_status
    elif new_status == "CANCELLED":
        for attempt in range(1, 6):
            if cancel_session(session_id):
                break

if __name__ == "__main__":
    process_order("sess-001", "192.168.1.1", 500)
    process_order("sess-002", "192.168.1.2", 1000)
    process_order("sess-003", "192.168.1.3", 300)
    
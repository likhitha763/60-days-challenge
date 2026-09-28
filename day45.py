"""
Hospital ER Patient Scheduling Engine (Priority Queue)
======================================================
Phase: Priority Queues

Description:
A hospital emergency room must prioritize incoming patients based on medical 
severity rather than arrival time. This script implements a priority scheduling 
engine using binary heaps to ensure critical patients are treated first, preventing 
waiting room chaos.

Real-World Impact:
- Operating Systems: CPU process scheduling (priority-based multitasking).
- Network Routing: Quality of Service (QoS) packet prioritization.
- Cloud Computing: Managing server resource allocation for urgent workloads.
"""

import heapq
import time
from datetime import datetime

class EmergencyRoomScheduler:
    """
    A priority queue-based scheduling system for emergency room management.
    """
    def __init__(self):
        # The heap will store tuples: (severity_rank, arrival_timestamp, patient_name, condition)
        # Lower severity_rank means higher priority (e.g., 1 = Critical/Red, 3 = Stable/Green)
        self.waiting_room = []
        self._counter = 0  # Tie-breaker for patients with the same severity (FIFO order)

    def admit_patient(self, name: str, severity: int, condition: str):
        """
        Admit a patient into the emergency room queue.
        
        Parameters:
            name (str): Patient's full name.
            severity (int): 1 = Critical (Immediate), 2 = Urgent, 3 = Stable.
            condition (str): Medical description of the ailment.
        """
        self._counter += 1
        entry = (severity, self._counter, name, condition)
        heapq.heappush(self.waiting_room, entry)
        
        severity_labels = {1: "CRITICAL", 2: "URGENT", 3: "STABLE"}
        print(f"[ADMIT] {name} arrived with [{condition}]. Priority: {severity_labels.get(severity, 'UNKNOWN')}")

    def treat_next_patient(self):
        """
        Treats the patient with the highest priority currently in the queue.
        """
        if not self.waiting_room:
            print("[INFO] The waiting room is currently empty. All patients treated.")
            return None
            
        severity, _, name, condition = heapq.heappop(self.waiting_room)
        severity_labels = {1: "CRITICAL", 2: "URGENT", 3: "STABLE"}
        
        print(f"\n---> [TREATING] Now attending to **{name}** ({severity_labels.get(severity)})")
        print(     f"     Condition: {condition}")
        return name

    def display_waiting_room(self):
        """
        Displays the current queue of waiting patients ordered by priority.
        """
        if not self.waiting_room:
            print("Waiting Room Status: Empty")
            return
            
        print("\n--- Current Waiting Room Status ---")
        # Create a sorted copy of the heap to display without disrupting order
        sorted_queue = sorted(self.waiting_room)
        for rank, counter, name, condition in sorted_queue:
            label = {1: "CRITICAL", 2: "URGENT", 3: "STABLE"}.get(rank, "NORMAL")
            print(f" - [{label}] {name} ({condition})")
        print("-----------------------------------")


# --- Execution and Simulation ---
if __name__ == "__main__":
    print("=== HOSPITAL EMERGENCY ROOM SCHEDULING ENGINE ===")
    er = EmergencyRoomScheduler()
    
    # Simulating incoming emergency requests
    print("\n[Simulating Incoming ER Requests...]")
    er.admit_patient("Alice Smith", severity=3, condition="Sprained ankle")
    er.admit_patient("Bob Jones", severity=1, condition="Severe chest pain / Cardiac arrest risk")
    er.admit_patient("Charlie Brown", severity=2, condition="Deep laceration on arm")
    
    # Display current waiting room lineup
    er.display_waiting_room()
    
    # New critical patient walks in while others are waiting
    print("\n[New Emergency Arrival!]")
    er.admit_patient("Diana Prince", severity=1, condition="Unresponsive / Severe trauma")
    
    er.display_waiting_room()
    
    # Process patients in order of priority
    print("\n[Processing Medical Queue...]")
    while er.waiting_room:
        er.treat_next_patient()


"""
--- LINKEDIN REFLECTION ---
Post Title: Why Priority Queues are Life-Savers in Software Engineering 🏥⚡

In a hospital emergency room, a first-come, first-served queue can lead to catastrophic 
failures. If a patient with a sprained ankle gets treated before someone experiencing cardiac 
arrest, the consequences are severe. That's why high-stakes systems rely on Priority Queues.

Today, I built a Priority Scheduling Engine using binary heaps. By leveraging Python's `heapq` 
module, we can insert patients dynamically and extract the highest-priority case in O(log N) 
time, while maintaining FIFO order for ties using timestamps. 

Beyond healthcare, priority queues power CPU task schedulers, network routers managing 
critical data packets, and cloud infrastructure load balancers. Understanding how to manage 
urgency efficiently is a core superpower for every software engineer!

#SoftwareEngineering #DataStructures #PriorityQueue #Python #HealthcareTech #CodingJourney
"""

"""
Cybersecurity Vault Records Manager (Databases)
==============================================
Phase: Databases

Description:
A cybersecurity company stores sensitive vault records inside a secure database. 
This script builds a local SQLite database system implementing full CRUD (Create, Read, 
Update, Delete) operations, secure parameterized queries, and performance indexes.

Real-World Impact:
- Enterprise Applications: Powering banking ledgers, healthcare records, and e-commerce transactions.
- Security Best Practices: Preventing SQL injection via parameterized inputs and secure record isolation.
"""

import sqlite3
from datetime import datetime

class CyberVaultDatabase:
    """
    A secure database wrapper managing encrypted/sensitive vault records 
    using SQLite with optimized indexing and parameterized queries.
    """
    def __init__(self, db_name: str = "cyber_vault.db"):
        self.db_name = db_name
        self.initialize_database()

    def get_connection(self) -> sqlite3.Connection:
        """Establishes and returns a connection to the SQLite database."""
        conn = sqlite3.connect(self.db_name)
        # Enable dictionary-like row factory for cleaner data handling
        conn.row_factory = sqlite3.Row
        return conn

    def initialize_database(self):
        """Creates the vault records table and efficiency indexes if they don't exist."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            
            # Create vault records table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS vault_records (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    category TEXT NOT NULL,
                    secret_data TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            
            # Create an index on category for efficient lookups/filtering
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_vault_category 
                ON vault_records(category)
            """)
            
            conn.commit()
        print("[DATABASE] Vault schema initialized successfully with optimized indexes.")

    def add_record(self, title: str, category: str, secret_data: str) -> int:
        """CREATE: Inserts a new confidential record into the vault securely."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Parameterized query prevents SQL injection attacks
            cursor.execute("""
                INSERT INTO vault_records (title, category, secret_data)
                VALUES (?, ?, ?)
            """, (title, category, secret_data))
            conn.commit()
            record_id = cursor.lastrowid
            print(f"[CREATE] Record #{record_id} ('{title}') added to category [{category}].")
            return record_id

    def search_records(self, search_term: str) -> list[dict]:
        """READ: Efficiently searches records by title or category."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            # Using LIKE with parameters for secure pattern matching
            query = """
                SELECT id, title, category, secret_data, created_at 
                FROM vault_records 
                WHERE title LIKE ? OR category LIKE ?
                ORDER BY created_at DESC
            """
            wildcard_term = f"%{search_term}%"
            cursor.execute(query, (wildcard_term, wildcard_term))
            rows = cursor.fetchall()
            
            results = [dict(row) for row in rows]
            print(f"[READ] Search for '{search_term}' returned {len(results)} matching record(s).")
            return results

    def update_record(self, record_id: int, new_secret_data: str) -> bool:
        """UPDATE: Modifies sensitive information for an existing vault record."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE vault_records 
                SET secret_data = ?, updated_at = CURRENT_TIMESTAMP
                WHERE id = ?
            """, (new_secret_data, record_id))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"[UPDATE] Record #{record_id} successfully updated.")
                return True
            else:
                print(f"[UPDATE WARNING] Record #{record_id} not found.")
                return False

    def delete_record(self, record_id: int) -> bool:
        """DELETE: Permanently removes a record from the secure vault."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM vault_records WHERE id = ?", (record_id,))
            conn.commit()
            
            if cursor.rowcount > 0:
                print(f"[DELETE] Record #{record_id} purged from the vault.")
                return True
            else:
                print(f"[DELETE WARNING] Record #{record_id} not found.")
                return False

    def list_all_records(self):
        """Utility: Displays all records currently stored in the vault."""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT id, title, category, created_at FROM vault_records")
            rows = cursor.fetchall()
            
            print("\n--- SECURE VAULT INVENTORY ---")
            for row in rows:
                print(f"ID: {row['id']} | Title: {row['title']} | Category: {row['category']} | Created: {row['created_at']}")
            print("------------------------------\n")


# --- SQL Query Examples & Documentation ---
"""
--- SQL QUERY REFERENCE & EFFICIENCY NOTES ---
1. Parameterized Queries (Security):
   - Always use placeholders (?) instead of string formatting (f-strings) to pass user inputs. 
     This completely neutralizes SQL injection vulnerabilities.
     Example: `cursor.execute("SELECT * FROM vault_records WHERE id = ?", (record_id,))`

2. Efficient Indexing:
   - The `idx_vault_category` index ensures that filtering records by category runs in 
     O(log N) time instead of performing a costly full table scan (O(N)).

3. Complex Analytical Queries:
   - Counting records per category:
     `SELECT category, COUNT(*) as total FROM vault_records GROUP BY category;`
"""


# --- Execution and Testing Suite ---
if __name__ == "__main__":
    print("=== CYBERSECURITY VAULT DATABASE SYSTEM ===")
    
    # Initialize vault database (creates local file 'cyber_vault.db')
    vault = CyberVaultDatabase()
    
    # 1. CREATE Operations (Adding secret records)
    vault.add_record("Project Titan Access Keys", "Infrastructure", "AKIA_TEST_KEY_998877")
    vault.add_record("Master Admin Database Password", "Credentials", "Secur3P@ssw0rd_2026!")
    vault.add_record("SSL Wildcard Certificate", "Security", "-----BEGIN CERTIFICATE----- ...")
    
    # List current inventory
    vault.list_all_records()
    
    # 2. READ Operations (Searching records)
    vault.search_records("Password")
    
    # 3. UPDATE Operations (Rotating credentials)
    vault.update_record(2, "NewRotatedP@ssw0rd_2026#")
    
    # Verify update via search
    vault.search_records("Password")
    
    # 4. DELETE Operations (Purging obsolete records)
    vault.delete_record(3)
    
    # Final Inventory
    vault.list_all_records()

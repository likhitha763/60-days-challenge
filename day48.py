"""
Alien Message Translator (Edit Distance / Levenshtein Distance)
==============================================================
Phase: String Dynamic Programming

Description:
Scientists intercepted messages from an alien civilization. This script 
determines the minimum translation energy (edits: insertions, deletions, 
replacements) required to transform one alien string into another.

Real-World Impact:
- Autocorrect & Spell Checkers: Calculating word similarity and typo corrections.
- Computational Biology: Aligning DNA, RNA, and protein sequences.
- Natural Language Processing (NLP): Machine translation evaluation metrics (BLEU, WER).
"""

def min_distance_dp(word1: str, word2: str) -> int:
    """
    Approach 1: Bottom-Up Dynamic Programming (Tabulation)
    -------------------------------------------------------
    Builds a 2D matrix where dp[i][j] represents the minimum edit distance 
    between the first `i` characters of word1 and the first `j` characters of word2.
    
    Time Complexity: O(M * N) where M and N are the lengths of the two strings.
    Space Complexity: O(M * N) for the 2D DP table.
    """
    m, n = len(word1), len(word2)
    
    # Create (m + 1) x (n + 1) DP table
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    # Base cases: converting empty string to/from word substrings
    for i in range(m + 1):
        dp[i][0] = i  # Deleting all characters from word1
    for j in range(n + 1):
        dp[0][j] = j  # Inserting all characters into word1
        
    # Fill the DP table
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                # Characters match, no operation cost added
                dp[i][j] = dp[i - 1][j - 1]
            else:
                # Minimum of Delete (dp[i-1][j]), Insert (dp[i][j-1]), Replace (dp[i-1][j-1]) + 1 cost
                dp[i][j] = 1 + min(
                    dp[i - 1][j],    # Deletion
                    dp[i][j - 1],    # Insertion
                    dp[i - 1][j - 1] # Replacement
                )
                
    return dp[m][n]


def min_distance_memoized(word1: str, word2: str) -> int:
    """
    Approach 2: Top-Down Recursion with Memoization
    ----------------------------------------------
    Breaks down the problem from the full strings down to base cases, 
    caching overlapping sub-problems to avoid exponential time overhead.
    
    Time Complexity: O(M * N)
    Space Complexity: O(M * N) for the memoization cache and call stack.
    """
    memo = {}
    
    def helper(i, j):
        # If word1 is exhausted, we need to insert all remaining characters of word2
        if i == 0:
            return j
        # If word2 is exhausted, we need to delete all remaining characters of word1
        if j == 0:
            return i
            
        if (i, j) in memo:
            return memo[(i, j)]
            
        if word1[i - 1] == word2[j - 1]:
            memo[(i, j)] = helper(i - 1, j - 1)
        else:
            memo[(i, j)] = 1 + min(
                helper(i - 1, j),     # Delete
                helper(i, j - 1),     # Insert
                helper(i - 1, j - 1)  # Replace
            )
            
        return memo[(i, j)]

    return helper(len(word1), len(word2))


def visualize_dp_table(word1: str, word2: str):
    """
    Visualizer: Generates and prints the DP table matrix to show 
    how edit costs accumulate across string transformations.
    """
    print(f"\n--- Visualizing DP Table for '{word1}' -> '{word2}' ---")
    m, n = len(word1), len(word2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    
    for i in range(m + 1):
        dp[i][0] = i
    for j in range(n + 1):
        dp[0][j] = j
        
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if word1[i - 1] == word2[j - 1]:
                dp[i][j] = dp[i - 1][j - 1]
            else:
                dp[i][j] = 1 + min(dp[i - 1][j], dp[i][j - 1], dp[i - 1][j - 1])
                
    # Print Header Row
    header = ["  ", "ε"] + list(word2)
    print(" ".join(f"{h:>3}" for h in header))
    
    # Print Rows with word1 labels
    for i in range(m + 1):
        row_label = "ε" if i == 0 else word1[i - 1]
        row_values = [f"{dp[i][j]:>3}" for j in range(n + 1)]
        print(f"{row_label:>3} " + " ".join(row_values))
    print(f"-> Minimum Translation Energy (Edit Distance): {dp[m][n]}\n")


# --- Execution and Testing ---
if __name__ == "__main__":
    print("=== ALIEN MESSAGE TRANSLATOR SYSTEM ===")
    
    # Test Case 1: Standard Alien Signal Translation
    alien_signal_a = "horse"
    alien_signal_b = "ros"
    
    print(f"\n[Test 1: Translating '{alien_signal_a}' to '{alien_signal_b}']")
    print(f"Bottom-Up DP Energy Cost : {min_distance_dp(alien_signal_a, alien_signal_b)}")
    print(f"Memoized Top-Down Cost   : {min_distance_memoized(alien_signal_a, alien_signal_b)}")
    visualize_dp_table(alien_signal_a, alien_signal_b)
    
    print("=" * 60)
    
    # Test Case 2: Complex Signal Mutation
    alien_signal_c = "intention"
    alien_signal_d = "execution"
    
    print(f"\n[Test 2: Translating '{alien_signal_c}' to '{alien_signal_d}']")
    print(f"Bottom-Up DP Energy Cost : {min_distance_dp(alien_signal_c, alien_signal_d)}")
    visualize_dp_table(alien_signal_c, alien_signal_d)

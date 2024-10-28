from collections import defaultdict, Counter
from datetime import datetime, timedelta

def top_k_users_with_longest_streaks(log_file_path, K):
    """
    This function processes a log file of user activities and returns the top K users 
    with the longest consecutive daily activity streaks. If multiple users have the same
    streak length, the user with a higher overall activity count is prioritized.

    Args:
    - log_file_path: String representing the path to the log file.
    - K: Integer representing the number of top users to return.

    Returns:
    - List of user IDs with the longest consecutive activity streaks.
    """

    # Step 1: Parse the log and organize activity by user
    user_activity = defaultdict(set)
    activity_count = Counter()

    # Read the log file
    with open(log_file_path, 'r') as file:
        for line in file:
            date_str, user_id, _ = line.strip().split(", ")
            date = datetime.strptime(date_str, "%Y-%m-%d").date()
            user_activity[user_id].add(date)
            activity_count[user_id] += 1  # Count total activities for tie-breaking

    # Step 2: Calculate the longest streak for each user
    user_streaks = {}

    for user_id, dates in user_activity.items():
        sorted_dates = sorted(dates)
        max_streak = 1
        current_streak = 1

        for i in range(1, len(sorted_dates)):
            if sorted_dates[i] == sorted_dates[i - 1] + timedelta(days=1):
                current_streak += 1
            else:
                max_streak = max(max_streak, current_streak)
                current_streak = 1
        
        max_streak = max(max_streak, current_streak)  # Final max for the user
        user_streaks[user_id] = max_streak

    # Step 3: Sort users first by longest streak, then by total activity count
    sorted_users = sorted(user_streaks.keys(), key=lambda user: (-user_streaks[user], -activity_count[user]))

    # Step 4: Return the top K users
    return sorted_users[:K]

# Example usage
log_file_path = 'log_file.txt'  # Specify the path to your log file
K = 2
top_users = top_k_users_with_longest_streaks(log_file_path, K)
print(top_users)  # Example output: ['User3', 'User1']

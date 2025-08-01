from datetime import datetime

def calculate_fine(issue_date, return_date, daily_rate=5):
    issue = datetime.strptime(issue_date, "%Y-%m-%d")
    ret = datetime.strptime(return_date, "%Y-%m-%d")
    delta_days = (ret - issue).days
    overdue_days = max(0, delta_days - 14)
    return overdue_days * daily_rate

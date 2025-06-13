from datetime import datetime, timezone, timedelta

def convert_to_ist(timestamp_ms):
    """
    Converts a Unix timestamp in milliseconds to IST datetime string.
    
    Args:
        timestamp_ms (int): Unix timestamp in milliseconds.
        
    Returns:
        str: Date and time in IST (YYYY-MM-DD HH:MM:SS format).
    """
    # Convert milliseconds to seconds
    timestamp_s = timestamp_ms / 1000

    # Create UTC datetime
    dt_utc = datetime.fromtimestamp(timestamp_s, tz=timezone.utc)

    # Define IST timezone (UTC+5:30)
    ist_timezone = timezone(timedelta(hours=5, minutes=30))

    # Convert to IST
    dt_ist = dt_utc.astimezone(ist_timezone)

    return dt_ist
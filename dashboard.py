import mysql.connector
import time
from rich.live import Live
from rich.table import Table
from rich.console import Console

# Database Connection
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root", # Keep your password
    database="fraud_engine",
    autocommit=True  # <--- THIS IS THE MAGIC FIX
)
console = Console()

def fetch_active_fraud():
    cursor = db.cursor(dictionary=True)
    # The fix: ORDER BY last_attempt DESC ensures real-time streaming behavior
    cursor.execute("""
        SELECT ip_address, email, failed_attempts, total_fraud_value, duration_seconds 
        FROM vw_fraud_velocity_alerts 
        ORDER BY last_attempt DESC 
        LIMIT 10
    """)
    results = cursor.fetchall()
    cursor.close()
    return results

def fetch_system_stats():
    cursor = db.cursor()
    # Count total blocked devices using the trigger we built
    cursor.execute("SELECT COUNT(*) FROM devices WHERE is_blocked = TRUE")
    blocked_count = cursor.fetchone()[0]
    cursor.close()
    return blocked_count

def generate_table():
    fraud_data = fetch_active_fraud()
    blocked_total = fetch_system_stats()
    
    # Building the UI
    table = Table(
        title=f"🚨 ACTIVE FRAUD ALERTS (Total Devices Blocked: {blocked_total}) 🚨", 
        style="red",
        header_style="bold white on red"
    )
    
    table.add_column("IP Address", style="cyan")
    table.add_column("Compromised Email", style="magenta")
    table.add_column("Failed Attempts", justify="right", style="yellow")
    table.add_column("Fraud Value ($)", justify="right", style="green")
    table.add_column("Velocity (Seconds)", justify="right", style="white")

    for row in fraud_data:
        table.add_row(
            row["ip_address"],
            row["email"],
            str(row["failed_attempts"]),
            f"${row['total_fraud_value']:,.2f}",
            str(row["duration_seconds"])
        )
        
    if not fraud_data:
        table.add_row("---", "No active fraud detected", "---", "---", "---")
        
    return table

if __name__ == "__main__":
    console.clear()
    # The Live context manager updates the terminal in place without scrolling
    with Live(generate_table(), refresh_per_second=2) as live:
        try:
            while True:
                time.sleep(1) # Poll the database every 1 second
                live.update(generate_table())
        except KeyboardInterrupt:
            console.print("[bold green]Dashboard terminated.[/bold green]")
            db.close()
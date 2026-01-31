import psutil
import time

def get_system_stats():
    try:
        cpu_usage = psutil.cpu_percent(interval=1)
        ram = psutil.virtual_memory()
        ram_usage = ram.percent
        
        # Get battery if laptop
        battery = psutil.sensors_battery()
        battery_usage = battery.percent if battery else 100
        
        return {
            "cpu": cpu_usage,
            "ram": ram_usage,
            "battery": battery_usage,
            "status": "Optimal" if cpu_usage < 80 else "Overloaded"
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    print(get_system_stats())

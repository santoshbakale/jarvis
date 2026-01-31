import time
import threading
import win32gui
import win32clipboard

class NotificationBridge:
    def __init__(self):
        self.last_window = ""
        self.last_clipboard = ""
        self.new_notifications = []
        self.running = False

    async def initialize(self):
        self.running = True
        return True

    async def poll_notifications(self):
        # 1. Monitor Window Changes
        try:
            window = win32gui.GetWindowText(win32gui.GetForegroundWindow())
            if window and window != self.last_window:
                if any(app in window.lower() for app in ["chrome", "code", "spotify", "discord", "slack"]):
                    app_name = "System"
                    if "chrome" in window.lower(): app_name = "Browser"
                    if "code" in window.lower(): app_name = "Development"
                    
                    self.new_notifications.append({
                        "id": f"win_{time.time()}",
                        "app": "SEC_EYE",
                        "title": f"Focus Shift: {app_name}",
                        "body": f"Activating profile for {window[:30]}..."
                    })
                self.last_window = window
        except:
            pass

        # 2. Monitor Clipboard
        try:
            win32clipboard.OpenClipboard()
            data = win32clipboard.GetClipboardData()
            win32clipboard.CloseClipboard()
            
            if data and data != self.last_clipboard and isinstance(data, str):
                if len(data) > 2:
                    self.new_notifications.append({
                        "id": f"clip_{time.time()}",
                        "app": "DATA_BRIDGE",
                        "title": "Intercepted Data",
                        "body": f"Sir, I've secured the copied snippet: {data[:40]}..."
                    })
                self.last_clipboard = data
        except:
            try: win32clipboard.CloseClipboard()
            except: pass

        return self.new_notifications

    def get_latest(self):
        res = list(self.new_notifications)
        self.new_notifications = []
        return res

if __name__ == "__main__":
    async def test():
        bridge = NotificationBridge()
        if await bridge.initialize():
            print("Listening for notifications...")
            while True:
                new = await bridge.poll_notifications()
                if new:
                    print(f"New Notifications: {new}")
                await asyncio.sleep(2)
    
    asyncio.run(test())

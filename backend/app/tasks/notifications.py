import threading


def send_booking_confirmation(email: str, event_title: str):
    def _send():
        print(f"[ASYNC] Email sent to {email} for event '{event_title}'")

    threading.Thread(target=_send, daemon=True).start()

"""WhatsApp alerts via Twilio, sent from a background thread so the video loop never blocks."""
import logging
import os
import queue
import threading

_client = None
_queue: "queue.Queue[str]" = queue.Queue()
_worker_started = False


def _get_client():
    global _client
    if _client is None:
        sid, token = os.getenv("TWILIO_ACCOUNT_SID"), os.getenv("TWILIO_AUTH_TOKEN")
        if not (sid and token):
            return None
        from twilio.rest import Client
        _client = Client(sid, token)
    return _client


def _worker():
    while True:
        body = _queue.get()
        client = _get_client()
        sender, recipient = os.getenv("TWILIO_WHATSAPP_NUMBER"), os.getenv("RECIPIENT_NUMBER")
        if not (client and sender and recipient):
            logging.warning("alert_skipped reason=twilio_not_configured message=%r", body)
            continue
        try:
            msg = client.messages.create(body=body, from_=sender, to=recipient)
            logging.info("alert_sent sid=%s", msg.sid)
        except Exception as e:  # network or Twilio error; keep the worker alive
            logging.error("alert_failed error=%s", e)


def send_alert(message: str):
    global _worker_started
    if not _worker_started:
        threading.Thread(target=_worker, daemon=True).start()
        _worker_started = True
    _queue.put(message)

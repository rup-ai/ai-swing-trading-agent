
import os
from unittest.mock import Mock, patch

from alerts.telegram import TelegramAlert


def main():
    with patch.dict(os.environ, {
        "TELEGRAM_BOT_TOKEN": "test-token",
        "TELEGRAM_CHAT_ID": "test-chat"
    }):
        with patch("alerts.telegram.requests.post") as post:
            response = Mock()
            response.status_code = 200
            response.json.return_value = {
                "ok": True,
                "result": {"message_id": 1}
            }
            response.raise_for_status.return_value = None
            post.return_value = response

            telegram = TelegramAlert()

            # Verify a normal message
            result = telegram.send_message("RupAI test report")

            assert len(result) == 1
            assert post.call_count == 1

            # Verify long messages are split, not truncated
            post.reset_mock()
            post.return_value = response

            long_message = "X" * 8000
            result = telegram.send_message(long_message)

            assert len(result) >= 3
            assert post.call_count == len(result)

            sent_text = "".join(
                call.kwargs["json"]["text"]
                for call in post.call_args_list
            )

            assert sent_text == long_message

            # Verify Telegram API rejection is detected
            post.reset_mock()
            rejected = Mock()
            rejected.raise_for_status.return_value = None
            rejected.json.return_value = {
                "ok": False,
                "description": "Test rejection"
            }
            post.return_value = rejected

            try:
                telegram.send_message("Rejected test")
            except RuntimeError:
                pass
            else:
                raise AssertionError(
                    "Telegram API rejection was not detected."
                )

    print("\nPASS: Telegram sender tests completed.")


if __name__ == "__main__":
    main()

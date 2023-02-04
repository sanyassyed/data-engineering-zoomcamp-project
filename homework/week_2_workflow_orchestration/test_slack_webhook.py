from prefect.blocks.notifications import SlackWebhook

slack_webhook_block = SlackWebhook.load("notifysuccess")
slack_webhook_block.notify("Hello from Prefect!")

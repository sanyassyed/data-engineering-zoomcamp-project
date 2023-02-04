from prefect.blocks.notifications import SlackWebhook

slack_webhook_block = SlackWebhook.load("notifysuccess")
slack_webhook_block.notify("Hello from Prefect!")

# Personal workspace webhook https://hooks.slack.com/services/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
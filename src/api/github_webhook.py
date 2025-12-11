import os
import hmac
import hashlib
from flask import Flask, request, jsonify, abort

app = Flask(__name__)

# Retrieve GitHub Webhook Secret from environment variables
# IMPORTANT: Use a strong, unique secret for each webhook setup.
GITHUB_WEBHOOK_SECRET = os.environ.get('GITHUB_WEBHOOK_SECRET')

@app.route('/webhook/github', methods=['POST'])
def github_webhook():
    if GITHUB_WEBHOOK_SECRET is None:
        app.logger.error("GITHUB_WEBHOOK_SECRET environment variable not set. Webhook verification will fail.")
        abort(500, description="Server misconfiguration: Webhook secret not set.")

    # 1. Get GitHub Event and Signature Headers
    github_event = request.headers.get('X-GitHub-Event')
    github_signature = request.headers.get('X-Hub-Signature-256')

    if not github_event or not github_signature:
        app.logger.warning("Missing X-GitHub-Event or X-Hub-Signature-256 header.")
        abort(400, description="Missing required GitHub headers.")

    # 2. Get Raw Request Body for Signature Verification
    # It's crucial to use the raw body, not request.json, as request.json might re-encode it.
    payload_body = request.get_data()

    # 3. Verify Signature
    try:
        # 'sha256=' prefix is part of the header, remove it for hmac comparison
        if not github_signature.startswith('sha256='):
            raise ValueError("Invalid X-Hub-Signature-256 format.")

        expected_signature = "sha256=" + hmac.new(
            GITHUB_WEBHOOK_SECRET.encode('utf-8'),
            msg=payload_body,
            digestmod=hashlib.sha256
        ).hexdigest()

        if not hmac.compare_digest(expected_signature, github_signature):
            app.logger.warning("Invalid GitHub webhook signature.")
            abort(401, description="Invalid GitHub webhook signature.")

    except ValueError as e:
        app.logger.error(f"Signature verification error: {e}")
        abort(400, description=f"Signature processing error: {e}")
    except Exception as e:
        app.logger.error(f"Unexpected error during signature verification: {e}")
        abort(500, description="Internal server error during signature verification.")

    # 4. Parse Payload (only after successful signature verification)
    try:
        payload = request.json
    except Exception as e:
        app.logger.error(f"Failed to parse JSON payload: {e}")
        abort(400, description="Invalid JSON payload.")

    app.logger.info(f"Received GitHub '{github_event}' event.")

    # Example: Process pull_request events
    if github_event == 'pull_request':
        action = payload.get('action')
        pull_request = payload.get('pull_request')
        repository = payload.get('repository')

        if pull_request and repository and action:
            pr_id = pull_request.get('id')
            pr_number = pull_request.get('number')
            repo_full_name = repository.get('full_name')
            app.logger.info(f"Processing PR #{pr_number} ({action}) in {repo_full_name} (PR ID: {pr_id})")
            # --- Your logic for PR analysis goes here ---
            # e.g., trigger LLM analysis, update database, add comment to PR
        else:
            app.logger.warning(f"Received pull_request event with missing key data: {payload}")

    # You can add more `elif github_event == '...'` blocks for other event types

    return jsonify({"status": "success", "message": "Webhook received and processed."}), 200

if __name__ == '__main__':
    # For development: `export GITHUB_WEBHOOK_SECRET="your_super_secret_key"`
    # In production, use a proper WSGI server (e.g., Gunicorn) and environment variable management.
    app.run(host='0.0.0.0', port=5000)

from flask import Flask, request, jsonify, render_template
from db_manager import add_alert, list_alerts, delete_alert
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Sample job categories for users to select
categories = {
    "Accounting & Consulting": "531770282584862721",
    "Admin Support": "531770282580668416",
    "Customer Service": "531770282580668417",
    "Data Science & Analytics": "531770282580668420",
    "Design & Creative": "531770282580668421",
    "Engineering & Architecture": "531770282584862722",
    "IT & Networking": "531770282580668419",
    "Legal": "531770282584862723",
    "Sales & Marketing": "531770282580668422",
    "Translation": "531770282584862720",
    "Web, Mobile & Software Dev": "531770282580668418",
    "Writing": "531770282580668423",
}

@app.route('/categories', methods=['GET'])
def get_categories():
    """Return available job categories."""
    return jsonify(categories)

@app.route('/alerts', methods=['POST'])
def create_alert():
    """Create a new job alert."""
    data = request.json
    user_id = data.get('user_id')
    filters = data.get('filters')
    
    if not user_id or not filters:
        return jsonify({"error": "Missing user_id or filters"}), 400

    add_alert(user_id, filters)
    return jsonify({"message": "Alert created successfully"}), 201

@app.route('/alerts/<user_id>', methods=['GET'])
def get_alerts(user_id):
    """Retrieve alerts for a specific user."""
    alerts = list_alerts(user_id)
    return jsonify(alerts)

@app.route('/alerts/<alert_id>', methods=['DELETE'])
def remove_alert(alert_id):
    """Delete a specific alert by its ID."""
    delete_alert(alert_id)
    return jsonify({"message": "Alert deleted successfully"}), 200

# Route to render the alert form in a Web View
@app.route('/set-alert', methods=['GET'])
def alert_form():
    """Render the HTML form for alert setup."""
    return render_template("alert_form.html", categories=categories)

if __name__ == '__main__':
    app.run(debug=True)

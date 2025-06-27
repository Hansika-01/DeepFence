import os
from flask import jsonify
from flask import render_template
from flask_cors import CORS
from flask import Flask
import logging
import os
import psycopg2

from WorkflowAgents.execute import run_agents
from static.Telemetry import ReadTelemetry,CountEventStatus

app = Flask(__name__)


from socket_io_setup import socketio
socketio.init_app(app, cors_allowed_origins="*")
# socketio = SocketIO(app, cors_allowed_origins="*", allow_EIO3=True)
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
app.config['model'] = ""
app.config['mname'] = ""
app.config['vname'] = ""

# Create a global logger object
logger = logging.getLogger(__name__)

# Configure the logger to use Stackdriver Logging
# You can also set the logging level and format if needed
logging.basicConfig(level=logging.INFO)


@app.route("/execute_agents", methods=["GET"])
async def execute_agents_route():
    """Asynchronous route to execute agents."""
    results = await run_agents()  # Correctly await the async function
    return jsonify(results)

@app.route("/")
def Landing():  
  return render_template('index.html')

@app.route("/AgenticWorkflow")
def AgenticWorkflow():  
  return render_template('AgenticWorkflow.html')

@app.route("/AgentTelemetry")
def AgentTelemetry():  
  return render_template('AgentTelemetry.html')

@app.route("/DataLoader")
def DataLoader():  
  return render_template('DataLoader.html')

@app.route("/AgentDashboard")
def AgentDashboard():  
  return render_template('AgentDashboard.html')

@app.route("/Contact")
def Contact():  
  return render_template('Contact.html')

@app.route("/FetchFromFirestore")
def FetchFromFirestore():
    return ReadTelemetry()


@app.route("/FetchFromDatabase")
def FetchFromDatabase():
    data = []
    try:
        event_count = CountEventStatus()
        return {"EventStatus":event_count}
    except Exception as error:
        print("Error fetching records from Firebase: ", error)
        return {"message": "Error fetching records from Firebase: " + error}
    

if __name__ == '__main__':
    app.run(debug=False, port=5000, host='0.0.0.0')

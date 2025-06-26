from flask import jsonify
from socket_io_setup import socketio
import google.cloud.firestore
import json
from datetime import datetime # Make sure datetime is imported
 
def paramsFilling(Workflow,EventTypeID, EventDescription, EventData, ObjectID,ChangeWorkflow=False):
    # Get the current datetime
    now = datetime.now()

    # Format it to include up to seconds
    formatted_time = now.strftime("%Y-%m-%dT%H:%M:%S")

    # print(formatted_time)
    telemetryObj = {
        "Workflow":Workflow,
        "Timestamp": formatted_time,
        "UserID": 1,
        "EventSourceID": 2,
        "EventTypeID": EventTypeID,
        "EventDescription": EventDescription,
        "EventData": EventData,
        "ObjectID": ObjectID
    }

    dbparams = {
        "queryType": "insert",
        "TelemetryObj": telemetryObj
    }
    socketio.emit(f'AgentExecuted', json.dumps(telemetryObj))
    if ChangeWorkflow:
        socketio.emit(f'WorkflowCompleted', "Workflow Completed")
    ManageTelemetry(dbparams)
    return "Working"

# --- Configuration ---
# project_id = "YOUR_CORRECT_GCP_PROJECT_ID" # You can often omit this if GOOGLE_APPLICATION_CREDENTIALS is set
database_id = "deepfence" # Ensure this is the correct ID for your Firestore database
collection_name = "eventData"
db = None # Initialize db to None

def FirestoreConnection():
    # global db # Declare db as a global variable
    # --- Initialize Firestore Client ---
    try:
        # The client will automatically look for GOOGLE_APPLICATION_CREDENTIALS
        db = google.cloud.firestore.Client(database=database_id)
        print(f"Successfully connected to Firestore database: {database_id}")
        return db
    except Exception as e:
        print(f"Error initializing Firestore client: {e}")
        print("Please ensure GOOGLE_APPLICATION_CREDENTIALS environment variable is set correctly,")
        print("or you are running in a Google Cloud environment with appropriate default credentials.")
        exit(1) # Exit if connection fails

def ManageTelemetry(dbparams):  
    db=FirestoreConnection()
    telemetryObj =dbparams["TelemetryObj"]
    # --- Add Data to Firestore ---
    if db: # Only proceed if db client was initialized successfully
        try:
            doc_ref = db.collection(collection_name)
            doc_id = f"event_{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{telemetryObj['EventTypeID']}"
            doc_ref.document(doc_id).set(telemetryObj)
            print(f"Document '{doc_id}' added to collection '{collection_name}' in database '{database_id}'.")
            print("Data added:")
            for key, value in telemetryObj.items():
                print(f"  {key}: {value}")
        except Exception as e:
            print(f"Error adding data to Firestore: {e}")
    else:
        print("Firestore client not initialized. Cannot add data.")

# --- Helper Function for JSON Serialization ---
def serialize_firestore_document(doc):
    """
    Converts a Firestore document object into a dictionary,
    handling special types like datetime for JSON serialization.
    Adds the document ID as a field.
    """
    if not doc.exists:
        return None

    data = doc.to_dict()
    data['id'] = doc.id # Add the document ID to the dictionary

    # Convert datetime objects to ISO 8601 strings for JSON compatibility
    for key, value in data.items():
        if isinstance(value, datetime):
            data[key] = value.isoformat()
        # You might add handling for other types if necessary, e.g., GeoPoint, Reference

    return data


# --- Fetch all documents from collection as a list of dictionaries ---
def fetch_all_documents_as_list_of_json(database_client, collection_name_str):
    """
    Fetches all documents from a specified Firestore collection
    and returns them as a list of dictionaries (JSON-like objects).
    Each dictionary includes the document 'id'.
    """
    all_documents_list = []
    if database_client:
        try:
            docs_stream = database_client.collection(collection_name_str).stream()
            for doc in docs_stream:
                serialized_data = serialize_firestore_document(doc)
                if serialized_data:
                    all_documents_list.append(serialized_data)
            print(f"Fetched {len(all_documents_list)} documents from '{collection_name_str}'.")
        except Exception as e:
            print(f"Error fetching documents from collection '{collection_name_str}': {e}")
    else:
        print("Firestore client not initialized. Cannot fetch data.")
    return all_documents_list



def ReadTelemetry():
    TelemetryData=[]
    db=FirestoreConnection()
    documents_as_json_list = fetch_all_documents_as_list_of_json(db, collection_name)

    if documents_as_json_list:
        print("\n--- Fetched Data (first 5 documents for brevity): ---")
        for i, doc_data in enumerate(documents_as_json_list):
            # if i >= 5: # Print only first 5 for readability if many docs
            #     print(f"... and {len(documents_as_json_list) - 5} more documents.")
            #     break
            # Use json.dumps for pretty printing if you want to see actual JSON string format
            print(json.dumps(doc_data, indent=2))
            TelemetryData.append(doc_data)
        return json.dumps(TelemetryData, indent=2)
           
    else:
        print("No documents were fetched. The list is empty.")    


def CountEventStatus():
    """
    Counts events specifically for "Success", "Error", and "Timeout" statuses
    from the nested 'EventData.Status' property in Google Cloud Firestore.
    
    Returns a JSON object with counts for these specific statuses.
    Missing statuses will have a count of 0.
    """
    # Initialize counts for the specific statuses we are interested in
    specific_event_status_counts = {
        "Success": 0,
        "Error": 0,
        "Timeout": 0
    }

    workflow_counts= {}
    db=FirestoreConnection()
    try:
        # 1. Get a reference to the 'Event' collection
        events_ref = db.collection('eventData')
        
        query = events_ref.where('EventTypeID', '>=', 13000)

        docs = list(query.stream())
        
        # 4. Iterate through fetched documents and count statuses
        for doc in docs:
            # doc.to_dict() converts the DocumentSnapshot to a Python dictionary
            event_data_dict = doc.to_dict()
            
            # Access the nested 'EventData' dictionary
            event_data_str = event_data_dict.get('EventData')
            event_data = json.loads(event_data_str)
            
            status = event_data.get('Status')
            # print(status)
            # Only count if the status is one of our target statuses
            if "Success" in status:
                specific_event_status_counts["Success"] += 1
            elif "Error" in status:
                specific_event_status_counts["Error"] += 1
            elif "Timeout" in status:
                specific_event_status_counts["Timeout"] += 1

             # Get the 'Workflow' field directly
        #     workflow = event_data_dict.get('Workflow')
            
        #     if workflow:  # Only count if 'Workflow' field exists and is not None
        #         if workflow not in workflow_counts:
        #             workflow_counts[workflow] = 0
        #         workflow_counts[workflow] += 1

        # output_list = []
        # for workflow_name, count in workflow_counts.items():
        #     output_list.append({"workflow": workflow_name, "count": count})
        # print(output_list)
        print(specific_event_status_counts)
        list_of_json_format = [
            {"value": count, "category": status}
            for status, count in specific_event_status_counts.items()
        ]
        print(list_of_json_format)
        return list_of_json_format

    except Exception as e:
        print(f"Error counting specific event statuses from Firestore: {e}")
        # In a production app, you might log the full traceback for debugging
        return {"message": f"Error fetching data from Firestore: {str(e)}"}, 500
    

    
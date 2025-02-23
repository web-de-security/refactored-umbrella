# DBModule: Simulates a simple database with basic CRUD operations.
class DBModule:
    def __init__(self):
        self.data = ["record1", "record2", "record3"]

    def get_data(self):
        """Retrieve all records from the database."""
        return self.data

    def add_record(self, record):
        """Add a new record to the database."""
        self.data.append(record)
        return self.data

    def update_record(self, index, record):
        """Update a record at the given index."""
        if 0 <= index < len(self.data):
            self.data[index] = record
            return self.data
        else:
            raise IndexError("Record index out of range")

    def delete_record(self, index):
        """Delete a record at the given index."""
        if 0 <= index < len(self.data):
            removed = self.data.pop(index)
            return removed
        else:
            raise IndexError("Record index out of range")

# NetworkModule: Simulates network operations like fetching and posting data.
class NetworkModule:
    def fetch_data(self):
        """Simulate fetching data from a network API."""
        # In a real application, you would make an HTTP request here.
        return {"status": 200, "data": ["api_record1", "api_record2"]}

    def post_data(self, payload):
        """Simulate posting data to a network API."""
        print("Posting data to network:", payload)
        return {"status": 201, "message": "Created"}

    def update_remote(self, record_id, data):
        """Simulate updating a remote record."""
        print(f"Updating remote record {record_id} with {data}")
        return {"status": 200, "message": "Updated"}

# UseCaseModule: Contains business logic that integrates DB and network operations.
class UseCaseModule:
    def __init__(self, db_module, network_module):
        self.db = db_module
        self.network = network_module

    def process_data(self):
        """Combine local DB records with data fetched from the network."""
        db_data = self.db.get_data()
        net_response = self.network.fetch_data()
        net_data = net_response.get("data", [])
        combined = db_data + net_data
        summary = f"Combined data count: {len(combined)}"
        return {"combined_data": combined, "summary": summary}

    def sync_data(self):
        """Sync local DB data with the network by posting combined data."""
        processed = self.process_data()
        payload = processed["combined_data"]
        response = self.network.post_data(payload)
        return response

    def update_record_both(self, index, new_record):
        """
        Update a local record and simulate updating the corresponding
        remote record (using the same index as an ID).
        """
        updated_data = self.db.update_record(index, new_record)
        remote_response = self.network.update_remote(index, new_record)
        return {"local": updated_data, "remote": remote_response}

# ViewModelModule: Handles presentation logic and user interactions.
class ViewModelModule:
    def __init__(self, use_case_module):
        self.use_case = use_case_module

    def display_summary(self):
        """Print a summary of the combined data."""
        result = self.use_case.process_data()
        print("Summary:", result["summary"])

    def display_combined_data(self):
        """Print all combined data from local and network sources."""
        result = self.use_case.process_data()
        print("Combined Data:", result["combined_data"])

    def sync_and_display(self):
        """Sync data with the network and display the network response."""
        response = self.use_case.sync_data()
        print("Sync Response:", response)

    def update_and_display(self, index, new_record):
        """Update a record locally and remotely, then display results."""
        result = self.use_case.update_record_both(index, new_record)
        print(f"Updated Local Data: {result['local']}")
        print(f"Remote Update Response: {result['remote']}")

def main():
    # Dependency Injection
    db_module = DBModule()
    network_module = NetworkModule()
    use_case = UseCaseModule(db_module, network_module)
    view_model = ViewModelModule(use_case)

    # Display initial state
    print("=== Initial Data ===")
    view_model.display_summary()
    view_model.display_combined_data()

    # Add a new record to the database
    print("\n=== Adding New Record to DB ===")
    db_module.add_record("record4")
    view_model.display_summary()
    view_model.display_combined_data()

    # Update a record locally and remotely
    print("\n=== Updating Record at Index 1 ===")
    view_model.update_and_display(1, "updated_record2")

    # Sync local data with the network
    print("\n=== Syncing Data with Network ===")
    view_model.sync_and_display()

    # Delete a record from the database
    print("\n=== Deleting Record at Index 0 ===")
    removed = db_module.delete_record(0)
    print("Removed Record:", removed)
    view_model.display_summary()
    view_model.display_combined_data()

if __name__ == "__main__":
    main()

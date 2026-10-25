import json
import time
import hashlib
from datetime import datetime

class GlobalNodeTelemetry:
    def __init__(self, node_id: str, region: str):
        self.node_id = node_id
        self.region = region
        self.metrics_log = []

    def collect_telemetry(self, solar_output_kwh: float, water_ph: float, dissolved_oxygen_mg_l: float) -> dict:
        """Simulates collection of off-grid sensor data from the 1-Hectare eco-parcel."""
        timestamp = datetime.utcnow().isoformat()
        
        payload = {
            "node_id": self.node_id,
            "region": self.region,
            "timestamp": timestamp,
            "sensors": {
                "solar_kwh": solar_output_kwh,
                "water_ph": water_ph,
                "dissolved_oxygen_mg_l": dissolved_oxygen_mg_l
            },
            "status": "OPTIMAL" if (6.5 <= water_ph <= 8.5 and dissolved_oxygen_mg_l >= 5.0) else "WARNING"
        }
        
        # Generate cryptographic hash for immutable record (DePIN audit trail)
        payload_string = json.dumps(payload, sort_keys=True)
        payload["data_hash"] = hashlib.sha256(payload_string.encode()).hexdigest()
        
        self.metrics_log.append(payload)
        return payload

if __name__ == "__main__":
    # Initialize a node instance
    node = GlobalNodeTelemetry(node_id="NODE-EU-CLUJ-01", region="Romania-Pisciculture-Zone")
    
    print("--- Initializing Decentralized Node Telemetry Audit ---")
    telemetry_data = node.collect_telemetry(solar_output_kwh=42.5, water_ph=7.2, dissolved_oxygen_mg_l=6.8)
    
    print(json.dumps(telemetry_data, indent=4))

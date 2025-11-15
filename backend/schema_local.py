EXPECTED_SCHEMA = {
    "type": "string (RANSOMWARE_DETECTED)",
    "severity": "low|medium|high",
    "timestamp": "ISO timestamp",
    "process": {
        "pid": "int",
        "name": "string",
        "exe": "string",
        "cmdline": "list of strings",
        "username": "string"
    },
    "network": {
        "attacker_ip": "string",
        "port": "int"
    },
    "events": [
        {
            "event_type": "string",
            "details": "dict"
        }
    ],
    "artifacts": [
        {
            "file_path": "string",
            "operation": "string",
            "hash": "string"
        }
    ]
}

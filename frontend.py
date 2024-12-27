from flask import Flask, jsonify, request
from kubernetes import client,config
import json
import os
import re
import logging
from pathlib import path 
from typing import List, Dict
import time
import logging
import re
from kubernetes import client

def create_load_test_modal() -> Dict:
    """Create the main load test management modal."""
    return {
        "type": "modal",
        "callback_id": "load_test_modal",
        "title": {
            "type": "plain_text",
            "text": "Load Test Management"
        },
        "blocks": [
            {
                "type": "input",
                "block_id": "job_name_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "job_name_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Enter the job name"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Job Name"
                }
            },
            {
                "type": "input",
                "block_id": "vus_block",
                "element": {
                    "type": "number_input",
                    "action_id": "vus_input",
                    "is_decimal_allowed": False,
                    "min_value": "1",
                    "initial_value": "1"
                },
                "label": {
                    "type": "plain_text",
                    "text": "Virtual Users"
                }
            },
            {
                "type": "input",
                "block_id": "duration_block",
                "element": {
                    "type": "plain_text_input",
                    "action_id": "duration_input",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "e.g., 30s, 1m, 1h"
                    }
                },
                "label": {
                    "type": "plain_text",
                    "text": "Test Duration"
                }
            },
            {
                "type": "actions",
                "block_id": "test_control_actions",
                "elements": [
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Start Load Test"
                        },
                        "style": "primary",
                        "action_id": "start_load_test"
                    },
                    {
                        "type": "button",
                        "text": {
                            "type": "plain_text",
                            "text": "Stop Load Test"
                        },
                        "style": "danger",
                        "action_id": "stop_load_test"
                    }
                ]
            }
        ]
    }

def create_stop_test_modal(running_jobs: List[str]) -> Dict:
    """Create the modal for stopping a specific load test."""
    return {
        "type": "modal",
        "callback_id": "stop_job_modal",
        "title": {
            "type": "plain_text",
            "text": "Stop Load Test"
        },
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "Select the job to stop:"
                }
            },
            {
                "type": "input",
                "block_id": "job_selection",
                "element": {
                    "type": "static_select",
                    "action_id": "job_to_stop",
                    "placeholder": {
                        "type": "plain_text",
                        "text": "Select a job"
                    },
                    "options": [
                        {
                            "text": {
                                "type": "plain_text",
                                "text": job
                            },
                            "value": job
                        } for job in running_jobs
                    ]
                },
                "label": {
                    "type": "plain_text",
                    "text": "Running Jobs"
                }
            }
        ],
        "submit": {
            "type": "plain_text",
            "text": "Stop Selected Job"
        }
    }

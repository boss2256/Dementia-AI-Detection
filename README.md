# Dementia CNN Deep-Learning AI-Detection

![Dementia AI Detection](https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41598-019-54548-6/MediaObjects/41598_2019_54548_Fig1_HTML.png)

## Overview

Dementia-AI-Detection is a machine learning-based web application designed to facilitate the early detection and risk prediction of dementia. The project integrates MRI image analysis and dementia risk prediction to provide comprehensive insights into the likelihood of dementia in patients.

## Features

- **User Registration and Login**: Users can register for an account or log in as an admin.
- **MRI Image Upload**: Users can upload MRI scans to get a confidence score of the dementia condition.
- **Dementia Risk Prediction**: Users can input various health and lifestyle parameters to predict the risk of dementia.

## Technologies Used

- **Backend**: Flask
- **Database**: SQLite
- **Frontend**: HTML, CSS, JavaScript
- **Machine Learning**: TensorFlow, Keras
- **Deployment**: Heroku

## Website

Access the application [here](https://dementiadetection-51c4fdc49ae6.herokuapp.com/admin_reports).

## Getting Started

### Prerequisites

- Python 3.7+
- Virtual Environment

### Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/boss2256/Dementia-AI-Detection.git
    ```
2. Navigate to the project directory:
    ```bash
    cd Dementia-AI-Detection
    ```
3. Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```
4. Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

### Running the Application

1. Run the application:
    ```bash
    python app.py
    ```
    or
    ```bash
    flask run
    ```
2. Access the application in your web browser at `http://127.0.0.1:5000`.

## Usage

1. **Register or Login**: Create a new account or log in as an admin.
2. **Upload MRI Image**: Navigate to the MRI Analysis section, upload an MRI image, and receive a confidence score for dementia detection.
3. **Risk Prediction**: Fill out the dementia risk prediction form with relevant health and lifestyle information to get a risk assessment.

## Contributing

Contributions are welcome! Please submit a pull request or open an issue to discuss any changes.

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

```
import os
import asyncio
from datetime import datetime, timezone, timedelta
from openleadr import OpenADRServer, enable_default_logging
from functools import partial
import logging

enable_default_logging()

# Configure logging
logging.basicConfig(filename='vtn_server.log',
                    level=logging.DEBUG,
                    format='%(asctime)s:%(levelname)s:%(message)s')

logger = logging.getLogger(__name__)

PORT = os.getenv("VTN_PORT", 8080)

async def on_create_party_registration(registration_info):
    logger.info("Party registration request received.")
    if registration_info['ven_name'] == 'ven123':
        ven_id = 'ven_id_123'
        registration_id = 'reg_id_123'
        logger.info(f"Registered ven_id: {ven_id}, registration_id: {registration_id}")
        return ven_id, registration_id
    else:
        logger.error("Invalid registration info.")
        return False

async def on_register_report(ven_id, resource_id, measurement, unit, scale,
                             min_sampling_interval, max_sampling_interval):
    logger.info(f"Report registration from ven_id: {ven_id}, resource_id: {resource_id}")
    callback = partial(on_update_report,
                       ven_id=ven_id,
                       resource_id=resource_id,
                       measurement=measurement)
    sampling_interval = min_sampling_interval
    return callback, sampling_interval

async def on_update_report(data, ven_id, resource_id, measurement):
    logger.info(f"Report update received from ven_id: {ven_id}, resource_id: {resource_id}")
    for time, value in data:
        logger.info(f"Time: {time}, Value: {value}")

async def event_response_callback(ven_id, event_id, opt_type):
    logger.info(f"Event response received from ven_id: {ven_id}, event_id: {event_id}, opt_type: {opt_type}")

def ven_lookup(ven_id):
    logger.info(f"VEN lookup for ven_id: {ven_id}")
    return {
        'ven_id': 'ven_id_123',
        'ven_name': 'ven123',
    }

# Create the server object
server = OpenADRServer(vtn_id='myvtn', http_port=PORT)

# Add the handler for client (VEN) registrations
server.add_handler('on_create_party_registration', on_create_party_registration)

# Add the handler for report registrations from the VEN
server.add_handler('on_register_report', on_register_report)

# Add a prepared event for a VEN that will be picked up when it polls for new messages.
server.add_event(ven_id='ven_id_123',
                 signal_name='simple',
                 signal_type='level',
                 intervals=[{
                     'dtstart': datetime.now(timezone.utc) + timedelta(minutes=5),
                     'duration': timedelta(minutes=60),
                     'signal_payload': 100.0
                 }],
                 callback=event_response_callback)

# Run the server on the asyncio event loop
loop = asyncio.get_event_loop()
loop.create_task(server.run())
loop.run_forever()

```

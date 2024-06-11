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
{
    "ven_name": "PNNLVEN",
    "vtn_url": "http://127.0.0.1:8080/OpenADR2/Simple/2.0b",
    "cert_path": "",
    "key_path": "",
    "debug": true,
    "disable_signature": true
}

```

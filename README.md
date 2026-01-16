# Azure Storage API

A FastAPI-based REST API for interacting with Azure Storage services, including Blob Storage, File Share, Queue, and Table Storage.

## Features

- **Blob Storage Operations**: Upload and download files to/from Azure Blob Storage.
- **File Share Operations**: Manage files in Azure File Shares.
- **Queue Operations**: Send messages to Azure Queues.
- **Table Storage Operations**: Perform CRUD operations on Azure Table entities.
- **Swagger Documentation**: Interactive API docs available at `/docs`.
- **CORS Enabled**: Allows cross-origin requests from any origin.
- **CI/CD Ready**: Includes Azure Pipelines configuration for automated builds and deployments.

## Prerequisites

- Python 3.10 or higher
- Azure Subscription with Storage Account
- Azure CLI (for local development and deployment)

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/your-username/azure-storage-api.git
   cd azure-storage-api
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file in the root directory with the following:
   ```
   AZURE_SUBSCRIPTION_ID=your-subscription-id
   STORAGE_ACCESS_KEY=your-storage-access-key
   CONN_STRING=your-connection-string
   RESOURCE_GRP=your-resource-group
   STORAGE_ACCOUNT=your-storage-account-name
   ```

## Usage

### Running Locally

1. **Start the server**:
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API**:
   - API Base URL: `http://localhost:8000`
   - Swagger UI: `http://localhost:8000/docs`
   - ReDoc: `http://localhost:8000/redoc`

### API Endpoints

#### Blob Storage
- **POST** `/upload_download_blob`
  - Upload a file to Blob Storage.
  - Parameters: `file` (UploadFile), `file_name` (str), `destination_file_name` (str)

#### File Share
- **POST** `/file_share`
  - Upload a file to File Share.
  - Parameters: `file` (UploadFile), `file_name` (str), `destination_file_name` (str)

#### Queue
- **POST** `/queue_send_message`
  - Send messages to a Queue.
  - Body: List of `QueueMessageModel` objects

#### Table Storage
- **POST** `/table_entity_operations`
  - Perform operations on Table entities.
  - Body: List of `TableEntityModel` objects

### Request Models

Refer to `Models/requestModel.py` for the Pydantic models used in requests.

## Deployment

### Azure Web App

1. **Create an Azure Web App** (Linux-based) with Python runtime.

2. **Set Environment Variables** in Azure Portal > Web App > Configuration > Application settings.

3. **Configure Startup Command**:
   ```
   gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind=0.0.0.0:$PORT
   ```

4. **Deploy via CI/CD**:
   - The project includes `azure-pipelines.yml` for automated deployment.
   - Push to the `main` branch to trigger deployment.

5. **Access Deployed App**:
   - URL: `https://your-webapp-name.azurewebsites.net`
   - Docs: `https://your-webapp-name.azurewebsites.net/docs`

### Local Deployment Testing

For testing deployment locally:
```bash
gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind=0.0.0.0:8000
```

## Project Structure

```
azure-project-storage/
├── main.py                 # FastAPI app and endpoints
├── storages.py             # Azure Storage service functions
├── settings.py             # Configuration and environment variables
├── Models/
│   └── requestModel.py     # Pydantic models for requests
├── requirements.txt        # Python dependencies
├── azure-pipelines.yml     # CI/CD pipeline configuration
├── .env                    # Environment variables (not committed)
└── README.md               # This file
```

## Contributing

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Commit changes: `git commit -am 'Add your feature'`
4. Push to the branch: `git push origin feature/your-feature`
5. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Troubleshooting

- **Module Not Found**: Ensure all dependencies are installed: `pip install -r requirements.txt`
- **Azure Credentials**: Verify environment variables are set correctly.
- **Deployment Issues**: Check Azure Web App logs for errors.
- **CORS Errors**: The app allows all origins; adjust in `main.py` if needed.

For more help, refer to the [FastAPI documentation](https://fastapi.tiangolo.com/) and [Azure Storage documentation](https://docs.microsoft.com/en-us/azure/storage/).
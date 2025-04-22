Health Monitor
This is a Python-based HTTP endpoint health monitoring tool that periodically checks the availability of a list of configured URLs and logs their status.
This will create a monitor.log file which which will keep the reports status of the endpoints in a structured format. 


Requirements
Python 3.7+
pip installed

Project Structure
.
├── monitor.py            # Main script
├── endpoints.yaml        # Configuration file for endpoints
├── .env                  # Environment variables
├── monitor.log           # Rotating log file (will be auto-generated)
└── README.md             # Readene.md



Install dependencies by running the 

pip3 install -r requirements.txt 



Run the script with the below command.

python main.py endpoints.yaml

You’ll see output like:


Request to https://example.com/api took 0.231 seconds 200
Request to https://api.example.org/post took 0.450 seconds 500

Logs
Logs are written to the file specified in .env (default: monitor.log)

Old logs are rotated daily and kept for 7 days

Stopping the Monitor
Just press Ctrl + C. The script will exit gracefully and log the shutdown.

Tips
Place monitor.py, .env, and config.yaml in the same directory

Use JSON payloads for POST/PUT requests

Use curl or Postman to validate endpoint formats before monitoring

License
MIT License – free to use and modify.

Let me know if you want a pre-filled repo template or a Dockerfile to containerize it!
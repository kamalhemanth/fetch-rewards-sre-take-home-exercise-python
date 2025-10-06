################################################################
Overview:

This project implements a Python-based monitoring tool that evaluates the availability of multiple HTTP endpoints as defined in a YAML configuration file.

It runs periodic health checks every 15 seconds, tracks cumulative domain availability, and logs results to the console.

This solution meets all the functional and behavioral requirements outlined in the Fetch Rewards SRE Take-Home Exercise specification.

################################################################

Requirements:

The program must:

1.Accept a YAML configuration file as a command-line argument

2.Perform health checks on each endpoint defined in the YAML

3.Consider an endpoint available ("UP") only if:

4.It returns a status code between 200 and 299

5.It responds in ≤ 500 ms

6.Report cumulative domain availability (ignoring port numbers)

7.Run checks and print a summary every 15 seconds

8.Drop any availability value after the decimal point

################################################################

Installation and Setup:

1.Clone the given git repository to your local repository
(example command: git clone https://github.com/<your-username>/sre-take-home-exercise-python.git)

2.Install dependencies : Make sure Python 3 is installed then  
 run: pip install requests pyyaml

3.  Verify files : Your folder structure should look like

    sre-take-home-exercise-python/
    │
    ├── main.py
    ├── README.md
    └── sample.yml

4.  Run the program with below command

         python main.py sample.yaml

    once above command is exectuted you will be able to see below output:

    Starting endpoint monitoring (press Ctrl+C to stop)...

    === Availability Report ===
    dev-sre-take-home-exercise-rubric.us-east-1.recruiting-public.fetchrewards.com: 75% availability
    ===========================

5.  if you want to stop monitoring the availability report then press Ctrl+C to stop once Ctrl+C is pressed you will get below message on the terminal

Monitoring stopped by user.

################################################################

Issues Identified and Fixes Made:

1.-----------------------------------------------------------
Issue Identified: Missing default HTTP method handling

Description: The original code didn’t handle endpoints without method specified.

Fix Implemented: Added method = endpoint.get('method', 'GET') to ensure a default method.

2--------------------------------------------------------------
Issue Identified: Timeout not enforced

Description: Original implementation could hang if endpoints were unresponsive.

Fix Implemented: Added timeout=0.5 in requests.request() to limit latency.

3.-------------------------------------------------------------
Issue Identified: Port handling in domain extraction

Description: Domain parsing used string splitting; ports could cause mismatches.

Fix Implemented: Replaced manual split logic with urlparse() to extract hostname cleanly.

4.-------------------------------------------------------------
Issue Identified: Incorrect availability rounding

Description: Original version displayed decimals in percentage.

Fix Implemented: Updated to use int((up / total) \* 100) and added a comment explaining the requirement

5.--------------------------------------------------------------
Issue Identified: Loop timing drift

Description: Long requests could shift check cycles beyond 15 seconds.

Fix Implemented: Calculated elapsed time per cycle and adjusted sleep time to maintain consistent intervals.

6.--------------------------------------------------------------
Issue Identified: Missing error handling for YAML file

Description: No graceful handling for missing or invalid YAML path.

Fix Implemented: Added file existence check and user-friendly error message.

---

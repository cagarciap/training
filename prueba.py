import argparse
from re import sub
import subprocess
import time
import json

def variables():
    parser = argparse.ArgumentParser()

    """Global variables"""
    parser.add_argument('-script', '--script', type=str,required=True, help='Script to run')
    parser.add_argument('-endpoint', '--endpoint', type=str, required=True, help='Endpoint to test')
    parser.add_argument('-port', '--port', type=str, required=True, help='Port')
    parser.add_argument('-url', '--url', type=str, help='Url to test')

    """Load and Endurace test variables"""
    parser.add_argument('-c', '--target_concurrency', help='Target concurrecy')
    parser.add_argument('-rt', '--ramp_up_time', help='Ramp up time')
    parser.add_argument('-rs', '--ramp_up_steps', help='Ramp up steps')
    parser.add_argument('-t', '--hold_target_rate_time', help='Hold target rate time')

    """Stress test variables"""
    parser.add_argument('-ts', '--threads_start', help='This group will start')
    parser.add_argument('-fw', '--first_wait', help='First, wait for')
    parser.add_argument('-ns', '--next_start', help='Then start with threads')
    parser.add_argument('-at', '--add_threads', help='Next, add threads')
    parser.add_argument('-tw', '--time_to_wait', help='Threads every, second')
    parser.add_argument('-r', '--ramp_up', help='using ramp-up')
    parser.add_argument('-hl', '--hold_load', help='Then hold load for seconds')
    parser.add_argument('-st', '--threads_to_stop', help='Finally, stop threads')
    parser.add_argument('-tp', '--time_to_stop', help='Stop threads every seconds')

    """Spike test variables"""
    parser.add_argument('-mt', '--maximum_threads', help='Maximunm threads spike')

    args = parser.parse_args()
    script(args)

def testInfoMethod(time_name, endpoint, testInfo):
    testInfo["scn_project_name"] = "Cesar Training"
    testInfo["scn_application_name"] = "Baldor Inc"
    testInfo["scn_build_number"] = time_name
    testInfo["scn_version"] = "V1.0.0"
    testInfo["scn_test_name"] = "8-Agosto-I"

    if (endpoint == "0"):
        testInfo["scn_transaction_name"] = "All Endpoints"
    elif (endpoint == "1"):
        testInfo["scn_transaction_name"] = "Add"
    elif (endpoint == "2"):
        testInfo["scn_transaction_name"] = "Subtract"
    elif (endpoint == "3"):
        testInfo["scn_transaction_name"] = "Multiply"
    elif (endpoint == "4"):
        testInfo["scn_transaction_name"] = "Divide"

    with open(f'results/results{time_name}/testInfo.json', 'w') as file:
        json.dump(testInfo, file, indent=2)

def script(args):
    time_gmtime=time.gmtime()
    time_name = f"{time_gmtime.tm_year}{time_gmtime.tm_mon}{time_gmtime.tm_mday}{time_gmtime.tm_hour}{time_gmtime.tm_min}{time_gmtime.tm_sec}"
    testInfo = {}
    if (args.script == "load"):
        print(f"Load test folder -> results/results{time_name}")
        testInfo["scn_tag"] =  "load-test"
        testInfo["scn_threads"] = args.target_concurrency
        testInfo["scn_job_name"] = "Load Test"
        name_script="load_test.jmx"
        command=f"sh /test/jmeter/bin/jmeter.sh -n -t /usr/perfexp-tutorial/{name_script} -l results/results{time_name}/results{time_name}.jtl -Jurl={args.url} -Jport={args.port} -Jendpoint={args.endpoint} -Jconcurrency={args.target_concurrency} -Jramp_up={args.ramp_up_time} -Jramp_up_steps={args.ramp_up_steps} -Jhold_target_rate_time={args.hold_target_rate_time}"
        subprocess.run(command,shell=True)
        testInfoMethod(time_name,args.endpoint,testInfo)
        command=f"psl-perfexp parse -rd results/results{time_name} jtl 'results/results{time_name}/results{time_name}.jtl'"
        subprocess.run(command,shell=True)
        command=f"psl-perfexp send jmeter complete -inf results/results{time_name}/testInfo.json results/results{time_name}"
        subprocess.run(command,shell=True)
       
    elif (args.script == "stress"):
        print(f"Stress test folder -> results/results{time_name}")
        testInfo["scn_tag"] =  "stress-test"
        testInfo["scn_threads"] = args.threads_start
        testInfo["scn_job_name"] = "Stress Test"
        name_script="stress_test.jmx"
        command=f"sh /test/jmeter/bin/jmeter.sh -n -t /usr/perfexp-tutorial/{name_script} -l results/results{time_name}/results{time_name}.jtl -Jurl={args.url} -Jport={args.port} -Jendpoint={args.endpoint} -Jthreads_start={args.threads_start} -Jfirst_wait={args.first_wait} -Jnext_start={args.next_start} -Jadd_threads={args.add_threads} -Jtime_to_wait={args.time_to_wait} -Jramp_up={args.ramp_up} -Jhold_load={args.hold_load} -Jthreads_to_stop={args.threads_to_stop} -Jtime_to_stop={args.time_to_stop}"
        subprocess.run(command,shell=True)
        testInfoMethod(time_name,args.endpoint,testInfo)
        command=f"psl-perfexp parse -rd results/results{time_name} jtl 'results/results{time_name}/results{time_name}.jtl'"
        subprocess.run(command,shell=True)
        command=f"psl-perfexp send jmeter complete -inf results/results{time_name}/testInfo.json results/results{time_name}"
        subprocess.run(command,shell=True)

    elif (args.script == "spike"):
        print(f"Spike test folder -> results/results{time_name}")
        testInfo["scn_tag"] =  "spike-test"
        testInfo["scn_threads"] = args.maximum_threads
        testInfo["scn_job_name"] = "Spike Test"
        name_script="spike_test.jmx"
        command=f"sh /test/jmeter/bin/jmeter.sh -n -t /usr/perfexp-tutorial/{name_script} -l results/results{time_name}/results{time_name}.jtl -Jurl={args.url} -Jport={args.port} -Jendpoint={args.endpoint}"
        subprocess.run(command,shell=True)
        testInfoMethod(time_name,args.endpoint,testInfo)
        command=f"psl-perfexp parse -rd results/results{time_name} jtl 'results/results{time_name}/results{time_name}.jtl'"
        subprocess.run(command,shell=True)
        command=f"psl-perfexp send jmeter complete -inf results/results{time_name}/testInfo.json results/results{time_name}"
        subprocess.run(command,shell=True)
    
    elif (args.script == "endurance"):
        print(f"Endurance test folder -> results/results{time_name}")
        testInfo["scn_tag"] =  "endurance-test"
        testInfo["scn_threads"] = args.target_concurrency
        testInfo["scn_job_name"] = "Endurance Test"
        name_script="endurance_test.jmx"
        command=f"sh /test/jmeter/bin/jmeter.sh -n -t /usr/perfexp-tutorial/{name_script} -l results/results{time_name}/results{time_name}.jtl -Jurl={args.url} -Jport={args.port} -Jendpoint={args.endpoint} -Jconcurrency={args.target_concurrency} -Jramp_up={args.ramp_up_time} -Jramp_up_steps={args.ramp_up_steps} -Jhold_target_rate_time={args.hold_target_rate_time}"
        subprocess.run(command,shell=True)
        testInfoMethod(time_name,args.endpoint,testInfo)
        command=f"psl-perfexp parse -rd results/results{time_name} jtl 'results/results{time_name}/results{time_name}.jtl'"
        subprocess.run(command,shell=True)
        command=f"psl-perfexp send jmeter complete -inf results/results{time_name}/testInfo.json results/results{time_name}"
        subprocess.run(command,shell=True)

if __name__ == "__main__":
  variables()
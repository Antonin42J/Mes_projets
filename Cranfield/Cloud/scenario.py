import paramiko
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import os

from test_elasticity import write_csv
from graph import Graph

# Define IP addresses for clients and servers
IP_client = ["54.226.112.152", "54.196.163.238", "54.160.157.148", "54.227.25.179"]
IP_server = ["3.86.52.114", "54.81.53.125"]
host_name_server = ["ec2-3-86-52-114.compute-1.amazonaws.com", "ec2-54-81-53-125.compute-1.amazonaws.com"]
host_name_collect = "ec2-44-203-60-36.compute-1.amazonaws.com"

# Define the path to the PEM file
PEM_file = r"AWS\MyEC2Intense\labsuser.pem"

def scenario():
    # Define the filename for scenario data
    filename = "scenario.csv"
    
    # Remove the file if it already exists
    if os.path.exists(filename):
        os.remove(filename)

    # Define the header for the CSV file
    header = ["time", "number of clients", "number of workers", "number of requests"]
    
    # Write the header to the CSV file
    write_csv(header, filename)
    
    # Create an SSH key from the PEM file
    private_key = paramiko.RSAKey.from_private_key_file(filename=PEM_file)
    
    # Collect data

    # Initialize an SSH client for connecting to the data collection server
    c_c = paramiko.SSHClient()
    c_c.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c_c.connect(hostname=host_name_collect, username='ec2-user', pkey=private_key)
    c_c.exec_command("python3 collect_data.py")

    # Wait for the database to be filled (30 seconds)
    print("Waiting for the database to be fill one time (30s)")
    time.sleep(30)

    # Set up servers

    # Initialize SSH clients for connecting to servers
    c_s1 = paramiko.SSHClient()
    c_s1.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c_s1.connect(hostname=host_name_server[0], username='ec2-user', pkey=private_key)
    c_s1.exec_command("python3 server.py")

    c_s2 = paramiko.SSHClient()
    c_s2.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    c_s2.connect(hostname=host_name_server[1], username='ec2-user', pkey=private_key)
    c_s2.exec_command("python3 server.py")

    # Initialize variables for managing clients
    Client_connecting = 0
    drivers = []
    start_time = time.time()
    request = 0

    while True:
        # Establish connections for clients

        if Client_connecting == 0:
            driver_1 = webdriver.Chrome()
            drivers.append(driver_1)
            driver_1.get("http://" + IP_client[1])
            Client_connecting += 1
            client_number = str(IP_client.index(IP_client[0]))
            client(driver_1, IP_server[0], client_number)

        elif Client_connecting == 1:
            driver_2 = webdriver.Chrome()
            drivers.append(driver_2)
            driver_2.get("http://" + IP_client[0])
            Client_connecting += 1
            client_number = str(IP_client.index(IP_client[1]))
            client(driver_2, IP_server[0], client_number)

        elif Client_connecting == 2:
            driver_3 = webdriver.Chrome()
            drivers.append(driver_3)
            driver_3.get("http://" + IP_client[2])
            Client_connecting += 1
            client_number = str(IP_client.index(IP_client[2]))
            client(driver_3, IP_server[1], client_number)

        elif Client_connecting == 3:
            driver_4 = webdriver.Chrome()
            drivers.append(driver_4)
            driver_4.get("http://" + IP_client[3])
            Client_connecting += 1
            client_number = str(IP_client.index(IP_client[3]))
            client(driver_4, IP_server[1], client_number)

        print("Number of clients: " + str(len(drivers)))

        # Execute client actions concurrently
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(drivers)) as executor:
            futures = [executor.submit(client_action, driver) for driver in drivers]
            results = [future.result() for future in concurrent.futures.as_completed(futures)]

            for result in results:
                request += result

        end_time = time.time()
        total_time = end_time - start_time

        # Determine the number of workers based on the number of connected clients
        number_workers = 2 if Client_connecting > 2 else 1

        # Log scenario results to CSV file
        row = [total_time, Client_connecting, number_workers, request]
        write_csv(row, filename)

        # Terminate client connections when all clients are connected
        if Client_connecting == 4:
            for driver in drivers:
                driver.close()
                driver.quit()
            break

    # Generate and save scenario graphs
    Graph.graph_scenario(filename)

    # Terminate processes on servers and data collection server
    c_c.exec_command("^C")
    c_s1.exec_command("^C")
    c_s2.exec_command("^C")

    # Close SSH connections
    c_c.close()
    c_s1.close()
    c_s2.close()
                
def client_action(driver):
    # Execute client actions (e.g., download sensor list) with retries
    for i in range(5):
        if i > 0:
            try:
                WebDriverWait(driver, 2).until(
                    lambda driver: driver.find_element(By.XPATH, "//p[@id='textcontrol']").text == "Sensors list has been downloaded"
                )
                i += 1
            except Exception:
                print("Error not normal")
                break

        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Download sensors list')]"))
        ).click()

        WebDriverWait(driver, 2).until(
            EC.presence_of_element_located((By.XPATH, "//p[@id='textcontrol']"))
        )

        # Check if the database is not out, then wait for the next action
        if driver.find_element(By.XPATH, "//p[@id='textcontrol']").text != "Database out":
            try:
                WebDriverWait(driver, 2).until(
                    lambda driver: driver.find_element(By.XPATH, "//p[@id='textcontrol']").text == "Download sensors list"
                )
            except Exception:
                break

        time.sleep(3)

    return i


def client(driver, ip_server, client_number):
    # Accept alerts and provide necessary information to clients
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert_ip = driver.switch_to.alert
    alert_ip.send_keys(ip_server)
    alert_ip.accept()

    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert_client = driver.switch_to.alert
    alert_client.send_keys(client_number)
    alert_client.accept()


if __name__ == "__main__":
    scenario()


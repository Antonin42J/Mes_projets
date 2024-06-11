# Import necessary libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import concurrent.futures
import time
import csv
import os

# Import the Graph class from the graph module
from graph import Graph

# Define IP addresses for clients and servers
IP_client = ["54.226.112.152", "54.196.163.238", "54.160.157.148", "54.227.25.179"]
IP_server = ["3.86.52.114", "54.81.53.125"]

# Function to execute workload in threads
def workload_thread(IP_c, ip_server, requests, filename):
    for number_requests in requests:
        start_time = time.time()
        workload = 0
        with concurrent.futures.ThreadPoolExecutor(max_workers=len(IP_c)) as executor:
            # Submit work_client tasks in parallel for each client
            futures = [executor.submit(work_client, ip_client, ip_server, number_requests, str(IP_c.index(ip_client))) for ip_client in IP_c]
            # Gather results from completed tasks
            results = [future.result() for future in concurrent.futures.as_completed(futures)]
            for result in results:
                workload += result
        end_time = time.time()
        total_time = end_time - start_time
        print(f"The workload is {workload} requests on a time of {total_time}s")
        row_csv = [str(total_time), str(number_requests), str(workload), str(len(IP_c))]
        write_csv(row_csv, filename)
    

def work_client(ip_client, ip_server, number_request, client_number):
    # Initialize a new Chrome WebDriver instance
    driver = webdriver.Chrome()
    
    # Open the specified URL for the client
    driver.get("http://" + ip_client)
    
    # Handle an alert asking for the IP server and accept it
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert_ip = driver.switch_to.alert
    alert_ip.send_keys(ip_server)
    alert_ip.accept()
    
    # Handle another alert asking for the client number and accept it
    WebDriverWait(driver, 10).until(EC.alert_is_present())
    alert_client = driver.switch_to.alert
    alert_client.send_keys(client_number)
    alert_client.accept()
    
    i = 0
    
    # Loop through the specified number of requests
    for i in range(number_request):
        # Check if this is not the first iteration
        if i > 0:
            try:
                # Wait until the text control indicates "Sensors list has been downloaded"
                WebDriverWait(driver, 2).until(lambda driver: driver.find_element(By.XPATH, "//p[@id='textcontrol']").text == "Sensors list has been downloaded")
                print(i)
                i += 1
            except Exception:
                print("Error not normal")
                break
                
        # Click the button to download sensors list
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//button[contains(text(),'Download sensors list')]"))).click()
        
        # Wait until the text control is present
        WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, "//p[@id='textcontrol']")))
        
        # Check if the text control doesn't indicate "Database out"
        if driver.find_element(By.XPATH, "//p[@id='textcontrol']").text != "Database out":
            try:
                # Wait until the text control indicates "Download sensors list"
                WebDriverWait(driver, 2).until(lambda driver: driver.find_element(By.XPATH, "//p[@id='textcontrol']").text == "Download sensors list")
            except Exception:
                break

    # Close and quit the WebDriver
    driver.close()
    driver.quit()
    
    # Return the number of iterations
    return i



def write_csv(row_csv, filename):
   
    with open(filename, "a", newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(row_csv)
    csv_file.close()


def main():
    
    requests = [10, 30, 50, 100]
    
    filename = "result_workload.csv"
    
    if os.path.exists(filename):
        os.remove(filename)
    
    header = ["execution time", "initial number of requests by clients", "workload", "number of clients"]
    
    # Write the header to the CSV file
    write_csv(header, filename)
    
    # Perform workload testing for different numbers of clients
    for num_clients in range(1, 5):
        IP_c = IP_client[:num_clients]
        ip_server = IP_server[0]
        workload_thread(IP_c, ip_server, requests, filename)
    
    # Generate and display a graph based on the results
    Graph.graph(filename)


if __name__ == "__main__":
    main()

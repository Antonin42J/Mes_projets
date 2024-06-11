import pandas as pd
import matplotlib.pyplot as plt

class Graph :
    
    def graph(file) :
        # Generate and save a graph representing the workload over time for different numbers of clients
        df = pd.read_csv(file)
        requests = []  # List to store unique requests
        
        # Lists to store data for different numbers of clients
        data_1 = [[], []]
        data_2 = [[], []]
        data_3 = [[], []]
        data_4 = [[], []]
        
        # Extract unique requests
        for element in df['initial number of requests by clients']:
            if element not in requests:
                requests.append(element)

        # Separate data based on the number of clients
        for index, row in df.iterrows():
            if row['number of clients'] == 1 :
                data_1[0].append(row['execution time'])
                data_1[1].append(row['workload'])
            if row['number of clients'] == 2 :
                data_2[0].append(row['execution time'])
                data_2[1].append(row['workload'])
            if row['number of clients'] == 3 :
                data_3[0].append(row['execution time'])
                data_3[1].append(row['workload'])
            if row['number of clients'] == 4 :
                data_4[0].append(row['execution time'])
                data_4[1].append(row['workload'])

        # Plotting the data
        plt.plot(data_1[0], data_1[1], label='1 client', linestyle='-', marker='o', color='blue')
        plt.plot(data_2[0], data_2[1], label='2 clients', linestyle='-', marker='o', color='green')
        plt.plot(data_3[0], data_3[1], label='3 clients', linestyle='-', marker='o', color='orange')
        plt.plot(data_4[0], data_4[1], label='4 clients', linestyle='-', marker='o', color='purple')
        
        # Plot horizontal lines for unique requests
        for request in requests :
            plt.axhline(y=request, color='red', linestyle='--')

        plt.title('Number of requests over time in function of the number of clients')
        plt.xlabel('Time (s)')
        plt.ylabel('Number of requests')
        plt.legend()
        
        plt.savefig("Workload_graph.png")

    def graph_scenario(file) :
        # Generate and save two graphs representing the number of clients and workers over time, and the number of requests over time
        df = pd.read_csv(file)
        
        # Lists to store data for clients, workers, and requests
        data_clients = [[], []]
        data_workers = [[], []]
        data_request = [[], []]
        
        # Extract data for each scenario
        for index, row in df.iterrows():
            data_clients[0].append(row['time'])
            data_clients[1].append(row['number of clients'])
            data_workers[0].append(row['time'])
            data_workers[1].append(row['number of workers'])
            data_request[0].append(row['time'])
            data_request[1].append(row['number of requests'])

        # Plotting the number of clients and workers over time
        plt.plot(data_clients[0], data_clients[1], label='clients', linestyle='-', marker='o', color='blue')
        plt.plot(data_workers[0], data_workers[1], label='workers', linestyle='-', marker='o', color='green')
        
        plt.title('Number of workers over time in function of the number of clients')
        plt.xlabel('Time (s)')
        plt.ylabel('Number of elements')
        plt.legend()
        
        plt.savefig("Workers_graph.png")
        
        plt.close()
        
        # Plotting the number of requests over time
        plt.plot(data_request[0], data_request[1], label='requests', linestyle='-', marker='o', color='blue')
        
        plt.title('Number of requests over time')
        plt.xlabel('Time (s)')
        plt.ylabel('Number of requests')
        plt.legend()
        
        plt.savefig("Requests_graph.png")

// Function to send filter data to the server for air quality data retrieval
function senddata() {
    // Retrieve filter values from HTML elements
    var ids = document.getElementById("ids").value;
    var lat = document.getElementById("lat").value;
    var long = document.getElementById("long").value;
    var alt = document.getElementById("alt").value;
    var country_code = document.getElementById("country_code").value;
    var country_name = document.getElementById("country_name").value;
    var starttime = document.getElementById("starttime").value;
    var endtime = document.getElementById("endtime").value;

    // Create an object with filter data
    var list_data = {
        ids: ids,
        lat: lat,
        long: long,
        alt: alt,
        country_code: country_code,
        country_name: country_name,
        starttime: starttime,
        endtime: endtime
    };

    // Message for display
    var message = "Filter applied";

    // Establish a WebSocket connection to the server
    var server = new WebSocket(serverUrl);

    // Send filter data to the server using the sendserver function
    sendserver(server, list_data, message);

    
    // Handle server response on successful connection
    server.onmessage = function (event) {
        const reicv_element = event.data;
        // Define CSV column titles
        const title = "id_sensors, timestamp, pm10, pm25, airquality, qualification, latitude, longitude, altitude, country_code, country_name";
        var controltext = document.getElementById("textcontrol");
            if (reicv_element == "Database out") {
                // Display message if there is a database issue
                message = reicv_element;
            } else {
                // Create a CSV file for sensors list and display success message
                createCSV(reicv_element, "airqualitydata.csv", title);
                message = "Data has been downloaded";
            }
            controltext.innerHTML = message;
    };
}

// Function to download the list of sensors
function Downloadlist() {
    // Message for server request
    var message = "Download sensors list"
    var send_element = Client + "//" + message;

    // Establish a WebSocket connection to the server
    var server = new WebSocket(serverUrl);

    // Send server request for sensor list using the sendserver function
    sendserver(server, send_element, message);

    // Handle server response
    server.onmessage = function (event) {
        const reicv_element = event.data;
        // Define CSV column titles for sensors list
        const title = "id, id_sensors, latitude, longitude, altitude, country_code, country_name";
        var controltext = document.getElementById("textcontrol");
        if (reicv_element == "Database out") {
            // Display message if there is a database issue
            message = reicv_element;
        } else {
            // Create a CSV file for sensors list and display success message
            createCSV(reicv_element, "sensorslist.csv", title);
            message = "Sensors list has been downloaded";
        }
        controltext.innerHTML = message;
    };
}

// Function to asynchronously create a CSV file from JSON data
async function createCSV(data, name_file, title) {
    // Convert JSON data to CSV string (replace this with your conversion logic)
    var jsondata = JSON.parse(data);
    var csvContent = title + "\n";

    // Iterate over JSON data and create CSV rows
    jsondata.forEach(function (row) {
        csvContent += Object.values(row).join(',') + '\n';
    });

    // Create a Blob object from the CSV string
    const blob = new Blob([csvContent], { type: 'text/csv' });

    // Create a download link
    var link = document.createElement('a');
    link.href = URL.createObjectURL(blob);
    link.download = name_file;

    // Append the link to the document
    document.body.appendChild(link);

    // Uncomment the following section to trigger the download
    // link.click();

    // Remove the link from the document
    document.body.removeChild(link);
}

// Function to download air quality data
function Downloaddata() {
    // Message for server request
    var message = "Download data"
    var send_element = Client + "//" + message;

    // Establish a WebSocket connection to the server
    var server = new WebSocket(serverUrl);

    // Send server request for air quality data using the sendserver function
    sendserver(server, send_element, message);

    // Handle server response
    server.onmessage = function (event) {
        const reicv_element = event.data;
        // Define CSV column titles
        const title = "id_sensors, timestamp, pm10, pm25, airquality, qualification, latitude, longitude, altitude, country_code, country_name";
        var controltext = document.getElementById("textcontrol");
            if (reicv_element == "Database out") {
                // Display message if there is a database issue
                message = reicv_element;
            } else {
                // Create a CSV file for sensors list and display success message
                createCSV(reicv_element, "airqualitydata.csv", title);
                message = "Data has been downloaded";
            }
            controltext.innerHTML = message;
    };
}

// Function to send a specified element to the server
function sendserver(server, send_element, message_html) {
    // Execute when the WebSocket connection is opened
    server.onopen = function (event) {
        // Send the specified element as a JSON string to the server
        server.send(JSON.stringify(send_element));
        // Display a message in the control text element
        var controltext = document.getElementById("textcontrol");
        controltext.innerHTML = message_html;
    };
}

// Prompt user for server IP and client number
const serverIp = prompt("Give the server IP:");
const serverPort = 8765;
const serverUrl = `ws://${serverIp}:${serverPort}`;

// Prompt user for the client number
const Client = "Client " + prompt("Give the client number (0-9) :")

// Retrieve HTML elements for buttons
var butonc = document.getElementById("c");
var butonsl = document.getElementById("sl");
var butond = document.getElementById("d");

// Add event listeners to buttons, linking them to their respective functions
butonc.addEventListener("click", senddata);
butonsl.addEventListener("click", Downloadlist);
butond.addEventListener("click", Downloaddata);

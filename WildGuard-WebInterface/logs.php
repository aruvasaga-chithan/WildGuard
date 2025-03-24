<?php
include 'db_connection.php';  // Include the connection file

// Fetch logs from the database
$sql = "SELECT * FROM detections ORDER BY timestamp DESC";
$result = $conn->query($sql);

$logs = array();
if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $logs[] = $row;
    }
}
$conn->close();

// Output the logs as JSON to be fetched by your frontend
echo json_encode($logs);
?>

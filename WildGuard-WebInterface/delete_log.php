<?php
// delete_log.php

header('Content-Type: application/json');

$input = json_decode(file_get_contents('php://input'), true);
$logId = $input['id'] ?? null;

if ($logId) {
    $servername = "localhost";
    $username = "root";
    $password = "";
    $dbname = "wildguard_db";

    // Create connection
    $conn = new mysqli($servername, $username, $password, $dbname);

    // Check connection
    if ($conn->connect_error) {
        echo json_encode(['success' => false, 'message' => 'Connection failed']);
        exit;
    }

    // Prepare and bind
    $stmt = $conn->prepare("DELETE FROM detections WHERE id = ?");
    $stmt->bind_param("i", $logId);

    if ($stmt->execute()) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Error deleting log']);
    }

    $stmt->close();
    $conn->close();
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid log ID']);
}
?>

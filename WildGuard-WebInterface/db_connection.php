<?php
// Database connection details
$servername = "localhost";
$username = "root";  // XAMPP default username
$password = "";      // Leave empty if you're using the default XAMPP MySQL setup
$dbname = "wildguard_db";  // The database you created in Step 3

// Create connection
$conn = new mysqli($servername, $username, $password, $dbname);

// Check connection
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>

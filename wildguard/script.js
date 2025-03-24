// script.js

document.addEventListener("DOMContentLoaded", function() {
    fetchLogs();

    // Fetch logs from the PHP backend
    function fetchLogs() {
        fetch("logs.php")
        .then(response => response.json())
        .then(data => {
            const logTableBody = document.querySelector("#log-table tbody");
            logTableBody.innerHTML = "";  // Clear current table rows

            data.forEach(log => {
                const row = document.createElement("tr");

                const timestampCell = document.createElement("td");
                timestampCell.textContent = log.timestamp;

                const infoCell = document.createElement("td");
                infoCell.textContent = log.info;

                const actionCell = document.createElement("td");
                const deleteButton = document.createElement("button");
                deleteButton.textContent = "Delete";
                deleteButton.addEventListener("click", () => {
                    deleteLog(log.id);  // Call delete function with log ID
                });

                actionCell.appendChild(deleteButton);
                row.appendChild(timestampCell);
                row.appendChild(infoCell);
                row.appendChild(actionCell);

                logTableBody.appendChild(row);
            });
        })
        .catch(error => console.error('Error fetching logs:', error));
    }

    // Delete a log entry
    function deleteLog(logId) {
        if (confirm("Are you sure you want to delete this log?")) {
            fetch("delete_log.php", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ id: logId })
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    alert("Log deleted successfully.");
                    fetchLogs();  // Refresh the logs
                } else {
                    alert("Error deleting log.");
                }
            })
            .catch(error => console.error('Error deleting log:', error));
        }
    }

    // Auto-refresh logs every 30 seconds
    setInterval(fetchLogs, 30000);
});

document.addEventListener("DOMContentLoaded", function() {
    const form = document.querySelector("form");

    form.addEventListener("submit", function(event) {
        const reporterName = document.getElementById("reporter_name").value;
        const jobNumber = document.getElementById("job_number").value;

        if (reporterName.trim() === "" || jobNumber.trim() === "") {
            alert("Please fill in all required fields.");
            event.preventDefault();
        }
    });
});

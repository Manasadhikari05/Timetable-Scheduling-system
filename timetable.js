async function checkTeacherAvailability() {
    // Define an asynchronous function to check teacher availability

    const teacher = document.getElementById("teacher-name").value;
    // Get the value of the input field with id "teacher-name" (teacher's name)

    const day = document.getElementById("day").value;
    // Get the value of the input field with id "day" (day of the week)

    const startTime = document.getElementById("start-time").value;
    // Get the value of the input field with id "start-time" (start time of the class)

    const endTime = document.getElementById("end-time").value;
    // Get the value of the input field with id "end-time" (end time of the class)

    const response = await fetch('/check_teacher_availability', {
        // Send a POST request to the server endpoint '/check_teacher_availability'
        method: 'POST',  // Specify the HTTP method as POST
        headers: {'Content-Type': 'application/json'},  // Set the header to indicate the body is JSON
        body: JSON.stringify({teacher, day, start_time: startTime, end_time: endTime})
        // Convert the data (teacher, day, startTime, endTime) into a JSON string and send it as the body of the request
    });

    const result = await response.json();
    // Wait for the response and parse the JSON result

    document.getElementById("teacher-availability").innerText = 
        result.available ? "Teacher is available" : "Teacher is not available";
    // Based on the response, set the inner text of the element with id "teacher-availability" 
    // to indicate whether the teacher is available or not
}

async function checkClassAvailability() {
    // Define an asynchronous function to check classroom availability

    const className = document.getElementById("class-name").value;
    // Get the value of the input field with id "class-name" (name of the classroom)

    const day = document.getElementById("class-day").value;
    // Get the value of the input field with id "class-day" (day of the week)

    const startTime = document.getElementById("class-start-time").value;
    // Get the value of the input field with id "class-start-time" (start time of the class)

    const endTime = document.getElementById("class-end-time").value;
    // Get the value of the input field with id "class-end-time" (end time of the class)

    const response = await fetch('/check_class_availability', {
        // Send a POST request to the server endpoint '/check_class_availability'
        method: 'POST',  // Specify the HTTP method as POST
        headers: {'Content-Type': 'application/json'},  // Set the header to indicate the body is JSON
        body: JSON.stringify({class_name: className, day, start_time: startTime, end_time: endTime})
        // Convert the data (className, day, startTime, endTime) into a JSON string and send it as the body of the request
    });

    const result = await response.json();
    // Wait for the response and parse the JSON result

    document.getElementById("class-availability").innerText = 
        result.available ? "Classroom is available" : "Classroom is not available";
    // Based on the response, set the inner text of the element with id "class-availability"
    // to indicate whether the classroom is available or not
}

async function scheduleClass() {
    // Define an asynchronous function to schedule a class

    const className = document.getElementById("schedule-class-name").value;
    // Get the value of the input field with id "schedule-class-name" (name of the class)

    const teacher = document.getElementById("schedule-teacher-name").value;
    // Get the value of the input field with id "schedule-teacher-name" (teacher's name)

    const day = document.getElementById("schedule-day").value;
    // Get the value of the input field with id "schedule-day" (day of the week)

    const startTime = document.getElementById("schedule-start-time").value;
    // Get the value of the input field with id "schedule-start-time" (start time of the class)

    const endTime = document.getElementById("schedule-end-time").value;
    // Get the value of the input field with id "schedule-end-time" (end time of the class)

    const response = await fetch('/schedule_class', {
        // Send a POST request to the server endpoint '/schedule_class'
        method: 'POST',  // Specify the HTTP method as POST
        headers: {'Content-Type': 'application/json'},  // Set the header to indicate the body is JSON
        body: JSON.stringify({class_name: className, teacher, day, start_time: startTime, end_time: endTime})
        // Convert the data (className, teacher, day, startTime, endTime) into a JSON string and send it as the body of the request
    });

    const result = await response.json();
    // Wait for the response and parse the JSON result

    document.getElementById("schedule-result").innerText = result.result;
    // Set the inner text of the element with id "schedule-result" to display the result (success or error message)
}

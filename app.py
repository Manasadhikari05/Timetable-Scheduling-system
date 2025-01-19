from flask import Flask, request, render_template
# Import necessary modules from Flask to handle web requests, render HTML templates, and retrieve form data

import pandas as pd
# Import pandas to read and manipulate CSV files, which store teacher and venue data

import random
# Import the random module to randomly assign teachers, subjects, and venues to time slots

from collections import defaultdict
# Import defaultdict to handle the grouping of timetable entries by days more easily

app = Flask(__name__)
# Initialize the Flask application, which is the core of the web app

class ScheduleSystem:
    # Define a class to handle the timetable generation and availability checks

    def __init__(self, teacher_csv='dataset.csv', venue_csv='VENUECSV.csv'):
        # Constructor to initialize the ScheduleSystem with teacher and venue CSV files

        self.teachers = pd.read_csv(teacher_csv)
        # Read the CSV file containing teacher data into a pandas DataFrame

        self.teachers['SECTION'] = self.teachers['SECTION'].apply(lambda x: x.split(','))
        # Split the 'SECTION' field of each teacher into a list (assuming multiple sections are separated by commas)

        self.venues = pd.read_csv(venue_csv)
        # Read the CSV file containing venue data into a pandas DataFrame

        self.schedule = pd.DataFrame(columns=["Section", "Subject", "Teacher", "Venue", "Day", "Time"])
        # Initialize an empty pandas DataFrame to store the generated timetable with columns for section, subject, teacher, venue, day, and time

    def generate_timetable(self, section):
        # Method to generate a timetable for the specified section

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
        # List of weekdays

        time_slots = [
            "8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00",
            "12:00-1:00", "2:00-3:00", "3:00-4:00", "4:00-5:00", "5:00-6:00"
        ]
        # List of available time slots for the timetable

        available_teachers = self.teachers[self.teachers['SECTION'].apply(lambda x: section in x)]
        # Filter teachers who are assigned to the specified section

        if available_teachers.empty:
            return {"error": f"No teachers available for section {section}"}
        # If no teachers are available for the section, return an error message

        self.schedule = self.schedule[self.schedule["Section"] != section]
        # Remove any previous schedule entries for the section (if any)

        for day in days:
            # Loop through each day of the week to assign subjects and teachers

            random.shuffle(time_slots)
            # Shuffle the list of time slots to randomize the timetable (assigning subjects at different times each time)

            for time in time_slots:
                # Loop through each available time slot for the day

                if available_teachers.empty:
                    break
                # Stop if no available teachers are left to assign

                row = available_teachers.sample(1)
                # Randomly select one teacher from the available teachers for the section

                teacher = row['FACULTY'].values[0]
                # Get the name of the selected teacher

                subject = row['SUBJECT'].values[0]
                # Get the subject assigned to the selected teacher

                venue = random.choice(self.venues['VENUE'].values)
                # Randomly choose a venue from the available venues

                # Create a new row as a pandas DataFrame to store the class information for the timetable
                new_row = pd.DataFrame({
                    "Section": [section],
                    "Subject": [subject],
                    "Teacher": [teacher],
                    "Venue": [venue],
                    "Day": [day],
                    "Time": [time]
                })

                self.schedule = pd.concat([self.schedule, new_row], ignore_index=True)
                # Append the new row to the existing schedule

        timetable = defaultdict(list)
        # Create a defaultdict to group the timetable entries by day

        section_schedule = self.schedule[self.schedule["Section"] == section]
        # Filter the timetable to include only entries for the selected section

        for _, entry in section_schedule.iterrows():
            timetable[entry["Day"]].append(entry)
        # Loop through each row in the section's timetable and group the entries by the "Day" field

        return timetable
        # Return the grouped timetable for the specified section

    def check_class_availability(self, venue, day, time):
        # Method to check if a particular venue is available at a given day and time

        is_available = not ((self.schedule['Venue'] == venue) &
                            (self.schedule['Day'] == day) &
                            (self.schedule['Time'] == time)).any()
        # Check if the venue is already booked by checking if any entry in the timetable matches the given venue, day, and time
        return is_available
        # Return True if the venue is available, otherwise False

    def check_faculty_availability(self, teacher, day, time):
        # Method to check if a particular teacher is available at a given day and time

        is_available = not ((self.schedule['Teacher'] == teacher) &
                            (self.schedule['Day'] == day) &
                            (self.schedule['Time'] == time)).any()
        # Check if the teacher is already assigned to a class at the given day and time
        return is_available
        # Return True if the teacher is available, otherwise False

# Initialize the scheduling system with the teacher and venue CSV files
schedule_system = ScheduleSystem()

@app.route('/', methods=['GET', 'POST'])
def index():
    # Define the route for the home page where timetable generation and availability checks happen

    sections = ['A', 'B', 'C', 'D', 'E', 'F', 'G']
    # List of available sections (hardcoded for this example)

    days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"]
    # List of weekdays

    time_slots = [
        "8:00-9:00", "9:00-10:00", "10:00-11:00", "11:00-12:00",
        "12:00-1:00", "2:00-3:00", "3:00-4:00", "4:00-5:00", "5:00-6:00"
    ]
    # List of time slots for the timetable

    venues = schedule_system.venues['VENUE'].tolist()
    # Get a list of all venue names from the ScheduleSystem's venue data

    teachers = schedule_system.teachers['FACULTY'].unique().tolist()
    # Get a list of all unique teacher names from the ScheduleSystem's teacher data

    if request.method == 'POST':
        # If the request method is POST (when a form is submitted)

        if 'generate_timetable' in request.form:
            # If the "Generate Timetable" form was submitted

            section = request.form.get('section')
            # Get the selected section from the form

            grouped_timetable = schedule_system.generate_timetable(section)
            # Call the generate_timetable method to create a timetable for the selected section

            if isinstance(grouped_timetable, dict) and "error" in grouped_timetable:
                # If there was an error (e.g., no teachers available for the section)

                return render_template('index.html', error=grouped_timetable["error"], sections=sections, days=days, time_slots=time_slots, venues=venues, teachers=teachers)
                # Render the page and display the error message

            return render_template('index.html', grouped_timetable=grouped_timetable, sections=sections, days=days, time_slots=time_slots, venues=venues, teachers=teachers, message="Timetable generated successfully!")
            # Render the page and display the generated timetable

        elif 'check_class_availability' in request.form:
            # If the "Check Class Availability" form was submitted

            venue = request.form.get('venue')
            day = request.form.get('day')
            time = request.form.get('time')
            # Get the selected venue, day, and time from the form

            class_available = schedule_system.check_class_availability(venue, day, time)
            # Check if the selected class is available using the check_class_availability method

            return render_template('index.html', class_result=class_available, sections=sections, days=days, time_slots=time_slots, venues=venues, teachers=teachers)
            # Render the page with the result of class availability check

        elif 'check_faculty_availability' in request.form:
            # If the "Check Faculty Availability" form was submitted

            teacher = request.form.get('teacher')
            day = request.form.get('day')
            time = request.form.get('time')
            # Get the selected teacher, day, and time from the form

            faculty_available = schedule_system.check_faculty_availability(teacher, day, time)
            # Check if the selected faculty member is available using the check_faculty_availability method

            return render_template('index.html', faculty_result=faculty_available, sections=sections, days=days, time_slots=time_slots, venues=venues, teachers=teachers)
            # Render the page with the result of faculty availability check

    return render_template('index.html', sections=sections, days=days, time_slots=time_slots, venues=venues, teachers=teachers)
    # For GET requests (initial page load), render the page with all the available data

if __name__ == "__main__":
    app.run(debug=True)
    # Run the Flask app in debug mode (useful for development and debugging)

import pandas as pd
# Import pandas library, which is used to handle and manipulate data in tabular form (CSV files in this case)

class ScheduleSystem:
    # Define the ScheduleSystem class to handle the scheduling logic

    def __init__(self, csv_file='dataset.csv'):
        # Constructor method to initialize the ScheduleSystem instance
        # Takes the CSV filename as an argument (default is 'dataset.csv')

        self.csv_file = csv_file
        # Store the CSV filename in the instance variable `csv_file`

        self.teachers = pd.read_csv(csv_file)
        # Read the CSV file (which contains teacher data) into a pandas DataFrame and store it in `self.teachers`

        self.schedule = pd.DataFrame(columns=["Section", "Subject", "Teacher", "Day", "Time"])
        # Initialize an empty DataFrame `self.schedule` to store the schedule with columns: "Section", "Subject", "Teacher", "Day", "Time"

    def add_schedule(self, section, subject, teacher, day, time):
        # Method to add a new entry to the timetable

        if self.check_teacher_availability(teacher, day, time):
            # Check if the teacher is available at the given day and time using the check_teacher_availability method

            # If teacher is available, create a new row in the schedule DataFrame
            new_entry = pd.DataFrame([[section, subject, teacher, day, time]],
                                     columns=["Section", "Subject", "Teacher", "Day", "Time"])
            # Create a pandas DataFrame for the new entry with the passed section, subject, teacher, day, and time

            self.schedule = pd.concat([self.schedule, new_entry], ignore_index=True)
            # Append the new entry to the `self.schedule` DataFrame. `ignore_index=True` ensures that the index is reset after concatenation

            return True
            # Return True to indicate that the new schedule entry was successfully added
        else:
            return False
            # Return False if the teacher is not available at the given day and time

    def check_class_availability(self, section, day, time):
        # Method to check if a class is available for the given section, day, and time

        return not any((self.schedule["Section"] == section) & 
                       (self.schedule["Day"] == day) & 
                       (self.schedule["Time"] == time))
        # Check if there is any existing entry in `self.schedule` with the same section, day, and time
        # If no match is found, the class is available (returns True), otherwise returns False

    def check_teacher_availability(self, teacher, day, time):
        # Method to check if a teacher is already scheduled for the given day and time

        return not any((self.schedule["Teacher"] == teacher) & 
                       (self.schedule["Day"] == day) & 
                       (self.schedule["Time"] == time))
        # Check if there is any existing entry in `self.schedule` where the teacher is already scheduled for the same day and time
        # If no match is found, the teacher is available (returns True), otherwise returns False

    def get_timetable(self):
        # Method to return the full timetable (schedule)
        return self.schedule
        # Return the `self.schedule` DataFrame which contains the entire schedule

    def save_schedule(self, filename="schedule.csv"):
        # Method to save the current schedule to a CSV file

        self.schedule.to_csv(filename, index=False)
        # Save the `self.schedule` DataFrame to a CSV file with the given filename
        # `index=False` ensures that the row indices are not included in the saved CSV

# Example usage
schedule_system = ScheduleSystem()
# Create an instance of the ScheduleSystem class. This will read the teachers from the 'dataset.csv' file

print(schedule_system.teachers)  # Print the teachers from the CSV file
# Print the DataFrame containing the teachers' data loaded from the CSV file

# Uncomment these lines to test scheduling
# schedule_system.add_schedule("A", "Math", "Alice", "Monday", "8:00-9:00")
# Uncomment this line to add a class for section "A", subject "Math", teacher "Alice", on Monday at 8:00-9:00
# print(schedule_system.get_timetable()) 
# Uncomment this line to print the current timetable after adding the class

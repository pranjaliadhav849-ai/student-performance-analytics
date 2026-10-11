"""
Student Performance Analytics System
Mini project for Python with AI course.
Run: python main.py
"""

import numpy as np
import pandas as pd

DATA_FILE = "students.csv"
SUBJECTS = ["Python_Marks", "AI_Marks", "Mathematics_Marks", "Data_Analysis_Marks"]
PASS_MARK = 35


def assign_grade(average):
    """Return a grade using the project grading rule."""
    if average >= 90:
        return "A+"
    elif average >= 80:
        return "A"
    elif average >= 70:
        return "B"
    elif average >= 60:
        return "C"
    elif average >= 50:
        return "D"
    else:
        return "F"


def load_data(filename):
    """Read student records from a CSV file into a Pandas DataFrame."""
    try:
        data = pd.read_csv(filename)
        required_columns = ["Student_ID", "Name", "Department"] + SUBJECTS + ["Attendance_Percent"]
        missing = [column for column in required_columns if column not in data.columns]
        if missing:
            raise ValueError("Missing columns: " + ", ".join(missing))
        return data
    except FileNotFoundError:
        print(f"Error: {filename} was not found. Keep it in the same folder as main.py.")
        raise


def calculate_performance(data):
    """Add total, average, grade and pass/fail columns."""
    data = data.copy()
    data["Total_Marks"] = data[SUBJECTS].sum(axis=1)
    data["Average_Marks"] = np.round(data[SUBJECTS].mean(axis=1), 2)
    data["Grade"] = data["Average_Marks"].apply(assign_grade)

    # A student passes only if marks in every subject are at least PASS_MARK.
    data["Result"] = data[SUBJECTS].ge(PASS_MARK).all(axis=1).map(
        {True: "Pass", False: "Fail"}
    )
    return data


def show_student_results(data):
    print("\n=== STUDENT PERFORMANCE ANALYTICS SYSTEM ===")
    print("\nStudent-wise results:")
    columns = ["Student_ID", "Name", "Department", "Total_Marks",
               "Average_Marks", "Grade", "Result", "Attendance_Percent"]
    print(data[columns].to_string(index=False))


def show_class_summary(data):
    print("\n=== CLASS SUMMARY ===")
    print(f"Number of students: {len(data)}")
    print(f"Class average (all subject marks): {data[SUBJECTS].to_numpy().mean():.2f}")
    print(f"Highest student average: {data['Average_Marks'].max():.2f}")
    print(f"Lowest student average: {data['Average_Marks'].min():.2f}")
    print(f"Students passed: {(data['Result'] == 'Pass').sum()}")
    print(f"Students failed: {(data['Result'] == 'Fail').sum()}")
    print(f"Average attendance: {data['Attendance_Percent'].mean():.2f}%")


def show_subject_analysis(data):
    print("\n=== SUBJECT-WISE AVERAGE ===")
    subject_averages = data[SUBJECTS].mean().round(2)
    for subject, average in subject_averages.items():
        print(f"{subject.replace('_Marks', '').replace('_', ' ')}: {average:.2f}")
    print("Best-performing subject:", subject_averages.idxmax().replace("_Marks", "").replace("_", " "))
    print("Lowest-performing subject:", subject_averages.idxmin().replace("_Marks", "").replace("_", " "))


def show_top_performers(data, count=3):
    print(f"\n=== TOP {count} PERFORMERS ===")
    top_students = data.sort_values(by="Average_Marks", ascending=False).head(count)
    print(top_students[["Student_ID", "Name", "Average_Marks", "Grade"]].to_string(index=False))


def main():
    data = load_data(DATA_FILE)
    results = calculate_performance(data)
    show_student_results(results)
    show_class_summary(results)
    show_subject_analysis(results)
    show_top_performers(results)

    output_file = "student_performance_results.csv"
    results.to_csv(output_file, index=False)
    print(f"\nDetailed results saved to: {output_file}")


if __name__ == "__main__":
    main()

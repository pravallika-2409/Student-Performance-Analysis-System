def calculate_percentage(obtained, maximum):
    if maximum <= 0:
        raise ValueError("Maximum marks must be greater than zero.")
    if obtained < 0 or obtained > maximum:
        raise ValueError("Obtained marks must be between zero and maximum marks.")
    return (obtained / maximum) * 100

def calculate_grade(percentage):
    if not 0 <= percentage <= 100:
        raise ValueError("Percentage must be between 0 and 100.")
    if percentage >= 90: return "A+"
    if percentage >= 80: return "A"
    if percentage >= 70: return "B"
    if percentage >= 60: return "C"
    if percentage >= 50: return "D"
    if percentage >= 40: return "E"
    return "F"

def pass_or_fail(obtained, pass_marks):
    return "Pass" if obtained >= pass_marks else "Fail"

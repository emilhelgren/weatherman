from datetime import datetime

def get_formatted_date(date: datetime):
    """
    Formats a datetime object to a datestr in the format required by the DMI API.

    Args:
        dates: A datetime object.
    """
    return date.strftime('%Y-%m-%dT00:00:00Z/%Y-%m-%dT23:59:00Z')


def print_column_graph(data):
    """
    Prints a column graph to the console from a list of floats.

    Args:
        data: A list of floats representing the data for the graph.
    """

    if not isinstance(data, list) or not all(isinstance(x, (int, float)) for x in data):
        print("Error: Input must be a list of numeric values.")
        return

    max_value = max(data)
    if max_value == 0:
        max_value = 1 #avoid division by zero if all values are zero

    for i, value in enumerate(data):
        bar_length = int((value / max_value) * 40)  # Scale to a maximum of 40 characters
        bar = "#" * bar_length
        print(f"{i:02d}: {bar} {value:.2f}")
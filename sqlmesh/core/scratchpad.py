import pandas as pd
from typing import List
import daff

# Create two sample dataframes
data1 = {
    "id": [1, 2, 3, 4, 5, 6, 7],
    "item_id": [2, 1, 3, 1, 1, 1, 1],
    "event_date": [
        "2020-01-01",
        "2020-01-01",
        "2020-01-03",
        "2020-01-04",
        "2020-01-05",
        "2020-01-06",
        "2020-01-07",
    ],
}
df1 = pd.DataFrame(data1)

data2 = {
    "id": [1, 2, 3, 4, 5, 9, 7],
    "item_id": [2, 1, 2, 1, 1, 1, 1],
    "event_dates": [
        "2020-01-01",
        "2020-01-01",
        "2020-01-03",
        "2020-01-04",
        "2020-01-05",
        "2020-01-07",
        "2020-01-07",
    ],
}
df2 = pd.DataFrame(data2)


def dataframe_to_sorted_list(df: pd.DataFrame) -> List[List]:
    """Converts a DataFrame into a sorted list of lists, where the first list is the header."""
    sorted_df = df.sort_values(by=list(df.columns))
    header = sorted_df.columns.tolist()
    rows = sorted_df.to_records(index=False).tolist()
    return [header] + rows


# Convert the dataframes to sorted lists of lists
source = dataframe_to_sorted_list(df1)
target = dataframe_to_sorted_list(df2)


class CustomTerminalDiffRender(daff.TerminalDiffRender):
    COLORS = {
        "header": "\033[96m",  # cyan
        "move": "\033[95m",  # magenta
        "insert": "\033[95m",  # green
        "delete": "\033[91m",  # red
        "modify_old": "\033[91m",  # red
        "modify_new": "\033[95m",  # green
        "conflict": "\033[91m",  # red
        "reset": "\033[0m",  # reset
    }

    def colorize(self, text: str, category: str) -> str:
        return f"{self.COLORS.get(category, self.COLORS['reset'])}{text}{self.COLORS['reset']}"


def run_daff_diff(source: List[List], target: List[List]) -> None:
    expected_daff_table = daff.PythonTableView(source)
    actual_daff_table = daff.PythonTableView(target)

    flags = daff.CompareFlags()
    flags.unchanged_context = 0  # Optional: set to 0 to only show changes
    flags.always_show_order = True  # Optional: set to True to always show row order changes

    alignment = daff.Coopy.compareTables(expected_daff_table, actual_daff_table, flags).align()
    result = daff.PythonTableView([])

    diff = daff.TableDiff(alignment, flags)
    diff.hilite(result)

    renderer = CustomTerminalDiffRender()
    rendered = renderer.render(result)
    print(rendered)
    return rendered


run_daff_diff(source, target)

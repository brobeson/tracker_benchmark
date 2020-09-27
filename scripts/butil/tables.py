"""Classes for printing tables of tracking results."""

ROW_NAMES = [
    "ALL",
    "BC",
    "DEF",
    "FM",
    "IPR",
    "IV",
    "LR",
    "MB",
    "OCC",
    "OPR",
    "OV",
    "SV",
]

FULL_NAMES = {
    ROW_NAMES[0]: "All",
    ROW_NAMES[1]: "Background Clutter",
    ROW_NAMES[2]: "Deformation",
    ROW_NAMES[3]: "Fast Motion",
    ROW_NAMES[4]: "In-Plane Rotation",
    ROW_NAMES[5]: "Illumination Variation",
    ROW_NAMES[6]: "Low Resolution",
    ROW_NAMES[7]: "Motion Blur",
    ROW_NAMES[8]: "Occlusion",
    ROW_NAMES[9]: "Out-of-Plane Rotation",
    ROW_NAMES[10]: "Out of View",
    ROW_NAMES[11]: "Scale Variation",
}

TABLE_TYPES = []


class Table:
    """The base class for different types of tables."""

    def __init__(self, column_headers, highlight_best: bool, delta_column: str):
        if delta_column and delta_column not in column_headers:
            raise ValueError(f"{delta_column} is not one of the trackers in the table")
        self._delta_column = delta_column
        self._deltas = None
        self._column_headers = column_headers
        self._highlight_best = highlight_best
        self._best_scores = None
        self._table_rows = {
            ROW_NAMES[0]: [0.0 for c in self._column_headers],
            ROW_NAMES[1]: [0.0 for c in self._column_headers],
            ROW_NAMES[2]: [0.0 for c in self._column_headers],
            ROW_NAMES[3]: [0.0 for c in self._column_headers],
            ROW_NAMES[4]: [0.0 for c in self._column_headers],
            ROW_NAMES[5]: [0.0 for c in self._column_headers],
            ROW_NAMES[6]: [0.0 for c in self._column_headers],
            ROW_NAMES[7]: [0.0 for c in self._column_headers],
            ROW_NAMES[8]: [0.0 for c in self._column_headers],
            ROW_NAMES[9]: [0.0 for c in self._column_headers],
            ROW_NAMES[10]: [0.0 for c in self._column_headers],
            ROW_NAMES[11]: [0.0 for c in self._column_headers],
        }

    def print(self) -> None:
        """Prepare the table and print it to standard output."""
        self.__calculate_best_scores()
        self.__calculate_delta_column()
        self._print_the_table()

    def _print_the_table(self) -> None:
        """
        Print the table to standard output.

        This must be re-implemented by subclasses. This implementation raises NotImplementedError.
        """
        raise NotImplementedError("This class does not implement print().")

    def set_row(self, row_name: str, row_data) -> None:
        """
        Set the values in a row.

        :param str row_name: The name of the row. This must be one of the row
            name constants.
        :param list row_data: The data to set for the row. This must be a
            list of floating point data, and must have the same length as the
            column headers list.
        """
        if row_name not in ROW_NAMES:
            raise ValueError(f"{row_name} is not a valid row name.")
        if len(row_data) != len(self._column_headers):
            raise ValueError(
                f"Row data length ({len(row_data)}) does not match column headers "
                "({len(self.__column_headers)})."
            )
        self._table_rows[row_name] = row_data

    def set_value(self, row_name: str, column: str, value: float) -> None:
        """
        Set a value in the table.

        :param str row_name: The name of the row. This must be one of the row
            name constants.
        :param str column: The tracker column for the value. This must be a
            tracker in the column headers.
        :param float value: The value to set.
        """
        if row_name not in ROW_NAMES:
            raise ValueError(f"{row_name} is not a valid row name.")
        if column not in self._column_headers:
            raise ValueError(f"{column} is not a valid column.")
        self._table_rows[row_name][self._column_headers.index(column)] = value

    def __calculate_best_scores(self):
        self._best_scores = [
            max(row_data) for row_data in self._table_rows.values()
        ]

    def __calculate_delta_column(self):
        delta_index = self._column_headers.index(self._delta_column)
        self._deltas = []
        for i, row in enumerate(ROW_NAMES):
            self._deltas.append(self._best_scores[i] - self._table_rows[row][delta_index])


class LatexTable(Table):
    """Support for printing a table using LaTeX."""

    TABLE_TYPES.append("latex")

    def _print_the_table(self) -> None:
        """Print the LaTeX table."""
        print("\\begin{table}")
        print("  \\caption{}\\label{}")
        c_count = len(self._column_headers)
        if self._delta_column:
            c_count += 1
        print("  \\begin{tabular}{l", " c" * c_count, "}", sep="", end="")
        print("    \\toprule")
        print("    Category &", " & ".join(self._column_headers), end="")
        if self._delta_column:
            print(" & \\(\\Delta\\) ", end="")
        print("\\\\")
        print("    \\midrule")
        for row, row_name in enumerate(ROW_NAMES):
            print(f"    {FULL_NAMES[row_name]} ", end="")
            for value in self._table_rows[row_name]:
                if self._highlight_best and value >= self._best_scores[row]:
                    print(f" & \\best{{{value:.2f}}}", end="")
                else:
                    print(f" & {value:.2f}", end="")
            if self._delta_column:
                print(f" & {self._deltas[row]:.2f}", end="")
            print(" \\\\")
        print("    \\bottomrule")
        print("  \\end{tabular}")
        print("\\end{table}")


class ConsoleTable(Table):
    """Support for printing a table in the console."""

    TABLE_TYPES.append("basic")

    def _print_the_table(self) -> None:
        """Print the table."""
        category_width, column_widths = self.__calculate_column_widths()
        header_line = self.__build_header_line(category_width, column_widths)
        print(header_line)
        print("-" * len(header_line))
        for row, row_name in enumerate(ROW_NAMES):
            print(FULL_NAMES[row_name].ljust(category_width), end="")
            for value, width in zip(self._table_rows[row_name], column_widths):
                if self._highlight_best and value >= self._best_scores[row]:
                    print(
                        "\033[95m",
                        f"{value:.2f}".rjust(width),
                        "\033[0m",
                        end="",
                        sep="",
                    )
                else:
                    print(f"{value:.2f}".rjust(width), end="")
            if self._delta_column:
                print(f"{self._deltas[row]:.2f}".rjust(6), end="")
            print()

    def __calculate_column_widths(self):
        widths = [len(header) + 1 for header in self._column_headers]
        category_width = max([len(category) for category in FULL_NAMES.values()]) + 1
        return category_width, widths

    def __build_header_line(self, category_width: int, column_widths):
        header_line = "Category".ljust(category_width) + "".join(
            [
                header.rjust(width)
                for header, width in zip(self._column_headers, column_widths)
            ]
        )
        if self._delta_column:
            return header_line + " Delta"
        return header_line


def make_table(table_type: str, column_headers, highlight_best: bool, delta_column: str) -> Table:
    """
    Make the type of table requested.

    :param str table_type: The type of table to create.
    :param list column_headers: The list of trackers to use as the column headers.
    :param bool highlight_best: True indicates to highlight the best scores in each row.
    :return: A table object.
    :rtype: A subclass of scripts.butil.tables.Table
    """
    if table_type == "basic":
        return ConsoleTable(column_headers, highlight_best, delta_column)
    if table_type == "latex":
        return LatexTable(column_headers, highlight_best, delta_column)
    raise ValueError(f"{table_type} is not a valid type of table to print.")

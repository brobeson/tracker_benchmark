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

    def __init__(self, column_headers):
        self._column_headers = column_headers
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


class LatexTable(Table):
    """Support for printing a table using LaTeX."""

    TABLE_TYPES.append("latex")

    def print(self) -> None:
        """Print the LaTeX table."""
        print("\\begin{table}")
        print("  \\caption{Foo}")
        print("  \\begin{tabular}{l", "c " * len(self._column_headers), "}")
        print("    \\toprule")
        print("    Category &", " & ".join(self._column_headers), "\\\\")
        print("    \\midrule")
        for category in ROW_NAMES:
            print(
                "   ",
                FULL_NAMES[category],
                "&",
                " & ".join([str(f) for f in self._table_rows[category]]),
                "\\\\",
            )
        print("    \\bottomrule")
        print("  \\end{tabular}{l c c c}")
        print("\\end{table}")


class ConsoleTable(Table):
    """Support for printing a table in the console."""

    TABLE_TYPES.append("basic")

    def print(self) -> None:
        """Print the table."""
        category_width, column_widths = self.__calculate_column_widths()
        header_line = self._build_header_line(category_width, column_widths)
        print(header_line)
        print("-" * len(header_line))
        for category in ROW_NAMES:
            print(
                FULL_NAMES[category].ljust(category_width),
                "".join(
                    [
                        str(value).rjust(width)
                        for value, width in zip(
                            self._table_rows[category], column_widths
                        )
                    ]
                ),
                sep="",
            )

    def __calculate_column_widths(self):
        widths = [len(header) + 1 for header in self._column_headers]
        category_width = max([len(category) for category in FULL_NAMES.values()]) + 1
        return category_width, widths

    def _build_header_line(self, category_width: int, column_widths):
        return "Category".ljust(category_width) + "".join(
            [
                header.rjust(width)
                for header, width in zip(self._column_headers, column_widths)
            ]
        )


def make_table(table_type: str, column_headers) -> Table:
    """
    Make the type of table requested.

    :param str table_type: The type of table to create.
    :param list column_headers: The list of trackers to use as the column headers.
    :return: A table object.
    :rtype: A subclass of scripts.butil.tables.Table
    """
    if table_type == "basic":
        return ConsoleTable(column_headers)
    if table_type == "latex":
        return LatexTable(column_headers)
    raise ValueError(f"{table_type} is not a valid type of table to print.")

import sqlite3
from collections.abc import Collection

class TableData(Collection):
    def __init__(self, database_name: str, table_name: str):
        self.database_name = database_name
        self.table_name = table_name

    def __len__(self) -> int:
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT COUNT(*) FROM {self.table_name}")
            count = cursor.fetchone()[0]
        return count

    def __getitem__(self, key: str) -> dict:
        with sqlite3.connect(self.database_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name} WHERE name = ?", (key,))
            row = cursor.fetchone()
        if row is None:
            raise KeyError(key)
        return dict(row)

    def __iter__(self):
        with sqlite3.connect(self.database_name) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute(f"SELECT * FROM {self.table_name}")
            row = cursor.fetchone()
            while row is not None:
                yield dict(row)
                row = cursor.fetchone()

    def __contains__(self, key: str) -> bool:
        with sqlite3.connect(self.database_name) as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT 1 FROM {self.table_name} WHERE name = ? LIMIT 1", (key,))
            return cursor.fetchone() is not None

if __name__ == '__main__':
    presidents = TableData(database_name='example.sqlite', table_name='presidents')
    print("Total records in presidents:", len(presidents))
    if 'Yeltsin' in presidents:
        print("'Yeltsin' is in the presidents table")
    else:
        print("'Yeltsin' is NOT in the presidents table")
    try:
        yeltsin_record = presidents['Yeltsin']
        print("Record for Yeltsin:", yeltsin_record)
    except KeyError:
        print("No record found for Yeltsin")
    print("Iterating over presidents:")
    for record in presidents:
        print(record['name'])

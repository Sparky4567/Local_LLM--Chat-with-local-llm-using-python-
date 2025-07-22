import sqlite3
from typing import List, Dict
from rapidfuzz  import fuzz  # or use rapidfuzz for better performance

from config.settings import SIMILARITY_TRESHHOLD

class MarkdownDB:
    def __init__(self, db_path: str = "markdown_files.db"):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        with self.conn:
            self.conn.execute("""
                CREATE TABLE IF NOT EXISTS markdown_files (
                    file_name TEXT,
                    file_route TEXT,
                    file_content TEXT
                )
            """)

    def insert_from_json(self, json_data: List[Dict]):
        with self.conn:
            self.conn.executemany("""
                INSERT INTO markdown_files (file_name, file_route, file_content)
                VALUES (:file_name, :file_route, :file_content)
            """, json_data)
            self.conn.commit()

    def search_fuzzy(self, keyword: str, threshold: int = SIMILARITY_TRESHHOLD) -> List[Dict]:
        cursor = self.conn.cursor()
        cursor.execute("SELECT file_name, file_route, file_content FROM markdown_files")
        all_rows = cursor.fetchall()
        results = []
        for file_name, file_route, file_content in all_rows:
            score = fuzz.ratio(str(keyword).strip().lower(), str(file_content).strip().lower())
            # print(score)
            if score >= threshold:
                results.append({
                    "file_name": file_name,
                    "file_route": file_route,
                    "file_content": file_content,
                    "score": score
                })
        # Sort results by score descending
        results.sort(key=lambda x: x["score"], reverse=True)
        return results

    def close(self):
        self.conn.close()

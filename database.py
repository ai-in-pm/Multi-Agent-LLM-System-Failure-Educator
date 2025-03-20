import sqlite3
import os
from typing import List, Dict, Any, Tuple
import json

class FailureEducatorDatabase:
    """Database manager for the Multi-Agent Failure Educator."""
    
    def __init__(self, db_path: str = "educator.db"):
        """Initialize the database connection.
        
        Args:
            db_path: Path to the SQLite database file.
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
        self._create_tables()
    
    def _connect(self):
        """Connect to the database."""
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row  # Enable dictionary-like access to rows
        self.cursor = self.conn.cursor()
    
    def _create_tables(self):
        """Create database tables if they don't exist."""
        # Table for tracking user queries
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_queries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            query TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Table for tracking viewed failure modes
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS viewed_failure_modes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            failure_mode TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        # Table for tracking user feedback on solutions
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS solution_feedback (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            failure_mode TEXT NOT NULL,
            solution_type TEXT NOT NULL,
            solution_text TEXT NOT NULL,
            rating INTEGER,
            comment TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
        """)
        
        self.conn.commit()
    
    def log_user_query(self, query: str) -> int:
        """Log a user query to the database.
        
        Args:
            query: The user's query text.
            
        Returns:
            The ID of the inserted record.
        """
        self.cursor.execute(
            "INSERT INTO user_queries (query) VALUES (?)",
            (query,)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def log_viewed_failure_mode(self, failure_mode: str) -> int:
        """Log a viewed failure mode to the database.
        
        Args:
            failure_mode: The name of the viewed failure mode.
            
        Returns:
            The ID of the inserted record.
        """
        self.cursor.execute(
            "INSERT INTO viewed_failure_modes (failure_mode) VALUES (?)",
            (failure_mode,)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def log_solution_feedback(self, failure_mode: str, solution_type: str, 
                             solution_text: str, rating: int = None, 
                             comment: str = None) -> int:
        """Log user feedback on a solution.
        
        Args:
            failure_mode: The name of the failure mode.
            solution_type: The type of solution (tactical or structural).
            solution_text: The text of the solution.
            rating: Optional rating (e.g., 1-5).
            comment: Optional user comment.
            
        Returns:
            The ID of the inserted record.
        """
        self.cursor.execute(
            """INSERT INTO solution_feedback 
               (failure_mode, solution_type, solution_text, rating, comment) 
               VALUES (?, ?, ?, ?, ?)""",
            (failure_mode, solution_type, solution_text, rating, comment)
        )
        self.conn.commit()
        return self.cursor.lastrowid
    
    def get_most_viewed_failure_modes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """Get the most frequently viewed failure modes.
        
        Args:
            limit: Maximum number of records to return.
            
        Returns:
            List of dictionaries containing failure mode names and view counts.
        """
        self.cursor.execute(
            """SELECT failure_mode, COUNT(*) as view_count 
               FROM viewed_failure_modes 
               GROUP BY failure_mode 
               ORDER BY view_count DESC 
               LIMIT ?""",
            (limit,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_recent_queries(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent user queries.
        
        Args:
            limit: Maximum number of queries to return.
            
        Returns:
            List of dictionaries containing query data.
        """
        self.cursor.execute(
            """SELECT * FROM user_queries 
               ORDER BY timestamp DESC 
               LIMIT ?""",
            (limit,)
        )
        return [dict(row) for row in self.cursor.fetchall()]
    
    def get_solution_feedback_stats(self) -> Dict[str, Any]:
        """Get statistics on solution feedback.
        
        Returns:
            Dictionary with feedback statistics.
        """
        # Get average ratings by solution type
        self.cursor.execute(
            """SELECT solution_type, AVG(rating) as avg_rating 
               FROM solution_feedback 
               WHERE rating IS NOT NULL 
               GROUP BY solution_type"""
        )
        avg_ratings_by_type = {row['solution_type']: row['avg_rating'] for row in self.cursor.fetchall()}
        
        # Get count of feedback by failure mode
        self.cursor.execute(
            """SELECT failure_mode, COUNT(*) as feedback_count 
               FROM solution_feedback 
               GROUP BY failure_mode"""
        )
        feedback_count_by_mode = {row['failure_mode']: row['feedback_count'] for row in self.cursor.fetchall()}
        
        return {
            'avg_ratings_by_type': avg_ratings_by_type,
            'feedback_count_by_mode': feedback_count_by_mode
        }
    
    def close(self):
        """Close the database connection."""
        if self.conn:
            self.conn.close()

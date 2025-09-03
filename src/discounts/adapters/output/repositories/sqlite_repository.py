import sqlite3
from typing import Optional, List
from src.discounts.domain.models import Discount
from src.discounts.application.ports.output.discount_repository import IDiscountRepository

class SqliteDiscountRepository(IDiscountRepository):
    """Implementación del repositorio que usa una base de datos SQLite."""

    def __init__(self, db_path: str):
        print(f"ADAPTER (DB-SQLITE): Repositorio SQLite inicializado. Archivo: {db_path}")
        self.db_path = db_path
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.row_factory = sqlite3.Row # Permite acceder a las columnas por nombre
        self._create_table()

    def _create_table(self):
        """Crea la tabla de descuentos si no existe."""
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS discounts (
                code TEXT PRIMARY KEY,
                percentage REAL NOT NULL,
                is_active INTEGER NOT NULL
            )
        """)
        self.conn.commit()

    def save(self, discount: Discount):
        print(f"ADAPTER (DB-SQLITE): Guardando/Actualizando descuento '{discount.code}' en el archivo DB...")
        cursor = self.conn.cursor()
        # INSERT OR REPLACE es un atajo de SQLite para hacer un "upsert"
        cursor.execute("""
            INSERT OR REPLACE INTO discounts (code, percentage, is_active)
            VALUES (?, ?, ?)
        """, (discount.code, discount.percentage, 1 if discount.is_active else 0))
        self.conn.commit()

    def find_by_code(self, code: str) -> Optional[Discount]:
        print(f"ADAPTER (DB-SQLITE): Buscando descuento '{code}' en el archivo DB...")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM discounts WHERE code = ?", (code,))
        row = cursor.fetchone()
        if row:
            return Discount(
                code=row["code"],
                percentage=row["percentage"],
                is_active=bool(row["is_active"])
            )
        return None

    def find_all(self) -> List[Discount]:
        print("ADAPTER (DB-SQLITE): Devolviendo todos los descuentos desde el archivo DB...")
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM discounts")
        rows = cursor.fetchall()
        return [
            Discount(
                code=row["code"],
                percentage=row["percentage"],
                is_active=bool(row["is_active"])
            ) for row in rows
        ]

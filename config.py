"""
db_config = {
    'user': 'root',
    'password': 'root',
    'host': '68.183.130.198',
    'port': 3308,
    'database': 'mysql'
}
"""

import os

# Configurar la base de datos desde las variables de entorno
db_config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': os.getenv('DB_PORT', 3308),  # Puedes establecer un valor por defecto para el puerto
    'database': os.getenv('DB_NAME')
}

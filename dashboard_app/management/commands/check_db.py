from django.core.management.base import BaseCommand
from django.db import connection
import logging

logger = logging.getLogger('dashboard_app')

class Command(BaseCommand):
    help = 'Check database records and counts'

    def handle(self, *args, **options):
        # Check database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT current_database(), current_user, version();")
                db_info = cursor.fetchone()
                logger.info(f"Connected to database: {db_info[0]}")
                logger.info(f"Current user: {db_info[1]}")
                logger.info(f"PostgreSQL version: {db_info[2]}")
                
                # Check table existence
                cursor.execute("""
                    SELECT table_name 
                    FROM information_schema.tables 
                    WHERE table_schema = 'public'
                    AND table_name IN ('accounts', 'locations');
                """)
                tables = cursor.fetchall()
                logger.info(f"Found tables: {[table[0] for table in tables]}")
                
                # Check table structure
                for table in ['accounts', 'locations']:
                    cursor.execute(f"""
                        SELECT column_name, data_type 
                        FROM information_schema.columns 
                        WHERE table_name = '{table}';
                    """)
                    columns = cursor.fetchall()
                    logger.info(f"Table {table} structure:")
                    for col in columns:
                        logger.info(f"  {col[0]}: {col[1]}")
                
                # Get counts
                cursor.execute("SELECT COUNT(*) FROM accounts;")
                account_count = cursor.fetchone()[0]
                logger.info(f"Total accounts in database: {account_count}")
                
                cursor.execute("SELECT COUNT(*) FROM locations;")
                location_count = cursor.fetchone()[0]
                logger.info(f"Total locations in database: {location_count}")
                
                # Display location records
                cursor.execute("SELECT id, name, code FROM locations;")
                locations = cursor.fetchall()
                logger.info("Location records:")
                for loc in locations:
                    logger.info(f"  ID: {loc[0]}, Name: {loc[1]}, Code: {loc[2]}")
                
                # Display sample account records
                if account_count > 0:
                    cursor.execute("""
                        SELECT a.id, a.account_number, a.balance, l.name as location_name 
                        FROM accounts a 
                        JOIN locations l ON a.location_id = l.id 
                        LIMIT 5;
                    """)
                    accounts = cursor.fetchall()
                    logger.info("Sample account records:")
                    for acc in accounts:
                        logger.info(f"  ID: {acc[0]}, Account: {acc[1]}, Balance: {acc[2]}, Location: {acc[3]}")
                
                # Check location distribution
                cursor.execute("""
                    SELECT l.name, COUNT(a.id) as account_count
                    FROM locations l
                    LEFT JOIN accounts a ON l.id = a.location_id
                    GROUP BY l.name;
                """)
                distribution = cursor.fetchall()
                logger.info("Location distribution:")
                for loc in distribution:
                    logger.info(f"  {loc[0]}: {loc[1]} accounts")
                    
        except Exception as e:
            logger.error(f"Database connection error: {str(e)}")
            return 
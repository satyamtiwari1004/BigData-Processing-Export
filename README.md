# BigData Processing & Export

A Django-based dashboard application for processing and exporting account data.

## Features

- Account dashboard with filtering capabilities
- Data export functionality
- Location-based data analysis
- User role-based access control
- Comprehensive logging system
- Environment-based configuration

## Prerequisites

- Python 3.8+
- PostgreSQL
- pip

## Setup

1. Clone the repository:
```bash
git clone https://github.com/satyamtiwari1004/BigData-Processing-Export.git
cd BigData-Processing-Export
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Environment Configuration:
   - Copy `.env.example` to `.env`:
   ```bash
   cp .env.example .env
   ```
   - Edit `.env` file with your configuration:
   ```bash
   # Django Settings
   SECRET_KEY='your-secret-key-here'
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1

   # Database Settings
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_HOST=localhost
   DB_PORT=5432

   # Logging Settings
   LOG_LEVEL=INFO
   LOG_FILE=logs/dashboard.log
   ```

5. Create PostgreSQL database:
```bash
createdb your_database_name
```

6. Run migrations:
```bash
python manage.py migrate
```

7. Start the development server:
```bash
python manage.py runserver
```

## Project Structure

- `dashboard_app/`: Main application directory
  - `models.py`: Database models
  - `views.py`: View functions
  - `templates/`: HTML templates
  - `static/`: Static files
  - `management/`: Custom management commands
- `.env`: Environment variables (not committed to git)
- `.env.example`: Example environment variables template

## Environment Variables

The application uses the following environment variables:

### Django Settings
- `SECRET_KEY`: Django secret key for cryptographic signing
- `DEBUG`: Debug mode (True/False)
- `ALLOWED_HOSTS`: Comma-separated list of allowed hosts

### Database Settings
- `DB_NAME`: PostgreSQL database name
- `DB_USER`: Database user
- `DB_PASSWORD`: Database password
- `DB_HOST`: Database host
- `DB_PORT`: Database port

### Logging Settings
- `LOG_LEVEL`: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
- `LOG_FILE`: Path to log file

## Logging

Logs are stored in the `logs/` directory. Monitor logs in real-time using:
```bash
tail -f logs/dashboard.log
```

## Security Notes

- Never commit the `.env` file to version control
- Keep your `SECRET_KEY` secure and unique
- Use strong passwords for database access
- In production, set `DEBUG=False` and configure proper `ALLOWED_HOSTS`

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request 
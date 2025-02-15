#!/bin/bash

# Directory for backups
BACKUP_DIR="db/backups"
BACKUP_FILE="$BACKUP_DIR/backup_$(date +%Y%m%d_%H%M%S).sql"

# Function to check and prepare backup directory
check_backup_dir() {
    echo "Checking backup directory..."

    # Check if directory exists
    if [ ! -d "$BACKUP_DIR" ]; then
        echo "Creating backup directory: $BACKUP_DIR"
        mkdir -p "$BACKUP_DIR"

        if [ $? -ne 0 ]; then
            echo "Error: Failed to create backup directory"
            return 1
        fi
    fi

    # Check write permissions
    if [ ! -w "$BACKUP_DIR" ]; then
        echo "Setting write permissions for backup directory..."
        chmod 755 "$BACKUP_DIR"

        if [ $? -ne 0 ]; then
            echo "Error: Failed to set permissions for backup directory"
            return 1
        fi
    fi

    # Check if we can create files in the directory
    touch "$BACKUP_DIR/.test_file" 2>/dev/null
    if [ $? -ne 0 ]; then
        echo "Error: Cannot write to backup directory"
        return 1
    fi
    rm -f "$BACKUP_DIR/.test_file"

    echo "Backup directory is ready"
    return 0
}

# Load environment variables from .env
if [ -f .env ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "Error: .env file not found"
    exit 1
fi

# Function to check if PostgreSQL is ready
check_postgres() {
    echo "Checking PostgreSQL connection..."
    if docker exec redirect_service_db pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_NAME" -h "$POSTGRES_HOST" -p "$POSTGRES_PORT" > /dev/null 2>&1; then
        return 0
    fi
    return 1
}

# Function to create backup
create_backup() {
    # First check backup directory
    if ! check_backup_dir; then
        return 1
    fi

    if check_postgres; then
        echo "Creating backup..."
        if docker exec redirect_service_db pg_dump \
            -U "$POSTGRES_USER" \
            -d "$POSTGRES_NAME" \
            -h "$POSTGRES_HOST" \
            -p "$POSTGRES_PORT" \
            --clean \
            --if-exists > "$BACKUP_FILE"; then

            # Set proper permissions for the backup file
            chmod 644 "$BACKUP_FILE"
            echo "Backup created successfully: $BACKUP_FILE"
            return 0
        else
            echo "Error: Failed to create backup"
            return 1
        fi
    else
        echo "Error: PostgreSQL is not ready"
        return 1
    fi
}

# Function to restore from backup
restore_backup() {
    # First check backup directory
    if ! check_backup_dir; then
        return 1
    fi

    if [ -z "$1" ]; then
        echo "Error: Please specify backup file to restore"
        echo "Usage: $0 restore <backup_file>"
        return 1
    fi

    local backup_file="$1"

    # Check if backup file exists and is readable
    if [ ! -f "$backup_file" ]; then
        echo "Error: Backup file not found: $backup_file"
        return 1
    fi

    if [ ! -r "$backup_file" ]; then
        echo "Error: Cannot read backup file: $backup_file"
        return 1
    fi

    if check_postgres; then
        echo "Restoring from backup: $backup_file"
        if docker exec -i redirect_service_db psql \
            -U "$POSTGRES_USER" \
            -d "$POSTGRES_NAME" \
            -h "$POSTGRES_HOST" \
            -p "$POSTGRES_PORT" < "$backup_file"; then
            echo "Database restored successfully"
            return 0
        else
            echo "Error: Failed to restore database"
            return 1
        fi
    else
        echo "Error: PostgreSQL is not ready"
        return 1
    fi
}

# Function to list available backups
list_backups() {
    # First check backup directory
    if ! check_backup_dir; then
        return 1
    fi

    echo "Available backups:"
    # Check if there are any backup files
    if [ -n "$(ls -A $BACKUP_DIR/*.sql 2>/dev/null)" ]; then
        ls -lh $BACKUP_DIR/*.sql
    else
        echo "No backup files found"
    fi
}

# Main script
case "$1" in
    "backup")
        create_backup
        ;;
    "restore")
        restore_backup "$2"
        ;;
    "list")
        list_backups
        ;;
    *)
        echo "Usage: $0 {backup|restore|list}"
        echo "  backup  - Create new backup"
        echo "  restore <file> - Restore from backup file"
        echo "  list    - Show available backups"
        exit 1
        ;;
esac
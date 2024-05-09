import os


def add_leading_zero(number: str):
    return f"{number:04}"


def create_migration_num_format(number: str):
    new_number = number.lstrip("0") if len(number) >= 4 else " "
    return new_number


def create_folder_migration_num(base_path: str):
    intial_number = 1
    migration_number = add_leading_zero(intial_number)

    migration_folder_path = os.path.join(base_path, migration_number)
    if os.path.exists(migration_folder_path):
        migration_number = [create_migration_num_format(folder) for folder in os.listdir(base_path)]

        max_migration_number = max([int(migration) for migration in migration_number if migration.isnumeric()])

        next_migration_number = add_leading_zero(max_migration_number + 1)

    else:
        next_migration_number = migration_number
    return next_migration_number

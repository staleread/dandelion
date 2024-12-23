# dandelion

<img src="https://images.vexels.com/content/244182/preview/dandelion-flower-color-stroke-18bf94.png" alt="Dandelion flower" width="100" />

The purpose of this project is to create a centralized system
(from now - System) for managing data of a policlynic

The System should store general information about doctors, patients,
examination rooms and treatment procedures, as well as to keep records of
patient visits, examinations and treatment (medical history, diagnosis,
prescribed tests, procedures, medications, etc.)

It is necessary to provide the ability to call a district doctor to the
house, to automate the issuance of various certificates and extracts for
patients, to create work schedule of doctors and treatment rooms
(in shifts on a certain day of the week).

As a DB admin, depending on given permissions, the user can connect to a DB,
access contents of DB tables, modify data in records, create/edit/delete
attributes and tables, and add new users.

Due to the System complexity, it'll be logically divided into 2 subdomains:
- dandelion-classic - for running domain queries and commands
- dandelion-db - for DB administration

## Launch with Docker

> [!IMPORTANT]
> Ensure that Docker is installed and running

### Environment Setup

Before launching the project, create a `.env` file in the root directory with the following variables:

> [!NOTE]
> Required environment variables:
> ```env
> JWT_SECRET=your_secure_jwt_secret
> JWT_ALGORITHM=HS256
> JWT_LIFETIME=700
> HASH_SALT=your_secure_salt
> COOKIE_NAME=id_token
> DB_USER=your_db_username
> DB_PASS=your_db_password
> DB_HOST=db:5432
> DB_NAME=dandelion-db
> ```

### Launch Steps

1. Build and start the containers:

```bash
docker compose up -d
```

2. Generate initial DB data

```bash
./scripts/gen-db-init.sh
```

3. Login to the PgAdmin using credentials:
- Email: admin@gmail.com
- Password: 123

4. Execute the sql script generated in `db-init.sql`, in PgAdmin

5. Generate a valid salt and hashed password with a script:

```bash
python scripts/generate_password_hash.py
```

> [!IMPORTANT]
> Ensure you have `getpass` and `bcrypt` python libraries installed
> either on system or in virtual environment

6. Insert the owner user credentials into the DB:

```sql
insert into "user" (username, hashed_password, role_id)
values ('YOUR_USERNAME', 'YOUR_HASHED_PASSWORD', 4)
```

Now you can use the username and password to login to the System

### Stopping the Project

To stop all containers:
```bash
docker compose down
```

To stop and remove all data (including database volume):
```bash
docker compose down -v
```

## Dandelion Classic
### Domain Queries
#### 1. Therapists schedules

-  Get therapists schedules

#### 2. Doctor's overview

-  Get Doctors' overview

#### 3. Filter patients

- Filter patients by last name
- Filter patients by medical history ID
- Filter patients by health status
- Filter patients by their therapist

#### 4. Patients statistics

- Get info about those patients, who were examined by more than two doctors
during this week
- Get the number of patients diagnosed with angina during this month

#### 5. Doctors statistics

- Get doctor's schedule for a week
- Get doctor's schedule for a month
- Get the list and total number of doctors of the specified profile

#### 6. Home visits info

- Get the last names and addresses of patients who ever called a district doctor
- Visits per doctor - get the number of home visits made by each doctor

#### 7. Procedures info

- Get a list of procedures provided by the clinic by the clinic
- Get procedures performed during this week
- Get the list of patients who received procedures during the week

#### 8. Procedures and vaccination

- Get a list of patients who had a fluorography on a given day 
- Get a list of patients who did not receive scheduled vaccinations

#### 9. Physiotherapy

- Get info about all physiotherapy rooms
- Get physiotherapy rooms schedule
- Get the number of doctors working in EACH room during the week

#### 10. Visits statistics

- Get the total number of visits to the clinic in a month
- Get the total number of visits to the clinic in a month grouped by doctors' profiles

### Domain Commands
#### 1. Issue a certificate

Must include:
- issue template ID
- info needed for a specific template

## Dandelion DB
### User Roles and Permissions

`Guest`
- `can_connect` - Can connect to DB with credentials (login, password)
- `can_read_public` - Can read contents of public DB tables

`Operator`
- Extends `Guest`'s permissions
- `can_modify_records`- Can add/modify/delete records

`Admin`
- Extends `Operator`'s permissions
- `can_modify_attributes` - Can modify table structure:
    - Add/delete attribute
    - Rename attribute
- `can_add_user` - Can add users of type `Guest`
- `can_add_operator` - Can add users of type `Operator`

`Owner`
- Extends `Admin`'s features
- `can_read_private` - Can read contents of `Keys` table
- `can_modify_tables` - Can add/delete tables
- `can_add_admin` - Can add users of type `Admin`

## UI requirements

- Language of UI - Ukrainian
- Displaying a table, the attributes must be in Ukrainian

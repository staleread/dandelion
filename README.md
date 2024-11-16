# dandelion

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

## Dandelion Classic
### Domain Queries
#### 1. Therapists schedules

-  Get therapists schedules

> [!NOTE]
> A doctor's schedule must include
>   1. day of week (in Ukrainian)
>   2. start hour
>   3. end hour
>   4. room number
>   5. room type name

#### 2. Doctor's overview

-  Get Doctors' overview

> [!NOTE]
> A doctor's overview consists of
>   1. personal info
>   2. unique list of certificate types ever given
>   3. amount of patients, examined during this week

#### 3. Filter patients

- Filter patients by last name
- Filter patients by medical history ID
- Filter patients by health status
- Filter patients by their therapist

#### 4. Special case #1

- Get info about those patients, who were examined by more than two doctors
during this week
- Get the number of patients diagnosed with angina during this month

#### 5. Doctor's schedule for period

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

#### 8. Special case #2

- Get a list of patients who had a fluorography on a given day 
- Get a list of patients who did not receive scheduled vaccinations

#### 9. Physiotherapy Rooms Info and more

- Get info about all physiotherapy rooms
- Get physiotherapy rooms schedule
- Get the number of doctors working in EACH room during the week

> [!NOTE]
> Room shcedule must include info about
>   1. first shift
>   2. second shift
>   3. two shifts

#### 10. Count of Visits

- Get the total number of visits to the clinic in a month
- Get the total number of visits to the clinic in a month grouped by doctors' profiles

It is necessary to provide the ability to call a district doctor to the
house, to automate the issuance of various certificates and extracts for
patients, to create work schedule of doctors and treatment rooms (in shifts on a certain day of the week).

### Domain Commands
#### 1. Add home visit request

Must include:
- patient ID
- address for visit (patient's home address by default)
- purpose

#### 2. Issue a certificate

Must include:
- issue template ID
- info needed for a specific template

#### 3. Update examination room schedule

Display the calendar view of room shedule (7 groups for each day containing
2 shifts). If the room is busy during some shift it must be colored and 
display info about the doctor (last name and first letters of first name and
patronymic), blank otherwise. By clicking on the shift section user should
see a form for updating the entry or creating one if it was blank.

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

# BounSailing Group Placement System

This project is designed to automate the group management and placement process for sailing training programs. It processes applicant data, identifies groups, and optimizes their placement into training slots based on various conditions, ensuring maximum utilization of available resources and fair allocation of training slots.

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation](#installation)
- [Usage](#usage)
- [Code Logic](#code-logic)
- [Example Scenario](#example-scenario)
- [Potential Improvements](#potential-improvements)

## Features

- **Applicant Identification**: Parses and processes data from applications, creating an ID card for each applicant.
- **Screening Process**: Filters applicants based on club membership, prerequisites for training, and payment status.
- **Dynamic Grouping**: Groups applicants based on their friendship relationships, including handling single applicants as individual groups.
- **Subset Removal**: Identifies and removes subset groups to avoid duplication.
- **Slot Assignment**: Assigns groups to available training slots based on application order and slot availability.
- **Optimization**: Implements an iterative placement system to maximize the number of placed applicants by exploring different slot allocation combinations.
- **Conflict Resolution**: Handles group merging, slot capacity, and reallocation of applicants in multiple stages for optimized placement.

## Project Structure

The project is organized as follows:

```
BounSailing/
│
├── .venv/                       # Python virtual environment directory
├── data/                        # Contains input CSV files with applicant data
├── src/                         # Main source code directory
│   ├── __init__.py              # Package initializer
│   ├── course_manager.py        # Handles course slot definitions and assignment logic
│   ├── elimination.py           # Filters out applicants based on prerequisites, membership, and deposit status
│   ├── group_manager.py         # Manages group creation, merging, and subset removal
│   ├── identification.py        # Identifies applicants and assigns them ID cards
│   ├── main.py                  # Main script to run the overall process (data loading, processing, and group placement)
│   └── schemas.py               # Contains class definitions (Human, Group, etc.) and data structures used throughout the system
└── README.md                    # This readme file
```

### Detailed Overview of Key Files

- **`course_manager.py`**: Defines available training slots and handles slot assignment.
- **`elimination.py`**: Filters out applicants based on conditions such as membership, prerequisites, and deposit status.
- **`group_manager.py`**: Manages the grouping process, including handling friend relationships, merging, and subset group removal.
- **`identification.py`**: Responsible for parsing the input data and creating `Human` objects for each applicant.
- **`schemas.py`**: Contains the core data models (`Human`, `Group`) used for managing applicants and groups.
- **`main.py`**: The entry point for running the full pipeline, from data loading to group placements.

## Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/BounSailing.git
   cd BounSailing
   ```

2. **Set up a virtual environment** (optional but recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # For Linux/Mac
   .venv\Scripts\activate     # For Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Prepare data**: Place your CSV files in the `data/` directory.

## Usage

To run the full process (identifying applicants, eliminating ineligible ones, creating groups, and placing them in slots), execute:

```bash
python src/main.py
```

This will:
1. Load the data from the CSV file.
2. Filter applicants based on membership, prerequisites, and deposit status.
3. Group applicants based on their friend relationships.
4. Perform slot assignment and optimization based on available slots and group sizes.
5. Output placement results into a dataframe.

## Code Logic

The core logic of the system works in multiple stages:

1. **Data Processing and Screening**:
    - Applicants are identified from the CSV data and assigned ID cards (`Human` objects).
    - Screening checks are applied: club membership, prerequisite fulfillment, and deposit verification.

2. **Grouping**:
    - Applicants are grouped based on friend relationships.
    - Single applicants are also treated as individual groups.

3. **Group Validation and Subset Removal**:
    - Groups with inconsistent course selections are filtered.
    - Groups that are subsets of larger groups are removed.
    - If two groups with equal population involve the same person, they are merged to form a larger group.

4. **Slot Assignment**:
    - Group slots are assigned based on the intersection of slots available for all group members.
    - If a group exceeds the slot’s capacity, the latest applicants are removed.
    - The slot assignment process uses an iterative loop to maximize the number of people placed.

5. **Optimization**:
    - Multiple placement combinations are explored, and the configuration that places the maximum number of applicants is chosen.

## Example Scenario

Consider a scenario where applicants A, B, C, and D have formed overlapping groups due to incomplete or inconsistent friend listings. The system will:
1. Remove subset groups ([C, B], [A, D]) and retain only the larger, more complete groups.
2. Merge remaining groups with equal population sizes.
3. Assign the final group to slots based on their availability and course preferences.

For instance, if multiple groups want the same slot but exceed the slot’s capacity, the latest applicants will be reallocated to different slots in the second iteration of placement.

## Potential Improvements

- **Runtime Optimization**: As the number of groups and applicants increases, the slot assignment process may take longer due to the combinational nature of the algorithm. Future enhancements can include optimizing the loop or parallelizing certain operations.
- **Logging**: Adding detailed logs for each step in the group formation and placement process could help trace and debug issues more easily.
- **Unit Testing**: Adding unit tests to validate the behavior of the individual modules and edge cases would improve the reliability of the code.

## License

This project is licensed for Bogazici University Sailing Club

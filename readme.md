project-root/
│
├── data/ # Folder for JSON files and other static data
│ ├── users.json # JSON file with user data
│
├── database/ # Folder for database-related operations
│ ├── **init**.py # Makes this folder a Python package
│ └── db_operations.py # CRUD functions for MongoDB
│
├── models/ # Folder for data models and validation
│ ├── **init**.py # Makes this folder a Python package
│ └── user.py # Pydantic model for user validation
│
├── utils/ # Folder for utility functions
│ ├── **init**.py # Makes this folder a Python package
│ └── helpers.py # Functions like typing effects, clearing the screen, etc.
│
├── main.py # Main application logic
├── seeder.py # For testing connections DB
├── requirements.txt # List of required Python packages
├── .env # Environment variables
├── .gitignore # Files to ignore in version control
└── README.md # Project documentation

#remove later (use for ref)

- Make a user register
- Users can reg and there after login.

# News Agency Project
## 🚀 Project Setup Guide
### 1. Clone the Repository
```
git clone https://github.com/Kostenikov/simple-newspaper-agency.git
cd simple-newspaper-agency
```
### 2. Create and Activate a Virtual Environment
```
python -m venv venv
source venv/bin/activate   # Linux / macOS
venv\Scripts\activate      # Windows
```
### 3. Install Dependencies
```
pip install -r requirements.txt
```
### 4. Configure the .env File
In the root directory, create a .env file based on .env.sample and add your settings:
```
SECRET_KEY="your-secret-key-here"
DEBUG=True
```
### 5. Apply Migrations
```
python manage.py migrate
```
### 6. Load Initial Fixture
```
python manage.py loaddata import_data.json
```

#### Default credentials:
```
Login: admin 
Password: Zaq12wsxcde3
```

### 7. Start the Development Server
```
python manage.py runserver
```

# Set Up Guide
1. **Prerequisites**<br/>
<a href="https://www.python.org/downloads/" target="_blank">Python 3.12.x</a><br/>
<a href="https://nodejs.org/en/download/package-manager" target="_blank">Node.js</a><br/>
<a href="https://dev.mysql.com/downloads/installer/" target="_blank">MySQL</a><br/>
2. **Set Up Frontend**

```bash
cd client
npm install
npm run dev
```

3. **Set up Backend**

```bash
cd server
```

```bash
Windows:
py -3 -m venv .venv
.venv\Scripts\activate

Mac:
python3 -m venv .venv
source .venv/bin/activate
```

```bash
pip install -r requirements.txt
```

Open create_database.py file and update the MySQL configuration with your MySQL password, then:

```bash
python3 create_database.py
python3 main.py
```


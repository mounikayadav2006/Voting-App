# --------------------------- STEP 1: Create and Populate Database ---------------------------
import sqlite3

conn = sqlite3.connect("voting.db")
cursor = conn.cursor()

# Create voters table
cursor.execute("""
CREATE TABLE IF NOT EXISTS voters (
    voter_id TEXT PRIMARY KEY,
    name TEXT,
    password TEXT,
    has_voted INTEGER DEFAULT 0
)
""")

# Create candidates table
cursor.execute("""
CREATE TABLE IF NOT EXISTS candidates (
    candidate_id TEXT PRIMARY KEY,
    name TEXT,
    party TEXT,
    symbol TEXT
)
""")

# Create votes table
cursor.execute("""
CREATE TABLE IF NOT EXISTS votes (
    voter_id TEXT PRIMARY KEY,
    candidate TEXT,
    party TEXT
)
""")

# Add voters
voters = [
    ("VOTER001", "A.Kumar", "pass1"),
    ("VOTER002", "S.Reddy", "pass2"),
    ("VOTER003", "M.Sharma", "pass3"),
    ("VOTER004", "R.Verma", "pass4"),
    ("VOTER005", "K.Meena", "pass5"),
    ("VOTER006", "P.Desai", "pass6"),
    ("VOTER007", "M.Sneha", "pass7"),
    ("VOTER008", "T.Kiran", "pass8"),
    ("VOTER009", "U.Das", "pass9"),
    ("VOTER010", "K.Deepika", "pass10"),
    ("VOTER011", "G.Naidu","pass11"),
    ("VOTER012","H.Anusha","pass12"),
    ("VOTER013","S.Laxman","pass13"),
    ("VOTER014","G,Prasanna","pass14"),
    ("VOTER015","M.Sai","pass15"),
     ("VOTER016","B.Mishra","pass16"),
     ("VOTER017","Y.Agarwal","pass17"),
      ("VOTER018","P.Raj","pass18"),
      ("VOTER019","K.Rahul","pass19"),
      ("VOTER020","N.Narayan","pass20"),
      ("VOTER021","Y.Ram","pass21"),
      ("VOTER022","S.Rakul","pass21"),
      ("VOTER023","K.Deva","pass21"),
      ("VOTER024","T.Suraj","pass21"),
      ("VOTER025","S.Anand","pass21"),
      ("VOTER026","U.Reena","pass21"),
      ("VOTER027","K.Ryan","pass21"),
      ("VOTER029","S.Ian","pass21"),
      ("VOTER030","S.Vamshi","pass21"),
      


]
for v in voters:
    cursor.execute("INSERT OR IGNORE INTO voters (voter_id, name, password) VALUES (?, ?, ?)", v)

# Add candidates
candidates = [
    ("C1", "Devansh", "Future Youth Party","lotus.png"),
    ("C2", "Pravallika", "People's Voice","star.png"),
    ("C3", "Arjun Das", "National Unity Front","tree.png"),
    ("C4", "Meera Joshi", "Progressive Circle","eagle.png"),
    ("C5", "Tanya", "Circle","circle.png"),
     ("C6", " Banerjee", "Justice union","lamp.png"),
      ("C7", "Karan ", "Common People's Alliance","sun.png"),
      ("C8","Priya ","Youth Empowerment Party","clock.png")

]
for c in candidates:
    cursor.execute("INSERT OR IGNORE INTO candidates VALUES (?, ?, ?, ?)", c)

conn.commit()
conn.close()

print("✅ Database 'voting.db' created and populated successfully!")
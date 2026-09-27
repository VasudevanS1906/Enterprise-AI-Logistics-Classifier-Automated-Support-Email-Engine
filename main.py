import sqlite3


conn = sqlite3.connect("parcel_db.sqlite")
cursor = conn.cursor()


cursor.execute("""
CREATE TABLE IF NOT EXISTS parcels (
    parcel_number TEXT PRIMARY KEY,
    customer_name TEXT,
    email_id TEXT,
    status TEXT
)
""")

#dummy data
sample_data = [
    ("80000001", "Priya Sharma", "priya.sharma@example.com", "In Transit"),
    ("80000002", "David Johnson", "david.johnson@example.com", "Delivered"),
    ("80000003", "Anita Rao", "anita.rao@example.com", "Delayed"),
    ("80000004", "Hansie Cronje", "hansie.cronje@example.com", "Delivered"),
    ("80000005", "Allan Donald", "allan.donald@example.com", "Delivered"),
    ("80000006", "Jonty Rhodes", "jonty.rhodes@example.com", "Delivered"),
    ("80000007", "Jacques Kallis", "jacques.kallis@example.com", "Delivered"),
    ("80000008", "Gary Kirsten", "gary.kirsten@example.com", "Parcel Loss"),
    ("80000009", "Shaun Pollock", "shaun.pollock@example.com", "Parcel Loss"),
    ("80000010", "Lance Klusener", "lance.klusener@example.com", "Parcel Loss"),
    ("80000011", "Mark Boucher", "mark.boucher@example.com", "Parcel Loss"),
    ("80000012", "Jack Cheetham", "jack.cheetham@example.com", "Delayed"),
    ("80000013", "Jackie McGlew", "jackie.mcglew@example.com", "Delayed"),
    ("80000014", "Neil Adcock", "neil.adcock@example.com", "Delayed"),
    ("80000015", "Bonnor Middleton", "bonnor.middleton@example.com", "Delayed"),
    ("80000016", "Kapil Dev", "kapil.dev@example.com", "In Transit"),
    ("80000017", "Sunil Gavaskar", "sunil.gavaskar@example.com", "In Transit"),
    ("80000018", "Mohinder Amarnath", "mohinder.amarnath@example.com", "In Transit"),
    ("80000019", "Kris Srikkanth", "kris.srikkanth@example.com", "In Transit"),
    ("80000020", "Syed Kirmani", "syed.kirmani@example.com", "Parcel Returned"),
    ("80000021", "Madan Lal", "madan.lal@example.com", "Parcel Returned"),
    ("80000022", "Roger Binny", "roger.binny@example.com", "Parcel Returned"),
    ("80000023", "Ravi Shastri", "ravishastri@example.com", "Parcel Returned"),
    ("80000024", "Allan Border", "allan.border@example.com", "Refund processed"),
    ("80000025", "Dennis Lillee", "dennis.lillee@example.com", "Refund processed"),
    ("80000026", "Rod Marsh", "rod.marsh@example.com", "Refund processed"),
    ("80000027", "Kim Hughes", "kim.hughes@example.com", "Refund processed"),
]

cursor.executemany("INSERT OR IGNORE INTO parcels VALUES (?, ?, ?, ?)", sample_data)

conn.commit()
conn.close()

print("SQLite database created and populated successfully!")

# Step 1: Import libraries
import pandas as pd
import sqlite3

# Step 2: Load training dataset (Excel file)
train_df = pd.read_excel("/kaggle/input/datasets/vasudevans19/train234/train.xlsx")

# Step 3: Define classification rules with DB validation + status check
def classify_tracking_number(tracking_number, customer_name, email_id, cursor):
    # Case 1: No parcel number
    if pd.isna(tracking_number) or str(tracking_number).strip() == "":
        return "no parcel number"
    
    # Case 2: Must be exactly 8 digits
    if not (str(tracking_number).isdigit() and len(str(tracking_number)) == 8):
        return "incorrect parcel number"
    
    # Case 3: Check if parcel exists in DB
    cursor.execute("SELECT customer_name, email_id, status FROM parcels WHERE parcel_number = ?", (str(tracking_number),))
    result = cursor.fetchone()
    
    if result is None:
        return "invalid parcel number"
    
    db_name, db_email, db_status = result
    if db_name.strip().lower() == customer_name.strip().lower() and db_email.strip().lower() == email_id.strip().lower():
        # Return status if valid
        return db_status
    else:
        return "wrong parcel number different customer"


# personalized replies
reply_templates = {
    "no parcel number": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "Thank you for contacting us. We noticed that your email does not include a parcel number. "
        "Kindly provide the parcel number so we can track your package.\n\n"
        "Sincerely,\nSupport Team"
    ),
    "incorrect parcel number": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "The parcel number you provided appears to be invalid. "
        "Please ensure it is exactly 8 digits (numbers only).\n\n"
        "Sincerely,\nSupport Team"
    ),
    "invalid parcel number": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "This is an invalid parcel number. Kindly check and provide the correct parcel number.\n\n"
        "Sincerely,\nSupport Team"
    ),
    "wrong parcel number different customer": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "The parcel number you provided belongs to another recipient. "
        "Please provide the correct parcel number so we can assist you.\n\n"
        "Sincerely,\nSupport Team"
    ),
    "Delivered": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "Your parcel has been delivered successfully.\n\n"
        "Sincerely,\nSupport Team"
    ),
    "Delayed": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "Your parcel has been delayed as we couldn't meet you today. "
        "We will deliver it tomorrow.\n\n"
        "Sincerely,\nSupport Team"
    ),
    "In Transit": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "Your parcel is in transit. We will deliver it in the next 2-3 business days.\n\n"
        "Sincerely,\nSupport Team"
    ),
    "Parcel Loss": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "As we can see it shows delivered on our end but since you couldn't find your package, "
        "we request you to contact refund@abc.com for refund initiation.\n\n"
        "Sincerely,\nSupport Team"
    ),
    "Refund processed": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "Your refund is being processed. Kindly check your bank account within the next 2-5 business days.\n\n"
        "Sincerely,\nSupport Team"
    ),
    "Parcel Returned": (
        "Dear Mr./Mrs. {customer_name},\n\n"
        "Your parcel is on its way back to the sender as you have refused acceptance. "
        "Once it reaches, the refund process will be initiated.\n\n"
        "Sincerely,\nSupport Team"
    )
}

# test file
test_df = pd.read_excel("/kaggle/input/datasets/vasudevans19/test2341/test.xlsx")

# connect to SQLite database
conn = sqlite3.connect("parcel_db.sqlite")
cursor = conn.cursor()

# classify based on tracking_number + DB validation
test_df["classification_label"] = test_df.apply(
    lambda row: classify_tracking_number(row["tracking_number"], row["customer_name"], row["email_id"], cursor),
    axis=1
)

# fill reply_template column
test_df["reply_template"] = test_df.apply(
    lambda row: reply_templates.get(row["classification_label"], "No template found").replace("{customer_name}", row["customer_name"]),
    axis=1
)


# save those results back to Excel
test_df.to_excel("results2341.xlsx", index=False)




conn.close()

print("Classification and reply templates generated successfully!")

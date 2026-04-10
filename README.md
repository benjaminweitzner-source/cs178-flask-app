# [Ben's Inventory Project]

**CS178: Cloud and Database Systems — Project #1**
**Author:** [Ben]
**GitHub:** [benjaminweitzner-source]

---

## Overview

<!-- Describe your project in 2-4 sentences. What does it do? Who is it for? What problem does it solve? -->
I added an orders system to the ProjectOneStore. This allows me to place, update, and remove orders for new inventory. This is useful for people who don't want to manually go into DynamoDB to add orders, they can just have them stored conveniently through the app.
---

## Technologies Used

- **Flask** — Python web framework
- **AWS EC2** — hosts the running Flask application
- **AWS RDS (MySQL)** — relational database for [I used the inventory and category tables from ProjectOneStore]
- **AWS DynamoDB** — non-relational database for [I created inbound_inv for tracking orders]
- **GitHub Actions** — auto-deploys code from GitHub to EC2 on push

---

## Project Structure

```
ProjectOne/
├── flaskapp.py          # Main Flask application — routes and app logic
├── dbCode.py            # Database helper functions (MySQL connection + queries)
├── creds_sample.py      # Sample credentials file (see Credential Setup below)
├── templates/
│   ├── home.html        # Landing page
│   ├── [add_order].html     # Add descriptions for your other templates
│   ├── [add_user].html     # Add descriptions for your other templates
│   ├── [delete_order].html     # Add descriptions for your other templates
│   ├── [display_users].html     # Add descriptions for your other templates
│   ├── [inbound_inv].html     # Add descriptions for your other templates
│   ├── [inventory_by_category].html     # Add descriptions for your other templates
│   ├── [update_order].html     # Add descriptions for your other templates
├── .gitignore           # Excludes creds.py and other sensitive files
└── README.md
```

---

## How to Run Locally

1. Clone the repository:

   ```bash
   git clone https://github.com/benjaminweitzner-source/cs178-flask-app.git
   cd cs178-flask-app
   ```

2. Install dependencies:

   ```bash
   pip3 install flask pymysql boto3
   ```

3. Set up your credentials (see Credential Setup below)

4. Run the app:

   ```bash
   python3 flaskapp.py
   ```

5. Open your browser and go to `http://127.0.0.1:8080`

---

## How to Access in the Cloud

The app is deployed on an AWS EC2 instance. To view the live version:

```
http://98.82.112.101:8080
```

_(Note: the EC2 instance may not be running after project submission.)_

---

## Credential Setup

This project requires a `creds.py` file that is **not included in this repository** for security reasons.

Create a file called `creds.py` in the project root with the following format (see `creds_sample.py` for reference):

```python
# creds.py — do not commit this file
host = "database-1.ckdku28oynpv.us-east-1.rds.amazonaws.com"
user = "admin"
password = "your-password"
db = "ProjectOneStore"  # change to 'movies' or 'ProjectOneStore' as needed
```

---

## Database Design

### SQL (MySQL on RDS)

<!-- Briefly describe your relational database schema. What tables do you have? What are the key relationships? -->

**Example:**

- `[Inventory]` — stores [inventory items]; primary key is `[categoryID]`
- `[Categories]` — stores [category names related to categoryid]; foreign key links to `[Inventory]`

The JOIN query used in this project: It joins the Inventory to Categories by categoryID, then drops categoryID for compact viewing

### DynamoDB

<!-- Describe your DynamoDB table. What is the partition key? What attributes does each item have? How does it connect to the rest of the app? -->


- **Table name:** `[Inbound_Inv]`
- **Partition key:** `[order_id]`
- **Used for:** [The DynamoDB table has the orders for the rest of the tables. It is partitioned by orderID, which is each individual order. They have the orderID, the product, the quantity, and the supplier.]

---

## CRUD Operations

| Operation | Route      | Description    |
| --------- | ---------- | -------------- |
| Create | `/add-order` | Adds a new inbound order to DynamoDB |
| Read   | `/inbound-orders` |Displays all inbound orders from DynamoDB |
| Update | `/update-order` |Updates the quantity of an existing order in DynamoDB |
| Delete | `/delete-order` | Deletes an inbound order from DynamoDB by order ID |

---

## Challenges and Insights

<!-- What was the hardest part? What did you learn? Any interesting design decisions? -->
The hardest part was the debugging. Apparently I had two instances running at the same time somehow, and the cache was preventing me from accessing my newly updated pages. Wouldn't of figured that out without Claude. A simply design decision was to use stuff from the older labs, it carries over very well.
---

## AI Assistance

<!-- List any AI tools you used (e.g., ChatGPT) and briefly describe what you used them for. Per course policy, AI use is allowed but must be cited in code comments and noted here. -->
Mostly debugging, every page did not work at first, and had to get creative (Claude had to get creative) to find why the code wasn't working, as it was outside of the scope of our class. Also used it to make sure that I didn't forget anything or have typos.
import sqlite3

def create_db_and_insert_data(db_name="mock_cfo.db"):
    # 1. Connect to (or create) the SQLite database
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    # 2. Enable foreign key support
    cursor.execute("PRAGMA foreign_keys = ON;")
    
    # 3. Drop tables if they already exist (optional cleanup)
    #    This ensures we start with a clean slate every time.
    cursor.execute("DROP TABLE IF EXISTS SlackReaction;")
    cursor.execute("DROP TABLE IF EXISTS SlackMessage;")
    cursor.execute("DROP TABLE IF EXISTS SlackChannel;")
    cursor.execute("DROP TABLE IF EXISTS SlackProfile;")
    cursor.execute("DROP TABLE IF EXISTS Note;")
    cursor.execute("DROP TABLE IF EXISTS Application;")
    cursor.execute("DROP TABLE IF EXISTS Member;")
    cursor.execute("DROP TABLE IF EXISTS Company;")
    cursor.execute("DROP TABLE IF EXISTS User;")
    cursor.execute("DROP TABLE IF EXISTS Topic;")
    
    # 4. Create tables
    
    # Company
    cursor.execute("""
    CREATE TABLE Company (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        industry TEXT,
        address TEXT,
        phone_number TEXT,
        founded_at TEXT,
        num_employees INTEGER,
        created_at TEXT
    );
    """)
    
    # User
    cursor.execute("""
    CREATE TABLE User (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT UNIQUE NOT NULL,
        first_name TEXT,
        last_name TEXT,
        password TEXT NOT NULL,
        is_active BOOLEAN DEFAULT TRUE,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    # Member
    cursor.execute("""
    CREATE TABLE Member (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name TEXT,
        last_name TEXT,
        email TEXT UNIQUE NOT NULL,
        phone_number TEXT,
        company_id INTEGER,
        FOREIGN KEY (company_id) REFERENCES Company (id) ON DELETE CASCADE
    );
    """)
    
    # SlackChannel
    cursor.execute("""
    CREATE TABLE SlackChannel (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        created_by INTEGER,
        topic TEXT,
        is_private BOOLEAN DEFAULT FALSE,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES User (id)
    );
    """)
    
    # SlackMessage
    cursor.execute("""
    CREATE TABLE SlackMessage (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        channel_id INTEGER,
        user_id INTEGER,
        text TEXT NOT NULL,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (channel_id) REFERENCES SlackChannel (id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE
    );
    """)
    
    # SlackReaction
    cursor.execute("""
    CREATE TABLE SlackReaction (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        message_id INTEGER,
        emoji TEXT NOT NULL,
        user_id INTEGER,
        FOREIGN KEY (message_id) REFERENCES SlackMessage (id) ON DELETE CASCADE,
        FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE
    );
    """)
    
    # Topic (currently not used much, but we’ll create it anyway)
    cursor.execute("""
    CREATE TABLE Topic (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
    );
    """)
    
    # SlackProfile
    cursor.execute("""
    CREATE TABLE SlackProfile (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        status TEXT,
        avatar_url TEXT,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (user_id) REFERENCES User (id) ON DELETE CASCADE
    );
    """)
    
    # Application
    cursor.execute("""
    CREATE TABLE Application (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL UNIQUE,
        created_by INTEGER,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (created_by) REFERENCES User (id)
    );
    """)
    
    # Note
    cursor.execute("""
    CREATE TABLE Note (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        content TEXT NOT NULL,
        author_id INTEGER,
        timestamp TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (author_id) REFERENCES User (id)
    );
    """)
    
    # 5. Insert mock data
    
    # 5.1. Company
    cursor.executescript("""
    INSERT INTO Company (id, name, industry, address, phone_number, founded_at, num_employees, created_at)
    VALUES
      (1, 'Highbridge Holdings', 'Investment', '123 Queen St, London, UK', '+44 20 1234 5678', '1985-06-12', 5000, '2019-01-15 10:00:00'),
      (2, 'Finex Solutions', 'Financial Services', '77 Baker St, London, UK', '+44 20 2222 3333', '1995-03-10', 2000, '2019-01-16 11:00:00'),
      (3, 'Alpha Finance', 'Banking', '10 King St, Manchester, UK', '+44 161 123 4567', '1970-01-01', 8000, '2019-01-17 09:30:00'),
      (4, 'Britannia Investments', 'Investment', '200 Duke Rd, Bristol, UK', '+44 117 999 8888', '2001-11-20', 1000, '2019-01-17 10:00:00'),
      (5, 'Summit Capital', 'Financial Services', '32 Peak Ave, Birmingham, UK', '+44 121 456 7890', '1990-05-12', 1200, '2019-01-18 08:45:00'),
      (6, 'NorthStar Banking', 'Banking', '55 North Rd, Leeds, UK', '+44 113 220 3141', '1988-09-29', 7000, '2019-01-18 09:15:00'),
      (7, 'Lionheart Consulting', 'Consulting', '6 Cathedral St, London, UK', '+44 20 5555 6666', '2005-02-23', 300, '2019-01-19 10:00:00'),
      (8, 'Crown Enterprises', 'Conglomerate', '99 Royal Way, Edinburgh, UK', '+44 131 444 7777', '1975-07-14', 10000, '2019-01-19 14:20:00');
    """)
    
    # 5.2. User
    cursor.executescript("""
    INSERT INTO User (id, username, email, first_name, last_name, password, is_active, created_at)
    VALUES
      (1, 'cfo_hbridge', 'charles@highbridge.com', 'Charles', 'Foster', 'hashedpw123', 1, '2019-02-01 09:00:00'),
      (2, 'cfo_finex', 'alice@finex.co.uk', 'Alice', 'Harper', 'hashedpw234', 1, '2019-02-02 09:30:00'),
      (3, 'cfo_alpha1', 'david@alphafinance.co.uk', 'David', 'Edwards', 'hashedpw345', 1, '2019-02-03 10:00:00'),
      (4, 'cfo_alpha2', 'claudia@alphafinance.co.uk', 'Claudia', 'Green', 'hashedpw456', 1, '2019-02-04 08:00:00'),
      (5, 'cfo_britannia1', 'george@britannia.com', 'George', 'Williams', 'hashedpw567', 1, '2019-02-05 13:00:00'),
      (6, 'cfo_britannia2', 'elizabeth@britannia.com', 'Elizabeth', 'Adams', 'hashedpw678', 1, '2019-02-06 15:20:00'),
      (7, 'cfo_summit', 'helen@summitcapital.co.uk', 'Helen', 'Moore', 'hashedpw789', 1, '2019-02-07 16:45:00'),
      (8, 'cfo_northstar', 'peter@northstarbank.co.uk', 'Peter', 'Owens', 'hashedpw890', 1, '2019-02-08 11:10:00'),
      (9, 'cfo_lionheart', 'fiona@lionheartconsulting.co.uk', 'Fiona', 'Baker', 'hashedpw901', 1, '2019-02-09 17:55:00'),
      (10, 'cfo_crown', 'richard@crownenterprises.co.uk', 'Richard', 'Clark', 'hashedpw012', 1, '2019-02-10 08:20:00');
    """)
    
    # 5.3. Member (aligning CFO users to companies)
    cursor.executescript("""
    INSERT INTO Member (id, first_name, last_name, email, phone_number, company_id)
    VALUES
      (1, 'Charles', 'Foster', 'charles@highbridge.com', '+44 20 1234 5678', 1),
      (2, 'Alice', 'Harper', 'alice@finex.co.uk', '+44 20 2222 3333', 2),
      (3, 'David', 'Edwards', 'david@alphafinance.co.uk', '+44 161 123 4567', 3),
      (4, 'Claudia', 'Green', 'claudia@alphafinance.co.uk', '+44 161 123 4568', 3),
      (5, 'George', 'Williams', 'george@britannia.com', '+44 117 999 1111', 4),
      (6, 'Elizabeth', 'Adams', 'elizabeth@britannia.com', '+44 117 999 2222', 4),
      (7, 'Helen', 'Moore', 'helen@summitcapital.co.uk', '+44 121 456 7890', 5),
      (8, 'Peter', 'Owens', 'peter@northstarbank.co.uk', '+44 113 220 3141', 6),
      (9, 'Fiona', 'Baker', 'fiona@lionheartconsulting.co.uk', '+44 20 5555 6666', 7),
      (10, 'Richard', 'Clark', 'richard@crownenterprises.co.uk', '+44 131 444 7777', 8);
    """)
    
    # 5.4. SlackChannel
    cursor.executescript("""
    INSERT INTO SlackChannel (id, name, created_by, topic, is_private, created_at)
    VALUES
      (1, '#cfo-lounge', 1, 'General lounge for CFO chats', 0, '2019-03-01 09:00:00'),
      (2, '#finance-tech', 2, 'Discussions about financial software, tools, etc.', 0, '2019-03-02 10:00:00'),
      (3, '#networking', 3, 'Meetups, events, professional networking', 0, '2019-03-03 11:00:00');
    """)
    
    # 5.5. SlackMessage (50 total)
    cursor.executescript("""
    INSERT INTO SlackMessage (id, channel_id, user_id, text, timestamp)
    VALUES
      -- #cfo-lounge
      (1, 1, 1, 'Hello everyone, Charles here! Glad to have a place for CFO discussions.', '2019-03-01 10:10:00'),
      (2, 1, 2, 'Hi Charles! Alice from Finex Solutions checking in.', '2019-03-01 10:15:00'),
      (3, 1, 3, 'David from Alpha Finance. Good to meet you all.', '2019-03-01 10:20:00'),
      (4, 1, 1, 'Has anyone used SAP for consolidation? We are considering it.', '2019-03-01 11:00:00'),
      (5, 1, 5, 'George here. Yes, we implemented SAP last year. Mixed results so far.', '2019-03-01 11:05:00'),
      (6, 1, 2, 'We use Workday for HR and financials; simpler than SAP in my opinion.', '2019-03-01 11:30:00'),
      (7, 1, 8, 'Peter from NorthStar. We are an Oracle shop, but always curious about alternatives.', '2019-03-01 12:15:00'),
      (8, 1, 9, 'Fiona here at Lionheart Consulting. We help clients evaluate these solutions if you need insights.', '2019-03-01 12:45:00'),
      (9, 1, 10, 'Richard from Crown. We run QuickBooks for smaller subsidiaries, SAP for the main HQ.', '2019-03-01 13:00:00'),
      (10, 1, 6, 'Elizabeth from Britannia. Good to meet all of you! We also have SAP— might share experiences soon.', '2019-03-01 13:10:00'),
      (11, 1, 4, 'Claudia from Alpha. It’s nice to see multiple SAP users. Let’s compare notes sometime.', '2019-03-02 09:00:00'),

      -- #finance-tech
      (12, 2, 2, 'Kicking off a new thread: Anyone tried Xero for mid-sized entities?', '2019-04-10 14:00:00'),
      (13, 2, 7, 'Helen from Summit. Yes, we love Xero for real-time bank feeds and multi-currency support.', '2019-04-10 14:05:00'),
      (14, 2, 8, 'I second that. Xero is user-friendly and cost-effective.', '2019-04-10 14:10:00'),
      (15, 2, 1, 'Charles: We might test Xero for a smaller division. Any big pitfalls to watch out for?', '2019-04-10 14:15:00'),
      (16, 2, 7, 'Just watch out for advanced consolidation features. Not as robust as SAP/Oracle.', '2019-04-10 14:20:00'),
      (17, 2, 3, 'We’ve done a pilot with NetSuite. Higher cost, but good for complex structures.', '2019-04-10 14:25:00'),
      (18, 2, 6, 'Elizabeth: We’re evaluating NetSuite vs Workday. Hard to decide, so any feedback is welcomed.', '2019-04-10 15:00:00'),
      (19, 2, 4, 'Claudia: NetSuite is strong in multi-entity but can be pricy. We chose SAP over it though.', '2019-04-10 15:10:00'),
      (20, 2, 5, 'George: We have an internal doc comparing these solutions. Happy to share if needed.', '2019-04-10 15:15:00'),
      (21, 2, 9, 'Yes please, that doc could be super helpful for new CFOs here.', '2019-04-10 15:25:00'),
      (22, 2, 10, 'Richard: I’ll DM you our notes on Oracle Cloud vs NetSuite as well.', '2019-04-10 15:30:00'),
      (23, 2, 2, 'Awesome collaboration, folks.', '2019-04-10 16:00:00'),
      (24, 2, 1, 'Charles: Revisiting Workday. Are you all satisfied with its budgeting module?', '2019-07-22 09:30:00'),
      (25, 2, 2, 'Alice: We’re mostly happy, though custom reporting can get tricky.', '2019-07-22 09:35:00'),
      (26, 2, 5, 'George: The real benefit is tight integration with HR. If that’s valuable, Workday is good.', '2019-07-22 09:40:00'),
      (27, 2, 8, 'Peter: We are purely Oracle, but always curious to learn about Workday’s expansions.', '2019-07-22 09:50:00'),
      (28, 2, 6, 'Elizabeth: We plan a pilot next quarter. Will share experience then!', '2019-07-22 10:00:00'),

      -- #networking
      (29, 3, 9, 'Any CFO meetups in London next month? Always looking to connect.', '2020-01-10 08:00:00'),
      (30, 3, 7, 'Helen: We have a small CFO roundtable on Feb 5th in Birmingham, all invited!', '2020-01-10 08:05:00'),
      (31, 3, 2, 'Alice: Count me in! Could we get details please?', '2020-01-10 08:10:00'),
      (32, 3, 7, 'Helen: Sure thing, will DM you. It’s a half-day event followed by networking.', '2020-01-10 08:15:00'),
      (33, 3, 3, 'David: We also have a quick meetup in Manchester on Feb 20th. Let me know if interested.', '2020-01-10 08:20:00'),
      (34, 3, 1, 'Charles: Great! I’ll drive up for that. Thanks for sharing.', '2020-01-10 08:30:00'),
      (35, 3, 4, 'Claudia: We’re hosting a CFO charity golf event in April 2021. Let me know if you want in.', '2021-01-15 09:00:00'),
      (36, 3, 10, 'Richard: That sounds fun. I’d love more details.', '2021-01-15 09:10:00'),
      (37, 3, 5, 'George: Let’s all go! CFOs + golf = deals on the course.', '2021-01-15 09:15:00'),
      (38, 3, 8, 'Peter: Sign me up too. We’ll bring a few of our VPs.', '2021-01-15 09:20:00'),

      -- More recent #cfo-lounge
      (39, 1, 2, 'Alice: Quick question: best practice for IFRS 16 compliance in SAP? Any tips appreciated.', '2022-05-06 14:00:00'),
      (40, 1, 9, 'Fiona: We consult on IFRS 16. Might have a quick reference doc. Let me check.', '2022-05-06 14:10:00'),
      (41, 1, 2, 'Alice: Thanks, Fiona. Perfect timing.', '2022-05-06 14:15:00'),
      (42, 1, 4, 'Claudia: Our compliance took 2 months to fully implement. Key is correct lease data setup.', '2022-05-06 14:20:00'),
      (43, 1, 3, 'David: Same experience. Let me know if you want to see our checklist.', '2022-05-06 14:25:00'),

      -- More #finance-tech in 2023
      (44, 2, 1, 'Charles: Considering a switch from QuickBooks to NetSuite for a new acquisition. Thoughts?', '2023-02-01 10:00:00'),
      (45, 2, 10, 'Richard: We did that. NetSuite handles growth better, but the cost jump is big.', '2023-02-01 10:15:00'),
      (46, 2, 7, 'Helen: I prefer Xero for small acquisitions, but if they’re big, NetSuite might be worth it.', '2023-02-01 10:30:00'),
      (47, 2, 3, 'David: We have a migration guide if needed, let me know.', '2023-02-01 10:40:00'),
      (48, 2, 6, 'Elizabeth: We’ll be watching closely. Keep us posted on your transition.', '2023-02-01 10:45:00'),
      (49, 2, 8, 'Peter: Maybe do a pilot first to confirm the ROI.', '2023-02-01 10:50:00'),
      (50, 2, 1, 'Charles: Great tips everyone, I appreciate it!', '2023-02-01 10:55:00');
    """)
    
    # 5.6. SlackReaction (some random emoji reactions)
    cursor.executescript("""
    INSERT INTO SlackReaction (id, message_id, emoji, user_id)
    VALUES
      (1, 1, ':wave:', 2),
      (2, 4, ':thumbsup:', 2),
      (3, 4, ':thumbsup:', 5),
      (4, 5, ':thinking:', 1),
      (5, 9, ':handshake:', 2),
      (6, 12, ':eyes:', 3),
      (7, 13, ':thumbsup:', 1),
      (8, 20, ':file_folder:', 9),
      (9, 21, ':thumbsup:', 10),
      (10, 29, ':wave:', 7),
      (11, 35, ':golf:', 6),
      (12, 37, ':thumbsup:', 8),
      (13, 39, ':question:', 3),
      (14, 45, ':thumbsup:', 1),
      (15, 49, ':rocket:', 6);
    """)
    
    # 5.7. Application
    cursor.executescript("""
    INSERT INTO Application (id, name, created_by, created_at)
    VALUES
      (1, 'SAP', 1, '2019-04-01 08:00:00'),
      (2, 'Workday', 2, '2019-04-01 08:05:00'),
      (3, 'Oracle NetSuite', 3, '2019-04-01 08:10:00'),
      (4, 'Xero', 4, '2019-04-01 08:20:00'),
      (5, 'QuickBooks', 5, '2019-04-01 08:30:00');
    """)
    
    # 5.8. Note
    cursor.executescript("""
    INSERT INTO Note (id, content, author_id, timestamp)
    VALUES
      (1, 'SAP performance analysis: we need more training for staff, but ROI is promising.', 1, '2019-08-15 10:00:00'),
      (2, 'Workday has simplified payroll processes across multiple branches.', 2, '2019-09-20 11:15:00'),
      (3, 'NetSuite pilot results: possible cost overrun if not carefully managed.', 3, '2020-02-10 14:30:00'),
      (4, 'Xero case study: good for SMEs, lacks advanced consolidation.', 4, '2020-05-01 09:45:00'),
      (5, 'QuickBooks is fine for small acquisitions but watch for limited multi-entity features.', 5, '2021-01-05 13:00:00'),
      (6, 'SAP IFRS 16 compliance required thorough data cleansing, took two months for us.', 4, '2022-06-10 15:00:00'),
      (7, 'Workday budgeting module feedback: custom reporting can be time-consuming.', 2, '2022-10-05 10:15:00'),
      (8, 'NetSuite vs Oracle Cloud: summary doc with pros/cons. Available on request.', 3, '2023-01-20 16:20:00');
    """)
    
    # Commit changes and close
    conn.commit()
    conn.close()
    print(f"Database '{db_name}' created and mock data inserted successfully.")

if __name__ == "__main__":
    create_db_and_insert_data("mock_cfo.db")

CREATE_TABLE = """
CREATE TABLE user (
        user_uuid VARCHAR(36) NOT NULL,
        created_at DATETIME DEFAULT (CURRENT_TIMESTAMP), 
        button VARCHAR(100) NOT NULL,
        model VARCHAR(100) NOT NULL, 
        status VARCHAR(100) DEFAULT 'Pending' NOT NULL, 
        processed_path VARCHAR(100) DEFAULT 'NaN' NOT NULL, 
        expiry INT NULL,
        PRIMARY KEY (user_uuid)
);
"""

DBSCHEMA = {
    "user_uuid" : 0,
    "created_at" : 1,
    "button" : 2,
    "model" : 3,
    "status" : 4,
    "processed_path" : 5,
    "expiry" : 6
}

INSERT_QUERY = """
            INSERT INTO user(user_uuid,created_at,button,model) VALUES (?,?,?,?) 
            """

def get_user_query(id):
    return f'SELECT * FROM user WHERE user_uuid="{id}"'
import psycopg2
import model
import get_image
import time

class IllegalRequestException(Exception):
    """General exception for illegal requests to this module."""
    pass

class db_interface:
    """Methods that access the database."""

    AFTER = 1
    BEFORE = 2

    def __init__(self, dsn):
        self.im = get_image()
        restarts = 3
        connected = False
        while not connected and restarts > 0:
            try:
                self.conn = psycopg2.connect(dsn)
                print "Established database connection!!"
                connected = True
            except Exception as e:
                print "Could not connect to postgres using dsn = '" + dsn + "\n'(" + e.message + ")"
                if restarts == 0:
                    raise e
                restarts -= 1
                print "There are " + str(restarts) + " attempts remaining."
                time.sleep(2)
        self.im = get_image(self.get_rules(), self.get_campaigns())

    def get_rules(self):
        """Return a list of rules in priority order."""
        sql = """
            SELECT rule.id, rule.field, rule.target, rule.campaign_id, rule_priority.priority
            FROM rule
            JOIN rule_priority ON rule.id = rule_priority.rule_id
            ORDER BY rule_priority.priority ASC
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        if result is None:
            return []
        return model.make_rules(result)

    def rule_change_priority(self, rule_id, new_priority):
        """Change priority for a rule."""
        sql = """
            UPDATE rule_priority 
            SET priority = %s
            WHERE rule_id = %s
        """
        cur = self.conn.cursor()
        
        cur.execute(sql, [new_priority, rule_id])

    def get_campaigns(self):
        """Return a mapping from campaign to the image ot be displayed."""
        sql = """
            SELECT * from campaign_to_image
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        result = cur.fetchall()
        if result is None:
            return {}
        return model.make_campaigns(result)

    def get_user(self, ip_address):
        """Get a user from its IP address."""
        sql = """
            SELECT ip_address, geo, industry, company_size from site_user 
            WHERE ip_address = %s
        """
        cur = self.conn.cursor()
        cur.execute(sql, [ip_address])
        result = cur.fetchone()
        if result is None:
            return None
        return model.make_user(result)

    def add_user(self, user_info):
        """Add a user to the user table."""
        sql = """
            INSERT INTO site_user VALUES (%s, %s, %s, %s, %s)
        """
        cur = self.conn.cursor()
        try:
            cur.execute(sql, [user_info['User ID'], user_info['IP'], user_info['Geo'], user_info['Industry'], user_info['Company Size']])
        except Exception as e:
            cur.execute('ROLLBACK')
            self.conn.commit()
            raise e

    def add_users(self, source):
        """Add users from an iterator."""
        cur = self.conn.cursor()
        cur.execute('BEGIN')
        items = 0
        for item in source:
            self.add_user(item)
            items += 1
        self.conn.commit()
        print "Added " + str(items) + " users"
        return items

    def rules_rewrite_priorities(self, rules, rule_id, index, direction):
        """Rewrite the priorities list when necessary."""
        i = 0
        cur = self.conn.cursor()
        cur.execute('BEGIN')
        priority = 100
        while i < len(rules):
            if rules[i].id != rule_id:
                if i == index: # here's the place we're putting it before/after
                    if direction == self.BEFORE:
                        self.rule_change_priority(rule_id, priority)
                        priority += 100
                    self.rule_change_priority(rules[i].id, priority)
                    priority += 100
                    if direction == self.AFTER:
                        self.rule_change_priority(rule_id, priority)
                        priority += 100
                else:
                    self.rule_change_priority(rules[i].id, priority)
                    priority += 100

            i += 1
        self.conn.commit()
        self.im.update_rules(rules)

if __name__ == '__main__':
    print 'nothing to do yet'


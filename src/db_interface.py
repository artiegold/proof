import psycopg2
import model
import get_image_mod

class db_interface:
    """Functions that access the database."""

    AFTER = 1
    BEFORE = 2

    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)

    def get_rules(self):
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
        sql = """
            UPDATE rule_priority 
            SET priority = %s
            WHERE rule_id = %s
        """
        cur = self.conn.cursor()
        
        cur.execute(sql, [new_priority, rule_id])

    def get_campaigns(self):
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
        cur = self.conn.cursor()
        cur.execute('BEGIN')
        items = 0
        for item in source:
            self.add_user(item)
            items += 1
        self.conn.commit()
        return items

    def rules_rewrite_priorities(self, rules, rule_id, index, direction):
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

    def move_rule_after(self, rule_id, target):
        def find_place(target, rules):
            i = 0
            while i < len(rules):
                if rules[i].id == target:
                    if i == len(rules) - 1:
                        return rules[i], None, i
                    return rules[i], rules[i + 1], i
                i += 1
            return None, None, -1

        rules = self.get_rules()
        this, next, index = find_place(target, rules)
        if this is None:
            return False # the target was not found
        if next is None:
            new_priority = this.priority + 100
        elif next.id == rule_id:
            return True # it is already there

        if next.priority - this.priority > 1:
            new_priority = (this.priority + next.priority) // 2
        else:
            self.rules_rewrite_priorities(rules, rule_id, index, self.AFTER)

        self.rule_change_priority(rule_id, new_priority)
        get_image_mod.update_rules(self.get_rules())
        return True 

    def move_rule_before(self, rule_id, target):
        def find_place(target, rules):
            i = 0
            prev = None
            while i < len(rules):
                if rules[i].id == target:
                    return prev, rules[i], i
                i += 1
                prev = rules[i]
            return None, None, -1

        rules = self.get_rules()
        prev, this, index = find_place(target, rules)
       
        if this is None:
            return False # the target was not found
        if prev is None:
            new_priority = this.priority // 2

        elif prev.id == rule_id:
            return True # it is already there

        if this.priority - prev.priority > 1:
            new_priority = (this.priority + next.priority) // 2
        else:
            self.rules_rewrite_priorities(rules, rule_id, index, self.BEFORE)

        self.rule_change_priority(rule_id, new_priority)
        get_image_mod.update_rules(self.get_rules())
        return True 


if __name__ == '__main__':
    print 'nothing to do yet'


import psycopg2
import model

class db_interface:
    """Functions that access the database."""

    def __init__(self, dsn):
        self.conn = psycopg2.connect(dsn)

    def get_rules(self):
        sql = """
            SELECT rule.id, rule.field, rule.target, rule.campaign_id
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

if __name__ == '__main__':
    print 'nothing to do yet'


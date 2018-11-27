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
        return model.make_rules(cur.fetchAll())

    def get_campaigns(self):
        sql = """
            SELECT * from campaign_to_image
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        return model.make_campaigns(cur.fetchAll())

    def get_user(self, ip_address):
        sql = """
            SELECT ip_address, geo, industry, company_size from user 
            WHERE ip_address = %s
            """
        cur = self.conn.cursor()
        cur.execute(sql, [ip_address])
        return model.make_user(cur.fetchone())

        
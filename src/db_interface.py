import psycopg2
import collections

User = collections.namedtuple("User", "ip_address geo industry company_size")

def make_user(the_tuple):
    def user(ip_address, geo, industry, company_size):
        return User(ip_address=ip_address, geo=geo, industry=industry, company_size=company_size)

    return apply(user, the_tuple)

Rule = collections.namedtuple("Rule", "id field target campaign_id")

def make_rules(tuples):
    def rule(id, field, target, campaign_id):
        return Rule(id=id, field=field, target=target, campaign_id=campaign_id)

    return [apply(rule, the_tuple) for the_tuple in tuples]

Campaign = collections.namedtuple("Campaign", "campaign_id name image_url")
def make_campaigns(items):
    def campaign(campaign_id, name, image_url):
        return Campaign(campaign_id=campaign_id, name=name, image_url=image_url)
    campaigns = [apply(campaign, item) for item in items]
    return dict([(campaign.campaign_id, campaign) for campaign in campaigns])
    


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
        return make_rules(cur.fetchAll())

    def get_campaigns(self):
        sql = """
            SELECT * from campaign_to_image
        """
        cur = self.conn.cursor()
        cur.execute(sql)
        return make_campaigns(cur.fetchAll())

    def get_user(self, ip_address):
        sql = """
            SELECT ip_address, geo, industry, company_size from user 
            WHERE ip_address = %s
            """
        cur = self.conn.cursor()
        cur.execute(sql, [ip_address])
        return make_user(cur.fetchone())

        
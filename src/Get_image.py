import db_interface

class Get_image:
    def __init__(self, dsn):
        self.interface = db_interface.db_interface(dsn)
        self.rules = self.interface.get_rules()
        self.campaigns = self.interface.get_campaigns()

    def update_rules(self):
        self.rules = self.interface.get_rules()

    def update_campaigns(self):
        self.campaigns = self.interface.get_campaigns()

    def get_campaign_id(self, ip_address):
        user = self.interface.get_user(ip_address)
        for rule in self.rules:
            if rule.field == '' or rule.field == 'geo' and user.geo == rule.target or rule.field == 'industry' and user.industry == rule.target or rule.field == 'company_size' and user.company_size == rule.target:
                return rule.campaign_id

    def get_image_url(self, ip_address):
        index = self.get_campaign_id(ip_address)
        return self.campaigns[index].image_url
            
            


    
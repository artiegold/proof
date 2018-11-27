import model

class get_image:
    def __init__(self, rules, campaigns):
        self.rules = rules
        self.campaigns = campaigns

    def update_rules(self, rules):
        self.rules = rules

    def update_campaigns(self, campaigns):
        self.campaigns = campaigns

    def get_campaign_id(self, user):
        for rule in self.rules:
            if rule.field == '' \
            or rule.field == 'geo' and user.geo == rule.target \
            or rule.field == 'industry' and user.industry == rule.target \
            or rule.field == 'company_size' and user.company_size == rule.target:
                return rule.campaign_id

    def get_image_basename(self, user):
        index = self.get_campaign_id(user)
        return self.campaigns[index].image_basename
            
            


    
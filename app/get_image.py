import model

class NoDefaultRuleException(Exception): 
    """Raised when no default rule is specified."""
    pass

class NotInitializedException(Exception):
    """Raised when using module before initialization"""

class get_image: 
    def __init__(self, rules, campaigns):
        self.rules = rules
        self.campaigns = campaigns
        self.default_rule = self.get_default_rule(rules)

    def update_rules(self, rules):
        self.rules = rules

    def update_campaigns(self, campaigns):
        self.campaigns = campaigns

    def update_default_rule(self, rule):
        self.default_rule = rule
    
    @staticmethod
    def get_default_rule(rules):
        """Get the default rule from the rules. Raise NoDefaultRuleException if none exists."""
        for rule in rules:
            if rule.field == '':
                return rule
        raise NoDefaultRuleException

    def get_campaign_id(self, user):
        """Examine the rules to determine to map user to campaign."""
        if user is None:
            return self.default_rule.campaign_id

        for rule in self.rules:
            if rule.field == '' \
            or rule.field == 'geo' and user.geo == rule.target \
            or rule.field == 'industry' and user.industry == rule.target \
            or rule.field == 'company_size' and user.company_size == rule.target:
                return rule.campaign_id

    def get_image_basename(self, user):
        """Return the image basename by indexing from the campaigns."""
        index = self.get_campaign_id(user)
        return self.campaigns[index].image_basename
                
            


    
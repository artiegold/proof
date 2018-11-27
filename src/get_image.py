import model

class NoDefaultRuleException(Exception): 
    """Raised when no default rule is specified."""
    pass

class get_image:
    """Get the right image for the user."""
    def __init__(self, rules, campaigns):
        """Manage rules and campaigns, provide the right image basename."""
        self.default_rule = get_image.get_default_rule(rules)
        self.rules = rules
        self.campaigns = campaigns
    
    @staticmethod
    def get_default_rule(rules):
        """Get the default rule from the rules. Raise NoDefaultRuleException if none exists."""
        for rule in rules:
            if rule.field == '':
                return rule
        raise NoDefaultRuleException

    def update_rules(self, rules):
        """Update the rules if they change."""
        self.rules = rules

    def update_campaigns(self, campaigns):
        """Update the campaigns if they change."""
        self.campaigns = campaigns

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
            
            


    
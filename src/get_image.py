import model

class NoDefaultRuleException(Exception): 
    """Raised when no default rule is specified."""
    pass

class NotInitializedException(Exception):
    """Raised when using module before initialization"""

_rules = []
_campaigns = {}
_default_rule = None
_initialized = False

def _update_rules(rules):
    global _rules
    _rules = rules

def _update_campaigns(campaigns):
    global _campaigns
    _campaigns = campaigns

def _update_default_rule(rule):
    global _default_rule
    _default_rule = rule

def initialize(rules, campaigns):
    """Manage rules and campaigns, provide the right image basename."""
    _update_default_rule(_get_default_rule(rules))
    _update_rules(rules)
    _update_campaigns(campaigns)
    
def _get_default_rule(rules):
    """Get the default rule from the rules. Raise NoDefaultRuleException if none exists."""
    for rule in rules:
        if rule.field == '':
            return rule
    raise NoDefaultRuleException

def update_rules(rules):
    """Update the rules if they change."""
    _update_rules(rules)

def update_campaigns(campaigns):
    """Update the campaigns if they change."""
    _update_campaigns(campaigns)

def get_campaign_id(user):
    """Examine the rules to determine to map user to campaign."""
    if user is None:
        return _default_rule.campaign_id

    for rule in _rules:
        if rule.field == '' \
        or rule.field == 'geo' and user.geo == rule.target \
        or rule.field == 'industry' and user.industry == rule.target \
        or rule.field == 'company_size' and user.company_size == rule.target:
            return rule.campaign_id

def get_image_basename(user):
    """Return the image basename by indexing from the campaigns."""
    index = get_campaign_id(user)
    return _campaigns[index].image_basename
            
            


    
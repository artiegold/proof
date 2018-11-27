import collections

User = collections.namedtuple('User', 'ip_address geo industry company_size')

def user(ip_address, geo, industry, company_size):
        return User(ip_address=ip_address, geo=geo, industry=industry, company_size=company_size)

def make_user(the_tuple):
    return apply(user, the_tuple)

Rule = collections.namedtuple('Rule', 'id field target campaign_id')

def rule(id, field, target, campaign_id):
    return Rule(id=id, field=field, target=target, campaign_id=campaign_id)

def make_rules(items):
    return [apply(rule, item) for item in items]

Campaign = collections.namedtuple('Campaign', 'campaign_id name image_basename')

def _campaign(campaign_id, name, image_basename):
    return Campaign(campaign_id=campaign_id, name=name, image_basename=image_basename)

def make_campaigns(items):
    campaigns = [apply(_campaign, item) for item in items]
    return dict([(campaign.campaign_id, campaign) for campaign in campaigns])
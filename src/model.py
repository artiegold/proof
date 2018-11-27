import collections

User = collections.namedtuple('User', 'ip_address geo industry company_size')

def user(ip_address, geo, industry, company_size):
        return User(ip_address=ip_address.strip(), geo=geo.strip(), industry=industry.strip(), company_size=company_size.strip())

def make_user(item):
    return apply(user, item)

Rule = collections.namedtuple('Rule', 'id field target campaign_id')

def rule(id, field, target, campaign_id):
    return Rule(id=id.strip(), field=field.strip(), target=target.strip(), campaign_id=campaign_id)

def make_rules(items):
    return [apply(rule, item) for item in items]

Campaign = collections.namedtuple('Campaign', 'campaign_id name image_basename')

def _campaign(campaign_id, name, image_basename):
    return Campaign(campaign_id=campaign_id, name=name.strip(), image_basename=image_basename.strip())

def make_campaigns(items):
    campaigns = [apply(_campaign, item) for item in items]
    return dict([(campaign.campaign_id, campaign) for campaign in campaigns])
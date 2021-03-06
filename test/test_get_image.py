import unittest
import app
from app import get_image
from app import model 

class test_get_image(unittest.TestCase):
    def setUp(self):
        rules_data = [
            ('GEO_ATX', 'geo', 'Austin', 1, 100),
            ('GEO_SF', 'geo', 'San Francisco', 2, 200),
            ('IND_SOFT', 'industry', 'Software', 3, 300),
            ('IND_SPORTS', 'industry', 'Sports', 4, 400),
            ('SIZE_0-50', 'company_size', '0 - 50', 5, 500),
            ('SIZE_100-200', 'company_size', '100 - 200', 6, 600),
            ('UNKNOWN', '', '', 7, 700)
        ]
        rules = model.make_rules(rules_data)
        campaigns_data = [
            (1, 'Users from Austin', 'Austin.jpg'),
            (2, 'Users from San Francisco', 'SanFrancisco.jpg'),
            (3, 'Users in Software', 'Software.jpg'),
            (4, 'Users in Sports', 'Sports.jpg'),
            (5, 'Users in Company Size 0 - 50', 'proof.jpg'),
            (6, 'Users in 100 - 200', 'smb.jpg'),
            (7, 'Unknown Users', 'shrug.jpg') 
        ]
        campaigns = model.make_campaigns(campaigns_data)
        self.get_image = app.get_image.get_image(rules, campaigns)

        self.user_austin_sports = model.user('192.168.2.2', 'Austin', 'Sports', '1 - 10')
        self.user_austin_software = model.user('192.168.3.3', 'Austin', 'Software', '100 - 200')
        self.user_newyork_software = model.user('192.168.4.4', 'New York', 'Software', '0 - 50')
        self.user_newyork_busking = model.user('192.168.5.5', 'New York', 'Busking', '100 - 200')
        self.user_sf_smb = model.user('192.168.6.6', 'San Francisco', 'Medicine', '201 - 500')
        self.user_la_proof = model.user('192.168.7.7', 'Los Angeles', 'Finance', '0 - 50')
        self.user_oshkosh = model.user('192.168.8.8', 'Oshkosh', "None", '5001 - 20000')

    def test_get_campaign_id(self):
        self.assertEquals(1, self.get_image.get_campaign_id(self.user_austin_sports))
        self.assertEquals(1, self.get_image.get_campaign_id(self.user_austin_software))
        self.assertEquals(3, self.get_image.get_campaign_id(self.user_newyork_software))
        self.assertEquals(6, self.get_image.get_campaign_id(self.user_newyork_busking))
        self.assertEquals(2, self.get_image.get_campaign_id(self.user_sf_smb))
        self.assertEquals(5, self.get_image.get_campaign_id(self.user_la_proof))

    def test_get_image(self):
        self.assertEquals('Austin.jpg', self.get_image.get_image_basename(self.user_austin_sports))
        self.assertEquals('SanFrancisco.jpg', self.get_image.get_image_basename(self.user_sf_smb))
        self.assertEquals('shrug.jpg', self.get_image.get_image_basename(self.user_oshkosh))
        self.assertEquals('proof.jpg', self.get_image.get_image_basename(self.user_la_proof))

if __name__ == '__main__':
    unittest.main()


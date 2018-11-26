-- Start from scratch so drop tables (if they exist).
drop table if exists site_user;
drop table if exists rule;
drop table if exists rule_priority;
drop table if exists campaign_to_image;

-- Drop types as well.
drop type if exists t_industry_name;
drop type if exists t_target_key;

-- Create the types

-- the industry names (for consistency)
create type t_industry_name as enum (
    'Software',
    'Sports',
    'Marketing',
    'Oil and Gas',
    'Tourism'
);

-- these are the relevant column names
create type t_target_key as enum (
    'geo',
    'industry',
    'company_size',
    ''
);

-- the users on the system
--     ip_address is most used key
create table site_user (
    id int primary key,
    ip_address varchar(63) not null, 
    geo varchar(63) not null,
    industry t_industry_name not null,
    company_size varchar(63) not null
);

create index on site_user (ip_address);

-- rules used to inspect the user to find what campaign they're part of
create table rule (
    id char(20) primary key,
    field t_target_key,
    target char(20),
    campaign_id int not null
);

-- initialize the rules
insert into rule values 
    ('GEO_ATX', 'geo', 'Austin', 1),
    ('GEO_SF', 'geo', 'San Francisco', 2),
    ('IND_SOFT', 'industry', 'Software', 3),
    ('IND_SPORTS', 'industry', 'Sports', 4),
    ('SIZE_0-50', 'company_size', '0 - 50', 5),
    ('SIZE_100-200', 'company_size', '100 - 200', 6),
    ('UNKNOWN', '', '', 7)
;


-- rule priority map rules to priority
create table rule_priority (
    id serial primary key,
    rule_id char(20) not null,
    priority int not null
);

-- priorities initialized to be 100 apart to allow for reordering
insert into rule_priority (rule_id, priority) values
    ('GEO_ATX', 100),
    ('GEO_SF', 200),
    ('IND_SOFT', 300),
    ('IND_SPORTS', 400),
    ('SIZE_0-50', 500),
    ('SIZE_100-200', 600),
    ('UNKNOWN', 700)
;

-- map campaign to image
create table campaign_to_image (
    campaign_id int primary key,
    name varchar(255) not null,
    image_url varchar(255) not null
);

insert into campaign_to_image values 
    (1, 'Users from Austin', 'Austin.jpg'),
    (2, 'Users from San Francisco', 'SanFrancisco.jpg'),
    (3, 'Users in Software', 'Software.jpg'),
    (4, 'Users in Sports', 'Sports.jpg'),
    (5, 'Users in Company Size 0 - 50', 'proof.jpg'),
    (6, 'Users in 100 - 200', 'smb.jpg'),
    (7, 'Unknown Users', 'shrug.jpg') 
;


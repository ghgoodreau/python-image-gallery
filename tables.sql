create table IF NOT EXISTS users (username varchar(100) not null primary key, password varchar(100), full_name varchar(100));
create table IF NOT EXISTS s3_imgs (username varchar(100), img_name varchar(100));
insert into users values ('thisisatest', 'cpsc4973', 'Dongji');

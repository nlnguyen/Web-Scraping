-- create the weblinks database and set it as the current DB
CREATE DATABASE weblinks;
USE weblinks;

-- create a user with its privileges
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'test123';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP
   ON weblinks.*
   TO 'testuser'@'localhost';

/*
   create a table having 4 fields (title, url, meta and description)
   to store http links
*/
CREATE TABLE webs1 (
	title	varchar(512),
	url	varchar(1024),
	meta	varchar(1024),
	description varchar(512)
);

/*
   verify that the table is created with the specified fields
*/
DESCRIBE webs1;


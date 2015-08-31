/*
   create the weblinks database and set it as the current DB
*/
CREATE DATABASE weblinks;

/*
   create a user with its privileges
*/
CREATE USER 'testuser'@'localhost' IDENTIFIED BY 'test123';
GRANT SELECT,INSERT,UPDATE,DELETE,CREATE,DROP
   ON weblinks.*
   TO 'testuser'@'localhost';



USE weblinks;
DROP TABLE IF EXISTS webs1;

/*
   create a table having 4 fields (title, url, keywds and description)
   to store http links
*/
CREATE TABLE webs1 (
	title	varchar(512),
	url	varchar(1024),
	keywds	varchar(1024),
	description varchar(1024)
);

/*
   verify that the table is created with the specified fields
*/
DESCRIBE webs1;


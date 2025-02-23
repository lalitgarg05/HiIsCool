#root does not have password
create database hiiscool;
use database hiiscool;

create table users (id int,
                    username varchar(255),
                    password varchar(255));

insert into users (id, username, password) values (1, 'lalitgarg2005@gmail.com', '11');

create table jobs (id int auto_increment primary key,
                   job_title varchar(255),
                   job_description varchar(255),
                   company_name varchar(255),
                   salary int,
                   job_location varchar(255),
                   posted_at datetime
                  );

create table students_profile (id int,
                               name varchar(255),
                               email varchar(255), phone varchar(255),
                               skills varchar(255),
                               grade_level int,
                               school_name varchar(255),
                               bio varchar(255),
                               interests varchar(255),
                               gpa double,
                               extracurricular varchar(255));
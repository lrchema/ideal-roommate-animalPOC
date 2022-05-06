drop database if exists heroku_b12dbd41fac3d4b;
create database heroku_b12dbd41fac3d4b;
use heroku_b12dbd41fac3d4b;

drop table if exists animals;

create table animals(
    id INT primary key AUTO_INCREMENT,
    name text not null,
    email text not null,
    password text not null,
    species text,
    image text,
    issetup boolean
);
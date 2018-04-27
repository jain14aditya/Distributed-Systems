
create table airport1_perm (
	from_loc varchar(50) , 
	to_loc varchar(50),
	data DATE ,
	tickets int,
	cost int);

create table airport1_temp (
	from_loc varchar(50) , 
	to_loc varchar(50),
	data DATE ,
	tickets int,
	cost int);

insert into airport1_perm values('A','B','2018-04-12',5,100);
insert into airport1_temp values('A','B','2018-04-12',5,100);
insert into airport1_perm values('A','B','2018-04-13',5,100);
insert into airport1_temp values('A','B','2018-04-13',5,100);
insert into airport1_perm values('A','B','2018-04-14',5,100);
insert into airport1_temp values('A','B','2018-04-14',5,100);
insert into airport1_perm values('A','B','2018-04-15',5,100);
insert into airport1_temp values('A','B','2018-04-15',5,100);

insert into airport1_perm values('C','B','2018-04-12',5,101);
insert into airport1_temp values('A','B','2018-04-12',5,101);
insert into airport1_perm values('C','B','2018-04-13',5,101);
insert into airport1_temp values('A','B','2018-04-13',5,101);
insert into airport1_perm values('C','B','2018-04-14',5,101);
insert into airport1_temp values('A','B','2018-04-14',5,101);
insert into airport1_perm values('C','B','2018-04-15',5,101);
insert into airport1_temp values('A','B','2018-04-15',5,101);


insert into airport1_perm values('D','B','2018-04-12',5,102);
insert into airport1_temp values('A','B','2018-04-12',5,102);	
insert into airport1_perm values('D','B','2018-04-13',5,102);
insert into airport1_temp values('A','B','2018-04-13',5,102);
insert into airport1_perm values('D','B','2018-04-14',5,102);
insert into airport1_temp values('A','B','2018-04-14',5,102);
insert into airport1_perm values('D','B','2018-04-15',5,102);
insert into airport1_temp values('A','B','2018-04-15',5,102);


insert into airport1_perm values('C','D','2018-04-12',5,103);
insert into airport1_temp values('A','B','2018-04-12',5,103);	
insert into airport1_perm values('C','D','2018-04-13',5,103);
insert into airport1_temp values('A','B','2018-04-13',5,103);
insert into airport1_perm values('C','D','2018-04-14',5,103);
insert into airport1_temp values('A','B','2018-04-14',5,103);
insert into airport1_perm values('C','D','2018-04-15',5,103);
insert into airport1_temp values('A','B','2018-04-15',5,103);





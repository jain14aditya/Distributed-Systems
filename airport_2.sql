
create table airport2_perm (
	from_loc varchar(50) , 
	to_loc varchar(50),
	data DATE ,
	tickets int,
	cost int);

create table airport2_temp (
	from_loc varchar(50) , 
	to_loc varchar(50),
	data DATE ,
	tickets int,
	cost int);

insert into airport2_perm values('B','A','2018-04-12',5,100);
insert into airport2_temp values('B','A','2018-04-12',5,100);

insert into airport2_perm values('B','A','2018-04-13',5,100);
insert into airport2_temp values('B','A','2018-04-13',5,100);

insert into airport2_perm values('B','A','2018-04-14',5,100);
insert into airport2_temp values('B','A','2018-04-14',5,100);

insert into airport2_perm values('B','A','2018-04-15',5,100);
insert into airport2_temp values('B','A','2018-04-15',5,100);



insert into airport2_perm values('B','C','2018-04-12',5,101);
insert into airport2_temp values('B','C','2018-04-12',5,101);
	
insert into airport2_perm values('B','C','2018-04-13',5,101);
insert into airport2_temp values('B','C','2018-04-13',5,101);

insert into airport2_perm values('B','C','2018-04-14',5,101);
insert into airport2_temp values('B','C','2018-04-14',5,101);

insert into airport2_perm values('B','C','2018-04-15',5,101);
insert into airport2_temp values('B','C','2018-04-15',5,101);



insert into airport2_perm values('B','D','2018-04-12',5,102);
insert into airport2_temp values('B','D','2018-04-12',5,102);
	
insert into airport2_perm values('B','D','2018-04-13',5,102);
insert into airport2_temp values('B','D','2018-04-13',5,102);

insert into airport2_perm values('B','D','2018-04-14',5,102);
insert into airport2_temp values('B','D','2018-04-14',5,102);

insert into airport2_perm values('B','D','2018-04-15',5,102);
insert into airport2_temp values('B','D','2018-04-15',5,102);



	








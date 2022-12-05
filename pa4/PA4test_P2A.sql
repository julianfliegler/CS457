-- On P2:
USE CS457_PA4;
select * from Flights;
begin transaction;
update flights set status = 1 where seat = 22;
--there should be nothing to commit; it's an "abort"
commit; 
select * from Flights;
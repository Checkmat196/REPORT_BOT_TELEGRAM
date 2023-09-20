SELECT
	A.id as 'ID_CHAMADO',
	A.date as 'DATA_ABERTURA_CHAMADO',
	B.name as 'ORIGEM',
	Upper(Concat(F.firstname, ' ', F.realname)) as 'SOLICITANTE',
	C.completename AS 'CATEGORIA',
	Convert(A.date, time) AS 'DATA OPENING',
	TIME_TO_SEC(TIMEDIFF(Convert(NOW(), time), Convert(A.date, time))) AS 'difference_in_minutes'
From glpi_tickets A 
	inner join glpi_entities B on A.entities_id = B.id
	inner join glpi_itilcategories C on A.itilcategories_id = C.id
	inner join glpi_users D on A.users_id_lastupdater = D.id 
	inner join glpi_users F on A.users_id_recipient = F.id 
	inner join glpi_solutiontypes G on A.status = G.id 
	inner join glpi_groups E on F.groups_id = E.id 
where Convert(A.date, DATE) >= CURDATE() and C.completename like '%MIS >%' and
TIME_TO_SEC(TIMEDIFF(Convert(NOW(), time), Convert(A.date, time)))  <= 300

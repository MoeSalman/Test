-- Creation des tableaus

Create Table Lieux (
ID int IDENTITY(1,1) primary key,
Commune varchar(255),
Departement varchar(255),
region varchar(255),
)

Create Table People (
ID int IDENTITY(1,1) primary key,
Prenom varchar(255),
Nom varchar(255),
Date_de_Naissance date,
CommuneID varchar (255) 
)


-- Method SQL pour importer les csv
Create Table #Lieux2 (
Commune varchar(255),
Departement varchar(255),
region varchar(255)
)

Create Table #People2 (
Prenom varchar(255),
Nom varchar(255),
Date_de_Naissance date,
commune varchar(255),
)


-- Insertion de données de fichiers csv dans un table temporaire pour les modifies puis au tableau associe
BULK INSERT #Lieux2
FROM 'C:\Users\User\Desktop\Files\Capgemini Test\data\lieux.csv'
WITH
(
        FORMAT='CSV',
        FIRSTROW=2
)
GO


insert into Lieux(commune,departement,region)
select Commune,Departement,region from #Lieux2

BULK INSERT  #People2
FROM 'C:\Users\User\Desktop\Files\Capgemini Test\data\people.csv'
WITH
(
        FORMAT='CSV',
        FIRSTROW=2
)
GO

--Remplacement du nom de la commune par l'identifiant dans la table temporaire des personnes 
update p
set p.commune=l.ID
from #People2 p inner join Lieux l
on p.commune=l.Commune

--Insertion des données finales dans les tables associées
insert into People(Prenom,Nom,Date_de_Naissance,CommuneID)
select Prenom,Nom,Date_de_Naissance,CAST(commune AS INT) as commune from #People2

select * FROM People
SELECT * FROM Lieux
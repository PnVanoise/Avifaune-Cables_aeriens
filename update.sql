
-- schema cables73

ALTER TABLE cables73.t_inventaire_poteaux_erdf ADD COLUMN insee INTEGER;
ALTER TABLE cables73.t_inventaire_poteaux_erdf ADD CONSTRAINT t_inventaire_poteaux_erdf_insee_fk FOREIGN KEY (insee) REFERENCES cables73.t_communes(insee);
UPDATE cables73.t_inventaire_poteaux_erdf SET insee = c.insee FROM cables73.t_inventaire_poteaux_erdf p JOIN cables73.t_communes c ON p.commune=c.nom_commune;

ALTER TABLE cables73.t_inventaire_troncons_erdf ADD COLUMN insee INTEGER;
ALTER TABLE cables73.t_inventaire_troncons_erdf ADD CONSTRAINT t_inventaire_troncons_erdf_insee_fk FOREIGN KEY (insee) REFERENCES cables73.t_communes(insee);
UPDATE cables73.t_inventaire_troncons_erdf SET insee = c.insee FROM cables73.t_inventaire_troncons_erdf p JOIN cables73.t_communes c ON p.commune=c.nom_commune;


-- schema cables74
ALTER TABLE cables74.t_communes ADD CONSTRAINT t_communes_pk PRIMARY KEY (insee);

ALTER TABLE cables74.t_inventaire_poteaux_erdf ADD COLUMN insee INTEGER;
ALTER TABLE cables74.t_inventaire_poteaux_erdf ADD CONSTRAINT t_inventaire_poteaux_erdf_insee_fk FOREIGN KEY (insee) REFERENCES cables74.t_communes(insee);
UPDATE cables74.t_inventaire_poteaux_erdf SET insee = c.insee FROM cables74.t_inventaire_poteaux_erdf p JOIN cables74.t_communes c ON p.commune=c.nom_commune;

ALTER TABLE cables74.t_inventaire_troncons_erdf ADD COLUMN insee INTEGER;
ALTER TABLE cables74.t_inventaire_troncons_erdf ADD CONSTRAINT t_inventaire_troncons_erdf_insee_fk FOREIGN KEY (insee) REFERENCES cables74.t_communes(insee);
UPDATE cables74.t_inventaire_troncons_erdf SET insee = c.insee FROM cables74.t_inventaire_troncons_erdf p JOIN cables74.t_communes c ON p.commune=c.nom_commune;

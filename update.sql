ALTER TABLE cables73.t_inventaire_poteaux_erdf ADD COLUMN insee INTEGER;
ALTER TABLE cables73.t_inventaire_poteaux_erdf ADD CONSTRAINT t_inventaire_poteaux_erdf_insee_fk FOREIGN KEY (insee) REFERENCES cables73.t_communes(insee);
UPDATE cables73.t_inventaire_poteaux_erdf SET insee = c.insee FROM cables73.t_inventaire_poteaux_erdf p JOIN cables73.t_communes c ON p.commune=c.nom_commune;

ALTER TABLE cables73.t_inventaire_troncons_erdf ADD COLUMN insee INTEGER;
ALTER TABLE cables73.t_inventaire_troncons_erdf ADD CONSTRAINT t_inventaire_troncons_erdf_insee_fk FOREIGN KEY (insee) REFERENCES cables73.t_communes(insee);
UPDATE cables73.t_inventaire_troncons_erdf SET insee = c.insee FROM cables73.t_inventaire_troncons_erdf p JOIN cables73.t_communes c ON p.commune=c.nom_commune;

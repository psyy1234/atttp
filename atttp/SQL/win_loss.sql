SELECT id as game_nr, datum, first_name, CASE WHEN SUM(win_loss) > 0 THEN 'WIN'
							       WHEN SUM(win_loss) < 0 THEN 'LOSS'
								   ELSE 'TIE' END AS win_loss
FROM (
		SELECT 	h.id AS id,
				h.datum AS datum, 
				u1.first_name AS first_name, 
				d.niz AS niz, 
				--d.rezultat_1 || ' - ' || d.rezultat_2 AS rezultat,
				CASE WHEN d.rezultat_1 - d.rezultat_2 < 0 THEN -1 ELSE 1 END AS win_loss
		FROM atttp_gamehead h, atttp_gamedetail d, auth_user u1
		WHERE h.id = d.igra_id
		AND h.oseba_1_id = u1.id
		UNION ALL
		SELECT 	h.id,
				h.datum, 
				u2.first_name, 
				d.niz, 
				--d.rezultat_1 || ' - ' || d.rezultat_2 AS rezultat,
				CASE WHEN d.rezultat_2 - d.rezultat_1 < 0 THEN -1 ELSE 1 END AS win_loss
		FROM atttp_gamehead h, atttp_gamedetail d, auth_user u2
		WHERE h.id = d.igra_id 
		AND h.oseba_2_id = u2.id)
GROUP BY id, datum, first_name
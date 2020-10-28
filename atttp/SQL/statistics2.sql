WITH games AS (SELECT oseba_1_id oseba_id,
				      CASE WHEN SUM(CASE WHEN d.rezultat_1 - d.rezultat_2 > 0 THEN 1
									ELSE -1 END) > 0 THEN 'WIN'
						   WHEN SUM(CASE WHEN d.rezultat_1 - d.rezultat_2 < 0 THEN 1
									ELSE -1 END) > 0 THEN 'LOSS'
						   ELSE 'TIE' END win_loss
			   FROM atttp_gamehead h, atttp_gamedetail d
			   WHERE h.id = d.igra_id
			   AND strftime("%Y", h.datum) = "2020"
			   GROUP BY oseba_1_id, h.id
			   UNION ALL
			   SELECT oseba_2_id oseba_id,
				      CASE WHEN SUM(CASE WHEN d.rezultat_2 - d.rezultat_1 > 0 THEN 1
									ELSE -1 END) > 0 THEN 'WIN'
						   WHEN SUM(CASE WHEN d.rezultat_2 - d.rezultat_1 < 0 THEN 1
									ELSE -1 END) > 0 THEN 'LOSS'
						   ELSE 'TIE' END win_loss
			   FROM atttp_gamehead h, atttp_gamedetail d
			   WHERE h.id = d.igra_id
			   AND strftime("%Y", h.datum) = "2020"
			   GROUP BY oseba_2_id, h.id)
			   
SELECT first_name 
FROM auth_user u LEFT OUTER JOIN
(
SELECT oseba_id,
	   IFNULL(SUM(CASE WHEN win_loss = 'WIN' THEN 1 ELSE 0 END), '0') AS wins, 
	   SUM(CASE WHEN win_loss = 'TIE' THEN 1 ELSE 0 END) AS ties, 
	   SUM(CASE WHEN win_loss = 'LOSS' THEN 1 ELSE 0 END) AS loss, 
	   SUM(CASE WHEN win_loss = 'WIN' THEN 3  
				WHEN win_loss = 'TIE' THEN 1 
				ELSE 0 END) AS points 
FROM games
GROUP BY oseba_id) ON u.id = oseba_id
ORDER BY points DESC
WITH users AS (SELECT u.id AS uid,
					  username,
					  first_name
			   FROM auth_user u,
					auth_user_groups ug,
					auth_group g
			   WHERE u.id = ug.user_id
			   and g.id = ug.group_id
			   AND g.name = 'atttp'),
 game_heads AS (SELECT h.id as head_id,
						   oseba_1_id,
						   oseba_2_id
				FROM atttp_gamehead h
				WHERE EXISTS (SELECT 1 FROM users u WHERE h.oseba_1_id = u.uid)
				AND EXISTS (SELECT 1 FROM users u WHERE h.oseba_2_id = u.uid)
				AND strftime('%Y', h.datum) = '2019'),
games AS (SELECT head_id, oseba_1_id oseba_id, 
				 CASE WHEN SUM(CASE WHEN d.rezultat_1 - d.rezultat_2 > 0 THEN 1 
								ELSE -1 END) > 0 THEN 'WIN' 
					WHEN SUM(CASE WHEN d.rezultat_1 - d.rezultat_2 < 0 THEN 1 
								ELSE -1 END) > 0 THEN 'LOSS' 
					ELSE 'TIE' END win_loss 
			FROM game_heads h, atttp_gamedetail d 
			WHERE h.head_id = d.igra_id 
			AND NOT(IFNULL(d.rezultat_1, 0) = 0 AND  IFNULL(d.rezultat_2, 0) = 0)
			GROUP BY oseba_1_id, h.head_id
			UNION ALL 
			SELECT head_id, oseba_2_id oseba_id, 
					CASE WHEN SUM(CASE WHEN d.rezultat_2 - d.rezultat_1 > 0 THEN 1 
									ELSE -1 END) > 0 THEN 'WIN' 
						WHEN SUM(CASE WHEN d.rezultat_2 - d.rezultat_1 < 0 THEN 1 
									ELSE -1 END) > 0 THEN 'LOSS' 
						ELSE 'TIE' END win_loss 
			FROM game_heads h, atttp_gamedetail d 
			WHERE h.head_id = d.igra_id 
			AND NOT(IFNULL(d.rezultat_1, 0) = 0 AND  IFNULL(d.rezultat_2, 0) = 0)
			GROUP BY oseba_2_id, h.head_id)
SELECT  first_name,
		IFNULL(wins,0) + IFNULL(ties, 0) + IFNULL(loss, 0) nr_games,
		IFNULL(wins, 0) wins,
		IFNULL(ties, 0) ties,
		IFNULL(loss, 0) loss,
		IFNULL(points, 0) points
FROM users u LEFT OUTER JOIN
(
SELECT oseba_id,
	   SUM(CASE WHEN win_loss = 'WIN' THEN 1 ELSE 0 END) AS wins, 
	   SUM(CASE WHEN win_loss = 'TIE' THEN 1 ELSE 0 END) AS ties, 
	   SUM(CASE WHEN win_loss = 'LOSS' THEN 1 ELSE 0 END) AS loss, 
	   SUM(CASE WHEN win_loss = 'WIN' THEN 3  
				WHEN win_loss = 'TIE' THEN 1 
				ELSE 0 END) AS points 
FROM games
GROUP BY oseba_id) ON u.uid = oseba_id
ORDER BY points DESC, nr_games DESC
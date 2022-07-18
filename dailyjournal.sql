

CREATE TABLE `Journalentries` (
	`id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	`date`	TEXT NOT NULL,
	`concept`	TEXT NOT NULL,
	`entry` TEXT NOT NULL,
    `mood_id` INTEGER NOT NULL, 
	FOREIGN KEY(`mood_id`) REFERENCES `moods`(`id`)

);

CREATE TABLE `entrytags` (
`id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
`entry_id` INTEGER NOT NULL,
`tag_id` INTEGER NOT NULL,
FOREIGN KEY(`entry_id`) REFERENCES `Journalentries`(`id`),
FOREIGN KEY(`tag_id`) REFERENCES `Tags`(`id`));



INSERT INTO entrytags VALUES (8, 2, 3)

INSERT INTO Journalentries VALUES (null, '7/13/2029992', 'okokokok', 'lets go babeyy', 2);

INSERT INTO Tags VALUES (3, 'quiznos')

SELECT *
FROM entrytags


SELECT
            a.id,
            a.date,
            a.concept,
            a.entry,
            a.mood_id, 
            m.label mood_label, 
			t.id tag_id
        FROM Journalentries a
        JOIN Moods m
            ON m.id = a.mood_id
		JOIN entrytags e
			ON e.entry_id  = a.id
        JOIN Tags t
			ON t.id = e.tag_id




SELECT 
            a.id,
            a.date,
            a.concept,
            a.entry,
            a.mood_id, 
            m.label mood_label,
			et.tag_id tag_id,
			t.name name
			
        FROM Journalentries a
        JOIN Moods m
            ON m.id = a.mood_id
		JOIN Entrytags et
			ON et.entry_id = a.id
		JOIN Tags t
			ON t.id = et.tag_id

SELECT
	et.id,
	et.entry_id
	et.tag_id
	t.name
FROM entrytags 
JOIN Tags t
	ON t.id = et.tag_id
	
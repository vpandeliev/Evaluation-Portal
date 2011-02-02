BEGIN;
ALTER TABLE `studies_userstage` ADD COLUMN 'study_id' integer REFERENCES 'studies_study' ("id");
COMMIT;

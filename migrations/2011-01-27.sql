BEGIN;
ALTER TABLE "studies_userstage" ADD COLUMN "curr_session_started" datetime;
COMMIT;

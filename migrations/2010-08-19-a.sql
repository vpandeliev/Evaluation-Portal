BEGIN;
ALTER TABLE "boggle_game" ADD COLUMN "round_max" integer NOT NULL DEFAULT 10;
ALTER TABLE "boggle_game" ADD COLUMN "game_over_url" varchar(200) NOT NULL DEFAULT '';
COMMIT;
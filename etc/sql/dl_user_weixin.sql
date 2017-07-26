create SEQUENCE dl_user_weixin_seq
    start 1000
    increment 1
    NO MAXVALUE
    CACHE 1;

CREATE TABLE "public"."dl_user_weixin" (
	"u_id" int8 NOT NULL DEFAULT nextval('dl_user_weixin_seq'::regclass),
	"user_name" varchar(50) UNIQUE NOT NULL DEFAULT ''::character varying COLLATE "default",
	"openid" varchar(255) NOT NULL DEFAULT ''::character varying COLLATE "default",
	"ctime" int8 NOT NULL DEFAULT (0)::bigint,
	"utime" int8 NOT NULL DEFAULT (0)::bigint,
	CONSTRAINT "dl_user_weixin_pkey" PRIMARY KEY ("u_id") NOT DEFERRABLE INITIALLY IMMEDIATE,
	CONSTRAINT "dl_user_weixin_user_name_key" UNIQUE ("user_name") NOT DEFERRABLE INITIALLY IMMEDIATE
)
WITH (OIDS=FALSE);
ALTER TABLE "public"."dl_user_weixin" OWNER TO "postgres";
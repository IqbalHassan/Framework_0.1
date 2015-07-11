--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

--
-- Name: postgres; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON DATABASE postgres IS 'default administrative connection database';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


--
-- Name: adminpack; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS adminpack WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION adminpack; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION adminpack IS 'administrative functions for PostgreSQL';


--
-- Name: ltree; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS ltree WITH SCHEMA public;


--
-- Name: EXTENSION ltree; Type: COMMENT; Schema: -; Owner: 
--

COMMENT ON EXTENSION ltree IS 'data type for hierarchical tree-like structures';


SET search_path = public, pg_catalog;

--
-- Name: changedatastructure(text, text); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION changedatastructure(oldval text, newval text) RETURNS void
    LANGUAGE sql
    AS $_$



Update pim_master_data set id = $2 where id = $1 and field in ('Other Street Address','Other City','Other State-Prov-Region','Other Zip-Postal Code','Other Country');

insert into pim_master_data (id, field, value) values ($1, 'Other Address', $2);

Update pim_master_data set field = substr(field,6) where id = $2 and field in ('Other Street Address','Other City','Other State-Prov-Region','Other Zip-Postal Code','Other Country');



$_$;


ALTER FUNCTION public.changedatastructure(oldval text, newval text) OWNER TO postgres;

--
-- Name: truncate_tables(character varying); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION truncate_tables(username character varying) RETURNS void
    LANGUAGE plpgsql
    AS $$

DECLARE

    statements CURSOR FOR

        SELECT tablename FROM pg_tables

        WHERE tableowner = username AND schemaname = 'public';

BEGIN

    FOR stmt IN statements LOOP

        EXECUTE 'TRUNCATE TABLE ' || quote_ident(stmt.tablename) || ' CASCADE;';

    END LOOP;

END;

$$;


ALTER FUNCTION public.truncate_tables(username character varying) OWNER TO postgres;

--
-- Name: update_test_case_tag(); Type: FUNCTION; Schema: public; Owner: postgres
--

CREATE FUNCTION update_test_case_tag() RETURNS void
    LANGUAGE plpgsql
    AS $$

DECLARE

	x record;

	project text;

	type text;

	

 BEGIN

    project:='135';

    type:='Team';

    FOR x IN select distinct tc_id from test_cases 

	  LOOP

		insert into test_case_tag(tc_id,name,property) values(x.tc_id,project,type);

	  END LOOP;

    RETURN;

END

$$;


ALTER FUNCTION public.update_test_case_tag() OWNER TO postgres;

--
-- Name: Platform_PlatformID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "Platform_PlatformID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "Platform_PlatformID_seq" OWNER TO postgres;

--
-- Name: TestRun_TestRunID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "TestRun_TestRunID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "TestRun_TestRunID_seq" OWNER TO postgres;

--
-- Name: TestStep_TestStepID_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE "TestStep_TestStepID_seq"
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE "TestStep_TestStepID_seq" OWNER TO postgres;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: branch; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE branch (
    id integer NOT NULL,
    branch_name character varying(50),
    project_id character varying(10),
    team_id integer
);


ALTER TABLE branch OWNER TO postgres;

--
-- Name: branch_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE branch_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE branch_id_seq OWNER TO postgres;

--
-- Name: branch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE branch_id_seq OWNED BY branch.id;


--
-- Name: branch_management; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE branch_management (
    project_id character varying(10),
    team_id integer,
    branch integer
);


ALTER TABLE branch_management OWNER TO postgres;

--
-- Name: bugid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE bugid_seq
    START WITH 40
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE bugid_seq OWNER TO postgres;

--
-- Name: bugs; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE bugs (
    bug_id character varying(20),
    bug_title character varying(100),
    bug_description text,
    bug_startingdate date,
    bug_endingdate date,
    bug_priority character varying(10),
    bug_milestone character varying(50),
    bug_createdby character varying(40),
    bug_creationdate date,
    bug_modifiedby character varying(40),
    bug_modifydate date,
    status character varying(30),
    team_id character varying,
    project_id character varying,
    tester character varying
);


ALTER TABLE bugs OWNER TO postgres;

--
-- Name: comment_attachment; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE comment_attachment (
    comment_id character varying(10) NOT NULL,
    docfile character varying(300) NOT NULL
);


ALTER TABLE comment_attachment OWNER TO postgres;

--
-- Name: comment_track; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE comment_track (
    child_comment character varying(10) NOT NULL,
    parent_comment character varying(300) NOT NULL
);


ALTER TABLE comment_track OWNER TO postgres;

--
-- Name: commentid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE commentid_seq
    START WITH 20
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE commentid_seq OWNER TO postgres;

--
-- Name: comments; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE comments (
    comment_id character varying(10) NOT NULL,
    project_id character varying(10) NOT NULL,
    comment_text text,
    comment_date timestamp without time zone,
    commented_by character varying(40) NOT NULL,
    rank character varying(40) NOT NULL,
    attachment boolean
);


ALTER TABLE comments OWNER TO postgres;

--
-- Name: components_map; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE components_map (
    id1 character varying,
    id2 character varying,
    type1 character varying,
    type2 character varying
);


ALTER TABLE components_map OWNER TO postgres;

--
-- Name: config_values; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE config_values (
    id integer NOT NULL,
    type character varying(100) NOT NULL,
    sub_type character varying(100),
    value character varying(100) NOT NULL
);


ALTER TABLE config_values OWNER TO postgres;

--
-- Name: config_values_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE config_values_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE config_values_id_seq OWNER TO postgres;

--
-- Name: config_values_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE config_values_id_seq OWNED BY config_values.id;


--
-- Name: containertypedata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE containertypedata_id_seq
    START WITH 201
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE containertypedata_id_seq OWNER TO postgres;

--
-- Name: container_type_data; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE container_type_data (
    id integer DEFAULT nextval('containertypedata_id_seq'::regclass) NOT NULL,
    dataid character varying(20),
    curname character varying(200),
    newname character varying(300),
    items_count integer
);


ALTER TABLE container_type_data OWNER TO postgres;

--
-- Name: COLUMN container_type_data.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN container_type_data.id IS 'Database index use only';


--
-- Name: daily_build_status; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE daily_build_status (
    id integer NOT NULL,
    daily_build_user character varying(100) NOT NULL,
    status character varying(100) NOT NULL,
    last_checked_time timestamp without time zone DEFAULT now(),
    bundle character varying(100) NOT NULL,
    machine_os character varying(100),
    local_ip character varying(30),
    branch character varying(30),
    release character varying(30),
    run_id character varying(100),
    build_path character varying(1000)
);


ALTER TABLE daily_build_status OWNER TO postgres;

--
-- Name: TABLE daily_build_status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE daily_build_status IS 'Contains daily build status information.

';


--
-- Name: COLUMN daily_build_status.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.id IS 'Database index use only';


--
-- Name: COLUMN daily_build_status.daily_build_user; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.daily_build_user IS 'Daily build User';


--
-- Name: COLUMN daily_build_status.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.status IS 'Used to report the Status of the daily build';


--
-- Name: COLUMN daily_build_status.last_checked_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.last_checked_time IS 'timestamp of last checked for the daliy bulid';


--
-- Name: COLUMN daily_build_status.bundle; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.bundle IS 'Desktop Bundle number';


--
-- Name: COLUMN daily_build_status.machine_os; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.machine_os IS 'Operating System';


--
-- Name: COLUMN daily_build_status.local_ip; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.local_ip IS 'ip address of SUT';


--
-- Name: COLUMN daily_build_status.branch; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.branch IS 'Build Branch (ie. SCM, Tachyon, jenkins)';


--
-- Name: COLUMN daily_build_status.release; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.release IS 'Desktop Release';


--
-- Name: COLUMN daily_build_status.run_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.run_id IS 'Run ID for the Current Test Run';


--
-- Name: COLUMN daily_build_status.build_path; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN daily_build_status.build_path IS 'path to build location';


--
-- Name: daily_build_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE daily_build_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE daily_build_status_id_seq OWNER TO postgres;

--
-- Name: daily_build_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE daily_build_status_id_seq OWNED BY daily_build_status.id;


--
-- Name: default_choice; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE default_choice (
    user_id character varying(5) NOT NULL,
    default_project character varying(10),
    default_team integer
);


ALTER TABLE default_choice OWNER TO postgres;

--
-- Name: dependency; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE dependency (
    id integer NOT NULL,
    dependency_name character varying(50) NOT NULL,
    project_id character varying(10),
    team_id integer
);


ALTER TABLE dependency OWNER TO postgres;

--
-- Name: dependency_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE dependency_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE dependency_id_seq OWNER TO postgres;

--
-- Name: dependency_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE dependency_id_seq OWNED BY dependency.id;


--
-- Name: dependency_management; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE dependency_management (
    project_id character varying(10) NOT NULL,
    team_id integer NOT NULL,
    dependency integer NOT NULL,
    default_choices character varying(50)
);


ALTER TABLE dependency_management OWNER TO postgres;

--
-- Name: dependency_name; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE dependency_name (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    dependency_id integer
);


ALTER TABLE dependency_name OWNER TO postgres;

--
-- Name: dependency_name_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE dependency_name_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE dependency_name_id_seq OWNER TO postgres;

--
-- Name: dependency_name_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE dependency_name_id_seq OWNED BY dependency_name.id;


--
-- Name: dependency_values; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE dependency_values (
    id integer NOT NULL,
    version character varying(50) NOT NULL,
    bit_name character varying(50) NOT NULL
);


ALTER TABLE dependency_values OWNER TO postgres;

--
-- Name: django_migrations; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE django_migrations (
    id integer NOT NULL,
    app character varying(255) NOT NULL,
    name character varying(255) NOT NULL,
    applied timestamp with time zone NOT NULL
);


ALTER TABLE django_migrations OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE django_migrations_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE django_migrations_id_seq OWNER TO postgres;

--
-- Name: django_migrations_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE django_migrations_id_seq OWNED BY django_migrations.id;


--
-- Name: drivers; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE drivers (
    id integer NOT NULL,
    driver_name character varying(50),
    project_id character varying(10),
    team_id integer
);


ALTER TABLE drivers OWNER TO postgres;

--
-- Name: drivers_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE drivers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE drivers_id_seq OWNER TO postgres;

--
-- Name: drivers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE drivers_id_seq OWNED BY drivers.id;


--
-- Name: email_config; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE email_config (
    id integer NOT NULL,
    project_id character varying,
    team_id integer,
    created_by character varying,
    created_date date,
    modified_by character varying,
    modified_date date,
    from_address character varying,
    username character varying,
    password character varying,
    smtp character varying,
    port integer,
    ttls boolean
);


ALTER TABLE email_config OWNER TO postgres;

--
-- Name: email_config_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE email_config_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE email_config_id_seq OWNER TO postgres;

--
-- Name: email_config_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE email_config_id_seq OWNED BY email_config.id;


--
-- Name: execution_log; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE execution_log (
    executionlogid integer NOT NULL,
    logid character varying(40),
    modulename character varying(60) NOT NULL,
    details text,
    status character varying(100) NOT NULL,
    loglevel integer NOT NULL,
    tstamp timestamp without time zone DEFAULT now()
);


ALTER TABLE execution_log OWNER TO postgres;

--
-- Name: TABLE execution_log; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE execution_log IS 'Contains detailed information on the execution of tasks.

For Example: Module CloseDTM: DTSGeneral was executed were Desktop Manager window not found ';


--
-- Name: COLUMN execution_log.executionlogid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN execution_log.executionlogid IS 'execution log id';


--
-- Name: COLUMN execution_log.modulename; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN execution_log.modulename IS 'module name that is being executed';


--
-- Name: COLUMN execution_log.details; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN execution_log.details IS 'A text description of the task being executed';


--
-- Name: COLUMN execution_log.loglevel; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN execution_log.loglevel IS 'log level = (1, 2, 3)';


--
-- Name: COLUMN execution_log.tstamp; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN execution_log.tstamp IS 'Timestamp';


--
-- Name: executionlog_executionlogid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE executionlog_executionlogid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE executionlog_executionlogid_seq OWNER TO postgres;

--
-- Name: executionlog_executionlogid_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE executionlog_executionlogid_seq OWNED BY execution_log.executionlogid;


--
-- Name: expectedcontainer_expectedplaylistid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE expectedcontainer_expectedplaylistid_seq
    START WITH 101
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE expectedcontainer_expectedplaylistid_seq OWNER TO postgres;

--
-- Name: product_features; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE product_features (
    feature_id integer NOT NULL,
    feature_path ltree NOT NULL,
    project_id character varying(10),
    team_id integer
);


ALTER TABLE product_features OWNER TO postgres;

--
-- Name: feature_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE feature_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE feature_id_seq OWNER TO postgres;

--
-- Name: feature_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE feature_id_seq OWNED BY product_features.feature_id;


--
-- Name: feature_map; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE feature_map (
    id character varying,
    type character varying,
    feature_id character varying
);


ALTER TABLE feature_map OWNER TO postgres;

--
-- Name: label_map; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE label_map (
    id character varying,
    label_id character varying,
    type character varying
);


ALTER TABLE label_map OWNER TO postgres;

--
-- Name: labelid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE labelid_seq
    START WITH 10
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE labelid_seq OWNER TO postgres;

--
-- Name: labels; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE labels (
    label_id character varying NOT NULL,
    label_name character varying,
    label_color character varying,
    project_id character varying,
    team_id character varying,
    created_by character varying,
    modified_by character varying,
    created_date date,
    modified_date date,
    private boolean
);


ALTER TABLE labels OWNER TO postgres;

--
-- Name: machine_dependency_settings; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE machine_dependency_settings (
    machine_serial integer,
    name character varying(50),
    "bit" integer,
    version character varying(50),
    type character varying(50)
);


ALTER TABLE machine_dependency_settings OWNER TO postgres;

--
-- Name: machine_project_map; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE machine_project_map (
    machine_serial integer,
    project_id character varying(10),
    team_id integer
);


ALTER TABLE machine_project_map OWNER TO postgres;

--
-- Name: master_data; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE master_data (
    id character varying(30) NOT NULL,
    field character varying(50) NOT NULL,
    value text NOT NULL,
    description character varying(200),
    keyfield boolean,
    ignorefield boolean
);


ALTER TABLE master_data OWNER TO postgres;

--
-- Name: milestone_info; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE milestone_info (
    id integer,
    name character varying,
    starting_date date,
    finishing_date date,
    status character varying(30),
    description character varying,
    created_by character varying,
    modified_by character varying,
    created_date date,
    modified_date date
);


ALTER TABLE milestone_info OWNER TO postgres;

--
-- Name: performance_results; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE performance_results (
    tc_id character varying(20) NOT NULL,
    run_id character varying(100),
    cycles text,
    max_time text,
    min_time text,
    avg_time text,
    total_time text,
    count text,
    success text,
    error text,
    result_type character varying(20)
);


ALTER TABLE performance_results OWNER TO postgres;

--
-- Name: permitted_user_list; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE permitted_user_list (
    user_id integer NOT NULL,
    user_names character varying(255) NOT NULL,
    user_level character varying(255) NOT NULL,
    email character varying(100) NOT NULL
);


ALTER TABLE permitted_user_list OWNER TO postgres;

--
-- Name: permitted_user_list_user_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE permitted_user_list_user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE permitted_user_list_user_id_seq OWNER TO postgres;

--
-- Name: permitted_user_list_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE permitted_user_list_user_id_seq OWNED BY permitted_user_list.user_id;


--
-- Name: product_sections; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE product_sections (
    section_id integer NOT NULL,
    section_path ltree NOT NULL,
    project_id character varying(10),
    team_id integer
);


ALTER TABLE product_sections OWNER TO postgres;

--
-- Name: product_sections_section_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE product_sections_section_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE product_sections_section_id_seq OWNER TO postgres;

--
-- Name: product_sections_section_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE product_sections_section_id_seq OWNED BY product_sections.section_id;


--
-- Name: project_team_map; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE project_team_map (
    project_id character varying(10),
    team_id character varying(10)
);


ALTER TABLE project_team_map OWNER TO postgres;

--
-- Name: projectid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE projectid_seq
    START WITH 16
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE projectid_seq OWNER TO postgres;

--
-- Name: projects; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE projects (
    project_id character varying(10) NOT NULL,
    project_name character varying(100) NOT NULL,
    project_description character varying(200) NOT NULL,
    project_startingdate date,
    project_endingdate date,
    project_owners text,
    project_createdby character varying(40) NOT NULL,
    project_creationdate date NOT NULL,
    project_modifiedby character varying(40) NOT NULL,
    project_modifydate date NOT NULL
);


ALTER TABLE projects OWNER TO postgres;

--
-- Name: related_items; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE related_items (
    project_id character varying,
    server_name character varying,
    hyperlink character varying,
    username character varying,
    password character varying,
    application character varying
);


ALTER TABLE related_items OWNER TO postgres;

--
-- Name: requirement_sections; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE requirement_sections (
    requirement_path_id integer NOT NULL,
    requirement_path ltree NOT NULL
);


ALTER TABLE requirement_sections OWNER TO postgres;

--
-- Name: requirement_sections_requirement_path_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE requirement_sections_requirement_path_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE requirement_sections_requirement_path_id_seq OWNER TO postgres;

--
-- Name: requirement_sections_requirement_path_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE requirement_sections_requirement_path_id_seq OWNED BY requirement_sections.requirement_path_id;


--
-- Name: requirementid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE requirementid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE requirementid_seq OWNER TO postgres;

--
-- Name: requirements; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE requirements (
    requirement_id character varying(10) NOT NULL,
    requirement_title character varying(100) NOT NULL,
    requirement_startingdate date NOT NULL,
    requirement_endingdate date NOT NULL,
    requirement_priority character varying(10),
    requirement_milestone character varying(50),
    requirement_createdby character varying(40) NOT NULL,
    requirement_creationdate date NOT NULL,
    requirement_modifiedby character varying(40) NOT NULL,
    requirement_modifydate date NOT NULL,
    project_id character varying(10),
    requirement_description character varying(200),
    status character varying(30),
    parent_requirement_id character varying(10),
    team_id character varying
);


ALTER TABLE requirements OWNER TO postgres;

--
-- Name: result_container_type_data; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE result_container_type_data (
    run_id character varying(100) NOT NULL,
    id integer NOT NULL,
    dataid character varying(20),
    curname character varying(200),
    newname character varying(300),
    items_count integer
);


ALTER TABLE result_container_type_data OWNER TO postgres;

--
-- Name: result_master_data; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE result_master_data (
    run_id character varying(100) NOT NULL,
    id character varying(30) NOT NULL,
    field character varying(50) NOT NULL,
    value text NOT NULL,
    description character varying(200),
    keyfield boolean,
    ignorefield boolean
);


ALTER TABLE result_master_data OWNER TO postgres;

--
-- Name: result_test_case_datasets; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE result_test_case_datasets (
    run_id character varying(100) NOT NULL,
    tcdatasetid character varying(20) NOT NULL,
    tc_id character varying(10),
    execornot character varying(10) NOT NULL,
    data_type text NOT NULL
);


ALTER TABLE result_test_case_datasets OWNER TO postgres;

--
-- Name: result_test_case_tag; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE result_test_case_tag (
    run_id character varying(100) NOT NULL,
    tc_id character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    property character varying(100) NOT NULL
);


ALTER TABLE result_test_case_tag OWNER TO postgres;

--
-- Name: result_test_cases; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE result_test_cases (
    run_id character varying(100) NOT NULL,
    tc_id character varying(10) NOT NULL,
    tc_name character varying(100) NOT NULL,
    tc_type character varying(10) NOT NULL,
    tc_executiontype character varying(20),
    tc_priority character varying(10),
    tc_localization character varying(10) NOT NULL,
    tc_createdby character varying(40) NOT NULL,
    tc_creationdate date NOT NULL,
    tc_modifiedby character varying(40) NOT NULL,
    tc_modifydate date NOT NULL,
    defectid character varying(15),
    prd_no character varying(15),
    test_case_type character varying(20),
    test_case_time character varying(10)
);


ALTER TABLE result_test_cases OWNER TO postgres;

--
-- Name: result_test_steps; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE result_test_steps (
    run_id character varying(100) NOT NULL,
    id integer NOT NULL,
    tc_id character varying(10),
    step_id integer NOT NULL,
    teststepsequence integer,
    test_step_type character varying(20)
);


ALTER TABLE result_test_steps OWNER TO postgres;

--
-- Name: result_test_steps_data; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE result_test_steps_data (
    run_id character varying(100) NOT NULL,
    id integer NOT NULL,
    tcdatasetid character varying(20),
    testdatasetid character varying(20) NOT NULL,
    teststepseq integer NOT NULL
);


ALTER TABLE result_test_steps_data OWNER TO postgres;

--
-- Name: result_test_steps_list; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE result_test_steps_list (
    run_id character varying(100) NOT NULL,
    step_id integer NOT NULL,
    stepname character varying(200) NOT NULL,
    description character varying(200),
    driver character varying(200) NOT NULL,
    steptype character varying(100) NOT NULL,
    data_required boolean,
    stepfeature character varying(200),
    stepenable boolean,
    step_editable boolean,
    case_desc character varying(200),
    expected character varying(200),
    verify_point boolean,
    step_continue boolean,
    estd_time character varying(100),
    automatable character varying,
    created_by character varying,
    modified_by character varying,
    created_date date,
    modified_date date,
    project_id character varying,
    team_id character varying,
    always_run boolean
);


ALTER TABLE result_test_steps_list OWNER TO postgres;

--
-- Name: schedule; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE schedule (
    schedule integer,
    run_test_query text,
    dependency text,
    machine text,
    testers character varying(50),
    email character varying(50),
    milestone character varying(50),
    project_id character varying(10),
    team_id integer,
    run_time character varying(10),
    run_day character varying(10),
    testobjective text
);


ALTER TABLE schedule OWNER TO postgres;

--
-- Name: schedule_run; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE schedule_run (
    id integer NOT NULL,
    schedule_name character varying(50),
    project_id character varying(10),
    team_id integer
);


ALTER TABLE schedule_run OWNER TO postgres;

--
-- Name: schedule_run_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE schedule_run_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE schedule_run_id_seq OWNER TO postgres;

--
-- Name: schedule_run_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE schedule_run_id_seq OWNED BY schedule_run.id;


--
-- Name: task_sections; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE task_sections (
    task_path_id integer NOT NULL,
    task_path ltree NOT NULL
);


ALTER TABLE task_sections OWNER TO postgres;

--
-- Name: task_sections_task_path_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE task_sections_task_path_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE task_sections_task_path_id_seq OWNER TO postgres;

--
-- Name: task_sections_task_path_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE task_sections_task_path_id_seq OWNED BY task_sections.task_path_id;


--
-- Name: taskid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE taskid_seq
    START WITH 42
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE taskid_seq OWNER TO postgres;

--
-- Name: tasks; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tasks (
    tasks_id character varying(10) NOT NULL,
    tasks_title character varying(100) NOT NULL,
    tasks_description text,
    tasks_startingdate date NOT NULL,
    tasks_endingdate date NOT NULL,
    tasks_priority character varying(10),
    tasks_milestone character varying(50),
    tasks_createdby character varying(40) NOT NULL,
    tasks_creationdate date NOT NULL,
    tasks_modifiedby character varying(40) NOT NULL,
    tasks_modifydate date NOT NULL,
    parent_id character varying(10),
    status character varying(30),
    tester character varying(10),
    project_id character varying,
    team_id character varying,
    private boolean
);


ALTER TABLE tasks OWNER TO postgres;

--
-- Name: tc_attachement; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE tc_attachement (
    tc_id character varying(10),
    file_path character varying(300),
    file_name character varying(300),
    file_type character varying(10)
);


ALTER TABLE tc_attachement OWNER TO postgres;

--
-- Name: team; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE team (
    id integer NOT NULL,
    team_name character varying(50),
    project_id character varying(10)
);


ALTER TABLE team OWNER TO postgres;

--
-- Name: team_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE team_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE team_id_seq OWNER TO postgres;

--
-- Name: team_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE team_id_seq OWNED BY team.id;


--
-- Name: team_info; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE team_info (
    team_id integer,
    user_id character varying(10)
);


ALTER TABLE team_info OWNER TO postgres;

--
-- Name: team_wise_settings; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE team_wise_settings (
    project_id character varying(10),
    team_id integer,
    parameters integer,
    type character varying(100)
);


ALTER TABLE team_wise_settings OWNER TO postgres;

--
-- Name: test_cases; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_cases (
    tc_id character varying(10) NOT NULL,
    tc_name character varying(100) NOT NULL,
    tc_type character varying(10) NOT NULL,
    tc_executiontype character varying(20),
    tc_priority character varying(10),
    tc_localization character varying(10) NOT NULL,
    tc_createdby character varying(40) NOT NULL,
    tc_creationdate date NOT NULL,
    tc_modifiedby character varying(40) NOT NULL,
    tc_modifydate date NOT NULL,
    defectid character varying(15),
    prd_no character varying(15),
    test_case_type character varying(20),
    test_case_time character varying(10)
);


ALTER TABLE test_cases OWNER TO postgres;

--
-- Name: COLUMN test_cases.tc_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_cases.tc_id IS 'Test Case id for referenceing a test case';


--
-- Name: COLUMN test_cases.tc_name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_cases.tc_name IS 'Test Case Name';


--
-- Name: COLUMN test_cases.tc_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_cases.tc_type IS 'Test Case Type (ie. Auto, Perfor)';


--
-- Name: COLUMN test_cases.tc_localization; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_cases.tc_localization IS 'Test Case Localization (yes, no)';


--
-- Name: COLUMN test_cases.tc_createdby; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_cases.tc_createdby IS 'name of the person who created the test case';


--
-- Name: COLUMN test_cases.tc_creationdate; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_cases.tc_creationdate IS 'Creation Date';


--
-- Name: COLUMN test_cases.tc_modifiedby; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_cases.tc_modifiedby IS 'Person who last modified the test case';


--
-- Name: COLUMN test_cases.tc_modifydate; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_cases.tc_modifydate IS 'Modification Date';


--
-- Name: test; Type: VIEW; Schema: public; Owner: postgres
--

CREATE VIEW test AS
 SELECT testcases.tc_id,
    testcases.tc_name,
    testcases.tc_type,
    testcases.tc_executiontype,
    testcases.tc_priority,
    testcases.tc_localization,
    testcases.tc_createdby,
    testcases.tc_creationdate,
    testcases.tc_modifiedby,
    testcases.tc_modifydate,
    testcases.defectid,
    testcases.prd_no
   FROM test_cases testcases;


ALTER TABLE test OWNER TO postgres;

--
-- Name: test_case_datasets; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_case_datasets (
    tcdatasetid character varying(20) NOT NULL,
    tc_id character varying(10),
    execornot character varying(10) NOT NULL,
    data_type text NOT NULL
);


ALTER TABLE test_case_datasets OWNER TO postgres;

--
-- Name: COLUMN test_case_datasets.tcdatasetid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_datasets.tcdatasetid IS 'Test Case Data Set ID';


--
-- Name: COLUMN test_case_datasets.tc_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_datasets.tc_id IS 'Test Case ID';


--
-- Name: COLUMN test_case_datasets.execornot; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_datasets.execornot IS 'Execute Test Case = Yes or No';


--
-- Name: COLUMN test_case_datasets.data_type; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_datasets.data_type IS 'Default';


--
-- Name: testresults_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE testresults_id_seq
    START WITH 821
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE testresults_id_seq OWNER TO postgres;

--
-- Name: test_case_results; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_case_results (
    id integer DEFAULT nextval('testresults_id_seq'::regclass) NOT NULL,
    run_id character varying(100) NOT NULL,
    tc_id character varying(20) NOT NULL,
    status character varying(20),
    teststarttime timestamp without time zone,
    testendtime timestamp without time zone,
    duration interval,
    failreason character varying(200),
    faildetail text,
    logid character varying(150),
    screenshotsid character varying(40),
    automationlogid character varying(40)
);


ALTER TABLE test_case_results OWNER TO postgres;

--
-- Name: COLUMN test_case_results.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_results.id IS 'Database index use only';


--
-- Name: COLUMN test_case_results.run_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_results.run_id IS 'Run ID for the Current Test Run';


--
-- Name: COLUMN test_case_results.tc_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_results.tc_id IS 'Test Case ID';


--
-- Name: COLUMN test_case_results.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_results.status IS 'Status = (In-Progress, Submitted, Failed, Passed)';


--
-- Name: COLUMN test_case_results.teststarttime; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_results.teststarttime IS 'Test Start Time';


--
-- Name: COLUMN test_case_results.testendtime; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_results.testendtime IS 'Test End Time';


--
-- Name: COLUMN test_case_results.duration; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_results.duration IS 'Duration of Test Case to complete';


--
-- Name: COLUMN test_case_results.logid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_results.logid IS 'location of log file (zipped format)';


--
-- Name: test_case_tag; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_case_tag (
    tc_id character varying(10) NOT NULL,
    name character varying(100) NOT NULL,
    property character varying(100) NOT NULL
);


ALTER TABLE test_case_tag OWNER TO postgres;

--
-- Name: COLUMN test_case_tag.tc_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_tag.tc_id IS 'Test Case ID';


--
-- Name: COLUMN test_case_tag.name; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_case_tag.name IS 'Tag Valule';


--
-- Name: test_env_results; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_env_results (
    id integer NOT NULL,
    run_id text NOT NULL,
    tester_id character varying(100) NOT NULL,
    status character varying(20),
    teststarttime timestamp without time zone,
    testendtime timestamp without time zone,
    duration interval,
    rundescription character varying(200)
);


ALTER TABLE test_env_results OWNER TO postgres;

--
-- Name: COLUMN test_env_results.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_env_results.id IS 'Database index use only';


--
-- Name: COLUMN test_env_results.run_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_env_results.run_id IS 'Run ID for the Current Test Run';


--
-- Name: COLUMN test_env_results.tester_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_env_results.tester_id IS 'Tester User ID';


--
-- Name: COLUMN test_env_results.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_env_results.status IS 'Status (In-Progress, Complete, Failed, Passed, Submitted)';


--
-- Name: COLUMN test_env_results.teststarttime; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_env_results.teststarttime IS 'Test Start Time';


--
-- Name: COLUMN test_env_results.testendtime; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_env_results.testendtime IS 'Test End Time';


--
-- Name: COLUMN test_env_results.duration; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_env_results.duration IS 'Duration of Test Case';


--
-- Name: COLUMN test_env_results.rundescription; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_env_results.rundescription IS 'Description of the Test Run (test run parameter from the web site)';


--
-- Name: test_run; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_run (
    id integer NOT NULL,
    run_id character varying(100) NOT NULL,
    tc_id character varying(20) NOT NULL,
    status character varying(20),
    executiontime date,
    test_order integer,
    copy_status boolean
);


ALTER TABLE test_run OWNER TO postgres;

--
-- Name: COLUMN test_run.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run.id IS 'Database index use only';


--
-- Name: COLUMN test_run.run_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run.run_id IS 'Run ID for the Current Test Run';


--
-- Name: COLUMN test_run.tc_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run.tc_id IS 'Test Case ID';


--
-- Name: test_run_env; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_run_env (
    id integer NOT NULL,
    run_id character varying(100),
    rundescription character varying(200),
    tester_id character varying(100) NOT NULL,
    status character varying(20),
    last_updated_time character varying(255),
    machine_ip character varying(30),
    email_notification text,
    test_objective character varying(50),
    assigned_tester character varying(50),
    run_type character varying(50),
    test_milestone character varying(100),
    branch_version character varying(100),
    start_date date,
    end_date date,
    email_flag boolean
);


ALTER TABLE test_run_env OWNER TO postgres;

--
-- Name: COLUMN test_run_env.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run_env.id IS 'Database index use only';


--
-- Name: COLUMN test_run_env.run_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run_env.run_id IS 'Run ID for the Current Test Run';


--
-- Name: COLUMN test_run_env.rundescription; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run_env.rundescription IS 'Description of the Test Run (test run parameter from the web site)';


--
-- Name: COLUMN test_run_env.tester_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run_env.tester_id IS 'User ID of Tester';


--
-- Name: COLUMN test_run_env.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run_env.status IS 'Status (Cancelled, Unassigned, In-Progress, Completed)';


--
-- Name: COLUMN test_run_env.last_updated_time; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run_env.last_updated_time IS 'timestamp for last update';


--
-- Name: COLUMN test_run_env.machine_ip; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run_env.machine_ip IS 'IP Address of SUT.';


--
-- Name: COLUMN test_run_env.email_notification; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_run_env.email_notification IS 'E-mail Notification';


--
-- Name: test_set_order; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_set_order (
    tc_id character varying(10),
    index integer,
    set_id integer
);


ALTER TABLE test_set_order OWNER TO postgres;

--
-- Name: teststepresults_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE teststepresults_id_seq
    START WITH 2697
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE teststepresults_id_seq OWNER TO postgres;

--
-- Name: test_step_results; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_step_results (
    id integer DEFAULT nextval('teststepresults_id_seq'::regclass) NOT NULL,
    run_id character varying(100) NOT NULL,
    tc_id character varying(20) NOT NULL,
    teststep_id integer NOT NULL,
    status character varying(20),
    stepstarttime timestamp without time zone,
    stependtime timestamp without time zone,
    duration interval,
    failreason character varying(200),
    faildetail text,
    logid character varying(100),
    start_memory character varying(100),
    end_memory character varying(100),
    memory_consumed character varying(100),
    teststepsequence integer,
    testcaseresulttindex integer
);


ALTER TABLE test_step_results OWNER TO postgres;

--
-- Name: COLUMN test_step_results.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.id IS 'Database index use only';


--
-- Name: COLUMN test_step_results.run_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.run_id IS 'Run ID for the Current Test Run';


--
-- Name: COLUMN test_step_results.tc_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.tc_id IS 'Test Case ID';


--
-- Name: COLUMN test_step_results.teststep_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.teststep_id IS 'Test Step ID';


--
-- Name: COLUMN test_step_results.status; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.status IS 'Test Step Status (Pass, Fail, In-Progress)';


--
-- Name: COLUMN test_step_results.stepstarttime; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.stepstarttime IS 'Start Time of Test Step';


--
-- Name: COLUMN test_step_results.stependtime; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.stependtime IS 'End Time of Test Step';


--
-- Name: COLUMN test_step_results.duration; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.duration IS 'Duration of Test Step';


--
-- Name: COLUMN test_step_results.memory_consumed; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.memory_consumed IS 'memory consumtion metric';


--
-- Name: COLUMN test_step_results.teststepsequence; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.teststepsequence IS 'Test Step Sequence Number';


--
-- Name: COLUMN test_step_results.testcaseresulttindex; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_step_results.testcaseresulttindex IS 'Test Case Results Index';


--
-- Name: teststepstemp_teststepsequence_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE teststepstemp_teststepsequence_seq
    START WITH 10
    INCREMENT BY 10
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE teststepstemp_teststepsequence_seq OWNER TO postgres;

--
-- Name: test_steps; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_steps (
    id integer NOT NULL,
    tc_id character varying(10),
    step_id integer NOT NULL,
    teststepsequence integer DEFAULT nextval('teststepstemp_teststepsequence_seq'::regclass),
    test_step_type character varying(20)
);


ALTER TABLE test_steps OWNER TO postgres;

--
-- Name: COLUMN test_steps.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps.id IS 'Database index use only';


--
-- Name: COLUMN test_steps.tc_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps.tc_id IS 'Test Case ID';


--
-- Name: COLUMN test_steps.step_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps.step_id IS 'Test Step ID (A reference to the test_steps_list of test steps)';


--
-- Name: COLUMN test_steps.teststepsequence; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps.teststepsequence IS 'Test Step Sequence';


--
-- Name: test_steps_data; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_steps_data (
    id integer NOT NULL,
    tcdatasetid character varying(20),
    testdatasetid character varying(20) NOT NULL,
    teststepseq integer NOT NULL
);


ALTER TABLE test_steps_data OWNER TO postgres;

--
-- Name: TABLE test_steps_data; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON TABLE test_steps_data IS 'Contains test step data adn the sequence number

For Example: ';


--
-- Name: COLUMN test_steps_data.id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps_data.id IS 'Database index use only';


--
-- Name: COLUMN test_steps_data.tcdatasetid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps_data.tcdatasetid IS 'Test Case Data Set ID';


--
-- Name: COLUMN test_steps_data.testdatasetid; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps_data.testdatasetid IS 'Test Data Set ID';


--
-- Name: COLUMN test_steps_data.teststepseq; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps_data.teststepseq IS 'Test Step Sequence Number';


--
-- Name: test_steps_list; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE test_steps_list (
    step_id integer NOT NULL,
    stepname character varying(200) NOT NULL,
    description character varying(200),
    driver character varying(200) NOT NULL,
    steptype character varying(100) NOT NULL,
    data_required boolean,
    stepfeature character varying(200),
    stepenable boolean,
    step_editable boolean,
    case_desc character varying(200),
    expected character varying(200),
    verify_point boolean,
    step_continue boolean,
    estd_time character varying(100),
    automatable character varying,
    created_by character varying,
    modified_by character varying,
    created_date date,
    modified_date date,
    project_id character varying,
    team_id character varying,
    always_run boolean
);


ALTER TABLE test_steps_list OWNER TO postgres;

--
-- Name: COLUMN test_steps_list.step_id; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps_list.step_id IS 'Database use only.';


--
-- Name: COLUMN test_steps_list.stepname; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps_list.stepname IS 'Name of the Test Stemp

For Example: Open DTS';


--
-- Name: COLUMN test_steps_list.driver; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps_list.driver IS 'Test Step functionality area (Music, Picture, Common, PIM)';


--
-- Name: COLUMN test_steps_list.steptype; Type: COMMENT; Schema: public; Owner: postgres
--

COMMENT ON COLUMN test_steps_list.steptype IS 'Test Step Type (DTS, Client, Common)';


--
-- Name: testcase_testcaseid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE testcase_testcaseid_seq
    START WITH 136
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE testcase_testcaseid_seq OWNER TO postgres;

--
-- Name: testenvresults_id; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE testenvresults_id
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE testenvresults_id OWNER TO postgres;

--
-- Name: testenvresults_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE testenvresults_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE testenvresults_id_seq OWNER TO postgres;

--
-- Name: testenvresults_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE testenvresults_id_seq OWNED BY test_env_results.id;


--
-- Name: testrun_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE testrun_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE testrun_id_seq OWNER TO postgres;

--
-- Name: testrun_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE testrun_id_seq OWNED BY test_run.id;


--
-- Name: testrun_testrunid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE testrun_testrunid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE testrun_testrunid_seq OWNER TO postgres;

--
-- Name: testrunenv_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE testrunenv_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE testrunenv_id_seq OWNER TO postgres;

--
-- Name: testrunenv_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE testrunenv_id_seq OWNED BY test_run_env.id;


--
-- Name: teststepdata_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE teststepdata_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE teststepdata_id_seq OWNER TO postgres;

--
-- Name: teststepdata_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE teststepdata_id_seq OWNED BY test_steps_data.id;


--
-- Name: teststeps_stepsid_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE teststeps_stepsid_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE teststeps_stepsid_seq OWNER TO postgres;

--
-- Name: teststepslist_step_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE teststepslist_step_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE teststepslist_step_id_seq OWNER TO postgres;

--
-- Name: teststepslist_step_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE teststepslist_step_id_seq OWNED BY test_steps_list.step_id;


--
-- Name: teststepstemp_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE teststepstemp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE teststepstemp_id_seq OWNER TO postgres;

--
-- Name: teststepstemp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE teststepstemp_id_seq OWNED BY test_steps.id;


--
-- Name: user_info; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE user_info (
    username character varying(255) NOT NULL,
    password character varying(255),
    full_name character varying(511),
    profile_picture_name character varying(150)
);


ALTER TABLE user_info OWNER TO postgres;

--
-- Name: user_project_map; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE user_project_map (
    user_id integer,
    project_id character varying(10)
);


ALTER TABLE user_project_map OWNER TO postgres;

--
-- Name: versions; Type: TABLE; Schema: public; Owner: postgres; Tablespace: 
--

CREATE TABLE versions (
    id integer,
    version_name character varying(50)
);


ALTER TABLE versions OWNER TO postgres;

--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY branch ALTER COLUMN id SET DEFAULT nextval('branch_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY config_values ALTER COLUMN id SET DEFAULT nextval('config_values_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY daily_build_status ALTER COLUMN id SET DEFAULT nextval('daily_build_status_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY dependency ALTER COLUMN id SET DEFAULT nextval('dependency_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY dependency_name ALTER COLUMN id SET DEFAULT nextval('dependency_name_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY django_migrations ALTER COLUMN id SET DEFAULT nextval('django_migrations_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY drivers ALTER COLUMN id SET DEFAULT nextval('drivers_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY email_config ALTER COLUMN id SET DEFAULT nextval('email_config_id_seq'::regclass);


--
-- Name: executionlogid; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY execution_log ALTER COLUMN executionlogid SET DEFAULT nextval('executionlog_executionlogid_seq'::regclass);


--
-- Name: user_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY permitted_user_list ALTER COLUMN user_id SET DEFAULT nextval('permitted_user_list_user_id_seq'::regclass);


--
-- Name: feature_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY product_features ALTER COLUMN feature_id SET DEFAULT nextval('feature_id_seq'::regclass);


--
-- Name: section_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY product_sections ALTER COLUMN section_id SET DEFAULT nextval('product_sections_section_id_seq'::regclass);


--
-- Name: requirement_path_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY requirement_sections ALTER COLUMN requirement_path_id SET DEFAULT nextval('requirement_sections_requirement_path_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY schedule_run ALTER COLUMN id SET DEFAULT nextval('schedule_run_id_seq'::regclass);


--
-- Name: task_path_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY task_sections ALTER COLUMN task_path_id SET DEFAULT nextval('task_sections_task_path_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY team ALTER COLUMN id SET DEFAULT nextval('team_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_env_results ALTER COLUMN id SET DEFAULT nextval('testenvresults_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_run ALTER COLUMN id SET DEFAULT nextval('testrun_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_run_env ALTER COLUMN id SET DEFAULT nextval('testrunenv_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_steps ALTER COLUMN id SET DEFAULT nextval('teststepstemp_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_steps_data ALTER COLUMN id SET DEFAULT nextval('teststepdata_id_seq'::regclass);


--
-- Name: step_id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_steps_list ALTER COLUMN step_id SET DEFAULT nextval('teststepslist_step_id_seq'::regclass);


--
-- Name: branch_branch_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY branch
    ADD CONSTRAINT branch_branch_name_key UNIQUE (branch_name, project_id, team_id);


--
-- Name: comment_attachment_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY comment_attachment
    ADD CONSTRAINT comment_attachment_pkey PRIMARY KEY (comment_id);


--
-- Name: comment_track_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY comment_track
    ADD CONSTRAINT comment_track_pkey PRIMARY KEY (child_comment);


--
-- Name: comments_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY comments
    ADD CONSTRAINT comments_pkey PRIMARY KEY (comment_id);


--
-- Name: config_values_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY config_values
    ADD CONSTRAINT config_values_pkey PRIMARY KEY (type, value);


--
-- Name: container_type_data_dataid_curname_newname_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY container_type_data
    ADD CONSTRAINT container_type_data_dataid_curname_newname_key UNIQUE (dataid, curname, newname);


--
-- Name: daily_build_user_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY daily_build_status
    ADD CONSTRAINT daily_build_user_pkey PRIMARY KEY (id);


--
-- Name: default_choice_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY default_choice
    ADD CONSTRAINT default_choice_pkey PRIMARY KEY (user_id);


--
-- Name: django_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY django_migrations
    ADD CONSTRAINT django_migrations_pkey PRIMARY KEY (id);


--
-- Name: executionlog_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY execution_log
    ADD CONSTRAINT executionlog_pkey PRIMARY KEY (executionlogid);


--
-- Name: labelid_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY labels
    ADD CONSTRAINT labelid_pkey PRIMARY KEY (label_id);


--
-- Name: permitted_user_list_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY permitted_user_list
    ADD CONSTRAINT permitted_user_list_pkey PRIMARY KEY (user_id);


--
-- Name: pim_master_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY master_data
    ADD CONSTRAINT pim_master_data_pkey PRIMARY KEY (id, field, value);


--
-- Name: pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY email_config
    ADD CONSTRAINT pkey PRIMARY KEY (id);


--
-- Name: playlistdata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY container_type_data
    ADD CONSTRAINT playlistdata_pkey PRIMARY KEY (id);


--
-- Name: product_sections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY product_sections
    ADD CONSTRAINT product_sections_pkey PRIMARY KEY (section_id);


--
-- Name: projects_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projects
    ADD CONSTRAINT projects_key UNIQUE (project_id, project_name);


--
-- Name: projects_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY projects
    ADD CONSTRAINT projects_pkey PRIMARY KEY (project_id);


--
-- Name: requirement_sections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY requirement_sections
    ADD CONSTRAINT requirement_sections_pkey PRIMARY KEY (requirement_path_id);


--
-- Name: requirements_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY requirements
    ADD CONSTRAINT requirements_key UNIQUE (requirement_id, requirement_title);


--
-- Name: requirements_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY requirements
    ADD CONSTRAINT requirements_pkey PRIMARY KEY (requirement_id);


--
-- Name: result_container_type_data_dataid_curname_newname_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_container_type_data
    ADD CONSTRAINT result_container_type_data_dataid_curname_newname_key UNIQUE (run_id, dataid, curname, newname);


--
-- Name: result_container_type_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_container_type_data
    ADD CONSTRAINT result_container_type_data_pkey PRIMARY KEY (run_id, id);


--
-- Name: result_master_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_master_data
    ADD CONSTRAINT result_master_data_pkey PRIMARY KEY (run_id, id, field, value);


--
-- Name: result_test_case_datasets_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_test_case_datasets
    ADD CONSTRAINT result_test_case_datasets_pkey PRIMARY KEY (run_id, tcdatasetid);


--
-- Name: resulttestcases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_test_cases
    ADD CONSTRAINT resulttestcases_pkey PRIMARY KEY (run_id, tc_id);


--
-- Name: resulttestcasetag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_test_case_tag
    ADD CONSTRAINT resulttestcasetag_pkey PRIMARY KEY (run_id, tc_id, name, property);


--
-- Name: resultteststepdata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_test_steps_data
    ADD CONSTRAINT resultteststepdata_pkey PRIMARY KEY (run_id, id);


--
-- Name: resultteststepslist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_test_steps_list
    ADD CONSTRAINT resultteststepslist_pkey PRIMARY KEY (run_id, step_id);


--
-- Name: resultteststepstemp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_test_steps
    ADD CONSTRAINT resultteststepstemp_pkey PRIMARY KEY (run_id, id);


--
-- Name: resultteststepstemp_tc_id_step_id_teststepsequence_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY result_test_steps
    ADD CONSTRAINT resultteststepstemp_tc_id_step_id_teststepsequence_key UNIQUE (run_id, tc_id, step_id, teststepsequence);


--
-- Name: schedule_run_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY schedule_run
    ADD CONSTRAINT schedule_run_pkey PRIMARY KEY (id);


--
-- Name: task_sections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY task_sections
    ADD CONSTRAINT task_sections_pkey PRIMARY KEY (task_path_id);


--
-- Name: tasks_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tasks
    ADD CONSTRAINT tasks_key UNIQUE (tasks_id, tasks_title);


--
-- Name: tasks_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY tasks
    ADD CONSTRAINT tasks_pkey PRIMARY KEY (tasks_id);


--
-- Name: tcdataset_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_case_datasets
    ADD CONSTRAINT tcdataset_pkey PRIMARY KEY (tcdatasetid);


--
-- Name: team_project; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY team
    ADD CONSTRAINT team_project UNIQUE (team_name, project_id);


--
-- Name: testcases_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_cases
    ADD CONSTRAINT testcases_pkey PRIMARY KEY (tc_id);


--
-- Name: testcasetag_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_case_tag
    ADD CONSTRAINT testcasetag_pkey PRIMARY KEY (tc_id, name, property);


--
-- Name: testenvresults_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_env_results
    ADD CONSTRAINT testenvresults_pkey PRIMARY KEY (id);


--
-- Name: testresults_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_case_results
    ADD CONSTRAINT testresults_pkey PRIMARY KEY (id);


--
-- Name: testrun_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_run
    ADD CONSTRAINT testrun_pkey PRIMARY KEY (id);


--
-- Name: testrunenv_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_run_env
    ADD CONSTRAINT testrunenv_pkey PRIMARY KEY (id);


--
-- Name: teststepdata_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_steps_data
    ADD CONSTRAINT teststepdata_pkey PRIMARY KEY (id);


--
-- Name: teststepresults_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_step_results
    ADD CONSTRAINT teststepresults_pkey PRIMARY KEY (id);


--
-- Name: teststepslist_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_steps_list
    ADD CONSTRAINT teststepslist_pkey PRIMARY KEY (step_id);


--
-- Name: teststepstemp_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_steps
    ADD CONSTRAINT teststepstemp_pkey PRIMARY KEY (id);


--
-- Name: teststepstemp_tc_id_step_id_teststepsequence_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY test_steps
    ADD CONSTRAINT teststepstemp_tc_id_step_id_teststepsequence_key UNIQUE (tc_id, step_id, teststepsequence);


--
-- Name: unique_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY branch_management
    ADD CONSTRAINT unique_key UNIQUE (project_id, team_id, branch);


--
-- Name: unique_name; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY dependency
    ADD CONSTRAINT unique_name UNIQUE (dependency_name, project_id, team_id);


--
-- Name: unique_name_feature; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY product_features
    ADD CONSTRAINT unique_name_feature UNIQUE (feature_path, project_id, team_id);


--
-- Name: unique_tuple; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY dependency_management
    ADD CONSTRAINT unique_tuple UNIQUE (project_id, team_id, dependency);


--
-- Name: unique_tuple_dependency_values; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY dependency_values
    ADD CONSTRAINT unique_tuple_dependency_values UNIQUE (id, version, bit_name);


--
-- Name: unique_tuple_name; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY dependency_name
    ADD CONSTRAINT unique_tuple_name UNIQUE (name, dependency_id);


--
-- Name: unique_user_pojrect_map; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY user_project_map
    ADD CONSTRAINT unique_user_pojrect_map UNIQUE (user_id, project_id);


--
-- Name: user; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY user_info
    ADD CONSTRAINT "user" PRIMARY KEY (username);


--
-- Name: versions_version_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres; Tablespace: 
--

ALTER TABLE ONLY versions
    ADD CONSTRAINT versions_version_name_key UNIQUE (id, version_name);


--
-- Name: performanceresults_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY performance_results
    ADD CONSTRAINT performanceresults_tc_id_fkey FOREIGN KEY (run_id, tc_id) REFERENCES result_test_cases(run_id, tc_id);


--
-- Name: project_team_map; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY project_team_map
    ADD CONSTRAINT project_team_map FOREIGN KEY (project_id) REFERENCES projects(project_id);


--
-- Name: result_test_case_datasets_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY result_test_case_datasets
    ADD CONSTRAINT result_test_case_datasets_tc_id_fkey FOREIGN KEY (run_id, tc_id) REFERENCES result_test_cases(run_id, tc_id);


--
-- Name: resulttestcasetag_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY result_test_case_tag
    ADD CONSTRAINT resulttestcasetag_tc_id_fkey FOREIGN KEY (run_id, tc_id) REFERENCES result_test_cases(run_id, tc_id);


--
-- Name: resultteststepdata_tcdatasetid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY result_test_steps_data
    ADD CONSTRAINT resultteststepdata_tcdatasetid_fkey FOREIGN KEY (run_id, tcdatasetid) REFERENCES result_test_case_datasets(run_id, tcdatasetid);


--
-- Name: resultteststepstemp_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY result_test_steps
    ADD CONSTRAINT resultteststepstemp_tc_id_fkey FOREIGN KEY (run_id, tc_id) REFERENCES result_test_cases(run_id, tc_id);


--
-- Name: schedule_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY schedule
    ADD CONSTRAINT schedule_fkey FOREIGN KEY (schedule) REFERENCES schedule_run(id);


--
-- Name: tc_attachement_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY tc_attachement
    ADD CONSTRAINT tc_attachement_tc_id_fkey FOREIGN KEY (tc_id) REFERENCES test_cases(tc_id);


--
-- Name: tcdataset_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_case_datasets
    ADD CONSTRAINT tcdataset_tc_id_fkey FOREIGN KEY (tc_id) REFERENCES test_cases(tc_id);


--
-- Name: testcasetag_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_case_tag
    ADD CONSTRAINT testcasetag_tc_id_fkey FOREIGN KEY (tc_id) REFERENCES test_cases(tc_id);


--
-- Name: testresults_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_case_results
    ADD CONSTRAINT testresults_tc_id_fkey FOREIGN KEY (run_id, tc_id) REFERENCES result_test_cases(run_id, tc_id);


--
-- Name: testrun_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_run
    ADD CONSTRAINT testrun_tc_id_fkey FOREIGN KEY (run_id, tc_id) REFERENCES result_test_cases(run_id, tc_id);


--
-- Name: teststepdata_tcdatasetid_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_steps_data
    ADD CONSTRAINT teststepdata_tcdatasetid_fkey FOREIGN KEY (tcdatasetid) REFERENCES test_case_datasets(tcdatasetid);


--
-- Name: teststepresults_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_step_results
    ADD CONSTRAINT teststepresults_tc_id_fkey FOREIGN KEY (run_id, tc_id) REFERENCES result_test_cases(run_id, tc_id);


--
-- Name: teststepstemp_step_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_steps
    ADD CONSTRAINT teststepstemp_step_id_fkey FOREIGN KEY (step_id) REFERENCES test_steps_list(step_id);


--
-- Name: teststepstemp_step_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY result_test_steps
    ADD CONSTRAINT teststepstemp_step_id_fkey FOREIGN KEY (run_id, step_id) REFERENCES result_test_steps_list(run_id, step_id);


--
-- Name: teststepstemp_tc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY test_steps
    ADD CONSTRAINT teststepstemp_tc_id_fkey FOREIGN KEY (tc_id) REFERENCES test_cases(tc_id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- Name: container_type_data; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE container_type_data FROM PUBLIC;
REVOKE ALL ON TABLE container_type_data FROM postgres;
GRANT ALL ON TABLE container_type_data TO postgres;
GRANT ALL ON TABLE container_type_data TO PUBLIC;


--
-- Name: execution_log; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE execution_log FROM PUBLIC;
REVOKE ALL ON TABLE execution_log FROM postgres;
GRANT ALL ON TABLE execution_log TO postgres;
GRANT ALL ON TABLE execution_log TO PUBLIC;


--
-- Name: permitted_user_list; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE permitted_user_list FROM PUBLIC;
REVOKE ALL ON TABLE permitted_user_list FROM postgres;
GRANT ALL ON TABLE permitted_user_list TO postgres;
GRANT ALL ON TABLE permitted_user_list TO PUBLIC;


--
-- Name: projects; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE projects FROM PUBLIC;
REVOKE ALL ON TABLE projects FROM postgres;
GRANT ALL ON TABLE projects TO postgres;
GRANT ALL ON TABLE projects TO PUBLIC;


--
-- Name: requirements; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE requirements FROM PUBLIC;
REVOKE ALL ON TABLE requirements FROM postgres;
GRANT ALL ON TABLE requirements TO postgres;
GRANT ALL ON TABLE requirements TO PUBLIC;


--
-- Name: tasks; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE tasks FROM PUBLIC;
REVOKE ALL ON TABLE tasks FROM postgres;
GRANT ALL ON TABLE tasks TO postgres;
GRANT ALL ON TABLE tasks TO PUBLIC;


--
-- Name: test_cases; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_cases FROM PUBLIC;
REVOKE ALL ON TABLE test_cases FROM postgres;
GRANT ALL ON TABLE test_cases TO postgres;
GRANT ALL ON TABLE test_cases TO PUBLIC;


--
-- Name: test_case_datasets; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_case_datasets FROM PUBLIC;
REVOKE ALL ON TABLE test_case_datasets FROM postgres;
GRANT ALL ON TABLE test_case_datasets TO postgres;
GRANT ALL ON TABLE test_case_datasets TO PUBLIC;


--
-- Name: test_case_results; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_case_results FROM PUBLIC;
REVOKE ALL ON TABLE test_case_results FROM postgres;
GRANT ALL ON TABLE test_case_results TO postgres;
GRANT ALL ON TABLE test_case_results TO PUBLIC;


--
-- Name: test_env_results; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_env_results FROM PUBLIC;
REVOKE ALL ON TABLE test_env_results FROM postgres;
GRANT ALL ON TABLE test_env_results TO postgres;
GRANT ALL ON TABLE test_env_results TO PUBLIC;


--
-- Name: test_run; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_run FROM PUBLIC;
REVOKE ALL ON TABLE test_run FROM postgres;
GRANT ALL ON TABLE test_run TO postgres;
GRANT ALL ON TABLE test_run TO PUBLIC;


--
-- Name: test_run_env; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_run_env FROM PUBLIC;
REVOKE ALL ON TABLE test_run_env FROM postgres;
GRANT ALL ON TABLE test_run_env TO postgres;
GRANT ALL ON TABLE test_run_env TO PUBLIC;


--
-- Name: test_step_results; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_step_results FROM PUBLIC;
REVOKE ALL ON TABLE test_step_results FROM postgres;
GRANT ALL ON TABLE test_step_results TO postgres;
GRANT ALL ON TABLE test_step_results TO PUBLIC;


--
-- Name: test_steps; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_steps FROM PUBLIC;
REVOKE ALL ON TABLE test_steps FROM postgres;
GRANT ALL ON TABLE test_steps TO postgres;
GRANT ALL ON TABLE test_steps TO PUBLIC;


--
-- Name: test_steps_list; Type: ACL; Schema: public; Owner: postgres
--

REVOKE ALL ON TABLE test_steps_list FROM PUBLIC;
REVOKE ALL ON TABLE test_steps_list FROM postgres;
GRANT ALL ON TABLE test_steps_list TO postgres;
GRANT ALL ON TABLE test_steps_list TO PUBLIC;


--
-- PostgreSQL database dump complete
--


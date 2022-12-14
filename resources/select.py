smev_wait_send = "select count(*) " \
                 "from smev_wait_send"

smev_request_sending = "select count(*) " \
                       "from smev_request_sending " \
                       "inner join SMEV_REQUEST_VIEW " \
                       "on SMEV_REQUEST_VIEW.ID = smev_request_sending.smev_request_id " \
                       "inner join smev_wait_send " \
                       "on smev_wait_send.smev_request_id = SMEV_REQUEST_VIEW.ID "

smev_report = "select avg(SMEV_REQUEST_VIEW.SMEV_REGLAM_ID), " \
              "SMEV_REQUEST_VIEW.ReglamName, " \
              "count(SMEV_REQUEST_VIEW.ReglamName) " \
              "from smev_request_sending " \
              "inner join SMEV_REQUEST_VIEW " \
              "on SMEV_REQUEST_VIEW.ID = smev_request_sending.smev_request_id " \
              "inner join smev_wait_send " \
              "on smev_wait_send.smev_request_id = SMEV_REQUEST_VIEW.ID " \
              "where smev_wait_send.after_dt >= '20000723' " \
              "group by SMEV_REQUEST_VIEW.ReglamName " \
              "order by count(SMEV_REQUEST_VIEW.ReglamName) desc"

smev_report_full = "select avg(SMEV_REQUEST_VIEW.SMEV_REGLAM_ID), SMEV_REQUEST_VIEW.ReglamName, count(SMEV_REQUEST_VIEW.ReglamName) " \
                   "from smev_wait_send inner join SMEV_REQUEST_VIEW on SMEV_REQUEST_VIEW.ID = smev_wait_send.smev_request_id " \
                   "where smev_wait_send.after_dt >= '20000723' group by SMEV_REQUEST_VIEW.ReglamName order by count(SMEV_REQUEST_VIEW.ReglamName) desc"

err_count_smev = "select distinct count(*) " \
                 "from EService_Request " \
                 "right join smev3_mes " \
                 "on smev3_mes.mesid = EService_Request.SMEV3MESSAGEID " \
                 "where EService_Request.requestId is null " \
                 "and sendstate = 2 " \
                 "and senddate >= DATEADD(day,-5, GETDATE()) " \
                 "and smev3_mes.mesid is not null"

err_count_pgu = "select distinct count(*) " \
                "from EService_Request " \
                "inner join smev3_mes " \
                "on smev3_mes.mesid = EService_Request.SMEV3MESSAGEID " \
                "where smev3_mes.sendstate = 2 " \
                "and EService_Request.requestId is not null " \
                "and senddate >= DATEADD(day,-20, GETDATE())"

smev_err = "select distinct " \
           "lower(smev3_mes.mesid) as '??????????????????', " \
           "smev3_mes.senddate as '???????? ??????????????????', " \
           "SMEV3_MESSAGE_TYPE.NAIMP as '?????? ??????????????'," \
           "smev3_mes.namespaceuri  as '????????????'," \
           "smev3_mes.comment as '??????????'," \
           "SMEV3_ENVIRONMENT_TYPE.NKOD as '?????? ??????????' " \
           "from smev3_mes " \
           "inner join SMEV3_MESSAGE_TYPE " \
           "on smev3_mes.reqtype = SMEV3_MESSAGE_TYPE.ID " \
           "inner join SMEV3_ENVIRONMENT_TYPE " \
           "on smev3_mes.environmenttype = SMEV3_ENVIRONMENT_TYPE.ID " \
           "and sendstate = 2 and senddate >= DATEADD(day,-5, GETDATE()) " \
           "and smev3_mes.mesid is not null " \
           "order by smev3_mes.senddate desc"

smev_err_heal = "select distinct" \
                " lower(smev3_mes.mesid) as '??????????????????', " \
                "smev3_mes.senddate as '???????? ??????????????????', " \
                "SMEV3_MESSAGE_TYPE.NAIMP as '?????? ??????????????', " \
                "smev3_mes.namespaceuri  as '????????????', " \
                "smev3_mes.comment as '??????????'," \
                "SMEV3_ENVIRONMENT_TYPE.NKOD as '?????? ??????????' " \
                "from smev3_mes " \
                "inner join SMEV3_MESSAGE_TYPE " \
                "on smev3_mes.reqtype = SMEV3_MESSAGE_TYPE.ID " \
                "inner join SMEV3_ENVIRONMENT_TYPE " \
                "on smev3_mes.environmenttype = SMEV3_ENVIRONMENT_TYPE.ID " \
                "where rowid in (select distinct rowid from smev3_mes " \
                "where rowid in (select distinct rowid from smev3_mes " \
                "where sendstate = 2 and senddate >= DATEADD(day,-5, GETDATE()) " \
                "and smev3_mes.mesid is not null and rowid is not null) " \
                "group by rowid having min(sendstate) > 1) " \
                "order by smev3_mes.senddate desc"

smev_err_req = "select distinct " \
               "EService_Request.requestId as '?????????? ????????????', " \
               "lower(smev3_mes.mesid) as '??????????????????', " \
               "smev3_mes.senddate as '???????? ??????????????????', " \
               "SMEV3_MESSAGE_TYPE.NAIMP as '?????? ??????????????'," \
               "smev3_mes.namespaceuri  as '????????????', " \
               "smev3_mes.comment as '??????????', " \
               "SMEV3_ENVIRONMENT_TYPE.NKOD as '?????? ??????????' " \
               "from EService_Request " \
               "inner join smev3_mes " \
               "on smev3_mes.mesid = EService_Request.SMEV3MESSAGEID " \
               "inner join SMEV3_ENVIRONMENT_TYPE " \
               "on smev3_mes.environmenttype = SMEV3_ENVIRONMENT_TYPE.ID " \
               "inner join SMEV3_MESSAGE_TYPE " \
               "on smev3_mes.reqtype = SMEV3_MESSAGE_TYPE.ID " \
               "where smev3_mes.sendstate = 2 " \
               "and EService_Request.requestId is not null " \
               "and senddate >= DATEADD(day,-20, GETDATE())" \
               "order by smev3_mes.senddate desc"

smev_err_req_heal = "select EService_Request.requestId as '?????????? ????????????', " \
                    "lower(smev3_mes.mesid) as '??????????????????', " \
                    "smev3_mes.senddate as '???????? ??????????????????', " \
                    "SMEV3_MESSAGE_TYPE.NAIMP as '?????? ??????????????', " \
                    "smev3_mes.namespaceuri  as '????????????', " \
                    "smev3_mes.comment as '??????????', " \
                    "SMEV3_ENVIRONMENT_TYPE.NKOD as '?????? ??????????' " \
                    "from EService_Request " \
                    "inner join smev3_mes " \
                    "on smev3_mes.mesid = EService_Request.SMEV3MESSAGEID " \
                    "inner join SMEV3_MESSAGE_TYPE " \
                    "on smev3_mes.reqtype = SMEV3_MESSAGE_TYPE.ID " \
                    "inner join SMEV3_ENVIRONMENT_TYPE " \
                    "on smev3_mes.environmenttype = SMEV3_ENVIRONMENT_TYPE.ID " \
                    "where mesid in (select metadata_mesid " \
                    "from smev3_mes where mesid in (select metadata_mesid " \
                    "from smev3_mes inner join EService_Request " \
                    "on smev3_mes.mesid = EService_Request.SMEV3MESSAGEID " \
                    "where smev3_mes.sendstate = 2 " \
                    "and senddate >= DATEADD(day,-20, GETDATE()) " \
                    "and mesid is not null) " \
                    "group by metadata_mesid " \
                    "having min(sendstate) > 1 or min(processed+0) > 1) " \
                    "order by smev3_mes.senddate desc"


smev_err_proc = "select" \
                " lower(smev3_mes.mesid) as '??????????????????', " \
                "smev3_mes.senddate as '???????? ??????????????????', " \
                "SMEV3_MESSAGE_TYPE.NAIMP as '?????? ??????????????', " \
                "smev3_mes.namespaceuri  as '????????????', " \
                "smev3_mes.processcomment as '???????????????? ??????????????????', " \
                "SMEV3_ENVIRONMENT_TYPE.NKOD as '?????? ??????????'  " \
                "from smev3_mes inner join SMEV3_MESSAGE_TYPE " \
                "on smev3_mes.reqtype = SMEV3_MESSAGE_TYPE.ID " \
                "inner join SMEV3_ENVIRONMENT_TYPE " \
                "on smev3_mes.environmenttype = SMEV3_ENVIRONMENT_TYPE.ID " \
                "where sendstate = 1 and processed = 'false' " \
                "and senddate >= DATEADD(day,-7, GETDATE())" \
                "order by smev3_mes.senddate desc"


smev_1013 = "select EService_Users.name, count(EService_Users.name) " \
            "from SMEV_SERVICE_TRAVEL_PRIVILEGE_LIP " \
            "inner join F2 on F2.ID = SMEV_SERVICE_TRAVEL_PRIVILEGE_LIP.F2_id " \
            "inner join EService_Users on F2.EService_Users_id = EService_Users.id " \
            "where DATEDIFF(day, SMEV_SERVICE_TRAVEL_PRIVILEGE_LIP.upload_date, GETDATE()) = 1 " \
            "group by EService_Users.name " \
            "order by EService_Users.name"

smev_err_asp = "select distinct requestId as '?????????? ????????????', lower(SMEV3MESSAGEID) as '??????????????????', requestId  as '???????? ??????????????????', senderName as '???? ??????????????????????' from EService_Request where (DATEDIFF(day, EService_Request.requestDate, GETDATE()) = 1 or DATEDIFF(day, EService_Request.requestDate, GETDATE()) = 0) and EService_Request.requestId not like '%_(%' and EService_Request.exportDate is null and DATEDIFF(hour, EService_Request.insertDate, GETDATE()) > 2"

sel = "select SMEV_REQUEST_VIEW.ID, SMEV_REQUEST_VIEW.StateName, SMEV_REQUEST_VIEW.Date_Request, smev3_mes.mesid from SMEV_REQUEST_VIEW inner join smev3_mes on smev3_mes.rowid = SMEV_REQUEST_VIEW.ID where SMEV_REQUEST_VIEW.StateName like '%????????%' and SMEV_REQUEST_VIEW.Date_Request >= DATEADD(day,-4, GETDATE())  and smev3_mes.mesid in (select origmesid from smev3_mes where sendstate = 6)"

#??????????
report_epgu_yest = "select count(*) from eService_Request where requestId not like '%-%' and requestId not like '%_(%' and DATEDIFF(day, requestDate, GETDATE()) = 1"
report_mfc_yest = "select count(*) from eService_Request where requestId like '%-%' and requestId not like '%_(%' and DATEDIFF(day, requestDate, GETDATE()) = 1"
report_gis_yest = "select count(*) from smev3_mes where namespaceuri = 'http://kvs.fri.com/initiative-distribution/1.0.2'and DATEDIFF(day, senddate, GETDATE()) = 1"
report_zags_yest = "select count(*) from smev3_mes where namespaceuri = 'urn://x-artefacts-zags-fatalinf/root/112-52/4.0.1'and DATEDIFF(day, senddate, GETDATE()) = 1"
report_all_yest = "select count(*) from eService_Request where DATEDIFF(day, requestDate, GETDATE()) = 1 and requestId not like '%_(%'"
report_net_yest = "select count(*) from eService_Request where DATEDIFF(day, requestDate, GETDATE()) = 1 and requestId not like '%_(%' and exportDate is null and DATEDIFF(hour, insertDate, GETDATE()) > 2"
report_elk = "select count(distinct reqtype) from smev3_mes where namespaceuri = 'http://epgu.gosuslugi.ru/elk/status/1.0.2' and DATEDIFF(day, senddate, GETDATE()) = 1"

#??????????????
report_epgu_to = "select count(*) from eService_Request where requestId not like '%-%' and requestId not like '%_(%' and DATEDIFF(day, requestDate, GETDATE()) = 0"
report_mfc_to = "select count(*) from eService_Request where requestId like '%-%' and requestId not like '%_(%' and DATEDIFF(day, requestDate, GETDATE()) = 0"
report_gis_to = "select count(*) from smev3_mes where namespaceuri = 'http://kvs.fri.com/initiative-distribution/1.0.2'and DATEDIFF(day, senddate, GETDATE()) = 0"
report_zags_to = "select count(*) from smev3_mes where namespaceuri = 'urn://x-artefacts-zags-fatalinf/root/112-52/4.0.1'and DATEDIFF(day, senddate, GETDATE()) = 0"
report_all_to = "select count(*) from eService_Request where DATEDIFF(day, requestDate, GETDATE()) = 0 and requestId not like '%_(%'"
report_net_to = "select count(*) from eService_Request where DATEDIFF(day, requestDate, GETDATE()) = 0 and requestId not like '%_(%' and exportDate is null and DATEDIFF(hour, insertDate, GETDATE()) > 2"

#????????????
report_gis_week = "select count(*) from smev3_mes where namespaceuri = 'http://kvs.fri.com/initiative-distribution/1.0.2'and senddate >= DATEADD(day,-7, GETDATE())"
report_zags_week = "select count(*) from smev3_mes where namespaceuri = 'urn://x-artefacts-zags-fatalinf/root/112-52/4.0.1'and senddate >= DATEADD(day,-7, GETDATE())"

nob_pgu = "select count(*) from eservice_missing_request where orderdate >= DATEADD(day,-3, GETDATE())"
uszn = "select count(*) from EService_Request where EService_Users_id = 26 and orderdate >= DATEADD(day,-7, GETDATE())"
distr_pgu = "select count(*) from EService_Request where EService_Users_id is null and orderdate >= DATEADD(day,-3, GETDATE())"
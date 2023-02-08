from locust import TaskSet, task, between, events, tag, HttpUser, SequentialTaskSet
from locust.contrib.fasthttp import FastHttpUser
from urllib3 import encode_multipart_formdata
import copy
import requests
import random
import time

# IS_CHECK 控制本次压测是否需要断言，True则断言：断言失败时返回请求失败，False则不断言：status_code>=400才返回请求失败，开启断言后会略微影响请求同并发时的QPS
# 比如未开启断言前，当并发为100时，最高QPS为(达到拐点)：2000，开启断言后，并发100时，QPS只有1980，但对最高QPS没有影响，最高QPS压出来还是2000，只是需要的并发数可能更高点

IS_CHECK = True

headers = dict()
headers[
    "user-auth"] = "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ7XCJleHBpcmVUaW1lU3RhbXBcIjoxNjE4MDgxOTg3NDM0LFwicGhvbmVcIjpcIjEyMzAwMDAwMTM0XCIsXCJyZWdpc3RlclNvdXJjZVwiOjEsXCJ0aW1lc3RhbXBcIjoxNjE3NzIxOTg3NDM0LFwidXNlcklkXCI6MzI2fSJ9.M1mAJH53lRAfsynRyoU75x45ygv5CWJYJs_wjPLD-voCC7td7fRA_fxQXl9ELlfLQXBzKEercINKVwhJ4MkhMKJ7hG-7HGLbvVJvvhGQOmSNfPfjlF-fvslWm6YsgAgEuaeI3H9Tnq5iFzGHEkJBGdCccWRLut8k5t3b1JZw9DA"

backend_headers = dict()
backend_headers[
    "authorization"] = "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiWDdINWVzMVp5eG1tN3o4aDJTOVFiRTRFT2E3aFBvbzZUSXh1S3Zkb3ZPUmRaT0lxbVpnV2R3Qk5OUHFMZDliN1FLK0xwMnhjT3lVSG9HbHFuVCtSbGxOazNmb0hHYnRYcjA0MGN0YlZBcFRZZ3dmWTFWV1ZGM1c1NVptM24wZlRORVloV2dwM0NUb0MwVDNGMkh1U3lUT05kVHZiZlBMdEJZNThvTjQ3bW1YZFpUNTErMDBzWCtiWGN1Z0d1akZHc2Z5TTNDYUhVV293bW5OOE1MNUlxdz09IiwiZXhwIjoxNjMyMTkyMDkyfQ._g1k6HwZwYYJmysCFKmQcdIG3j5gTJYjOuPMw9gbRRY"

comment_headers = dict()
comment_headers[
    "authorization"] = "eyJhbGciOiJIUzI1NiJ9.eyJkYXRhIjoiNEx1ejhGT1M3d1ZwVURpODh2ZEVKeFlKcUNFdVFBT2lLQlc0NHNVanZLa1ZUKzBXM2hhU3cyN1ZFcDc4bS93REtnVHVJQVBhYk13ODFveXNJZUdtR1NGQ0ZiRmhIM1JOR0VjR1RiOFl1SGY2a3pJaGZ1aHlSZ0g3UVdFM3FMbWhvSU05Y0FjbkJjeVJMVC9NdjhDcVVDTGJmZ2ZVWVFtNDhaRGxlU0NEWEJyYlE3R2lVaTQ0RzBwc05vWGhEcmZGL2k4NEdpenFtTzhFcXRCSVpBTWlSUitnK1dzK1ptSUI1U2FQQ1lPVUVNUT0iLCJleHAiOjE2MzMyNjAzMjR9.6DQz6PkJ_R83zH3N6jm5YZf8D-ZyXl71aJHNGa5_kUI"

user_list = [19491561,
             19128264,
             19525592,
             19731432,
             19243003,
             19359038,
             19485363,
             19044973,
             19130257,
             17481363,
             19745008,
             19618419,
             18009100,
             18128679,
             19429523,
             19607039,
             19416703,
             19295204,
             19268999,
             19139913,
             17962719,
             19287340,
             19240335,
             12664563,
             17485523,
             10759941,
             19477136,
             19146777,
             19147015,
             18794405,
             19750720,
             19321721,
             19123753,
             16454319,
             19808556,
             17977773,
             19038487,
             19676824,
             19398932,
             17823445,
             17238371,
             17751125,
             18995562,
             11096732,
             18254760,
             19655766,
             19503823,
             19843518,
             19027988,
             19132557,
             19550876,
             19802381,
             19823286,
             19495124,
             19415681,
             19181801,
             19412592,
             19881204,
             18432599,
             19432369,
             19373720,
             17371373,
             19658449,
             19721006,
             19407345,
             18567141,
             16742784,
             19151121,
             19897879,
             19992044,
             19953909,
             19178373,
             19655828,
             17608022,
             19170068,
             19303533,
             19923687,
             18234255,
             19162644,
             19671111,
             18073202,
             19153860,
             19846225,
             19279608,
             19686925,
             19362145,
             19357870,
             19265755,
             19324133,
             19040127,
             19576900,
             18323738,
             17699794,
             19139040,
             19749390,
             19862235,
             18052670,
             17564227,
             19308407,
             18252469,
             19195060,
             19242238,
             18583196,
             16722008,
             18677410,
             17042836,
             16596384,
             19588648,
             18159358,
             19988376,
             19374943,
             18159358,
             19360671,
             19838374,
             18008754,
             17346474,
             17110096,
             19061592,
             18374345,
             19544873,
             19863089,
             19625710,
             19385935,
             19317219,
             19237942,
             17683067,
             19327484,
             19303310,
             16834253, ]

order_list = ["AI20201226073523416mols",
              "AI20201210183621410k7gp",
              "AI20201227124435369w3u9",
              "AI202101042056516191yz6",
              "AI20201215160224966jy6c",
              "AI20201220091922649aqfq",
              "AI20201225222117266d1uh",
              "AI202012061814409913s44",
              "AI20201210203356227qlfh",
              "AI202010011132196809gd7",
              "AI20210105093236026ef4i",
              "AI20201231012254797i2ii",
              "AI20201024084908385lvnt",
              "AI20201030110833632x719",
              "AI20201223091653149rzns",
              "AI20201230144216458oa3x",
              "AI20201222175558207e2fc",
              "AI20201218104135310nee6",
              "AI20201216220741406llp7",
              "AI20201210234726288l7td",
              "AI20201021124156658lsdx",
              "AI20201217222704684wta0",
              "AI202012151255363550cvc",
              "AI20200911103550092055i",
              "AI20201001153842166083w",
              "AI2020090119545663721lz",
              "AI20201225140806472lo6b",
              "AI20201211063239589kw0u",
              "AI20201211071013918p8gl",
              "AI20201128161150909bpln",
              "AI202101051240233263v9l",
              "AI202012191149570296c0s",
              "AI2020121013442549986zd",
              "AI20201027155128377avp4",
              "AI20210107120431175v7xx",
              "AI20201022125222679qnk6",
              "AI202012060939056518kmo",
              "AI20210102205805656wfhv",
              "AI20201221203925714wuwy",
              "AI20201014220640849ubkr",
              "AI20200921201116785zgun",
              "AI20201011104759399v1ad",
              "AI20201203184127066t72y",
              "AI20201017224927107asys",
              "AI2020110418071395249rr",
              "AI20210101204628093x3rg",
              "AI20201226171118018chau",
              "AI20210108144847339fka4",
              "AI20201205190019112gr6d",
              "AI2020121021260630349bq",
              "AI2020122814104745538gw",
              "AI20210107081616667iviy",
              "AI20210108000731642wo3m",
              "AI202012260957164860knc",
              "AI20201222163703140nln9",
              "AI20201212215719097gcvg",
              "AI20201222124738104hhpc",
              "AI20210109201913666r0q2",
              "AI20201216084803711e2mu",
              "AI202012231157082884xvx",
              "AI20201220223632431exik",
              "AI2020092721270670850cm",
              "AI20210102002554564mno8",
              "AI202101041313332656r31",
              "AI20201222084415656j402",
              "AI202011191811086878uf9",
              "AI20200903124653746x87d",
              "AI20201211113642688y3nu",
              "AI20210110080214248fgrl",
              "AI20210112204855091pa71",
              "AI20210111152449903aflf",
              "AI20201212185514202nhbi",
              "AI202101012046521715nsj",
              "AI202010051934438188fnb",
              "AI202012120801082370axu",
              "AI20201218193452754tdxf",
              "AI20210110220318256jfq2",
              "AI20201103201214251o6lc",
              "AI20201211214407630rrqx",
              "AI20210102144600245dhdx",
              "AI20201027123744159o6wy",
              "AI20201211123011630vw5g",
              "AI20210108171948879qbz5",
              "AI20201217132720972xa0y",
              "AI202101030752360366wd8",
              "AI20201220111558063z2ca",
              "AI20201220084109939pdlk",
              "AI20201216205630860r9ty",
              "AI20201219133917969f8we",
              "AI20201206113035486n6py",
              "AI20201229120642149dy54",
              "AI202011071719205896s1k",
              "AI20201009120028857dgd8",
              "AI20201210234120336u6ue",
              "AI20210105113342787jrvz",
              "AI20210109072433643rvhr",
              "AI20201026104231099r3zd",
              "AI202010040943414073k12",
              "AI20201218225142506mt9o",
              "AI202011041339026164ju3",
              "AI20201213115251863zlw7",
              "AI20201215150437295h8m3",
              "AI20201120154812627uqzk",
              "AI20201112103940103d3ny",
              "AI20201124163337556iuu9",
              "AI20200912202824978xm6t",
              "AI20201130140640785pxg5",
              "AI20201229215206097a2i9",
              "AI20201031215221384lj81",
              "AI202101121345207700jq4",
              "AI20201221012842630jt19",
              "AI20201031215221384lj81",
              "AI20201220102146976ko1c",
              "AI20210108110624272aq5n",
              "AI20201024131308236uha6",
              "AI20200926230135395050z",
              "AI20200915010444025dcou",
              "AI202012071440356587yez",
              "AI20201109181425109ijnj",
              "AI20201228085743760tav0",
              "AI20210109081433633y418",
              "AI202012310849148559x56",
              "AI20201221064751986gv83",
              "AI20201219093939007pprz",
              "AI20201215095936083om6v",
              "AI20201008202510032tqt1",
              "AI202012191611149098953",
              "AI202012181924484007i1q",
              "AI20200910113512125ag01", ]
user_reward_list = [19355806,
                    19600192,
                    19387058,
                    19061621,
                    19742810,
                    19651829,
                    19261871,
                    19245581,
                    19262760,
                    19296507,
                    18474507,
                    19068078,
                    19278397,
                    19171198,
                    18471593,
                    19777804,
                    19407223,
                    19945342,
                    19609242,
                    19308407,
                    18008727,
                    19571266,
                    19771026,
                    19496374,
                    19306799,
                    18324619,
                    19871215,
                    18059057,
                    19809111,
                    18961505,
                    19374723,
                    19471488,
                    18579471,
                    18707278,
                    18817477,
                    19604132,
                    19284281,
                    18209067,
                    17033630,
                    19990084,
                    19160992,
                    19198659,
                    19729930,
                    18132099,
                    19333670,
                    19139058,
                    18854556,
                    19697199,
                    18675770,
                    18103798,
                    19308519,
                    19259277,
                    19426967,
                    19063052,
                    19324685,
                    19949378,
                    19715298,
                    19010519,
                    18528382,
                    19194271,
                    19295732,
                    18653881,
                    19075362,
                    19426328,
                    19785203,
                    19406572,
                    10703693,
                    17819902,
                    19942060,
                    18993413,
                    18056896,
                    17298575,
                    17731377,
                    19598972,
                    19533439,
                    18816965,
                    19074486,
                    17817390,
                    19600946,
                    19511953,
                    16166899,
                    19526648,
                    18322095,
                    18798026,
                    19357233,
                    19876581,
                    19711825,
                    17657157,
                    19657381,
                    19556554,
                    17543073,
                    18525821,
                    18960879,
                    19554305,
                    19321025,
                    19639737,
                    19946678,
                    17658005,
                    19357792,
                    19245154,
                    17509296,
                    19375084,
                    17755789,
                    19606475,
                    12821771,
                    19601910,
                    19085235,
                    19321273,
                    19124757,
                    18158153,
                    19591197,
                    19270940,
                    19299432,
                    18850898,
                    19281737,
                    19368677,
                    19635059,
                    19688615,
                    18413766,
                    19296751,
                    18847886,
                    19556595,
                    19199749,
                    19024056,
                    19745032,
                    18282938,
                    18577158,
                    19949121,
                    19812766,
                    18676848,
                    18236525,
                    19898024,
                    18988047,
                    19645905,
                    17521682,
                    19790597,
                    19421298,
                    19227771,
                    17606813,
                    19942191,
                    19721358,
                    19880206,
                    19741652,
                    16175730,
                    19362269,
                    19723739,
                    19742784,
                    19408634,
                    19754439,
                    19302727,
                    19278624,
                    15036758,
                    17835314,
                    17652977,
                    19306630,
                    19248399,
                    19322723,
                    19963540,
                    19999935,
                    18847070,
                    19223199,
                    17432964,
                    19332187,
                    19606149,
                    19521924,
                    19465759,
                    16871882,
                    19911553,
                    19626604,
                    18944226,
                    19521202,
                    19726982,
                    19448561,
                    18392088,
                    19355432,
                    19663762,
                    ]
qrcode_list = [592,
               731,
               462,
               440,
               1077,
               331,
               781,
               810,
               1107,
               185,
               1251,
               153,
               600,
               166,
               1006,
               219,
               1223,
               883,
               1216,
               787,
               1256,
               871,
               2023,
               922,
               866,
               570,
               169,
               747,
               280,
               902,
               2034,
               169,
               1087,
               105,
               367,
               491,
               835,
               147,
               496,
               739,
               992,
               366,
               705,
               828,
               1268,
               1047,
               406,
               928,
               548,
               549,
               688,
               1128,
               597,
               466,
               946,
               1068,
               351,
               143,
               239,
               888,
               210,
               105,
               171,
               477,
               546,
               961,
               2027,
               2037,
               529,
               628,
               843,
               501,
               925,
               1002,
               561,
               438,
               551,
               679,
               1176,
               467,
               468,
               850,
               189,
               1150,
               157,
               587,
               419,
               878,
               784,
               1158,
               1007,
               479,
               975,
               102,
               230,
               447,
               760,
               1247,
               256,
               228,
               990,
               966,
               837,
               2027,
               682,
               432,
               535,
               1070,
               273,
               466,
               475,
               1209,
               785,
               1041,
               1272,
               728,
               270,
               909,
               195,
               325,
               1218,
               878,
               252,
               1135,
               573,
               1082,
               217,
               1012,
               1254,
               662,
               216,
               553,
               583,
               1217,
               583,
               2025,
               1136,
               392,
               1155,
               1084,
               1117,
               821,
               424,
               530,
               834,
               253,
               840]

user_task_list = [324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 336, 337, 338, 339,
                  340, 341, 342, 343, 344, 345, 346, 347, 348, 349, 350, 351, 352, 1346, 1347, 1348, 1349, 1350, 1351,
                  1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1367, 1368,
                  1369, 1370, 1371, 1372, 1373, 1374, 1375, 1376, 9872772, 9872880, 9872881, 9872882, 9873108, 9873109,
                  5480528, 9873222, 7589064, 103068, 9873355, 9873356, 9873357, 9873489, 9873490, 9873491, 9873492,
                  8903429, 9873802, 9873997, 9874186, 9874187, 9874188, 9874352, 9874514, 9874688, 9927654, 10008268,
                  10047371, 10225436, 10392627, 10515002]


# # 声明一个全局变量Q
# global Q
#
#
# # 此方法每次点击locust页面上的start都会调用
# @events.test_start.add_listener
# def on_test_start(**kwargs):
#     # 从CSV中读取文件，然后存储到队列里
#     global Q
#     Q = queue.Queue()
#     for i in user_task_list:
#         Q.put(i)


# 断言方法
def check(response, is_check):
    if is_check:
        try:
            if response.status_code == 200 and not response.json()["succeed"]:
                response.failure(response.text)
            # else:
            #     print(response.text)
        except Exception as e:
            response.failure(response.text + "--失败原因:json解析失败--" + str(e))


class UserBehavior(TaskSet):

    # def on_start(self):
    #     self.user_task = Q.get()

    @tag("t3")
    @task(3)
    def pageQuery(self):
        # 当接口的的参数类型为application/x-www-form-urlencoded时，使用data传参
        # 当接口的的参数类型application/json时，使用json传参，即下面的data=body改成json=body
        # 大多时候，这两种参数类型可以互相兼容的
        url = "/pjx-backend/o/oa/v1/user/pageQuery"
        body = {
            "pageNum": 1,
            "pageSize": 10,
            "param": {
                "city": "",
                "courseCategoryId": 0,
                "deptLevels": [],
                "expBatch": 0,
                "expCourseLatelyLearningProgressCode": "",
                "expCourseTeacherId": 0,
                "expEnrollmentId": 0,
                "expIsBind": 0,
                "expOpenCourseTime": "",
                "isAll": 0,
                "nickName": "",
                "payStatus": 0,
                "phone": "",
                "sortRule": 0,
                "sysBatch": 0,
                "sysCourseLatelyLearningProgressCode": "",
                "sysCourseTeacherId": 0,
                "sysEnrollmentId": 0,
                "sysIsBind": 0,
                "sysOpenCourseTime": "",
                "teacherOaId": 0,
                "userId": 0,
                "userSource": 0,
                "userSourceChannelGroupId": 0,
                "userSourceChannelId": 0,
                "userSourceChannelTeamId": 0,
                "userType": 0,
                "writingExpBatch": 0,
                "writingExpIsBind": 0,
                "writingExpOpenCourseTime": "",
                "writingSysBatch": 0,
                "writingSysIsBind": 0,
                "writingSysOpenCourseTime": "",
                "wxNickName": ""
            }
        }
        with self.client.post(url, headers=backend_headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t4")
    @task(1)
    def pageQueryP2(self):
        # 当接口的的参数类型为application/x-www-form-urlencoded时，使用data传参
        # 当接口的的参数类型application/json时，使用json传参，即下面的data=body改成json=body
        # 大多时候，这两种参数类型可以互相兼容的
        url = "/pjx-backend/o/userCourseStatistics/pageQueryP2"
        body = {"courseCategoryId": 1, "courseType": 1, "ageStageId": 2, "courseNum": 8, "teacherOaId": "", "phone": "",
                "sort": "", "openCourseTime": "2021-03-29", "userId": "", "fieldIndex": 11, "pageNum": 1,
                "pageSize": 10, "enrollmentIds": [1131, 1107, 870, 851, 848, 847, 846, 845, 841, 839, 837],
                "isFinishClass": -1, "isAttendClass": -1, "isConvertStandard": -1, "isCcBind": -1, "isComment": -1,
                "isCommit": -1, "isObtainCoupon": -1, "isReadComment": -1}
        with self.client.post(url, headers=backend_headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t5")
    @task(28)
    def getCommentTeacherByOaIdAndCourseCourseCategoryId(self):
        params_list = [(("courseCourseCategoryId", 1), ('oaId', 100076),),
                       (("courseCourseCategoryId", 1), ('oaId', 100108),),
                       (("courseCourseCategoryId", 2), ('oaId', 100106),),
                       (("courseCourseCategoryId", 2), ('oaId', 100107),)]
        url = "/pjx-comment/i/commentTeacher/v1.0/getCommentTeacherByOaIdAndCourseCourseCategoryId"
        params = random.choice(params_list)
        with self.client.get(url, name=url, headers=comment_headers,
                             params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t6")
    @task(18)
    def getCommentGroupNumber(self):
        # 字符串参数，也可以在url后面使用?拼接,没有参数可以直接省略params传参
        # 注意：当url改变时，locust会识别为不同的接口，统计时也会分开统计，此时要使用name来命名此接口
        url = "/pjx-comment/p/comment/getCommentGroupNumber"
        body = {
            "ageStageId": 0,
            "beginDate": "",
            "courseCategoryId": 0,
            "courseId": 0,
            "courseType": random.randint(1, 3),
            "nearlyMonth": random.randint(0, 1),
            "nearlyWeek": random.randint(0, 1),
            "searchText": ""
        }
        with self.client.post(url, headers=comment_headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t7")
    @task(9)
    def getCommentPage(self):
        url = "/pjx-comment/p/comment/getCommentPage"
        body = {
            "ageStageId": 0,
            "appVersion": "",
            "beginDate": "",
            "commentStatus": 0,
            "courseCategoryId": 0,
            "courseId": 0,
            "courseType": random.randint(1, 3),
            "nearlyMonth": random.randint(0, 1),
            "nearlyWeek": random.randint(0, 1),
            "pageNum": 1,
            "pageSize": 10,
            "phone": "",
            "searchText": ""
        }
        with self.client.post(url, headers=comment_headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t8")
    @task(6)
    def getCourseCommentNum(self):
        url = "/pjx-comment/p/comment/getCourseCommentNum"
        body = {
            "ageStageId": 0,
            "beginDate": "",
            "commentStatus": 0,
            "courseType": random.randint(1, 3),
            "oaId": 0,
            "searchText": ""
        }
        with self.client.post(url, headers=comment_headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t9")
    @task(6)
    def getCourseAgeStageCommentNum(self):
        url = "/pjx-comment/p/comment/getCourseAgeStageCommentNum"
        body = {
            "beginDate": "",
            "commentStatus": 0,
            "courseCategoryId": 0,
            "courseType": random.randint(1, 3),
            "oaId": 0,
            "searchText": ""
        }
        with self.client.post(url, headers=comment_headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t10")
    @task(5)
    def getAllCurrentCommentTeacher(self):
        url = "/pjx-comment/i/commentTeacher/v1.0/getAllCurrentCommentTeacher"
        body = {
            "courseCategoryId": random.randint(1, 2),
            "teacherOdIdList": []
        }
        with self.client.post(url, headers=comment_headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t11")
    @task(212)
    def getCourseSubjectContainLessonNum(self):
        url = "/pjx-component/i/courseSubject/getCourseSubjectContainLessonNum"
        params = (("ageStageId", 1), ('courseSubjectId', 1),)
        with self.client.get(url, name=url, headers=headers,
                             params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t12")
    @task(87)
    def getCourseMealByIdV2(self):
        url = "/pjx-component/i/courseMeal/v1.0/getCourseMealByIdV2"
        params = (("courseMealId", random.randint(1, 20)), ('needDetailMessage', random.choice([True, False])),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t13")
    @task(82)
    def getCourseMealById(self):
        # 字符串参数，也可以在url后面使用?拼接,没有参数可以直接省略params传参
        # 注意：当url改变时，locust会识别为不同的接口，统计时也会分开统计，此时要使用name来命名此接口
        url = "/pjx-component/i/courseMeal/v1.0/getCourseMealById"
        params = (("courseMealId", random.randint(1, 20)), ('needDetailMessage', random.choice([True, False])),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t14")  # t + excel中接口的编号
    @task(76)  # excel中接口的调用次数÷10000，四舍五入
    def getCurrentEnrollmentByCourseMealId(self):  # 方法名，用接口url的最后一层路径命名
        # 接口url，注意excel中有的接口路径不全，需要手动补上对应的服务比如/pjx-uc
        url = "/pjx-component/i/enroll/v1.0/getCurrentEnrollmentByCourseMealId"
        body = {"courseMealId": random.choice([1, 2, 3, 4, 5, 7, 8, 9, 10])}  # 接口参数
        with self.client.post(url, headers=headers, data=body, catch_response=IS_CHECK) as r:  # 接口的请求类型
            check(r, IS_CHECK)

    @tag("t15")
    @task(74)
    def getCourseMealByChannelId(self):
        # 字符串参数，也可以在url后面使用?拼接,没有参数可以直接省略params传参
        # 注意：当url改变时，locust会识别为不同的接口，统计时也会分开统计，此时要使用name来命名此接口
        url = "/pjx-component/i/channel/v1.0/getCourseMealByChannelId"
        params = (("channelId", random.randint(1, 8000)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t16")
    @task(74)
    def getChannelById(self):
        # 字符串参数，也可以在url后面使用?拼接,没有参数可以直接省略params传参
        # 注意：当url改变时，locust会识别为不同的接口，统计时也会分开统计，此时要使用name来命名此接口
        url = "/pjx-component/i/channel/v1.0/getChannelById"
        params = (("channelId", random.randint(1100, 8000)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t17")
    @task(66)
    def getByCourseId(self):
        # 字符串参数，也可以在url后面使用?拼接,没有参数可以直接省略params传参
        # 注意：当url改变时，locust会识别为不同的接口，统计时也会分开统计，此时要使用name来命名此接口
        url = "/pjx-component/i/course/v1.0/getByCourseId"
        params = (("courseId", random.randint(1, 300)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t18")
    @task(57)
    def listPosterTemplateByCourseCategoryIdBizTypeAndStyleType(self):
        # 字符串参数，也可以在url后面使用?拼接,没有参数可以直接省略params传参
        # 注意：当url改变时，locust会识别为不同的接口，统计时也会分开统计，此时要使用name来命名此接口
        url = "/pjx-component/i/poster/v1.0/listPosterTemplateByCourseCategoryIdBizTypeAndStyleType"
        params = (("bizType", 1), ("courseCategoryId", random.randint(1, 2)),
                  ("styleType", random.randint(1, 2)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t19")
    @task(56)
    def getCourseMealTypeList(self):
        # 字符串参数，也可以在url后面使用?拼接,没有参数可以直接省略params传参
        # 注意：当url改变时，locust会识别为不同的接口，统计时也会分开统计，此时要使用name来命名此接口
        url = "/pjx-component/i/courseMeal/v1.0/getCourseMealTypeList"
        course = random.randint(1, 50)
        params = (("courseMealIdList", [i for i in range(course, course + 10)]),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t20")
    @task(53)
    def getCourseCategory(self):
        # 字符串参数，也可以在url后面使用?拼接,没有参数可以直接省略params传参
        # 注意：当url改变时，locust会识别为不同的接口，统计时也会分开统计，此时要使用name来命名此接口
        url = "/pjx-component/i/coursecategory/v1.0/getCourseCategory"
        with self.client.get(url, headers=headers, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t21")
    @task(27)
    def getAgeStageById(self):
        url = "/pjx-component/i/ageStage/v1.0/getAgeStageById"
        params = (("id", random.randint(1, 6)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t22")
    @task(22)
    def getPurchaseRecommendConfigurationByBizType(self):
        url = "/pjx-component/i/v2.0/purchaseRecommend/getPurchaseRecommendConfigurationByBizType"
        params = (("bizType", random.randint(1, 4)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t23")
    @task(18)
    def getCourseMealIdListBySpecialType(self):
        url = "/pjx-component/i/courseMeal/v1.0/getCourseMealIdListBySpecialType"
        params = (("specialType", 1),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t24")
    @task(17)
    def getByQrCodeIdList(self):
        url = "/pjx-component//i/qrCode/getByQrCodeIdList"
        qrCode = random.choices(qrcode_list, k=10)
        body = {"qrCodeIdList": ",".join(str(i) for i in qrCode)}
        with self.client.post(url, headers=headers, data=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t25")
    @task(15)
    def getCoursePageDataRespDto(self):
        url = "/pjx-component/i/course/v1.0/getCoursePageDataRespDto"
        course = random.randint(1, 35)
        params = (("courseStageIdList", [i for i in range(course, course + 5)]), ("pageNum", 1), ("pageSize", 10),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t26")
    @task(14)
    def getAppUpgradeStrategyConfigForApp(self):
        url = "/pjx-component/i/appVersion/getAppUpgradeStrategyConfigForApp"
        body = {
            "appCode": "",
            "deviceType": random.randint(1, 2)
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t27")
    @task(12)
    def getCourseStageById(self):
        url = "/pjx-component/i/courseStage/v1.0/getCourseStageById"
        params = (("courseStageId", random.randint(1, 40)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t28")
    @task(10)
    def getByBizTypeAndCourseMealId(self):
        url = "/pjx-component/i/purchaseConfiguration/v1.0/getByBizTypeAndCourseMealId"
        params = (("bizType", random.randint(1, 4)), ("courseMealId", 1),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t29")
    @task(8)
    def getByCourseStageIdAndLessonNumAndCourseStagVersion(self):
        url = "/pjx-component/i/course/v2.0/getByCourseStageIdAndLessonNumAndCourseStagVersion"
        params = (("courseStagVersion", random.randint(1, 2)), ("courseStageId", random.randint(1, 30)),
                  ("lessonNum", random.randint(1, 6)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)
            # print(params, "---", r.text)

    @tag("t30")
    @task(6)
    def getByCourseSubjectIdList(self):
        url = "/pjx-component/i/courseStage/v2.0/getByCourseSubjectIdList"
        course = random.randint(1, 13)
        params = (("courseSubjectIdList", [i for i in range(course, course + 3)]),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t31")
    @task(6)
    def getQrCodeById(self):
        url = "/pjx-component/i/qrCode/getQrCodeById"
        params = (("qrCodeId", random.randint(11, 1250)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t32")
    @task(6)
    def getByCourseStageIdAndCourseId(self):
        url = "/pjx-component/i/course/v2.0/getByCourseStageIdAndCourseId"
        params_list = [(('courseId', 250), ('courseStageId', 31)), (('courseId', 216), ('courseStageId', 28)),
                       (('courseId', 253), ('courseStageId', 32)), (('courseId', 7), ('courseStageId', 10)),
                       (('courseId', 73), ('courseStageId', 7)), (('courseId', 60), ('courseStageId', 6)),
                       (('courseId', 31), ('courseStageId', 18)), (('courseId', 53), ('courseStageId', 19)),
                       (('courseId', 59), ('courseStageId', 29)), (('courseId', 93), ('courseStageId', 11))]
        params = random.choice(params_list)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)
            # if r.json()["data"]:
            #     print(params, "---", r.text)

    @tag("t33")
    @task(4)
    def getCourseSubjectById(self):
        url = "/pjx-component/i/courseSubject/getCourseSubjectById"
        params = (("courseSubjectId", random.randint(1, 15)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t34")
    @task(8)
    def isPurchaseCourse(self):
        url = "/pjx-fission/o/qrCode/isPurchaseCourse"
        with self.client.get(url, headers=headers, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t35")
    @task(4)
    def getPurchaseLinkUrlV2(self):
        url = "/pjx-fission/i/v1/qrCode/getPurchaseLinkUrlV2"
        params = (("bizKey", random.randint(1, 10)), ("bizType", random.randint(1, 4)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    # TODO 返回数据为空
    @tag("t36")
    @task(19)
    def confirm(self):
        url = "/pjx-mall/o/coinStrategy/confirm"
        body = {
            "businessId": "1",
            "changeNum": 0,
            "strategyId": "1",
            "symbol": "1",
            "userId": 0
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            pass

    # TODO 待切换Q
    @tag("t37")
    @task(39)
    def doBatchTaskReward(self):
        url = "/pjx-mall/i/v1/task/doBatchTaskReward"
        body = {
            "rewardReqDtoList": [
                {
                    "businessId": 'test' + str(random.randint(1, 10000000)),
                    "description": random.choice('abcdefghijklmnopqrstuvwxyz!@#$%^&*()'),
                    "extraInfo": {},
                    "flowType": random.randint(1, 2),
                    "number": random.randint(1, 10),
                    "strategyIdentification": random.choice(
                        ["AIactivity_gemstone_use", "AIactivity_coin_use", "give_GC"]),
                    # "userId": random.choice(user_task_list),
                    "userId": user_task_list[1],
                    "virtualCurrencyType": random.randint(1, 2)
                }
            ]

        }

        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, False)

    @tag("t38")
    @task(19)
    def userSummary(self):
        url = "/pjx-mall/i/v1/invitation/userSummary"
        params = (("symbol", "GC"), ("userId", random.randint(1, 55000)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t39")
    @task(21)
    def getUserSummary(self):
        url = "/pjx-mall/i/v1/task/getUserSummary"
        body = {"symbol": "GC", "userId": random.randint(1, 55000)}
        with self.client.post(url, headers=headers, data=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t40")
    @task(5)
    def goods_list(self):
        url = "/pjx-mall/o/goods/list"
        body = {
            "businessType": random.randint(2, 3),
            "dmNumMax": 0,
            "dmNumMin": 0,
            "pageNum": random.randint(1, 2),
            "pageSize": 10
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t41")
    @task(4)
    def getUserRewardList(self):
        url = "/pjx-mall/i/v1/userReward/getUserRewardList"
        params = (("userId", random.choice(user_reward_list)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, True)

    @tag("t42")
    @task(279)
    def accumulateStudyTime(self):
        # 当接口的的参数类型为application/x-www-form-urlencoded时，使用data传参
        # 当接口的的参数类型application/json时，使用json传参，即下面的data=body改成json=body
        # 大多时候，这两种参数类型可以互相兼容的
        url = "/pjx-mobile/o/studyReport/accumulateStudyTime"
        body = {
            "seconds": random.randint(1, 1000),
            "userCourseId": random.randint(491515, 704541)
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, False)

    @tag("t43")
    @task(5)
    def getAppHomePage(self):
        url = "/pjx-mobile/o/user/homepage/getAppHomePage"
        body = {"appId": 1, "deviceId": "5724a438d" + str(random.randint(1000000, 9999999)), "pageCode": "home",
                "appChannel": "i61",
                "appVersion": "2.7.0", "mobileOs": random.randint(1, 2), "systemVersion": "10"}
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t44")
    @task(5)
    def getTerminalConfig(self):
        code_list = [
            "AI_IOS",
            "AI_H5",
            "AI_Android",
            "AI_WEB",
            "AI_GAME_RESOURCE",
            "DING_ALERT",
            "AI_SERVER_CONFIG",
            "AI_CMS"]
        url = "/pjx-mobile/o/user/terminal/getTerminalConfig"
        body = {
            "terminalDefineCode": random.choice(code_list)
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t45")
    @task(24)
    def userComment_getUserCommentRedDot(self):
        url = "/pjx-mobile/o/user/userComment/getUserCommentRedDot"
        body = {}
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t46")
    @task(22)
    def getCourseCategoryList(self):
        url = "/pjx-mobile/o/user/lessonV2/getCourseCategoryList"
        with self.client.post(url, headers=headers, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t47")
    @task(22)
    def getUserWorkUrl(self):
        url = "/pjx-mobile/o/user/work/getUserWorkUrl"
        body = {
            "userCourseId": random.randint(10000, 20000)
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, False)

    @tag("t48")
    @task(20)
    def getUserCourseData(self):
        url = "/pjx-mobile/o/user/lesson/getUserCourseData"
        body = {
            "userCourseId": random.randint(10000, 20000)
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, False)

    @tag("t49")
    @task(19)
    def getUnLockCourseList(self):
        url = "/pjx-mobile/o/user/lessonV2/getUnLockCourseList"
        body = {
            "courseCategoryId": 1,
            "endTime": ""
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t50")
    @task(18)
    def getUserTeacherList(self):
        url = "/pjx-mobile/o/user/lessonV2/getUserTeacherList"
        body = {
            "courseCategoryId": random.randint(1, 2),
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t51")
    @task(18)
    def getUnFillAddressInfo(self):
        url = "/pjx-mobile/o/user/address/getUnFillAddressInfo"
        body = {}
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t52")
    @task(18)
    def getUpcomingClassesList(self):
        url = "/pjx-mobile/o/user/lessonV2/getUpcomingClassesList"
        body = {
            "courseCategoryId": random.randint(1, 2),
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t53")
    @task(15)
    def getDefaultPageCourseMeal(self):
        url = "/pjx-mobile/o/user/lessonV2/getDefaultPageCourseMeal"
        body = {
            "courseCategoryId": random.randint(1, 2),
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t54")
    @task(14)
    def systemInfo(self):
        url = "/pjx-mobile/o/system/systemInfo/v1"
        body = {
            "appChannel": "",
            "appVersion": "",
            "mobileOs": 0,
            "systemVersion": ""
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t55")
    @task(14)
    def getAppVersion(self):
        url = "/pjx-mobile/o/system/getAppVersion"
        body = {
            "appChannel": "",
            "appCode": "",
            "appVersion": "",
            "code": 0,
            "mobileOs": 0,
            "systemVersion": ""
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t56")
    @task(12)
    def lesson_updateVisitStatus(self):
        url = "/pjx-mobile/o/user/lesson/updateVisitStatus"
        body = {
            "userCourseId": random.choice([116750, 594727, 16751594728, 16752, 594729, 16753, 594733, 16754]),
            "visitStatus": random.randint(0, 100)
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t57")
    @task(11)
    def getRecommendedCourseMeal(self):
        url = "/pjx-mobile/o/user/lessonV2/getRecommendedCourseMeal"
        body = {
            "courseCategoryId": random.randint(1, 2),
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t58")
    @task(11)
    def updateLessonStatus(self):
        headers_1 = {
            "user-auth": "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ7XCJhcHBWZXJzaW9uXCI6XCJcIixcImFyZWFcIjpcIjg2XCIsXCJkZXZpY2VJZFwiOlwiXCIsXCJleHBpcmVUaW1lU3RhbXBcIjoxNjE3MjY0MTIwOTgxLFwibW9iaWxlTW9kZWxcIjpcImlwaG9uZVhcIixcInBob25lXCI6XCIxNTg5OTkzXCIsXCJyZWdpc3RlclNvdXJjZVwiOjQsXCJ0aW1lc3RhbXBcIjoxNjE3MjYwNTIwOTgxLFwidXNlcklkXCI6NjAwMTM2MTc5fSJ9.MD7jtvUMXAl4M3ZCh-z8YqrlrSnnf6xieK_BBXtCGPfGk-W6P0onbAF2LtYlw86YdRRv97s_da8R9yZHSIxuSdP5VJkFZEovDMXKQyd6KvOB6-PdwYAXWn-fNlwWPUyNQ83cSqzy0DJwBSO2FMYR6WO1F1gRbErEuZEHZLt2jb0"}
        url = "/pjx-mobile/o/user/lesson/updateLessonStatus"
        body = {
            "aiCourseDetailNum": 0,
            "aiDetail": "",
            "lessonStatus": random.choice([1, 2, 16]),
            "userCourseId": random.choice([4947990, 4947992, 4947991])
        }
        with self.client.post(url, headers=headers_1, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t59")
    @task(8)
    def square(self):
        url = "/pjx-mobile/o/user/workShow/square"
        body = {
            "appChannel": "",
            "appVersion": "",
            "courseCategoryId": random.randint(1, 2),
            "id": 0,
            "mobileOs": 0,
            "pageNum": 1,
            "pageSize": 10,
            "sortType": 0,
            "systemVersion": "",
            "zoomPx": 0
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, True)

    @tag("t60")
    @task(9)
    def getCourseModelPicturePopupStatus(self):
        url = "/pjx-mobile/o/user/evaluation/getCourseModelPicturePopupStatus"
        body = {
            "userCourseId": random.randint(10000, 20000)
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t61")
    @task(9)
    def getModelPictureStatus(self):
        url = "/pjx-mobile/o/user/evaluation/getModelPictureStatus"
        body = {}
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t62")
    @task(8)
    def showExGiveUserCoupon(self):
        url = "/pjx-mobile/o/user/lessonV2/showExGiveUserCoupon"
        body = {
            "userCourseId": random.choice([4947982, 4947984, 4947985])
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t63")
    @task(5)
    def getUserConfigurationInfo(self):
        url = "/pjx-mobile/o/system/getUserConfigurationInfo"

        body = {
            "appChannel": "i61",
            "appVersion": "2.7.0",
            "deviceId": "5e76a7a497e98" + str(random.randint(1, 100)).zfill(3),
            "mobileOs": random.randint(1, 2),
            "systemVersion": "10"
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t64")
    @task(5)
    def uploadMP3(self):
        url = "/pjx-mobile/o/upload/uploadMP3"
        body = {}
        body['file'] = ("onion.mp3", open("onion.mp3", 'rb').read())
        encode_data = encode_multipart_formdata(body)
        body = encode_data[0]
        h = copy.copy(headers)
        h['Content-Type'] = encode_data[1]
        with self.client.post(url, headers=h, data=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t65")
    @task(4)
    def firstIntoReportPopupStatus(self):
        url = "/pjx-mobile/o/user/evaluation/firstIntoReportPopupStatus"
        body = {
            "userCourseId": random.randint(10000, 100000)
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t66")
    @task(4)
    def getCourseSharePoster(self):
        url = "/pjx-mobile/o/studyReport/getCourseSharePoster"
        body = {
            "posterTemplateId": random.randint(1, 2),
            "userCourseId": random.choice(
                [16750, 594727, 16751, 594728, 16752, 594729, 16753, 594733, 16754, 594730, 16755])
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t67")
    @task(74)
    def getCourseMealGroup(self):
        url = "/pjx-pay/o/coursemeal/getCourseMealGroup"
        body = {
            "appChannel": "",
            "appVersion": "",
            "channelId": random.randint(1100, 8000),
            "code": "",
            "courseType": 1,
            "mobileOs": 0,
            "systemVersion": "",
            "userId": 0
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t68")
    @task(74)
    def getUserExperienceOrderStatus(self):
        url = "/pjx-pay/o/pay/experience/getUserExperienceOrderStatus"
        with self.client.post(url, headers=headers, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t69")
    @task(67)
    def getUserPayOrder(self):
        url = '/pjx-pay/i/order/v1.0/getUserPayOrder'
        params = (("userId", random.choice(user_list)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t70")
    @task(67)
    def getRedPoint(self):
        url = "/pjx-pay/o/coupon/getRedPoint"
        with self.client.post(url, headers=headers, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t71")
    @task(18)
    def getHasPayOrderListByUserId(self):
        url = '/pjx-pay/i/order/v2.0/getHasPayOrderListByUserId'
        params = (("userId", random.choice(user_list)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t72")
    @task(4)
    def getApplePayOpenStatus(self):
        url = "/pjx-pay/o/coursemeal/getApplePayOpenStatus"
        body = {
            "appChannel": random.choice(["AppStore", "Fir"]),
            "appVersion": random.choice(
                ["1.1.0", "1.2.0", "1.3.0", "1.4.0", "1.5.0", "1.6.0", "1.7.0", "1.8.0", "1.9.0", "2.1.0", "2.2.0",
                 "2.3.0", "2.4.0", "2.5.0", "2.6.0", ]),
            "mobileOs": 2,
            "systemVersion": ""
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t73")
    @task(5)
    def getPayOrderExtendByOrderNo(self):
        url = '/pjx-pay/i/order/v1.0/getPayOrderExtendByOrderNo'
        params = (("orderNo", random.choice(order_list)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, False)

    @tag("t74")
    @task(109)
    def getSensorsCommonData(self):
        url = "/pjx-statistics/sensorsData/getSensorsCommonData"
        body = {
            "abTestGroup": "",
            "abTestId": "",
            "anonymousId": "",
            "appChannel": "",
            "appVersion": "",
            "browser": "",
            "browserVersion": "",
            "carrier": "",
            "deviceId": "",
            "deviceToken": "",
            "isFirstDay": True,
            "latestUtmCampaign": "",
            "latestUtmContent": "",
            "latestUtmMedium": "",
            "latestUtmSource": "",
            "latestUtmTerm": "",
            "manufacturer": "",
            "model": "",
            "networkType": "",
            "os": "",
            "osVersion": "",
            "screenHeight": 0,
            "screenOrientation": "",
            "screenWidth": 0,
            "url": "",
            "wifi": True
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t75")
    @task(76)
    def clickEventCollect(self):
        url = "/pjx-statistics/eventCollect/clickEventCollect"
        body = {
            "ageStageId": 4,
            "browser": random.choice(["none", "WeChat", "Safari", ""]),
            "button": random.choice(["", "一键参团", "点我参团"]),
            "channelId": "50631",
            "code": "7727a92f-3a8f-4db4-bdcf-119cd5f107c3",
            "handlerType": 1,
            "mobileModel": "iPhone",
            "mobileOs": "iOS",
            "screenResolution": random.choice(["1920*1080", "414*896"]),
            "statisticsCode": random.choice(["pjx_1_10000", "pjx_1_10001"]),
            "url": "http://test-static-resource.61info.cn/ai_course_pay_h5_view/web/experience-wx-v6?channelId=50631",
            "userStudyReportShareSnapshotId": 0
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t76")
    @task(58)
    def collectSensorsEvent(self):
        url = "/pjx-statistics/i/v1.0/sa/collectSensorsEvent"
        body = {"distinctId": "100038", "eventName": "get_packet",
                "properties": {"packet_amount": 1.0, "activity_id": "20210101"}}
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t77")
    @task(92)
    def getUserIdByOpenIdAndAppType(self):
        '''获取用户信息'''
        url = '/pjx-uc/i/v1.0/user/getUserIdByOpenIdAndAppType'
        params = (("appType", 1), ("openId", "o71aTjqyXsC9BJkzR6iYplQ2UjIE"),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t78")
    @task(79)
    def getByUserId(self):
        '''获取用户信息'''
        url = '/pjx-uc/i/v1.0/user/getByUserId?userId=19696473'
        # params = (("userId", 19696473),)
        with self.client.get(url, headers=headers, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t79")
    @task(75)
    def getUserInfo(self):
        '''获取用户信息'''
        url = '/pjx-uc/userinfo/getUserInfo'
        params = (("isOwn", 'true'),)
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t80")
    @task(75)
    def getCurrentByUserIdAndCourseCategoryId(self):
        '''获取当前有效的报名记录'''
        url = '/pjx-uc/i/v1.0/standardSignUp/getCurrentByUserIdAndCourseCategoryId'
        params = (("courseCategoryId", 1), ('userId', 19696473),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t81")
    @task(75)
    def getByUserCourseId(self):
        '''通过id来获取userCourse'''
        url = '/pjx-uc/i/v1.0/userCourse/getByUserCourseId'
        params = (("userCourseId", 3497871),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t82")
    @task(37)
    def getExperienceSignUpByUserId(self):
        '''通过用户Id获取体验课报名学员信息'''
        url = '/pjx-uc/i/v1.0/experienceSignUp/getExperienceSignUpByUserId'
        params = (("courseCategoryId", 1), ("userId", 19696473),)
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t83")
    @task(31)
    def syncUserCourseToTigerWhale(self):
        '''同步用户信息到虎鲸'''
        url = '/pjx-uc/v1/aiBindUserWx/syncUserCourseToTigerWhale'
        body = {"userId": 19696473}
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t84")
    @task(25)
    def getUserCourseLineByUserIdAndStatusList(self):
        '''通过userId和状态集合获取用户的课程线列表'''
        url = '/pjx-uc/i/v2.0/userCourse/getUserCourseLineByUserIdAndStatusList'
        params = (("userId", 19696473),)
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t85")
    @task(24)
    def getUserCommentRedDot(self):
        '''通过userId和状态集合获取用户的课程线列表'''
        url = '/pjx-uc/i/v1.0/comment/getUserCommentRedDot'
        params = (("userId", 19696473),)
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t86")
    @task(18)
    def selectByDictionaryType(self):
        '''通过字典所属类别获取对应列表值'''
        url = '/pjx-uc/userinfo/selectByDictionaryType'
        params = (("dictionaryType", 1),)
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t87")
    @task(19)
    def getUserDefaultAddress(self):
        '''获取默认地址'''
        url = '/pjx-uc/i/v1.0/userExpress/getUserDefaultAddress'
        params = (("userId", 19696473),)
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t88")
    @task(17)
    def getUserInfoAboutCourse(self):
        '''获取用户有关课程的信息'''
        url = '/pjx-uc/tiger/whale/getUserInfoAboutCourse'
        params = (("courseCategoryId", '1'), ("oaId", '400167'), ("userWeChatId", "wxid_83zluxnw08vc21"),)
        with self.client.get(url, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t89")
    @task(18)
    def getUnLockCourseListByCourseCategoryId(self):
        '''获取全部解锁课程'''
        url = '/pjx-uc/i/v2.0/userCourse/getUnLockCourseListByCourseCategoryId'
        body = {"courseCategoryId": 1,
                "endTime": "2021-02-26 00:00:00",
                "maxLimit": 0,
                "userId": 19696473}
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t90")
    @task(18)
    def getUserTeacherListByUserIdList(self):
        '''通过userId列表获取辅导老师信息'''
        url = '/pjx-uc/i/v1.0/userTeacher/getUserTeacherListByUserIdList'
        params = (("userIdList", 19696473),)
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t91")
    @task(16)
    def userCoupon_getRedPoint(self):
        '''获取用户即将逾期或未读的优惠券，即红点信息'''
        url = '/pjx-uc/i/v1.0/userCoupon/getRedPoint'
        body = {"courseCategoryId": 1, "userId": 19696473}
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t92")
    @task(16)
    def getUserExtendByUserId(self):
        '''通过用户id获取到用户的扩展信息'''
        url = '/pjx-uc/i/v2.0/userExtend/getUserExtendByUserId'
        params = (("userId", 19696473),)
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t93")
    @task(12)
    def updateVisitStatus(self):
        '''更新用户该节课的visitStatus状态'''
        url = '/pjx-uc/i/v1.0/userCourse/updateVisitStatus'
        body = {"userCourseId": 3497871, "visitStatus": 15}
        with self.client.post(url, headers=headers, data=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t94")
    @task(11)
    def countUserCourseModelPictureEvaluationByCourseId(self):
        # 通过userId和courseId查询用户是否评价过课程范画
        url = "/pjx-uc/i/v1.0/userEvaluation/countUserCourseModelPictureEvaluationByCourseId"
        params = (("userCourseId", 4776448), ("userId", 600135360),)
        with self.client.get(url, headers=headers, name=url, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t95")
    @task(11)
    def getUserCoursePackageByUserId(self):
        # 通过用户id来获取课时包列表
        url = "/pjx-uc/i/v2.0/userCoursePackage/getUserCoursePackageByUserId"
        params = (("userId", 326),)
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t96")
    @task(11)
    def getUserData(self):
        # 获取用户作品，金币，宝石，优惠券数量
        url = "/pjx-uc/userinfo/getUserData"
        body = {
            "appChannel": "",
            "appVersion": "",
            "mobileOs": random.randint(1, 2),
            "systemVersion": ""
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t97")
    @task(10)
    def getUserInfoForApp(self):
        # 查询用户信息(app)
        url = "/pjx-uc/userinfo/getUserInfoForApp"
        body = {
            "appChannel": "",
            "appVersion": "",
            "isOwn": random.randint(0, 1),
            "mobileOs": random.randint(1, 2),
            "systemVersion": ""
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t98")
    @task(10)
    def refreshToken(self):
        # 刷新token
        url = "/pjx-uc/i/v1.0/token/refreshToken"
        params = (("userToken",
                   "eyJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJ7XCJhcHBWZXJzaW9uXCI6XCIyLjYuMFwiLFwiYXJlYVwiOlwiODZcIixcImRldmljZUlkXCI6XCIzOTc2OGQwZjU3Y2Q0MTU3XCIsXCJleHBpcmVUaW1lU3RhbXBcIjoxNjE3MDE1MjU2ODMxLFwibW9iaWxlTW9kZWxcIjpcIk1pIDEwIFByb1wiLFwicGhvbmVcIjpcIjEyMzAwMDAwMTM0XCIsXCJyZWdpc3RlclNvdXJjZVwiOjMsXCJ0aW1lc3RhbXBcIjoxNjE3MDExNjU2ODMxLFwidXNlcklkXCI6MzI2fSJ9.cW5cC6QU6NdRE2S0wGbgERziLvqYyun1v2ijTEE68t--_ZJFN5WwSoYjfiPhkFDhkh66aEY672vin1778XK4eU0Rk0mUBVVYl9Tc0Lrz0jUIekTK2mILiRS7BWa92jetgli9Lh40b-Pkn5-fwurJo5Toefkiq4q73R0LG6XNLkY"),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t99")
    @task(9)
    def getRecentDateOpenCourseList(self):
        # 获取指定用户最近开课日期的课程解锁列表
        url = "/pjx-uc/i/v2.0/userCourse/getRecentDateOpenCourseList"
        params = (("courseStatus", random.choice([1, 3, 7, 15, 31])), ("userId", 326))
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t100")
    @task(9)
    def countManageUserNumOfTeacherV2(self):
        # 获取体验课对应子课程下批次辅导老师分配到的学员数量
        url = "/pjx-uc/i/v1.0/experienceSignUp/countManageUserNumOfTeacherV2"
        params = (("courseSubjectId", 4), ("enrollmentId", 1138), ("qrCodeId", 736))
        with self.client.get(url, headers=headers, params=params, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t101")
    @task(7)
    def listByCursor(self):
        # 通过游标查询列表
        url = "/pjx-uc/i/v1.0/userWorkShow/listByCursor"
        body = {
            "courseCategoryId": random.randint(1, 2),
            "id": 0,
            "pageNum": 0,
            "pageSize": 0,
            "userId": 0
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t102")
    @task(6)
    def getUserHomeWorkById(self):
        # 通过id获取作业
        url = "/pjx-uc/i/v1.0/homework/getUserHomeWorkById"
        params = (("userHomeWorkId", random.randint(77, 1980133)),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t103")
    @task(5)
    def getBindWxByUserList(self):
        # 获取绑定微信的用户列表
        url = "/pjx-uc/i/v1.0/user/getBindWxByUserList"
        body = {
            "appType": 0,
            "userIdList": [22038786, 22038785, 22038783, 22038781, 22038766, 22038761, 22038751, 22038769]
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t104")
    @task(5)
    def getUserConfiguration(self):
        # 获取用户配置相关信息
        url = "/pjx-uc/i/v1.0/userConfiguration/getUserConfiguration"
        body = {
            "deviceId": "5e76a7a497e98012",
            "userId": 326
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t105")
    @task(5)
    def reduceCourse(self):
        # 扣减课时
        url = "/pjx-uc/i/v1.0/userCourseCash/reduceCourse"
        body = {
            "cashDetail": "体验课扣课时",
            "cashFlowBusiness": "UNLOCK_EXPERIENCE_COURSE",
            "courseCategoryId": 1,
            "reduceNum": random.randint(1, 4),
            "userId": 600136179
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t106")
    @task(4)
    def getCourseSharePosterNeedData(self):
        # 获取生成学习分享海报所需要的数据
        url = "/pjx-uc/i/v1.0/studyReport/getCourseSharePosterNeedData"
        params = (("posterTemplateId", random.randint(1, 2)), ("userCourseId", 4912175), ("userId", 600135863),)
        with self.client.get(url, headers=headers, params=params, name=url, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t107")
    @task(4)
    def getExGiveUserCoupon(self):
        # 获取用户体验课解锁赠送的优惠券信息
        url = "/pjx-uc/i/v1.0/userCoupon/getExGiveUserCoupon"
        body = {
            "courseCategoryId": 1,
            "userId": 600135861
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t108")
    @task(4)
    def addFriendInfo(self):
        # 好友增量监控接口
        url = "/pjx-uc/v1/aiBindUserWx/addFriendInfo"
        body = {
            "friends": [
                {
                    "alias": "",
                    "comment": "",
                    "createTime": "",
                    "headImg": "",
                    "id": "",
                    "nickName": ""
                }
            ],
            "salesId": "4272",
            "salesWx": ""
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)

    @tag("t109")
    @task(6)
    def callback(self):
        # 微信回调
        url = "/pjx-wx/o/wx/callback/1"
        # params=(("appType",1),)
        with self.client.get(url, headers=headers, catch_response=IS_CHECK) as r:
            pass

    @tag("t110")
    @task(5)
    def getSignature(self):
        # 微信分享
        url = "/pjx-wx/o/wx/common/getSignature"
        body = {
            "appType": 1,
            "noncestr": "ai_course_pay_h5_view",
            "timestamp": "",
            "url": "http://test-static-resource.61info.cn/ai_course_pay_h5_view/web/experience-wx-v6?channelId=50631"
        }
        with self.client.post(url, headers=headers, json=body, catch_response=IS_CHECK) as r:
            check(r, IS_CHECK)


class WebsiteUser(HttpUser):
    tasks = [UserBehavior]
    host = "http://gw-ai-test.61info.cn"
    wait_time = between(0, 0)


# 右键启动会出现全局中的代码运行两次的情况
if __name__ == "__main__":
    import os

    e_tag = " t6 t7 t8 t9"
    tag = "t42 t43 t44 t45 t46 t47 t48 t49 t50 t51 t52 t53 t54 t55 t56 t57 t58 t59 t60 t61 t62 t63 t64 t65 t66"

    # os.system(F"locust -f gubi_ai_all.py -T {tag}  ")  # 普通压测
    os.system(F"locust -f gubi_ai_all.py -E {e_tag} --step-load ")  # 普通压测
    # os.system(F"locust -f gubi_ai_all.py  --step-load ")  # 普通压测
    # os.system(F"locust -f gubi_ai_all.py -T {tag} --step-load  ")  # 逐步负载

"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
import mysql.connector
from json import load
from steamauth import auth, get_uid
from django.shortcuts import redirect
from django.views.decorators.http import require_POST, require_GET
from django.http import JsonResponse
from itertools import islice


with open('WebAdmin/secrets.json', 'r') as secrets_file: data = load(secrets_file)

def check_permissions(view_func):
    def _wrapped_view(request, *args, **kwargs):
        uid = request.session.get('steam_uid')
        allowed_uids = data["ALLOWED_UIDS"]  # Здесь вы можете определить свои разрешенные uid
        if uid is None or uid not in allowed_uids:
            return redirect('/')
        return view_func(request, *args, **kwargs)
    return _wrapped_view
        

def convert_bool(v):
  return v in ("1", 1)

class MYSQL():
    def __init__(self):
        self.user = data['USER']
        self.password = data['PASSWORD']
        self.host = data['HOST']
        self.database = data['NAME2']
        self.dbConnect = None

    def connect(self):
        self.dbConnect = mysql.connector.connect(user=self.user, password=self.password, host=self.host, database=self.database)

    def connect_close(self):
        if not None:
            self.dbConnect.close()
            self.dbConnect = None
            
            
    def db_query(self, query):
        if self.dbConnect is None or not self.dbConnect.is_connected():
            self.connect()
        rows = None
        with self.dbConnect.cursor() as cursor:
            cursor.execute(query)
            if 'UPDATE' in query or 'INSERT' in query: 
                self.dbConnect.commit()
            else:
                rows = cursor.fetchall()  
            
        self.connect_close()  
        return rows 
     

def get_modal(request):
    return render(
        request,
        'app/modal.html',
        {
        }
    )



@check_permissions
@require_POST
def update_items(request):  
    #print(request.POST)
    if request.htmx and len(request.POST) == 2:
        # Параметры для пропуска первого элемента
        start_index = 1
        for cloth, value in islice(request.POST.items(), start_index, None):
            _targetUID = request.POST.get('steamid')
            _query = f"UPDATE rolesaccess SET {cloth}='{value}' WHERE steamid='{_targetUID}'"
            MYSQL().db_query(_query)
            
            _query2 = f"INSERT INTO cloth_update_logs VALUES ('{request.session.get('steam_uid')}', '{_targetUID}', '{cloth}', {value}, current_timestamp())"
            MYSQL().db_query(_query2)
            
        return JsonResponse({'status': 'success'})

@check_permissions
@require_GET
def details(request, uid):
    assert isinstance(request, HttpRequest)

    query_from_roles_access = f"SELECT * FROM rolesaccess WHERE steamid='{uid}'"
    query_from_players = f"SELECT donat_level, donat_time, adminLevel, name FROM players WHERE steamid='{uid}'"
    query_from_pc_info = f"SELECT * FROM player_pc_info WHERE steamid='{uid}'"
    query_from_roles = f"SELECT * FROM roles WHERE steamid='{uid}'"
    query_from_bans = f"SELECT name, reason, time_until FROM bans WHERE uid='{uid}'"

    db_received_1 = MYSQL().db_query(query_from_roles_access)
    db_received_2 = MYSQL().db_query(query_from_players)
    db_received_3 = MYSQL().db_query(query_from_pc_info)
    db_received_4 = MYSQL().db_query(query_from_roles)
    db_received_5 = MYSQL().db_query(query_from_bans)
    
    #print(db_received_1[0][2:])
    #print(db_received_2[0])
    #print(db_received_3[0][2:])
    #print(db_received_4[0][3:])
   # print(db_received_5)

    roles_info = db_received_1[0][2:]
    if len(roles_info) > 0:
        WAGNER_SET = roles_info[0]
        DYNCORP_SET = roles_info[1]
        RU_SNIPER = roles_info[2]
        UA_SNIPER = roles_info[3]
        RU_STORMER = roles_info[4]
        UA_STORMER = roles_info[5]
        RU_MEDIC = roles_info[6]
        UA_MEDIC = roles_info[7]
        RU_GRENADER = roles_info[8]
        UA_GRENADER = roles_info[9]
        RU_SPECUAV = roles_info[10]
        UA_SPECUAV = roles_info[11]
        RU_GUNNER = roles_info[12]
        UA_GUNNER = roles_info[13]
        RU_COMMANDER = roles_info[14]
        UA_COMMANDER = roles_info[15]
        RU_TANKIST = roles_info[16]
        UA_TANKIST = roles_info[17]
        RU_PILOT = roles_info[18]
        UA_PILOT = roles_info[19]
        AZOV = roles_info[20]
        GOSTOMEL = roles_info[21]
        PRORIV = roles_info[22]
        
    player_info = db_received_2[0]
    if len(player_info) > 0:
        vip_level = player_info[0]
        vip_endtime = player_info[1]
        adminLevel = player_info[2]
        pName = player_info[3]

    return render(
        request,
        'app/details.html',
        {
           'year':datetime.now().year,
           'cloth_access': {
               'WAGNER_SET':   [convert_bool(WAGNER_SET),  "[WAGNER] Полный доступ"],
               'DYNCORP_SET':  [convert_bool(DYNCORP_SET), "[DYNCORP] Полный доступ"],
               'RU_SNIPER':    [convert_bool(RU_SNIPER),   "[WAGNER] Снайпер"],
               'UA_SNIPER':    [convert_bool(UA_SNIPER),   "[DYNCORP] Снайпер"],
               'RU_STORMER':   [convert_bool(RU_STORMER),  "[WAGNER] Штурмовик"],
               'UA_STORMER':   [convert_bool(UA_STORMER),  "[DYNCORP] Штурмовик"],
               'RU_MEDIC':     [convert_bool(RU_MEDIC),    "[WAGNER] Медик"],
               'UA_MEDIC':     [convert_bool(UA_MEDIC),    "[DYNCORP] Медик"],
               'RU_GRENADER':  [convert_bool(RU_GRENADER), "[WAGNER] Гранатомётчик"],
               'UA_GRENADER':  [convert_bool(UA_GRENADER), "[DYNCORP] Гранатомётчик"],
               'RU_SPECUAV':   [convert_bool(RU_SPECUAV),  "[WAGNER] Спец. БПЛА"],
               'UA_SPECUAV':   [convert_bool(UA_SPECUAV),  "[DYNCORP] Спец. БПЛА"],
               'RU_GUNNER':    [convert_bool(RU_GUNNER),   "[WAGNER] Пулемётчик"],
               'UA_GUNNER':    [convert_bool(UA_GUNNER),   "[DYNCORP] Пулемётчик"],
               'RU_COMMANDER': [convert_bool(RU_COMMANDER),"[WAGNER] Командир"],
               'UA_COMMANDER': [convert_bool(UA_COMMANDER),"[DYNCORP] Командир"],
               'RU_TANKIST':   [convert_bool(RU_TANKIST),  "[WAGNER] Экипаж"],
               'UA_TANKIST':   [convert_bool(UA_TANKIST),  "[DYNCORP] Экипаж"],
               'RU_PILOT':     [convert_bool(RU_PILOT),    "[WAGNER] Пилот"],
               'UA_PILOT':     [convert_bool(UA_PILOT),    "[DYNCORP] Пилот"],
               'AZOV':         [convert_bool(AZOV),        "Комплект - АЗОВ"],
               'GOSTOMEL':     [convert_bool(GOSTOMEL),    "Комплект - ГОСТОМЕЛЬ"],
               'PRORIV':       [convert_bool(PRORIV),      "Комплект - ПРОРЫВ"],
               }, 
           'main_info':{
               'vil_level': vip_level,
               'vip_endtime': vip_endtime.strftime("%d/%m/%Y, %H:%M:%S"),
               'adminLevel': adminLevel,
               'pName': pName,
               'uid': uid,
               }
        }
    )


@check_permissions
@require_GET
def search(request):
    query = request.GET.get('query', "")
    q = f"SELECT name, steamid FROM players WHERE name LIKE '%{query}%' or steamid LIKE '%{query}%'"
    db_received = MYSQL().db_query(q)
    
    return render(request, 'app/search_results.html', {
        'db_rows': db_received,
        'has_more': True,
    })

@require_GET
def home(request):
    assert isinstance(request, HttpRequest)
    query = f"SELECT name, steamid FROM players"
    db_received = MYSQL().db_query(query)
    steam_uid = request.session.get('steam_uid')
    noHaveAccess = True;
    if steam_uid is None or steam_uid not in data["ALLOWED_UIDS"]:
        noHaveAccess = False;
    return render(
        request,
        'app/index.html',
        {
            'title':'GladiuZ - Панель Администратора',
            'year':datetime.now().year,
            'db_rows': db_received,
            'steam_uid': steam_uid,
            'header_text': "GladiuZ - Players",
            'header_text_notAuthorized': "GladiuZ",
            'noHaveAccess': True if noHaveAccess else False,
        }
    )




# ----------- Steam ----------- #
def login(request):
    # if your service does not support ssl, set use_ssl parameters value to False
    return auth('/callback', use_ssl=False)
    #return auth('/callback')


def login_callback(request):
    steam_uid = get_uid(request.GET)
    if steam_uid is None:
        # login failed
        return redirect('/')
    else:
        if steam_uid:
            request.session['steam_uid'] = steam_uid
        # login success
        # do something with variable `steam_uid`
        return redirect('/')


@require_GET
def logout(request):
    assert isinstance(request, HttpRequest)
    del request.session['steam_uid']
    return redirect('/')


# ----------- Steam ----------- #
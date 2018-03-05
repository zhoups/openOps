from django.shortcuts import render
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from assets.models.asset import Asset
from .DataStoreFile import *
from django.contrib.auth.decorators import login_required

import json

# Create your views here.
@csrf_exempt
def list(request, page=''):
    # if request.methon == "POST":
    #
    #     a = json.loads(request.body.decode('utf-8'))
    #     print(type(a))
    # else:
    _li = [{"IP": "127.0.1.1", "name": "ubuntu"},{"IP": "127.0.1.2", "name": "ubuntu2"}]
    _li = Asset.objects.all()
    paginator = Paginator(_li, 3)

    # 获取分页之后的总页数
    num_pages = paginator.num_pages

    # 取第page页数据
    if page == '' or int(page) > num_pages:
        page = 1
    else:
        page = int(page)

    # 返回值是一个Page类的实例对象
    books_li = paginator.page(page)

    # 进行页码控制
    # 1.总页数<5, 显示所有页码
    # 2.当前页是前3页，显示1-5页
    # 3.当前页是后3页，显示后5页 10 9 8 7
    # 4.其他情况，显示当前页前2页，后2页，当前页
    if num_pages < 5:
        pages = range(1, num_pages + 1)
    elif page <= 3:
        pages = range(1, 6)
    elif num_pages - page <= 2:
        pages = range(num_pages - 4, num_pages + 1)
    else:
        pages = range(page - 2, page + 3)
    context = {
        'books_li': books_li,

        'pages': pages
    }
    return render(request, 'machine/machine_list.html', context=context)

def sysinfo(request,machine_id):
    id = request.GET.get('machine_id')
    # 先查询机器，因为不是对象没法便利数据库
    xdata = {
        "cpu": [],
        "disk": [],
        "memory": [],
        "network": {
            "Net_sent": [],
            "Net_recv": []
        }
    }
    ydata = []
    DIR = 'data/' + time_file() + '/sysinfo/'
    # (st_mtime=1330498089, st_ctime=1330498089)#文件最后访问时间
    result = [(i, os.stat(DIR + i).st_mtime) for i in os.listdir(DIR)]
    print(result)
    # 安最后访问排序,遍历,目前只有一个元祖列表
    for i in sorted(result, key=lambda x: x[1]):
        if machine_id in i[0]:  # i[0]是文件名
            with open('data/' + time_file() + '/sysinfo/' + i[0]) as f:
                file_body = json.loads(f.read())
            try:
                xdata['cpu'].append(file_body['CPU'].split('%')[0])
                xdata['disk'].append(file_body['Disk'].split('%')[0])
                xdata['memory'].append(file_body['Memory'].split('%')[0])
                xdata['network']['Net_sent'].append(file_body['Net_sent'].split('K/s')[0].split('B/s')[0])
                xdata['network']['Net_recv'].append(file_body['Net_recv'].split('K/s')[0].split('B/s')[0])
                ydata.append(file_body['time'])
            except:
                pass
                # self.render('500.html')
            name = file_body['name']
            print(xdata,ydata,name)
    # self.render('sysinfo.html', xdata=xdata, name=name, ydata=ydata)
    return render(request, 'machine/sysinfo.html', context={"xdata":xdata,"ydata":ydata,"name":name})




@login_required()
def lanxi(request,machine_id):
    return render(request, 'machine/lanxifuwu.html', {})

@csrf_exempt
def collectSysInfoHandler(request):
    if request.method == 'POST':
        dic = {}
        dic['name'] = request.POST.get('name')  # json_args?
        dic['ip'] = request.POST.get('ip')
        dic['CPU'] = request.POST.get('CPU')
        dic['Memory'] = request.POST.get('Memory')
        dic['Disk'] = request.POST.get('Disk')
        dic['Net_sent'] = request.POST.get('Net_sent')
        dic['Net_recv'] = request.POST.get('Net_recv')
        dic['time'] = request.POST.get('time')
        DataStoreFile('sysinfo', json.dumps(dic), dic['name'])
        return JsonResponse({"code":200,'msg':'文件保存成功'})
    return JsonResponse({"code":200,'msg':'get返回none'})


@csrf_exempt
def collectPackageHandler(request):
    dic = {}
    packages_dic = json.loads(request.body.decode('utf-8'))
    print(packages_dic)
    dic['name'] = packages_dic['name']
    dic['IP'] = packages_dic['IP']
    dic['json_dic'] = packages_dic
    DataStoreFile('lxinfo', json.dumps(dic), packages_dic['name'])
    return JsonResponse({"code":200})
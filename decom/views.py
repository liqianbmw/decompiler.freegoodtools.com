# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import traceback
import urllib
from wsgiref.util import FileWrapper
import commands
from django.template import loader
from urllib import parse
from decom import constant
from decom.models import FileItem, FileUrlPath,DownFileItem
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import time,base64
import os, json
from django.views.decorators.csrf import csrf_exempt
import shutil
import logging # 导入模块
from django.conf import settings
logger = logging.getLogger('django') # 使用在配置文件中定义的名为“django”的日志器


constant.FILE_PATH = settings.FILE_PATH;
# 主页
# def index(request):
#     context = {};
#     context['segment'] = 'index';
#     html_template = loader.get_template('index.html')
#     return HttpResponse(html_template.render(context, request))
# 主页
def javaDecompilersIndex(request):
    context = {};
    context['segment'] = 'index';
    html_template = loader.get_template('decompiler/java_decompiler.html')
    return HttpResponse(html_template.render(context, request))

# javaDecompilers 跳转到java_decompiler.html
def javaDecompilers(request):
    context = {};
    context['segment'] = 'index';
    t = time.time()
    customerID = (int(round(t * 1000)))
    context['customerID'] = customerID;
    html_template = loader.get_template('decompiler/java_decompiler.html')
    return HttpResponse(html_template.render(context, request))



# downloadTools
def downloadJadPage(request):
    # 工具下载页面
    context = {};
    context['segment'] = 'downloads';
    context['procyonDownList'] = getDownFiles("procyonDownList");
    context['CFRDownList'] = getDownFiles("CFRDownList");
    context['JDCoreDownList'] = getDownFiles("JDCoreDownList");
    context['jadDownList'] = getDownFiles("jadDownList");
    context['apktoolsDownList'] = getDownFiles("apktoolsDownList");
    context['jadxDownList'] = getDownFiles("jadxDownList");
    context['fernflowerDownList'] = getDownFiles("fernflowerDownList");
    html_template = loader.get_template('decompiler/download_jad.html')
    return HttpResponse(html_template.render(context, request))



# about
def about(request):
    # 为每一次刷新生成新的时间令牌
    t = time.time()
    context = {};
    customerID = (int(round(t * 1000)))
    context['customerID'] = customerID;
    context['segment'] = 'about';
    html_template = loader.get_template('about.html')
    return HttpResponse(html_template.render(context, request))


def getDownFiles(file):
    downFile = settings.DOWN_FILE+"/"+file+".txt";
    f = json.load(open(downFile))
    endList=[];
    for item in f:
        endList.append(DownFileItem(item["version"],item["comment"],item["size"],item["date"],item["downURL"]));
    return endList;


#上传jar、class文件
@csrf_exempt
def javaDecompilerAnalyze(request):
    context = {};
    try:
        if len(request.FILES)==0:
            html_template = loader.get_template('decompiler/java_decompiler_analyze.html')
        else:
            uploadFile = request.FILES['file']
            customerID = request.POST["customerID"];
            if customerID is None or customerID == "":
                t = time.time()
                context = {};
                customerID = (int(round(t*10000)))
            context['customerID'] = customerID;
            if uploadFile is not None and uploadFile != "":
                file, customerID, filesChilds,endFile = analyzeJAVA(customerID, uploadFile)
                reList=[]
                reList.append(FileUrlPath(endFile, endFile));
                context['uploadFileName'] = file;       #用户上传的文件名
                context['filePath'] = reList;               #用户上传的文件路径,初始上传时，显示文件名
                context['filesChilds'] = filesChilds;   #文件路径
                html_template = loader.get_template('decompiler/java_decompiler_analyze.html')
            else:
                html_template = loader.get_template('decompiler/java_decompiler_analyze.html')
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        context['errorInfo'] = "Error parsing the file, you need to upload it again!";
        html_template = loader.get_template('404.html')

    return HttpResponse(html_template.render(context, request))

# 解析java文件
def analyzeJAVA(customerID, upload):
    FILE_PATH = constant.FILE_PATH;
    folder = os.path.exists(FILE_PATH+"/"+str(customerID))
    if not folder:  # 判断是否存在文件夹如果不存在则创建文件夹
        os.makedirs(FILE_PATH+"/"+str(customerID))
    #保存文件
    fss = FileSystemStorage(FILE_PATH+"/"+str(customerID))
    file = fss.save(upload.name, upload)

    #判断文件类型
    endFile = "";       #文件扩展名
    allFileName = "";   #文件全名
    if "." in upload.name:
        # filePath = FILE_PATH + '/' + upload.name[0:upload.name.index(".")];
        # expandFile=upload.name[upload.name.rindex("."):];
        endFile = upload.name[0:upload.name.rindex(".")]; #截取最右侧.之前的名字
        allFileName=upload.name;
    else:
        # filePath = FILE_PATH + '/' + upload.name
        endFile = upload.name;
        allFileName=upload.name;

    # if ".apk"==expandFile or ".aab" == expandFile:
    #     paths = 'java -Xmx128m -jar /Users/qianli/workspace/python/www/tools/apktool_2.6.1.jar d -f ' + FILE_PATH + '/' + allFileName + " -o " + filePath;
    #     print(paths)
    #     os.system(paths)
    #     if ".apk"==expandFile:
    #         paths="jadx -d "+FILE_PATH + '/' + endFile+"/java/  "+FILE_PATH + '/' + endFile+"/smali/ ";
    #         print(paths)
    #         os.system(paths)
    # elif ".class"==expandFile or ".war"==expandFile:
    #     paths = "jadx -d " + FILE_PATH + '/' + endFile + "/  " + FILE_PATH + '/' + allFileName + "/ ";
    #     print(paths)
    #     os.system(paths)
    # else:
    #     paths = "jadx -d " + FILE_PATH + '/' + endFile + "/  " + FILE_PATH + '/' + allFileName + "/ ";
    #     print(paths)
    #     os.system(paths)
    folder = os.path.exists(FILE_PATH +"/"+str(customerID)+ '/' + endFile )
    if not folder:  # 判断是否存在文件夹如果不存在则创建文件夹
        os.makedirs(FILE_PATH+"/" +str(customerID)+ '/' + endFile )

    try:
        # paths = "jadx --log-level ERROR -d  " + FILE_PATH + '/' + endFile + "/  " + FILE_PATH + '/' + allFileName;
        ccdd = settings.JADX_HOME + FILE_PATH+"/"+str(customerID) + '/' + endFile + "/  " + FILE_PATH+"/"+str(customerID) + '/' + allFileName;
        logger.info(ccdd)
        os.system(ccdd)
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
    # path = FILE_PATH+"/"+str(customerID) + '/' + endFile;
    # path = FILE_PATH+"/"+str(customerID) ;
    endList = analyzeFilePath(str(customerID),endFile,endFile);


    return file,customerID,endList,endFile;

# 解析文件路径
def analyzeFilePath(customerID,endFile,currentPath):
    '''
    :param customerID: 客户编号
    :param endFile: 本次生成的文件夹名字
    :param currentPath: 当前要显示的路径
    :return:
    '''
    endList = [];
    FILE_PATH = constant.FILE_PATH;
    if endFile==currentPath:
        FILE_PATH=FILE_PATH+"/"+customerID+"/"+endFile; # 得到当前点击的路径信息
        prefixFileTemp=endFile;
    else:
        FILE_PATH = FILE_PATH + "/" + customerID + "/" + currentPath;  # 得到当前点击的路径信息
        prefixFileTemp = currentPath;
    filesChild = os.listdir(FILE_PATH)
    for filename in filesChild:
        tmp = urllib.parse.quote(prefixFileTemp+"/"+filename);  # 进行base64url编码
        pathTmp=os.path.join(FILE_PATH, filename) ;
        createTime = os.path.getctime(pathTmp); #文件创建时间
        timeArray = time.localtime(createTime)
        createTime = time.strftime("%b %d %Y %h:%M:%S", timeArray)

        if os.path.isdir(pathTmp):  # 判断是否为目录
            endList.append(FileItem(tmp, filename, "<System Dir>", "Directory", createTime, "folder.png"));
        elif os.path.isfile(pathTmp):  # 判断是否为文件
            fileType = os.path.splitext(filename)[-1]
            filesize = os.path.getsize(pathTmp)  # 如果是文件，则获取相应文件的大小
            fileIcon,fileType=getFileInfo(fileType);
            endList.append(FileItem(tmp,  filename, fileType, covertFukeSize(filesize), createTime, fileIcon));
    return endList;

def getFileInfo(fileType):
    if ".java" == fileType: return  "java.png" ,"Java File";
    if ".class" == fileType: return "class.png" , "Class File";
    if ".docx" == fileType: return "word.png" , "Word File";
    if ".xml" == fileType: return "xml.png" , "XML File";
    if ".css" == fileType: return "css.png","Css File";
    if ".json" == fileType: return  "json.png" ,"Json File";
    if ".js" == fileType: return  "js.png" ,"Json File";
    if ".yml" == fileType: return  "yml.png" ,"YML File";
    if ".version" == fileType: return  "version.png" ,"version File";
    if ".sql" == fileType: return  "sql.png" ,"sql File";
    if ".zip" == fileType: return  "zip.png" ,"zip File";
    if ".xlsx" == fileType: return  "excel.png" ,"excel File";
    if ".png" == fileType: return  "png.png" ,"png File";
    if ".jpg" == fileType: return  "image.png" ,"image File";
    return "file.png", "file File";


#点击java文件夹后，显示文件下的所有文件
@csrf_exempt
def javaDecompilerFolder(request):
    context = {};
    try:
        uploadFileName = request.GET.get("uploadFileName");
        filePath = request.GET.get("filePath");
        customerID = request.GET.get("customerID");
        context['customerID'] = customerID;
        context['uploadFileName'] = uploadFileName;

        if customerID is None or customerID == ""\
                or filePath is None or filePath ==""\
                or uploadFileName is None or uploadFileName == "":
            html_template = loader.get_template('404.html')
            context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
        else:
            uploadFileFolder = uploadFileName[0:uploadFileName.rindex(".")];  # 截取最右侧.之前的名字
            # path = constant.FILE_PATH +"/"+str(customerID) +"/"+ uploadFileFolder; #根路径，包括包的名字
            currentPath = filePath;  # 当前选择的路径

            if ("/"+uploadFileFolder)==currentPath: #如果选择的是根路径，不需要再加上包的名字
                # currentPath="";
                context['filePath'] = covertFileUrlPath((currentPath).split('/'),uploadFileFolder);  # 当前根路径
            else:
                context['filePath'] = covertFileUrlPath((filePath).split('/'),uploadFileFolder);  # 当前显示的文件路径

            filesChilds = analyzeFilePath(str(customerID),uploadFileFolder,currentPath);

            # print(context['filePath'])
            context['uploadFileName'] = uploadFileName;# 用户上传的文件名
            context['filesChilds'] = filesChilds;# 文件路径

            html_template = loader.get_template('decompiler/java_decompiler_analyze.html')
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
        html_template = loader.get_template('404.html')


    return HttpResponse(html_template.render(context, request))



# @csrf_exempt
def javaDecompileFileDetail(request):
    context = {};
    textContext = "";
    try:
        FILE_PATH = constant.FILE_PATH;
        filePath = request.GET.get("filePath")  #显示的文件路径
        customerID = request.GET.get("customerID");
        uploadFileName = request.GET.get("uploadFileName");
        context['customerID'] = customerID;
        context['uploadFileName'] = uploadFileName;
        if customerID is None or customerID == "" \
                or filePath is None or filePath == ""\
                or uploadFileName is None or uploadFileName =="":
            html_template = loader.get_template('404.html')
            context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
        else:
            uploadFileFolder = uploadFileName[0:uploadFileName.rindex(".")];  # 截取最右侧.之前的名字
            FILE_PATH=FILE_PATH+"/"+customerID+"/"+filePath; # 根路径信息
            isdir = os.path.isdir(FILE_PATH);
            context['filePath'] = covertFileUrlPath(filePath.split('/'),uploadFileFolder);
            if not isdir:
                root, extension = os.path.splitext(FILE_PATH);  # 取得文件扩展名
                if (extension in [".png", ".jpg", ".jpeg", "gif"]):
                    with open(FILE_PATH, "rb") as img_file:
                        b64_string = base64.b64encode(img_file.read())
                    textContext = str(b64_string.decode('utf-8'));
                    context['jpegContext'] = textContext;
                    html_template = loader.get_template('decompiler/java_decom_jpeg_detail.html')
                else:
                    f = open(FILE_PATH, 'r',encoding="unicode_escape")
                    textContext = f.read()
                    f.close()
                    context['fileContextLines'] = textContext.strip();
                    html_template = loader.get_template('decompiler/java_decom_class_detail.html')
            else:
                context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
                html_template = loader.get_template('404.html')
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
        html_template = loader.get_template('404.html')
    return HttpResponse(html_template.render(context, request))



#############################
#############################
#############################

# 主页
def apkDecompilersIndex(request):
    context = {};
    context['segment'] = 'index';
    html_template = loader.get_template('decompiler/apk_decompiler.html')
    return HttpResponse(html_template.render(context, request))

# apkDecompilers 跳转到apk_decompiler.html
def apkDecompilers(request):
    context = {};
    context['segment'] = 'index';
    t = time.time()
    customerID = (int(round(t * 1000)))
    context['customerID'] = customerID;
    html_template = loader.get_template('decompiler/apk_decompiler.html')
    return HttpResponse(html_template.render(context, request))


#上传jar、class文件
@csrf_exempt
def apkDecompilerAnalyze(request):
    context = {};
    try:
        if len(request.FILES)==0:
            html_template = loader.get_template('decompiler/apk_decompiler_analyze.html')
        else:
            uploadFile = request.FILES['file']
            customerID = request.POST["customerID"];
            if customerID is None or customerID == "":
                t = time.time()
                context = {};
                customerID = (int(round(t*10000)))
            context['customerID'] = customerID;
            if uploadFile is not None and uploadFile != "":
                file, customerID, filesChilds,endFile = analyzeJAVA(customerID, uploadFile)
                reList=[]
                reList.append(FileUrlPath(endFile, endFile));
                context['uploadFileName'] = file;       #用户上传的文件名
                context['filePath'] = reList;               #用户上传的文件路径,初始上传时，显示文件名
                context['filesChilds'] = filesChilds;   #文件路径
                html_template = loader.get_template('decompiler/apk_decompiler_analyze.html')
            else:
                html_template = loader.get_template('decompiler/apk_decompiler_analyze.html')
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        context['errorInfo'] = "Error parsing the file, you need to upload it again!";
        html_template = loader.get_template('404.html')

    return HttpResponse(html_template.render(context, request))

# 解析文件路径
def analyzeFilePathAPK(customerID,endFile,currentPath):
    '''
    :param customerID: 客户编号
    :param endFile: 本次生成的文件夹名字
    :param currentPath: 当前要显示的路径
    :return:
    '''
    endList = [];
    FILE_PATH = constant.FILE_PATH;
    if endFile==currentPath:
        FILE_PATH=FILE_PATH+"/"+customerID+"/"+endFile; # 得到当前点击的路径信息
        prefixFileTemp=endFile;
    else:
        FILE_PATH = FILE_PATH + "/" + customerID + "/" + currentPath;  # 得到当前点击的路径信息
        prefixFileTemp = currentPath;
    filesChild = os.listdir(FILE_PATH)
    for filename in filesChild:
        tmp = urllib.parse.quote(prefixFileTemp+"/"+filename);  # 进行base64url编码
        pathTmp=os.path.join(FILE_PATH, filename) ;
        createTime = os.path.getctime(pathTmp); #文件创建时间
        timeArray = time.localtime(createTime)
        createTime = time.strftime("%b %d %Y %h:%M:%S", timeArray)

        if os.path.isdir(pathTmp):  # 判断是否为目录
            endList.append(FileItem(tmp, filename, "<System Dir>", "Directory", createTime, "folder.png"));
        elif os.path.isfile(pathTmp):  # 判断是否为文件
            fileType = os.path.splitext(filename)[-1]
            filesize = os.path.getsize(pathTmp)  # 如果是文件，则获取相应文件的大小
            fileIcon,fileType=getFileInfo(fileType);
            endList.append(FileItem(tmp,  filename, fileType, covertFukeSize(filesize), createTime, fileIcon));
    return endList;

# 解析java文件
def analyzeAPK(customerID, upload):
    FILE_PATH = constant.FILE_PATH;
    folder = os.path.exists(FILE_PATH+"/"+str(customerID))
    if not folder:  # 判断是否存在文件夹如果不存在则创建文件夹
        os.makedirs(FILE_PATH+"/"+str(customerID))
    #保存文件
    fss = FileSystemStorage(FILE_PATH+"/"+str(customerID))
    file = fss.save(upload.name, upload)

    #判断文件类型
    endFile = "";       #文件扩展名
    allFileName = "";   #文件全名
    if "." in upload.name:
        endFile = upload.name[0:upload.name.rindex(".")]; #截取最右侧.之前的名字
        allFileName=upload.name;
    else:
        endFile = upload.name;
        allFileName=upload.name;
    try:
        paths = 'java -Xmx64m -jar '+settings.APKTOOL_HOME+' d -f ' + FILE_PATH + '/' + allFileName + " -o " + FILE_PATH;
        # print(paths)
        os.system(paths)

        paths = settings.JADX_HOME + FILE_PATH + '/' + endFile + "/java/  " + FILE_PATH + '/' + endFile + "/smali/ ";
        # print(paths)
        os.system(paths)

        folder = os.path.exists(FILE_PATH + "/" + str(customerID) + '/' + endFile)
        if not folder:  # 判断是否存在文件夹如果不存在则创建文件夹
            os.makedirs(FILE_PATH + "/" + str(customerID) + '/' + endFile)

    except Exception as e:
        traceback.print_exc()
        logger.error(e)
    # path = FILE_PATH+"/"+str(customerID) + '/' + endFile;
    # path = FILE_PATH+"/"+str(customerID) ;
    endList = analyzeFilePathAPK(str(customerID),endFile,endFile);


    return file,customerID,endList,endFile;

#点击java文件夹后，显示文件下的所有文件
@csrf_exempt
def apkDecompilerFolder(request):
    context = {};
    try:
        uploadFileName = request.GET.get("uploadFileName");
        filePath = request.GET.get("filePath");
        customerID = request.GET.get("customerID");
        context['customerID'] = customerID;
        context['uploadFileName'] = uploadFileName;

        if customerID is None or customerID == ""\
                or filePath is None or filePath ==""\
                or uploadFileName is None or uploadFileName == "":
            html_template = loader.get_template('404.html')
            context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
        else:
            uploadFileFolder = uploadFileName[0:uploadFileName.rindex(".")];  # 截取最右侧.之前的名字
            # path = constant.FILE_PATH +"/"+str(customerID) +"/"+ uploadFileFolder; #根路径，包括包的名字
            currentPath = filePath;  # 当前选择的路径

            if ("/"+uploadFileFolder)==currentPath: #如果选择的是根路径，不需要再加上包的名字
                # currentPath="";
                context['filePath'] = covertFileUrlPath((currentPath).split('/'),uploadFileFolder);  # 当前根路径
            else:
                context['filePath'] = covertFileUrlPath((filePath).split('/'),uploadFileFolder);  # 当前显示的文件路径

            filesChilds = analyzeFilePathAPK(str(customerID),uploadFileFolder,currentPath);

            # print(context['filePath'])
            context['uploadFileName'] = uploadFileName;# 用户上传的文件名
            context['filesChilds'] = filesChilds;# 文件路径

            html_template = loader.get_template('decompiler/apk_decompiler_analyze.html')
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
        html_template = loader.get_template('404.html')


    return HttpResponse(html_template.render(context, request))


# @csrf_exempt
def apkDecompileFileDetail(request):
    context = {};
    textContext = "";
    try:
        FILE_PATH = constant.FILE_PATH;
        filePath = request.GET.get("filePath")  #显示的文件路径
        customerID = request.GET.get("customerID");
        uploadFileName = request.GET.get("uploadFileName");
        context['customerID'] = customerID;
        context['uploadFileName'] = uploadFileName;
        if customerID is None or customerID == "" \
                or filePath is None or filePath == ""\
                or uploadFileName is None or uploadFileName =="":
            html_template = loader.get_template('404.html')
            context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
        else:
            uploadFileFolder = uploadFileName[0:uploadFileName.rindex(".")];  # 截取最右侧.之前的名字
            FILE_PATH=FILE_PATH+"/"+customerID+"/"+filePath; # 根路径信息
            isdir = os.path.isdir(FILE_PATH);
            context['filePath'] = covertFileUrlPath(filePath.split('/'),uploadFileFolder);
            if not isdir:
                root, extension = os.path.splitext(FILE_PATH);  # 取得文件扩展名
                if (extension in [".png", ".jpg", ".jpeg", "gif"]):
                    with open(FILE_PATH, "rb") as img_file:
                        b64_string = base64.b64encode(img_file.read())
                    textContext = str(b64_string.decode('utf-8'));
                    context['jpegContext'] = textContext;
                    html_template = loader.get_template('decompiler/apk_decom_jpeg_detail.html')
                elif (extension in [".dex", ".jpg", ".jpeg", "gif"]):
                    f = open(FILE_PATH, 'r',encoding='latin-1')
                    textContext = f.read()
                    f.close()
                    context['fileContextLines'] = textContext.strip();
                    html_template = loader.get_template('decompiler/apk_decom_class_detail.html')
                else:
                    f = open(FILE_PATH, 'r',encoding="unicode_escape")
                    textContext = f.read()
                    f.close()
                    context['fileContextLines'] = textContext.strip();
                    html_template = loader.get_template('decompiler/apk_decom_class_detail.html')
            else:
                context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
                html_template = loader.get_template('404.html')
    except Exception as e:
        traceback.print_exc()
        logger.error(e)
        context['errorInfo'] = "The file is only saved for 48 hours and needs to be re-uploaded by you!";
        html_template = loader.get_template('404.html')
    return HttpResponse(html_template.render(context, request))

#转化文件大小单位
def covertFukeSize(size):
    kb = 1024;
    mb = kb * 1024;
    gb = mb * 1024;
    tb = gb * 1024;

    if size >= tb:
        return "%.2f TB" % float(size / tb)
    if size >= gb:
        return "%.2f GB" % float(size / gb)
    if size >= mb:
        return "%.2f MB" % float(size / mb)
    if size >= kb:
        return "%.2f KB" % float(size / kb)
    return  "%.2f Byte" % float(size)

#转化一下显示多级目录时的文件路径
def covertFileUrlPath(files,rootPath):
    tmpUrl="";
    reFileUrlPath=[];
    for item in files:
        if item != rootPath:
            tmpUrl=tmpUrl+"/"+item;
        else:
            tmpUrl=rootPath;
        reFileUrlPath.append(FileUrlPath(item,tmpUrl));
    return reFileUrlPath;



@csrf_exempt
def downloadZip(request):
    FILE_PATH = constant.FILE_PATH;
    customerID = request.GET.get("customerID");
    uploadFileName = request.GET.get("uploadFileName");

    fileName=uploadFileName[0:uploadFileName.rindex(".")];
    shutil.make_archive(FILE_PATH+"/"+customerID+"/"+fileName, 'zip', FILE_PATH+"/"+customerID+"/"+fileName)

    response = HttpResponse(FileWrapper(open(FILE_PATH+"/"+customerID+"/"+fileName+".zip", 'rb')), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename="{filename}"'.format(
        filename=fileName+".zip".replace(" ", "_")
    )
    os.remove(FILE_PATH+"/"+customerID+"/"+fileName+".zip")
    return response



def getEndFileName(fileName):
    fileName = fileName.split("/");
    return fileName[len(fileName) - 1:len(fileName)][0];



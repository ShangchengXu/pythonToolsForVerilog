from enum import Flag
import os
import re
# import uvm_gen as ug
from file_analyse import File_analyse as fa
# path = "../verilog_python"
class Verilog_tools:
    def __init__(self):
        self.keyword = ['always', 'and', 'assign', 'begin', 'buf', 'bufif0', 'bufif1', 'case', 'casex', 'casez', 'cmos', 'deassign',
           'default',
           'defparam', 'disable', 'edge', 'else', 'end', 'endcase', 'endmodule', 'endfunction', 'endprimitive',
           'endspecify',
           'endtable', 'endtask', 'event', 'for', 'force', 'forever', 'fork', 'function', 'highz0', 'highz1', 'if',
           'initial',
           'inout', 'input', 'integer', 'join', 'large', 'macromodule', 'medium', 'module', 'nand', 'negedge', 'nmos',
           'nor', 'not', 'notif0',
           'notifl', 'or', 'output', 'parameter', 'pmos', 'posedge', 'primitive', 'pull0', 'pull1', 'pullup',
           'pulldown', 'rcmos',
           'reg', 'releses', 'repeat', 'mmos', 'rpmos', 'rtran', 'rtranif0', 'rtranif1', 'scalared', 'small', 'specify',
           'specparam',
           'strength', 'strong0', 'strong1', 'supply0', 'supply1', 'table', 'task', 'time', 'tran', 'tranif0',
           'tranif1', 'tri',
           'tri0', 'tri1', 'triand', 'trior', 'trireg', 'vectored', 'wait', 'wand', 'weak0', 'weak1', 'while', 'wire',
           'wor', 'xnor', 'xor','extends','uvm_report_server','int','void','virtual','new','uvm_analysis_port','super'
           ,'extern0',"uvm_component_utils","type_id",'bit','byte','unsiged','shortint','longint','timer','real','interface','class',
           'logic','genvar','uvm_tlm_analysis_fifo','uvm_blocking_get_port','constraint','import','uvm_active_passive_enum','define','undef'
           ,'ifdef','elsif','endif',"uvm_object_utils_begin","uvm_object_utils_end"]
# path = "/home/IC/xsc"
        self.filename = "fifo_ctr"
        self.rtl_filemap = {}
        self.rtl_definemap = {}
        self.test_filemap = {}
        self.test_definemap = {}
    # except_module = ['assert_never_unknown']
        self.except_module = []
        self.mapGenFlag = False
        self.SourcePath = []
        self.TargetPath = ""
        self.moduleFound = []
        self.fa = fa("")

    def test_map_initial(self):
            os.chdir(os.path.dirname(__file__))
            for relpath, dirs, files in os.walk(self.TargetPath):
                for File in files:
                    if re.match('.+\.s?v$', File) is not None:
                        fp = open(os.path.join(relpath, File), "r", errors="ignore")
                        str = fp.read()
                        str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
                        # str_temp = re.sub(r'//.*',"",str_temp)
                        str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
                        str_temp = re.sub("\$.*?;","",str_temp,flags=re.S)
                        str_temp = re.sub("\".*?\"","",str_temp,flags=re.S)
                        full_path = os.path.join(relpath, File)
                        real_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                        module_temp =  re.findall('\\b(module|interface|class|program)\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\\b', str_temp)
                        define_temp = self.fa.find_define_word(str_temp) 
                        for item in module_temp:
                            # flag_file = 0
                            if ((item[1]  in self.test_filemap) and (real_path.strip() != self.test_filemap[item[1]].strip())):
                                    print("find mutidefine module\n" + item[0])
                                    print(os.path.normpath(os.path.abspath(full_path)).replace("\\", "/") + " Y ")
                                    print(self.test_filemap[item[1]] + " N ")
                                    # sel = input("select:")
                                    # if sel == "Y":
                                    #     self.test_filemap.update({item[1]:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                            elif item[1]  not in self.test_filemap :
                                self.test_filemap.update({item[1]:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                        for item in define_temp:
                            if ((item[0]  in self.test_definemap)  and (real_path.strip() != self.test_definemap[item[0]][0].strip())):
                                    print("find mutidefine define_word\n" + item[0])
                                    print(os.path.normpath(os.path.abspath(full_path)).replace("\\", "/") + " Y ")
                                    print(self.test_definemap[item[0]] + " N ")
                                    # sel = input("select:")
                                    # if sel == "Y":
                                    #     self.test_definemap.update({item:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                            elif item[0] not in self.test_definemap:
                                self.test_definemap.update({item[0]:[os.path.normpath(os.path.abspath(full_path)).replace("\\", "/"),item[1]]})

    def rtl_map_initial(self):

        os.chdir(os.path.dirname(__file__))
        for start in self.SourcePath:
            for relpath, dirs, files in os.walk(start):
                for File in files:
                    if re.match('.+\.s?v$', File) is not None:
                        fp = open(os.path.join(relpath, File), "r", errors="ignore")
                        str = fp.read()






                        str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
                        # str_temp = re.sub(r'//.*',"",str_temp)
                        str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
                        str_temp = re.sub("\$.*?;","",str_temp,flags=re.S)
                        # str_temp = re.sub("\".*?\"","",str_temp,flags=re.S)

                        full_path = os.path.join(relpath, File)
                        real_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                        module_temp =  re.findall('\\b(module|interface|class|program)\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\\b', str_temp)
                        define_temp = self.fa.find_define_word(str_temp) 
                        for item in module_temp:
                            # flag_file = 0
                            if ((item[1]  in self.rtl_filemap) and (real_path.strip() is not self.rtl_filemap[item[1]].strip())):
                                    print("find mutidefine module  " +item[1] )
                                    # print(real_path + " Y ")
                                    # print(self.rtl_filemap[item[1]] + " N ")
                                    # sel = input("select:")
                                    # if sel == "Y":
                                    #     self.rtl_filemap.update({item[1]:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                            elif item[1] not in self.rtl_filemap:
                                    self.rtl_filemap.update({item[1]:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                                        
                        for item in define_temp:
                            if ((item[0]  in self.rtl_definemap) and (real_path.strip() != self.rtl_definemap[item[0]][0].strip())):
                                    print("find mutidefine define_word  " + item[0] )
                                    # print(real_path + " Y ")
                                    # print(self.rtl_definemap[item] + " N ")
                                    # sel = input("select:")
                                    # if sel == "Y":
                                    #     self.rtl_definemap.update({item:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                            elif item[0] not in self.rtl_definemap:
                                self.rtl_definemap.update({item[0]:[os.path.normpath(os.path.abspath(full_path)).replace("\\", "/"),item[1]]})
                                # self.filemap[item[1]] = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
        # return out_path
    def map_initial(self):
        self.rtl_map_initial()
        self.test_map_initial()
        # fp = open("/home/IC/map.txt","w+")
        # for key in self.rtl_definemap:
        #     fp.write(key + "\n")
        # fp.close()
        # fp = open("/home/IC/rtl_map.txt","w+")
        # for key in self.rtl_filemap:
        #     fp.write(key + "\n")
        # fp.close()

        self.mapGenFlag = True



    def find_port(self,filename,name):
        # ports = []
        # parameters = []
        # parameters_all = []
        fd = open(filename, errors='ignore')
        str = fd.read()
        string = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
        string = re.sub('//.*?\n', "", string, flags=re.S)
        match = re.search("\\bmodule\s*"+name+"\s*.*?\\bendmodule\\b",string,flags=re.S)
        if match == None:
            print("error")
            return [[],[],[]]
    
        return self.fa.find_port_parameter(match.group()) 


    def find_define(self,path):
        fp = open(path, "r", errors="ignore")
        string = fp.read()

        return self.fa.find_define(string)


    def find_rtl_define_file(self,path, define_word):
        out_path = ""
        if self.mapGenFlag is not True:
            self.map_initial()
        if define_word not in self.rtl_definemap:
            print("waring: define "+ define_word + " not find ")
        return self.rtl_definemap.get(define_word)[0]
    
    def find_test_define_file(self,path, define_word):
        out_path = ""
        if self.mapGenFlag is not True:
            self.map_initial()
        if define_word not in self.test_definemap:
            print("waring: define "+ define_word + " not find ")
        return self.test_definemap.get(define_word)[0]
    
        for start in path:
            for relpath, dirs, files in os.walk(start):
                for File in files:
                    if re.match('.+\.s?v$', File) is not None:
                        fp = open(os.path.join(relpath, File), "r", errors="ignore")
                        str = fp.read()
                        # str_temp = re.sub("\/\*[\s\S]*?\*\/", "", str)
                        # str_temp = re.sub(r'//.*$',"",str_temp)
                        # str_temp = re.sub('//[\s\S]*?\n', "", str_temp)
                        res_temp = self.fa.find_define_word(str) 
                        # print(File)

                        full_path = os.path.join(relpath, File)
                        # if(re.match(name + '.s?v$',File) != None):
                        # res_temp = re.findall("`define\s*([\S]*)\s*",str_temp)
                        for item in res_temp:
                            if item  not in self.definemap:
                               self.definemap.update({item:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                            # if item  not in self.definemap:
                            #     self.definemap[item] = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")




                        # if re.search('`define\s*(\\b'+define_word+'\\b)', str_temp) is not None:
                        if define_word in res_temp:
                        # for 
                            if out_path == "":
                                out_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                            else:
                                print("find mutidefine\n")
                                print(os.path.normpath(os.path.abspath(full_path)).replace("\\", "/") + "Y")
                                print(out_path + "N")
                                sel = input("select:")
                                if sel == "Y":
                                    out_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                            # return out_path
                            # print(full_path)
                            # return os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
        return out_path


    def find_module(self,path,flag):
        fp = open(path, "r", errors="ignore")
        if self.mapGenFlag is not True:
            self.map_initial()
        str = fp.read()
        # str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
        # str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)
        # str_temp = re.sub('\\bif\s*\(', " if \(; ", str_temp, flags=re.S)
        # str_temp = re.sub('\\bcase\s*\(', "case \(; ", str_temp, flags=re.S)
        # str_temp = re.sub('\\bextern.*?;', " ; ", str_temp, flags=re.S)
        # str_temp = re.sub('\\bfunction.*?\\bendfunction', " ; ", str_temp, flags=re.S)
        # str_temp = re.sub('\\bdefine.*', " ; ", str_temp)
        # str_temp = re.sub('\\btask.*?\\bendtask', " ; ", str_temp, flags=re.S)

        modules = []
        # if flag == 0 or flag == 5:
        #     result = re.findall("#\(\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*\)",str_temp,flags=re.S)
        #     for item in result:
        #         if(item not in self.keyword):
        #             modules.append(item)

        # str7 = "(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\s*(?:\(.*?\))?;"
        # str6 = "(\\b[a-zA-Z_`][a-zA-Z0-9_$]*\\b)\s*(?:#\s*\([^;]*?\))?\s*(\\b[a-zA-Z_`][a-zA-Z0-9_$]*\\b)\s*\([^;]*?\)\s*;"

        if flag != 1:
            # result = re.findall(str7, str_temp,flags=re.S)
            result = self.fa.find_module_uvm(str)
        else:
            # result = re.findall(str6, str_temp,flags=re.S)
            result = self.fa.find_module_inst(str)[1]


        for item in result:
            if (item not in self.except_module):
                modules.append(item)

        return modules

    def find_test_file(self,starts, name):
        if self.mapGenFlag is not True:
            self.map_initial()
        out_path = ""
        if name not in self.test_filemap:
            self.test_map_initial()
            if name not in self.test_filemap:
                print("warning module " + name + " not find")

        return self.test_filemap.get(name)

    def find_rtl_file(self,starts, name):
        if self.mapGenFlag is not True:
            self.map_initial()
        out_path = ""
        if name not in self.rtl_filemap:
            self.rtl_map_initial()
            if name not in self.rtl_filemap:
                print("warning module " + name + " not find")

        return self.rtl_filemap.get(name)
        for start in starts:
            for relpath, dirs, files in os.walk(start):
                for File in files:
                    if re.match('.+\.s?v$', File) is not None:
                        fp = open(os.path.join(relpath, File), "r", errors="ignore")
                        str = fp.read()
                        str_temp = re.sub("\/\*.*?\*\/", "", str, flags=re.S)
                        # str_temp = re.sub(r'//.*',"",str_temp)
                        str_temp = re.sub('//.*?\n', "", str_temp, flags=re.S)

                        full_path = os.path.join(relpath, File)
                        res_temp =  re.findall('\\b(module|interface|class|program)\\b\s*(\\b[a-zA-Z_][a-zA-Z0-9_$]*\\b)\\b', str_temp)
                        for item in res_temp:
                            # flag_file = 0
                            if item[1] not in self.filemap:
                                self.filemap.update({item[1]:os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")})
                                # self.filemap[item[1]] = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                        if re.search('\\b(module|interface|class|program)\\b\s*' + name + '\\b', str_temp) is not None:
                                if out_path == "":
                                    out_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
                                else:
                                    print("find mutidefine\n")
                                    print(os.path.normpath(os.path.abspath(full_path)).replace("\\", "/") + "Y")
                                    print(out_path + "N")
                                    sel = input("select:")
                                    if sel == "Y":
                                        out_path = os.path.normpath(os.path.abspath(full_path)).replace("\\", "/")
        return out_path

    def dfs(self,lists:list,index:int,flags = 1) -> list:
        # if index >= len(lists):
        #     return []
        for i in range(index,len(lists)):
            if lists[i] in self.moduleFound:
                return lists[index:i] + (self.dfs(lists,i+1,flags))
            if flags == 1:
                path = self.find_rtl_file(self.SourcePath,lists[ i ])
            else:
                path = self.find_test_file(self.TargetPath,lists[ i ])
            list_temp = self.find_module(path,flags)
            # defines_temp = self.find_define(path)
            # for define in defines_temp:
            #     if flags == 1:
            #         if define not in define_words:
            #             define_file = self.find_rtl_define_file(self.SourcePath, define)
            #             if define_file not in lists_root and define_file != "":
            #                 lists_root.append(define_file)
            #             define_words.append(define)
            #     else:
            #         define_file = self.find_test_define_file(self.SourcePath, define)
            self.moduleFound.append(lists[i])
            if len(list_temp) != 0:
                # if i == 0:
                #     return [].append(self.dfs(list_temp, 0, flags)).append(lists[i]).append(self.dfs(lists,i + 1, flags))
                # else:
                list1 = lists[index:i]+ (self.dfs(list_temp, 0, flags))
                list1.append(lists[i])
                list3 = list1 + (self.dfs(lists,i + 1, flags))
                return list3
                return lists[0:i].append(self.dfs(list_temp, 0, flags)).append(lists[i]).append(self.dfs(lists,i + 1, flags))

        return lists[index:len(lists)]

    def filelist_gen(self,source_path, target_path, name, flags,flag1):
        os.chdir(os.path.dirname(__file__))
        if self.mapGenFlag is not True:
            self.map_initial()
        os.chdir(os.path.dirname(__file__))
        # path = self.find_rtl_file(source_path, name)
        if flags == 1:
            path = self.find_rtl_file(source_path, name)
            defines = self.find_define(path)
            lists_root = []
            define_words = []
            for item in defines:
                if item not in define_words:
                    define_words.append(item)
                define_files = self.find_rtl_define_file(source_path, item)
                if define_files not in lists_root:
                    lists_root.append(define_files)
        else:
            path = self.find_test_file(source_path,name)
            defines = self.find_define(path)
            lists_root = []
            # for item in defines:
            #     define_files = self.find_test_define_file(source_path, item)
            #     if define_files not in lists_root:
            #         lists_root.append(define_files)

           
        # lists_root = []
        # if flags == 1:
        #     defines = self.find_define(path)
        #     lists_root = []
        #     for item in defines:
        #         define_files = self.find_define_file(source_path, item)
        #         if define_files not in lists_root:
        #             lists_root.append(define_files)

        lists = self.find_module(path,flags)
        flag = 1
        list_pass = []
        # self.moduleFound.append("")
        lists = self.dfs(lists,0,flags)
        # fp = open("/home/IC/log.txt","w+",errors="ignore")
        for item in lists:
            if flags == 1:
                path_local = self.find_rtl_file(self.SourcePath,item)
                # print(path_local+"\n")
                string = open(path_local,"r",errors="ignore").read()
                define_temp = self.find_define(path_local)
                for define in define_temp:
                    # fp.write(define +  "\n")
                    if define not in define_words:
                        # fp.write(define + "\n")
                        define_file = self.find_rtl_define_file(source_path, define)
                        if define_file not in lists_root and define_file != "":
                            lists_root.append(define_file)
                        define_words.append(define)
        # fp.close()
        # while flag == 1:
        #     list_temp = []
        #     flag = 0
        #     for list in lists:
        #         modules = []
        #         if list not in list_temp:
        #             if flags == 1:
        #                 dic = self.find_rtl_file(source_path,list)
        #             else:
        #                 dic = self.find_test_file(source_path,list)
        #             if dic == "":
        #                 print("error: module unfind = "+ list + "\n")
        #             else:
        #                 modules = self.find_module(dic,flags)            
        #                 defines_temp = self.find_define(dic)
        #                 for define in defines_temp:
        #                     if flags == 1:
        #                         if define not in define_words:
        #                             define_file = self.find_rtl_define_file(source_path, define)
        #                             if define_file not in lists_root and define_file != "":
        #                                 lists_root.append(define_file)
        #                             define_words.append(define)
        #                     else:
        #                         define_file = self.find_test_define_file(source_path, define)
                        
        #                 for module in modules:
        #                     if module not in list_temp:
        #                         list_temp.append(module)
        #                     if module not in lists:
        #                         flag = 1
        #                 list_temp.append(list)
        #     lists = list_temp
        # if flags == 1 or flags == 3:
        #     for list in lists:
        #         defines_temp = self.find_define(self.find_file(source_path,list))
        #         for define in defines_temp:
        #             define_file = self.find_define_file(source_path, define)
        #             if define_file not in lists_root and define_file != "":
        #                 lists_root.append(define_file)
        os.chdir(target_path)
        name_temp = re.sub("_base_test$","",name)
        if flags != 1:
            fk = open(name_temp+"_package.sv","w")
            fk.write("import uvm_pkg::*;\n")
            fk.close()
        if flags != 1 :
            fo = open("filelist_uvm_base.f","w")
            path_temp = os.path.relpath(os.path.abspath(os.path.dirname(name_temp+"_package.sv")).replace("\\", "/") + "/"+name_temp+'_package.sv',target_path).replace("\\","/")
            # fo.write(os.path.abspath(os.path.dirname(name_temp+"_package.sv")).replace("\\", "/") + "/"+name_temp+'_package.sv' + "\n")
            fo.write(path_temp + "\n")
            os.chdir(os.path.dirname(__file__))
            file_path_temp = []
            for item in lists:
                temp_path = self.find_test_file(source_path,item)
                if temp_path not in file_path_temp:
                    file_path_temp.append(temp_path)
            for item in file_path_temp:
                fo.write(os.path.relpath(item,target_path).replace("\\","/") + "\n")
            fo.write(os.path.relpath(path,target_path).replace("\\","/") + "\n")
            fo.close()
        if flag1 == 1:
            os.chdir(target_path)
            fl = open("filelist_uvm_case.f","w")
            os.chdir(os.path.dirname(__file__))
            fl.write(os.path.relpath(self.find_test_file(source_path,name_temp+"_case0"),target_path).replace("\\","/")+"\n")
            fl.close()
            os.chdir(target_path)
            fl = open("filelist_uvm.f","w")
            fl.write("-f "+os.path.relpath(os.path.abspath(os.path.dirname("filelist_uvm_base.f")).replace("\\", "/") + '/filelist_uvm_base.f',target_path).replace("\\","/") + "\n")
            fl.write("-f "+os.path.relpath(os.path.abspath(os.path.dirname("filelist_uvm_case.f")).replace("\\", "/") + '/filelist_uvm_case.f',target_path).replace("\\","/")+ "\n")
            fl.close()



        if flags == 1:
            os.chdir(target_path)
            fp = open("filelist_modules.f", "w")
            os.chdir(os.path.dirname(__file__))
            file_path_temp = []
            for item in lists:
                temp_path = self.find_rtl_file(source_path,item)
                if temp_path not in file_path_temp:
                    file_path_temp.append(temp_path)
            for item in file_path_temp:
                if item is not None:
                    fp.write(os.path.relpath(item,target_path).replace("\\","/") + "\n")
            if flag1 == 1:
                fp.write(os.path.relpath(path,target_path).replace("\\","/") + "\n")
            fp.close()
        if flags == 1:
            os.chdir(target_path)
            fq = open("filelist_defines.f", "w")
            os.chdir(os.path.dirname(__file__))
            for item in lists_root :
                if  item not in file_path_temp and item is not None :
                    fq.write(os.path.relpath(item,target_path).replace("\\","/") + "\n")
            fq.close()
        if flags == 1:
            os.chdir(target_path)
            fj = open("filelist.f", "w")
            fj.write("-f "+ os.path.relpath(os.path.abspath(os.path.dirname("filelist_defines.f")).replace("\\", "/") +"/filelist_defines.f",target_path).replace("\\","/")+ "\n")
            fj.write("-f "+ os.path.relpath(os.path.abspath(os.path.dirname("filelist_modules.f")).replace("\\", "/") + '/filelist_modules.f',target_path).replace("\\","/") + "\n")
            fj.write("-f "+ os.path.relpath(os.path.abspath(os.path.dirname("filelist_uvm.f")).replace("\\", "/") + '/filelist_uvm.f',target_path).replace("\\","/") + "\n")
            fj.close()


    def makefile_src_gen(self,target_path, name):
        path = self.make_sim_dic(target_path,name)
        os.chdir(path)
        fp = open("makefile", "w")
        fp.write("OUTPUT = " + name + "TB\n")
        fp.write("export name = ${OUTPUT}\n")
        fp.write("VCS:\n")
        fp.write("\tvcs  +acc +vpi  -full64 +v2k -sverilog +incdir+"+r"${UVM_HOME}/src  ${UVM_HOME}/src/uvm_pkg.sv ${UVM_HOME}/src/dpi/uvm_dpi.cc -CFLAGS -DVCS -lca -kdb -timescale=1ns/1ps -debug_acc+all -debug_region+cell+encrypt -LDFLAGS -rdynamic  ")
        fp.write(r"-P ${VERDI_HOME}/share/PLI/VCS/LINUX64/novas.tab ")
        fp.write(r"${VERDI_HOME}/share/PLI/VCS/LINUX64/pli.a ")
        fp.write(r" -f filelist.f  -l sim.log" + " ./" + name + "TB.sv\n")
        str = "VERDI:\n\tverdi -f file_list.f " + r"-ssf ${OUTPUT}.fsdb -nologo  -l v.log " + "\n"
        fp.write(str)
        str = "SIM:\n\t" + r"./simv  +UVM_TESTNAME="+name+"_case0 -gui=verdi -i  "+ " ./run.scr  +fsdbfile+" + r"${OUTPUT}.fsdb" " + autoflush  -l sim.log" + "\n"
        fp.write(str)
        str = "SIM_NO_GUI:\n\t" + r"./simv  +UVM_TESTNAME="+name+"_case0  -l sim.log" + "\n"
        fp.write(str)
        str = "CLEAN:\n\t" + "rm -rf  ./verdiLog  ./dff ./csrc *.daidir *log *.vpd *.vdb simv* *.key *race.out* *.rc *.fsdb *.vpd *.log *.conf *.dat *.conf\n"
        fp.write(str)
        str = "TEST: VCS SIM\n"
        fp.write(str)
        str = "CASE: VCS SIM_NO_GUI"
        fp.write(str)
        fp.close()
        fp = open("run.scr", "w")
        str = "global env\n#fsdbDumpfile " + '"$env(name).fsdb"\n' + 'fsdbDumpvars 0 "$env(name)" \nrun'
        fp.write(str)
        fp.close()


    def file_inst(self,dic, path, flags=1):
        os.chdir(os.path.dirname(__file__))
        # path = self.find_file(dic, name)
        fp = open(path, "r+", errors='ignore')
        lines = fp.readlines()
        fp.close()
        fp = open(path + '.bak', 'w', errors='ignore')
        fp.writelines(lines)
        fp.close()
        fp = open(path, "w+")
        for lineT in lines:
            resTemp = re.search('(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s+(\\b[a-zA-Z_][a-zA-Z0-9_$]+\\b)\s*\(/\*inst\*/\)', lineT)
            if resTemp is not None:
                # fp.write(resTemp.group(1) + " " + resTemp.group(2) + " " + r"(" + "\n")
                ports = self.find_port(self.find_rtl_file(dic, resTemp.group(1)),resTemp.group(1))
                lenStr = 0
                for port in ports[0]:
                    if len(port[3]) > lenStr:
                        lenStr = len(port[3])
                for para in ports[1]:
                    if len(para) > lenStr:
                        lenStr = len(para)
                if len(ports[1]) != 0:
                    fp.write(resTemp.group(1) + " #(\n")
                    for para in ports[1]:
                        if flags==1:
                            if para == ports[1][len(ports[1]) - 1]:
                                fp.write(" " * 8 + r"." + para+ " " * (lenStr + 2 - len(para)) + r"())" + "\n")
                            else:
                                fp.write(" " * 8 + r"." + para+ " " * (lenStr + 2 - len(para)) + r"()," + "\n")
                        else:
                            if para == ports[1][len(ports[1]) - 1]:
                                fp.write(" " * 8 + r"." + para+ " " * (lenStr + 2 - len(para)) + r"(" + para+ " " * (lenStr + 2 - len(para))  + r"))" + "\n")
                            else:
                                fp.write(" " * 8 + r"." + para+ " " * (lenStr + 2 - len(para)) + r"(" + para+ " " * (lenStr + 2 - len(para))  + r")," + "\n")

                    fp.write(" " * len(resTemp.group(1)) + " " + resTemp.group(2) + " " + r"(" + "\n")
                else:
                    fp.write(resTemp.group(1) + " " + resTemp.group(2) + " " + r"(" + "\n")

                        # print(lenStr)

                for port in ports[0]:
                    if flags==1:
                        if port == ports[0][len(ports[0]) - 1]:
                            fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"());" + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")
                        else:
                            fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"() ," + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")
                    else:
                        if port == ports[0][len(ports[0]) - 1]:
                            fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"("+ port[3] + " " * (lenStr + 2 - len(port[3]))  + r"));" + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")
                        else:
                            fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"("+ port[3] + " " * (lenStr + 2 - len(port[3]))  + r") ," + r"//" + port[0] + " " * (8 - len(port[0])) + port[2] + "\n")

            else:
                fp.write(lineT)
        fp.close()
    def autodefine(self,fullpath):
        os.chdir(os.path.dirname(__file__))
        fp = open(fullpath,"r")
        string = fp.read()
        fs = open(fullpath+"bak","w+")
        fs.write(string)
        fs.close()
        fp.close()
        res = re.findall("\\bmodule.*?\\bendmodule\\b",string,flags=re.S)
        for item in res:
            string_rep = ""
            [vardefine,string_out] = self.fa.find_varDefine(item)
            [ports ,paras ,para_all]= self.fa.find_port_parameter(item)
            for i in para_all:
                string_out = string_out.replace(i,"")
            for port in ports:
                var_name = port[3]
                varAttr = {"type":"wire","width":0,"has_load":False,"has_drive":False,"signed":"","only_inst_port_connect_width":0,"reWrite":True}
                varAttr["type"] = "reg" if port[1] == "reg" else "wire"
                varAttr["width"] = port[2]
                varAttr["reWrite"] = False
                vardefine.update({var_name:varAttr})
            [detail_module,modules] = self.fa.find_module_inst(string)
            text_used = self.fa.text_used(item)
            port_use = {}
            for module in modules:
               path = self.find_rtl_file(self.SourcePath,module)
               [ports_local,para_local,para_all_local] = self.find_port(path,module)
               portAttr = {}
               for item1 in ports_local:
                   port_name = item1[3]
                   port_width = item1[2]
                   portAttr.update({port_name:port_width})
               port_use.update({module:portAttr})
            for module in detail_module.keys():
                value = detail_module[module]
                port_con = port_use[value["type"]]
                for item2 in value["con"]:
                    pattern = re.compile("[`a-z_A-Z][a-zA-Z0-9_]*",flags=re.S)
                    text_used = text_used + " " + item2

                    if pattern.match(item2) != None:
                        varAttr = {"type":"wire","width":0,"has_load":False,"has_drive":False,"signed":"","only_inst_port_connect_width":4,"reWrite":True}
                        if item2 not in vardefine:
                            varAttr["width"] = port_con[value["con"][item2]["type"]]
                            vardefine.update({item2:varAttr})
            for item0 in vardefine:
                if item0 not in text_used:
                    attr = vardefine[item0]
                    attr["reWrite"] = False
                    vardefine[item0] = attr

            pattern = re.compile("\\bmodule.*?;",flags=re.S)
            match = pattern.match(string_out)
            # fp.write(match.group())
            string_rep = match.group() + "\n"
            
            for item0 in para_all:
                # fp.write(para_all+"\n")
                string_rep = string_rep + "parameter " + item0 + ";\n"
            for item0 in vardefine:
                value = vardefine[item0]
                if value["reWrite"] == True:
                    # fp.write(value["type"] + " " + value["width"] + " " + item + ";\n")
                    len_space = 1 if value["signed"] != "" else 0
                    string_rep = string_rep + value["type"] + " "+value["signed"]  + value["width"] + len_space * " " + item0 + ";\n"
            string_tmp = string_out[match.end():]
            string_sp = " \n\t"
            index_r = 0
            for index in range(0,len(string_tmp)):
                if string_tmp[index] in string_sp:
                    index_r = index_r + 1
                else:
                    break
            string_rep = string_rep + "\n\n" +string_tmp[index_r:] 
            string = string.replace(item,string_rep)
            if len(string) == 0:
                return False

            # fk = open(fullpath+"test","w+")
            # fk.write(string_rep)
            # fk.close()
        if len(string) == 0:
            return False
        fp = open(fullpath,"w")
        fp.write(string)
        fp.close()
        return True
            # fp.write(string_out[match.out])

                









    def tb_inst(self,SourceDic, TargetDic, name  ,flag = 0, flags = 0):
        os.chdir(os.path.dirname(__file__))
        if self.mapGenFlag is not True:
            self.map_initial()
        os.chdir(os.path.dirname(__file__))
        TargetPath = self.make_sim_dic(TargetDic,name)
        os.chdir(os.path.dirname(__file__))
        path = self.find_rtl_file(SourceDic, name)
        # print(path)
        ports = self.find_port(path,name) #????????????ports????????????????????????
        # if(flag == 1):

        #     fr = open(path, "r+", errors='ignore')
        #     modules = find_module(path,2)
        #     lines = fr.readlines()
        #     string_file = fr.read()
        #     fr.close()
        #     fr = open(path + '.bak', 'w', errors='ignore')
        #     fr.writelines(lines)
        #     fr.close()
        #     for module in modules:
        #         path_file = find_file(SourceDic,module)
        #         if(path_file != ""):
        #             ports = find_port(path_file,module)

        #     fr = open(path,"w+")






        os.chdir(TargetPath)
        if not os.path.isfile(name + r"TB.sv"):
            lenStr = 0
            for para in ports[1]:
                if len(para) > lenStr:
                    lenStr = len(para)
            lenPara = lenStr
            for port in ports[0]:
                if len(port[3]) > lenStr:
                    lenStr = len(port[3])
            fp = open(name + r"TB.sv", "w+")
            fp.write("`include \"uvm_macros.svh\"\n")
            # fp.write("import uvm_pkg::*;\n")
            fp.write("module " + name + "TB;\n")
            for para_all in ports[2]:
                fp.write("parameter "+para_all+";\n")
            if len(ports[1]) != 0:           
                fp.write(name + "_interface_port #(\n")
                for para in ports[1]:
                    if para == ports[1][len(ports[1]) - 1]:
                        fp.write(" " * 8 + r"." + para+ " " * (lenPara + 2 - len(para)) + r"("+para+" "*(lenPara + 2 -len(para))+r"))" + "\n")
                    else:
                        fp.write(" " * 8 + r"." + para+ " " * (lenPara + 2 - len(para)) + r"("+para+" "*(lenPara + 2 -len(para))+r")," + "\n")
                # fp.write(" " * len(name + "_interface_port") + " " + name+"_if" + " " + r"();" + "\n")
                fp.write(" " * len(name + "_interface_port") + " " + "ifo" + " " + r"();" + "\n")
            else:
                fp.write(name + "_interface_port"+ " " + "ifo" + " " + r"();" + "\n")
                # fp.write(name+"_interface_port "+name+"_if();\n")

            fp.write(name+"_interface_inner " + "ifi ();\n")
            fp.write("logic clk;\n")
            fp.write("logic rst_n;\n")
            fp.write("logic rst_p;\n")
            # fp.write(name + " " + name + "Inst(\n")

            if len(ports[1]) != 0:
                fp.write(name + " #(\n")
                for para in ports[1]:
                    if para == ports[1][len(ports[1]) - 1]:
                        fp.write(" " * 8 + r"." + para+ " " * (lenPara + 2 - len(para)) + r"("+para+" "*(lenPara + 2 -len(para))+r"))" + "\n")
                    else:
                        fp.write(" " * 8 + r"." + para+ " " * (lenPara + 2 - len(para)) + r"("+para+" "*(lenPara + 2 -len(para))+r")," + "\n")
                fp.write(" " * len(name) + " " + name+"_inst" + " " + r"(" + "\n")
            else:
                fp.write(name + " " + name+"_inst" + " " + r"(" + "\n")

                    # print(lenStr)

            for port in ports[0]:
                if port == ports[0][len(ports[0]) - 1]:
                    fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + "ifo." + port[3] + " " * (
                            lenStr - len(port[3])) + "));" + r"//" + port[
                        0] + " " * (8 - len(port[0])) + port[2] + "\n")
                else:
                    fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + "ifo." + port[3] + " " * (
                            lenStr - len(port[3])) + ") ," + r"//" + port[
                        0] + " " * (8 - len(port[0])) + port[2] + "\n")




            # for port in ports:
            #     if len(port[3]) > lenStr:
            #         lenStr = len(port[3])
            #         # print(lenStr)
            # for port in ports:
            #     if port == ports[len(ports) - 1]:
            #         fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(if.ifo." + port[3] + " " * (
            #                 lenStr - len(port[3])) + "));" + r"//" + port[0] + " " * (8 - len(port[0])) + port[
            #                      2] + "\n")
            #     else:
            #         fp.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(if.ifo." + port[3] + " " * (
            #                 lenStr - len(port[3])) + ") ," + r"//" + port[0] + " " * (8 - len(port[0])) + port[
            #                      2] + "\n")

            fp.write("always #5 clk = ~clk;\n\n")

            fp.write("initial begin\n")
            fp.write("clk = 0;\n")
            fp.write("rst_n = 0;\n")
            fp.write("rst_p = 1;\n")
            fp.write("#8 rst_n = 1;\n")
            fp.write("#6 rst_p = 0;\n")

            fp.write("\n")
            fp.write("end\n\n")

            fp.write("always@ * begin\n")
            if(flags == 0):
                fp.write("ifo.clk <= clk;\n")
                fp.write("ifo.rst_n <= rst_n;\n")
            elif(flags == 1):
                fp.write("ifo.clk <= clk;\n")
                fp.write("ifo.rst <= rst_p;\n")
            fp.write("\nend\n\n")

            fp.write("initial begin\n")
            fp.write("   run_test();\n")
            fp.write("end\n\n")








            fp.write("initial begin\n")
            fp.write("   uvm_config_db#(virtual "+name+"_interface_port)::set(null, \"uvm_test_top.env.i_agt.drv\", \"vif\", " + "ifo);\n")
            fp.write("   uvm_config_db#(virtual "+name+"_interface_port)::set(null, \"uvm_test_top.env.i_agt.mon\", \"vif\", " + "ifo);\n")
            fp.write("   uvm_config_db#(virtual "+name+"_interface_port)::set(null, \"uvm_test_top.env.o_agt.mon\", \"vif\", " + "ifo);\n")
            fp.write("   uvm_config_db#(virtual "+name+"_interface_inner)::set(null, \"uvm_test_top.env.i_agt.drv\", \"vif_i\", " + "ifi);\n")
            fp.write("   uvm_config_db#(virtual "+name+"_interface_inner)::set(null, \"uvm_test_top.env.i_agt.mon\", \"vif_i\", " + "ifi);\n")
            fp.write("   uvm_config_db#(virtual "+name+"_interface_inner)::set(null, \"uvm_test_top.env.o_agt.mon\", \"vif_i\", " + "ifi);\n")
            fp.write("end\n")
            fp.write("\n\n\n\n\nendmodule\n")
            fp.close()
        elif flag == 1:
            print("file exists file refresh\n")
            os.chdir(TargetPath)
            fo = open(name + r"TB.sv","r")
            fi = open(name + r"TB.sv.bak","w+")
            string_temp = fo.read()
            fi.write(string_temp)
            fi.close()
            fo.close()
            fo = open(name + r"TB.sv","w+")
            # print(string_temp)
            res_para = re.findall("\\blogic\\b.*?;",string_temp,flags=re.S)
            res = re.findall("(?:\\binitial\\b|\\balways\\b\s*\@\s*\*)\s*\\bbegin\\b\s*.*?end\\b",string_temp,flags=re.S)
            # print(res)
            lenStr = 0
            for para in ports[1]:
                if len(para) > lenStr:
                    lenStr = len(para)
            lenPara = lenStr
            for port in ports[0]:
                if len(port[3]) > lenStr:
                    lenStr = len(port[3])
            fo = open(name + r"TB.sv", "w+")
            fo.write("`include \"uvm_macros.svh\"\n")
            # fo.write("import uvm_pkg::*;\n")
            fo.write("module " + name + "TB;\n")
            for para_all in ports[2]:
                fo.write("parameter "+para_all+";\n")
            if len(ports[1]) != 0:           
                fo.write(name + "_interface_port #(\n")
                for para in ports[1]:
                    if para == ports[1][len(ports[1]) - 1]:
                        fo.write(" " * 8 + r"." + para+ " " * (lenPara + 2 - len(para)) + r"("+para+" "*(lenPara + 2 -len(para))+r"))" + "\n")
                    else:
                        fo.write(" " * 8 + r"." + para+ " " * (lenPara + 2 - len(para)) + r"("+para+" "*(lenPara + 2 -len(para))+r")," + "\n")
                # fo.write(" " * len(name + "_interface_port") + " " + name+"_if" + " " + r"();" + "\n")
                fo.write(" " * len(name + "_interface_port") + " " + "ifo" + " " + r"();" + "\n")
            else:
                fo.write(name + "_interface_port"+ " " + "ifo" + " " + r"();" + "\n")
                # fo.write(name+"_interface_port "+name+"_if();\n")

            fo.write(name+"_interface_inner " + "ifi ();\n")
            # fo.write("logic clk;\n")
            # fo.write("logic rst_n;\n")
            # fo.write("logic rst_p;\n")
            for res_para_temp in res_para:
                fo.write(res_para_temp + "\n")
            # fo.write(name + " " + name + "Inst(\n")

            if len(ports[1]) != 0:
                fo.write(name + " #(\n")
                for para in ports[1]:
                    if para == ports[1][len(ports[1]) - 1]:
                        fo.write(" " * 8 + r"." + para+ " " * (lenPara + 2 - len(para)) + r"("+para+" "*(lenPara + 2 -len(para))+r"))" + "\n")
                    else:
                        fo.write(" " * 8 + r"." + para+ " " * (lenPara + 2 - len(para)) + r"("+para+" "*(lenPara + 2 -len(para))+r")," + "\n")
                fo.write(" " * len(name) + " " + name+"_inst" + " " + r"(" + "\n")
            else:
                fo.write(name + " " + name+"_inst" + " " + r"(" + "\n")

                    # print(lenStr)

            for port in ports[0]:
                if port == ports[0][len(ports[0]) - 1]:
                    fo.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + "ifo." + port[3] + " " * (
                            lenStr - len(port[3])) + "));" + r"//" + port[
                        0] + " " * (8 - len(port[0])) + port[2] + "\n")
                else:
                    fo.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(" + "ifo." + port[3] + " " * (
                            lenStr - len(port[3])) + ") ," + r"//" + port[
                        0] + " " * (8 - len(port[0])) + port[2] + "\n")




            # for port in ports:
            #     if len(port[3]) > lenStr:
            #         lenStr = len(port[3])
            #         # print(lenStr)
            # for port in ports:
            #     if port == ports[len(ports) - 1]:
            #         fo.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(if.ifo." + port[3] + " " * (
            #                 lenStr - len(port[3])) + "));" + r"//" + port[0] + " " * (8 - len(port[0])) + port[
            #                      2] + "\n")
            #     else:
            #         fo.write(" " * 8 + r"." + port[3] + " " * (lenStr + 2 - len(port[3])) + r"(if.ifo." + port[3] + " " * (
            #                 lenStr - len(port[3])) + ") ," + r"//" + port[0] + " " * (8 - len(port[0])) + port[
            #                      2] + "\n")

            # fo.write("\ninitial begin\n")
            # fo.write("clk = 0;\n")
            # fo.write("rst_n = 0;\n")
            # fo.write("rst_p = 1;\n")
            # fo.write("#8 rst_n = 1;\n")
            # fo.write("#6 rst_p = 0;\n")
            # fo.write("\n")
            # fo.write("end\n\n\n")
            fo.write("always #5 clk = ~clk;\n\n")
            for res_temp in res:
                fo.write(res_temp + "\n\n")



            # fo.write("always@ * begin\n")
            # if(flags == 0):
            #     fo.write("ifo.clk <= clk;\n")
            #     fo.write("ifo.rst_n <= rst_n;\n")
            # elif(flags == 1):
            #     fo.write("ifo.clk <= clk;\n")
            #     fo.write("ifo.rst <= rst_p;\n")


            # fo.write("\n\n\nend\n\n")


            # fo.write("initial begin\n")
            # fo.write("   run_test();\n")
            # fo.write("end\n")


            # fo.write("initial begin\n")
            # fo.write("   uvm_config_db#(virtual "+name+"_interface_port)::set(null, \"uvm_test_top.env.i_agt.drv\", \"vif\", " + "ifo);\n")
            # fo.write("   uvm_config_db#(virtual "+name+"_interface_port)::set(null, \"uvm_test_top.env.i_agt.mon\", \"vif\", " + "ifo);\n")
            # fo.write("   uvm_config_db#(virtual "+name+"_interface_port)::set(null, \"uvm_test_top.env.o_agt.mon\", \"vif\", " + "ifo);\n")
            # fo.write("   uvm_config_db#(virtual "+name+"_interface_inner)::set(null, \"uvm_test_top.env.i_agt.drv\", \"vif_i\", " + "ifi);\n")
            # fo.write("   uvm_config_db#(virtual "+name+"_interface_inner)::set(null, \"uvm_test_top.env.i_agt.mon\", \"vif_i\", " + "ifi);\n")
            # fo.write("   uvm_config_db#(virtual "+name+"_interface_inner)::set(null, \"uvm_test_top.env.o_agt.mon\", \"vif_i\", " + "ifi);\n")
            # fo.write("end\n")
            fo.write("\n\n\n\nendmodule\n")
            fo.close()
        else:
            print("file exist, gen stop")








        return name + r"TB"


    def make_sim_dic(self,targetPath, name):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        # str = "../sim/"
        str = targetPath
        if not os.path.isdir(str):
            print("creat "+targetPath + "/path")
            os.makedirs(str)
        if not os.path.isdir(str + name + "Test"):
            print("creat "+targetPath +name+"Test path")
            os.makedirs(str + name + "Test")
        return os.path.normpath(os.path.abspath(str + name + r"Test/")).replace("\\", "/")



    def interface_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        file_path = self.find_rtl_file(Source_path,name)
        ports = self.find_port(file_path,name)
        interface_path = self.make_sim_dic(TargetPath,name) 
        os.chdir(interface_path)
        fj = open(name+"_interface_port.sv","w")
        fj.write("interface "+name+"_interface_port;\n" )
        if flag==1:
            fq = open(name+"_interface_inner.sv","w")
            # fp = open(name+"_interface.sv","w")
            # fp.write("interface "+name+"_interface;\n" )
            # fp.write(name+"_interface_port ifo();\n")
            # fp.write(name+"_interface_inner ifi();\n")
            # fp.write("\n\n\n\nendinterface")
            fq.write("interface "+name+"_interface_inner;\n" )
            fq.write("\n\n\n\nendinterface")
            fq.close()
        for para in ports[2]:
            fj.write("parameter "+ para + ";\n")
        for port in ports[0]:
            fj.write("logic " + port[2] + (0 if len(port[2]) == 0 else 1) * " " + port[3] + ";\n")
        fj.write("\n\n\n\nendinterface")
        fj.close()

    def transaction_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_transaction.sv","w")
        # fp.write("import uvm_pkg::*;\n")
        fp.write("class "+name+"_transaction extends uvm_sequence_item;\n")
        fp.write("rand bit variable_for_test;\n")
        fp.write("\n\n\nconstraint con{\nvariable_for_test == 0;\n\n}\n")
        fp.write("`uvm_object_utils_begin("+name+"_transaction)\n")
        fp.write("\n\n`uvm_object_utils_end\n")
        fp.write("function new(string name = \""+name+"_transaction\");\nsuper.new();\nendfunction\n")
        fp.write("endclass\n")
        fp.close()


    def sequencer_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_sequencer.sv","w")
        fp.write("class "+name+"_sequencer extends uvm_sequencer #("+ name +"_transaction);\n")
        fp.write("    function new(string name, uvm_component parent);\n        super.new(name, parent);\n    endfunction \n")
        fp.write("    `uvm_component_utils("+name+"_sequencer)\n")
        fp.write("endclass\n")
        fp.close()

    def scoreboard_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        if flag == 1:
            write_str = re.sub("my",name,open("./uvm/my_scoreboard_seq.sv","r").read())
        else:
            write_str = re.sub("my",name,open("./uvm/my_scoreboard_comb.sv","r").read())
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_scoreboard.sv","w")
        fp.write(write_str)
        fp.close()

    def monitor_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        write_str = re.sub("my",name,open("./uvm/my_monitor.sv","r").read())
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_monitor.sv","w")
        fp.write(write_str)
        fp.close()

    def model_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        write_str = re.sub("my",name,open("./uvm/my_model.sv","r").read())
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_model.sv","w")
        fp.write(write_str)
        fp.close()

    def env_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        write_str = re.sub("my",name,open("./uvm/my_env.sv","r").read())
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_env.sv","w")
        fp.write(write_str)
        fp.close()

    def drive_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        write_str = re.sub("my",name,open("./uvm/my_driver.sv","r").read())
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_driver.sv","w")
        fp.write(write_str)
        fp.close()

    def case_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        write_str = re.sub("my",name,open("./uvm/my_case0.sv","r").read())
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_case0.sv","w")
        fp.write(write_str)
        fp.close()

    def agent_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        write_str = re.sub("my",name,open("./uvm/my_agent.sv","r").read())
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_agent.sv","w")
        fp.write(write_str)
        fp.close()

    def base_test_gen(self,Source_path,TargetPath,name,flag):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        write_str = re.sub("my",name,open("./uvm/base_test.sv","r").read())
        path = self.make_sim_dic(TargetPath,name)
        os.chdir(path)
        fp = open(name+"_base_test.sv","w")
        fp.write(write_str)
        fp.close()


    def sim_gen(self,dic, name):
        TargetPath = self.make_sim_dic(name)
        self.tb_inst(dic, TargetPath, name)

    #   flag_tb???????????????sim?????????flag_tb1:1-????????????base_test filelist; 5-??????????????????uvmfilelist flag_dicmake????????????????????????flags?????????1,3???define_filelist;2,3???module_filelist;3???filelist??? 
    #   flag1????????????????????????????????? 


    def filelist_regen(self,flags,flag1,sourcePath,targetPath,name):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        if self.mapGenFlag is not True:
            self.map_initial()
        search_path = sourcePath
        # path = self.find_rtl_file(search_path,name)
        # if flag_dicmake==1:
        real_targetPath = self.make_sim_dic(targetPath, name)
        # else:
        #     real_targetPath = os.path.dirname(path)
        # if flag_tb == 1:
        self.filelist_gen([targetPath],real_targetPath,name+"_base_test",flags+1,flag1)
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        self.filelist_gen(search_path,real_targetPath,name,flags,flag1)


    def simflow_seq(self,sourcePath, targetPath, name):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        # SourcePath = "../code/"
        targetpath = self.make_sim_dic(targetPath, name)
        # makefile_src_gen(targetpath, name)
        # # tb_inst(path,targetpath,"uart_byte_tx")
        # filelist_gen(sourcePath, targetpath, TB)
        flag = 1
        self.makefile_src_gen(targetPath,name)
        self.base_test_gen(sourcePath,targetPath,name,flag)
        self.agent_gen(sourcePath,targetPath,name,flag)
        self.case_gen(sourcePath,targetPath,name,flag)
        self.drive_gen(sourcePath,targetPath,name,flag)
        self.env_gen(sourcePath,targetPath,name,flag)
        self.interface_gen(sourcePath,targetPath,name,flag)
        self.model_gen(sourcePath,targetPath,name,flag)
        self.monitor_gen(sourcePath,targetPath,name,flag)
        self.scoreboard_gen(sourcePath,targetPath,name,flag)
        self.sequencer_gen(sourcePath,targetPath,name,flag)
        self.transaction_gen(sourcePath,targetPath,name,flag)
        TB = self.tb_inst(sourcePath, targetPath, name)
        self.filelist_regen(1,1,sourcePath,targetPath,name)




    def simflow_comb(self,sourcePath, targetPath, name):
        os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
        # SourcePath = "../code/"
        targetpath = self.make_sim_dic(targetPath, name)
        # makefile_src_gen(targetpath, name)
        # # tb_inst(path,targetpath,"uart_byte_tx")
        # filelist_gen(sourcePath, targetpath, TB)
        flag = 1
        self.makefile_src_gen(targetPath,name)
        self.base_test_gen(sourcePath,targetPath,name,flag)
        self.agent_gen(sourcePath,targetPath,name,flag)
        self.case_gen(sourcePath,targetPath,name,flag)
        self.drive_gen(sourcePath,targetPath,name,flag)
        self.env_gen(sourcePath,targetPath,name,flag)
        self.interface_gen(sourcePath,targetPath,name,flag)
        self.model_gen(sourcePath,targetPath,name,flag)
        self.monitor_gen(sourcePath,targetPath,name,flag)
        self.scoreboard_gen(sourcePath,targetPath,name,0)
        self.sequencer_gen(sourcePath,targetPath,name,flag)
        self.transaction_gen(sourcePath,targetPath,name,flag)
        TB = self.tb_inst(sourcePath, targetPath, name)
        self.filelist_regen(1,1,sourcePath,targetPath,name)



if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))  # ???????????????python?????????????????????
    name = "top"
    # TargetPath = make_sim_dic(TargetPath, name)
    vt = Verilog_tools ()
    vt.SourcePath = ["./code/"]
    vt.TargetPath = "./sim/"
    vt.except_module = ['assert_never_unknown','ca53dpu_crypto_alu_sha']
    # vt.autodefine("/home/IC/xsc/git_pro/RISCV/code/top.v")

    vt.simflow_seq(vt.SourcePath,vt.TargetPath,name)
    # filelist_gen([SourcePath], TargetPath, "top", 3)
    # filelist_gen(SourcePath,TargetPath, name,3, 0)
    # file_inst(SourcePath, 'test')
    # targetpath = make_sim_dic("Top")
    # makefile_src_gen(targetpath,"Top")
    # filelist_gen(path,targetpath,"uart_byte_txTB")

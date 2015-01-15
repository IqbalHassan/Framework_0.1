import inspect
import copy
import CommonUtil    
class CompareModule():
    def convert_to_new_format(self,expected_list):
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        final_list=[]
        for each in expected_list:
            TupleFieldList=[]
            for eachitem in each:
                if eachitem[1]!='' and eachitem[0] not in TupleFieldList:
                    TupleFieldList.append(eachitem[0])
            TupleFieldList=list(set(TupleFieldList))
            tuple_data_formed=[]
            for index in range(len(each)-1,-1,-1):
                if each[index][0] not in TupleFieldList:
                    tuple_data_formed.append((each[index][0],each[index][2]))
                    each.pop(index)
            group_data_form=[]
            for eachtuplelabel in TupleFieldList:
                temp=[]
                for eachitem in each:
                    if eachtuplelabel==eachitem[0]:
                        temp.append(eachitem)
                group_data_form.append(temp)
            for eachgroupdataitem in group_data_form:
                if eachgroupdataitem:
                    group_data_label=eachgroupdataitem[0][0]
                    temp=[]
                    for eachitem in eachgroupdataitem:
                        temp.append((eachitem[1],eachitem[2]))
                    tuple_data_formed.append((group_data_label,temp))
            final_list.append(tuple_data_formed)
        
        return final_list
    
def main():
    oCompare=CompareModule()
    expected_list=[
                   [
                    ('name','','Shetu'),
                    ('roll','','0905011'),
                    ('phone','home','01719-267494'),
                    ('phone','mobile','0421-3466'),
                    ('address','road','bezpara'),
                    ('address','home','736')
                    ],
                   [
                    ('name','','Minar'),
                    ('roll','','0905105'),
                    ('academic','dept','cse'),
                    ('academic','cg','3.24'),
                    ('phone','home','01720-267494'),
                    ('phone','mobile','0423-3466')
                    ]
                   ]
    actual_list=  [
                   [
                    ('name','','Shetu'),
                    ('roll','','0905011'),
                    ('phone','home','01719-267494'),
                    ('phone','mobile','0421-3466')
                    ],
                   [
                    ('name','','Minar'),
                    ('phone','home','01720-267494'),                    
                    ('academic','dept','cse'),
                    ('academic','cg','3.24'),
                    ('phone','mobile','0423-3466')
                    ]
                   ]
    oComare=CompareModule()
    expected_list=oCompare.convert_to_new_format(expected_list)
    actual_list=oCompare.convert_to_new_format(actual_list)
    print expected_list
    print actual_list
if __name__=='__main__':
    main()
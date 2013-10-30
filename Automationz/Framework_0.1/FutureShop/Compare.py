# coding=utf-8


import inspect
import copy
import CommonUtil

class Compare():
    def FieldCompare(self, ExpectedList, ActualList, IgnoreFieldsList=[], KeyFieldsList=[]):
        sModuleInfo = inspect.stack()[0][3] + " : " + inspect.getmoduleinfo(__file__).name
        try:
            ExpectedList = CommonUtil.NormalizeTimeInputs(ExpectedList)
            ActualList = CommonUtil.NormalizeTimeInputs(ActualList)

            #Initialize all lists for storing comparisson values
            ExpectedListCopy = copy.deepcopy(ExpectedList)
            ActualListCopy = copy.deepcopy(ActualList)
            ExpMissing = []
            ExpFound = []
            ExpDuplicate = []
            ExpError = []
            ExpKeyFieldMatch = []
            ExpNonKeyFieldMisMatch = []
            ExpNonKeyFieldActual = []

            ActMissing = []
            ActFound = []
            ActDuplicate = []
            ActError = []
            ActKeyFieldMatch = []
            ActNonKeyFieldMisMatch = []
            ActNonKeyFieldActual = []

            TupleListFields = []
            #Find List items which are a tuple of list (like the Details)
            for eachList in ExpectedList:
                for eachItem in eachList:
                    if isinstance(eachItem, tuple):
                        if isinstance(eachItem[1], list):
                            TupleListFields.append(eachItem[0])

            for eachList in ActualList:
                for eachItem in eachList:
                    if isinstance(eachItem, tuple):
                        if isinstance(eachItem[1], list):
                            TupleListFields.append(eachItem[0])
            #Remove duplicates if any
            TupleListFields = list(set(TupleListFields))

            #Loops thru all expected records against all actual items found
            for iExp in range(0, len(ExpectedList)):

                expitem = copy.deepcopy(ExpectedList[iExp])
                expItemFound = False
                ExpTempFound = []
                ExpKeyFieldTemp = []
                ExpNonKeyFieldNotMatching = []
                ExpNonKeyFieldValues = []

                #Take addresses out of expected contact and store in AddressesList
                expitemAddresses = []
                for i in range(len(expitem) - 1, -1, -1):
                    e = expitem[i]
                    if e[0] in TupleListFields:
                        #Check if any Address fields are there in ignorelist, if yes get rid of them
                        for k in range(len(e[1]) - 1, -1, -1):
                            if e[1][k][0] in IgnoreFieldsList:
                                e[1].pop(k)
                        expitemAddresses.append(e)
                        expitem.pop(i)
                    #Remove problem fields which are in ignore list so they are not compared
                    if e[0] in IgnoreFieldsList:
                        expitem.pop(i)

                for iAct in range(len(ActualList) - 1, -1, -1):

                    actitem = copy.deepcopy(ActualList[iAct])

                    #Take addresses out of actual contact and store in AddressesList
                    actitemAddresses = []
                    for i in range(len(actitem) - 1, -1, -1):

                        e = actitem[i]

                        if e[0] in TupleListFields:
                            #Check if any Address fields are there in ignorelist, if yes get rid of them
                            for k in range(len(e[1]) - 1, -1, -1):
                                if e[1][k][0] in IgnoreFieldsList:
                                    e[1].pop(k)
                            actitemAddresses.append(e)
                            actitem.pop(i)
                        #Remove problem fields which are in ignore list so they are not compared
                        if e[0] in IgnoreFieldsList:
                            print "ignored: %s" % e[0]
                            actitem.pop(i)

                    #Compare Exp List & Actual List to find matches and differences
                    matchExpToActList = list(set(expitem) & set(actitem))
                    diffExpToActList = list(set(expitem) - set(actitem))
                    diffActToExpList = list(set(actitem) - set(expitem))

                    #Find matches & differences between exp & actual addresses
                    expitemAddressesFound = []
                    for i in range(len(expitemAddresses) - 1, -1, -1):
                        eachExpAddress = expitemAddresses[i]
                        ExpAddressFound = False
                        for j in range(len(actitemAddresses) - 1, -1, -1):
                            eachActAddress = actitemAddresses[j]
                            if eachExpAddress[0] == eachActAddress[0]:
                                matchAddrExpToActList = list(set(eachExpAddress[1]) & set(eachActAddress[1]))
                                diffAddrExpToActList = list(set(eachExpAddress[1]) - set(eachActAddress[1]))
                                diffAddrActToExpList = list(set(eachActAddress[1]) - set(eachExpAddress[1]))
                                #Check if it its a complete match
                                if len(matchAddrExpToActList) > 0 and len(diffAddrExpToActList) == 0 and len(diffAddrActToExpList) == 0:
                                    ExpAddressFound = True
                                    actitemAddresses.pop(j)
                                    break

                        if ExpAddressFound:
                            expitemAddressesFound.append(True)
                        else:
                            expitemAddressesFound.append(False)

                    #if we were expecting any addresses in the expected contact, then loop thru the list we created in the previous address comparison 
                    if len(expitemAddressesFound) > 0:
                        i = 0
                        for i in range(len(expitemAddressesFound)):
                            if expitemAddressesFound[0]:
                                matchExpToActList.append(expitemAddresses[i])
                            else:
                                diffExpToActList.append(expitemAddresses[i])
                                if [x for x in matchExpToActList if x[0] in KeyFieldsList]:
                                    for j in range(len(actitemAddresses)):
                                        diffActToExpList.append(actitemAddresses[j])

                    #if an expected record completely matches with an actual record, then store it temp and look for duplicates later
                    if len(matchExpToActList) > 0 and len(diffExpToActList) == 0 and len(diffActToExpList) == 0:
                        ExpTempFound.append(matchExpToActList)
                        expItemFound = True
                    #if an expected record partially matches with an actual record And if it has differences with the actual record
                    elif len(matchExpToActList) > 0 and (len(diffExpToActList) > 0 or len(diffActToExpList) > 0):
                        #if the partially matching fields are the key fields, then store it as key field matching records. also store differences
                        if [x for x in matchExpToActList if x[0] in KeyFieldsList]:
                            #print "Partial Key fields match: %s with not matching fields: %s having actual values: %s"%(matchExpToActList,diffExpToActList,diffActToExpList)
                            ExpKeyFieldTemp.append(matchExpToActList)
                            ExpNonKeyFieldNotMatching.append(diffExpToActList)
                            ExpNonKeyFieldValues.append(diffActToExpList)

                #Once all actual records are searched, then store the result for the expected record
                #recopy the expected item once more since the current item was manipulated
                expitem = copy.deepcopy(ExpectedList[iExp])
                #expected item is completely missing in actual                        
                if expItemFound == False:
                    #expected item is partially matched with an actual item with key fields having matching values
                    if len(ExpKeyFieldTemp) > 0:
                        ExpKeyFieldMatch.append(ExpKeyFieldTemp)
                        ExpNonKeyFieldMisMatch.append(ExpNonKeyFieldNotMatching)
                        ExpNonKeyFieldActual.append(ExpNonKeyFieldValues)
                    else:
                        ExpMissing.append(expitem)
                #expected item is found, but duplicated in actual
                elif len(ExpTempFound) > 1:
                    ExpDuplicate.append(expitem)
                #expected item is completely matching with an actual record
                elif len(ExpTempFound) == 1:
                    ExpFound.append(expitem)
                #some error in comparisson
                else:
                    ExpError.append(expitem)

            for iAct in range(0, len(ActualList)):
                actitem = copy.deepcopy(ActualList[iAct])
                actItemFound = False
                ActTempFound = []
                ActKeyFieldTemp = []
                ActNonKeyFieldNotMatching = []
                ActNonKeyFieldValues = []

                #Take addresses out of actual contact and store in AddressesList
                actitemAddresses = []
                for i in range(len(actitem) - 1, -1, -1):
                    e = actitem[i]
                    if e[0] in TupleListFields:
                        #Check if any Address fields are there in ignorelist, if yes get rid of them
                        for k in range(len(e[1]) - 1, -1, -1):
                            if e[1][k][0] in IgnoreFieldsList:
                                e[1].pop(k)

                        actitemAddresses.append(e)
                        actitem.pop(i)
                    #Remove problem fields which are in ignore list so they are not compared
                    if e[0] in IgnoreFieldsList:
                        actitem.pop(i)

                for y in range(len(ExpectedList) - 1, -1, -1):
                    expitem = copy.deepcopy(ExpectedList[y])

                    #Take addresses out of expected contact and store in AddressesList
                    expitemAddresses = []
                    for i in range(len(expitem) - 1, -1, -1):
                        e = expitem[i]
                        if e[0] in TupleListFields:
                            #Check if any Address fields are there in ignorelist, if yes get rid of them
                            for k in range(len(e[1]) - 1, -1, -1):
                                if e[1][k][0] in IgnoreFieldsList:
                                    e[1].pop(k)
                            expitemAddresses.append(e)
                            expitem.pop(i)

                        #Remove problem fields which are in ignore list so they are not compared
                        if e[0] in IgnoreFieldsList:
                            expitem.pop(i)


                    matchActToExpList = list(set(actitem) & set(expitem))
                    diffExpToActList = list(set(expitem) - set(actitem))
                    diffActToExpList = list(set(actitem) - set(expitem))

                    #Find matches & differences between exp & actual addresses
                    actitemAddressesFound = []
                    for i in range(len(actitemAddresses) - 1, -1, -1):
                        eachActAddress = actitemAddresses[i]
                        ActAddressFound = False
                        for j in range(len(expitemAddresses) - 1, -1, -1):
                           eachExpAddress = expitemAddresses[j]
                           if eachActAddress[0] == eachExpAddress[0]:
                                matchAddrActToExpList = list(set(eachActAddress[1]) & set(eachExpAddress[1]))
                                diffAddrActToExpList = list(set(eachActAddress[1]) - set(eachExpAddress[1]))
                                diffAddrExpToActList = list(set(eachExpAddress[1]) - set(eachActAddress[1]))
                                #Check if it its a complete match
                                if len(matchAddrActToExpList) > 0 and len(diffAddrActToExpList) == 0 and len(diffAddrExpToActList) == 0:
                                    ActAddressFound = True
                                    expitemAddresses.pop(j)
                                    break

                        if ActAddressFound:
                            actitemAddressesFound.append(True)
                        else:
                            actitemAddressesFound.append(False)

                    #if the Actual contact contained any address fields, then loop thru the list we created in the previous address comparison 
                    if len(actitemAddressesFound) > 0:
                        i = 0
                        for i in range(len(actitemAddressesFound)):
                            if actitemAddressesFound[0]:
                                matchActToExpList.append(actitemAddresses[i])
                            else:
                                diffActToExpList.append(actitemAddresses[i])
                                if [x for x in matchActToExpList if x[0] in KeyFieldsList]:
                                    for j in range(len(expitemAddresses)):
                                        diffExpToActList.append(expitemAddresses[j])


                    if len(matchActToExpList) > 0 and len(diffExpToActList) == 0 and len(diffActToExpList) == 0:
                        ActTempFound.append(matchActToExpList)
                        actItemFound = True
                    elif len(matchActToExpList) > 0 and (len(diffExpToActList) > 0 or len(diffActToExpList) > 0):
                        #check if key fields are there in match list
                        if [x for x in matchActToExpList if x[0] in KeyFieldsList]:
                            #print "Partial Key fields match: %s with not matching fields: %s having actual values: %s"%(matchActToExpList,diffExpToActList,diffActToExpList)
                            ActKeyFieldTemp.append(matchActToExpList)
                            ActNonKeyFieldNotMatching.append(diffActToExpList)
                            ActNonKeyFieldValues.append(diffExpToActList)

                actitem = copy.deepcopy(ActualList[iAct])
                if actItemFound == False:
                    if len(ActKeyFieldTemp) > 0:
                        ActKeyFieldMatch.append(ActKeyFieldTemp)
                        ActNonKeyFieldMisMatch.append(ActNonKeyFieldNotMatching)
                        ActNonKeyFieldActual.append(ActNonKeyFieldValues)
                    else:
                        ActMissing.append(actitem)
                elif len(ActTempFound) > 1:
                    ActDuplicate.append(actitem)
                elif len(ActTempFound) == 1:
                    ActFound.append(actitem)
                else:
                    ActError.append(actitem)

            #need to add logic for extra duplicates

            #Logging & return values
            print "Expected           records:", len(ExpectedList)
            CommonUtil.ExecLog(sModuleInfo, "Expected           records:%s" % len(ExpectedList), 1)
            for i in range(len(ExpectedList)):
                CommonUtil.ExecLog(sModuleInfo, "Expected           records#%s:%s" % (i, ExpectedList[i]), 4)
            print "Actual             records:", len(ActualList)
            CommonUtil.ExecLog(sModuleInfo, "Actual             records:%s" % len(ActualList), 1)
            for i in range(len(ActualList)):
                CommonUtil.ExecLog(sModuleInfo, "Actual             records#%s:%s" % (i, ActualList[i]), 4)

            if (len(ExpMissing) == 0 and len(ActMissing) == 0) and (len(ExpectedList) == len(ExpFound)) and (len(ExpDuplicate) == 0 and len(ActDuplicate) == 0):
                print "Found              records:", len(ExpFound)
                CommonUtil.ExecLog(sModuleInfo, "Found              records:%s" % len(ExpFound), 1)

                for i in range(len(ExpFound)):
                    CommonUtil.ExecLog(sModuleInfo, "Matching           records#%s" % (i + 1), 1)
                    CommonUtil.ExecLog(sModuleInfo, "%s" % (str(ExpFound[i])), 1)

                print "Missing            records:", len(ExpMissing)
                CommonUtil.ExecLog(sModuleInfo, "Missing            records:%s" % len(ExpMissing), 1)

                print "Verification of expected and actual  data matched"
                CommonUtil.ExecLog(sModuleInfo, "Verification of expected and actual  data matched", 1)

                sVerificationStatus = "Pass"
            else:
                print "Matching           records:", len(ExpFound)
                CommonUtil.ExecLog(sModuleInfo, "Matching           records:%s" % len(ExpFound), 1)
                for i in range(len(ExpFound)):
                    CommonUtil.ExecLog(sModuleInfo, "Matching           record #%s" % (i + 1), 1)
                    CommonUtil.ExecLog(sModuleInfo, "%s" % (str(ExpFound[i])), 1)

                print "Missing            records:", len(ExpMissing)
                CommonUtil.ExecLog(sModuleInfo, "Missing            records:%s" % len(ExpMissing), 1)
                for i in range(len(ExpMissing)):
                    CommonUtil.ExecLog(sModuleInfo, "Missing            record #%s" % (i + 1), 2)
                    CommonUtil.ExecLog(sModuleInfo, "%s" % (str(ExpMissing[i])), 2)

                print "Extra              records:", len(ActMissing)
                CommonUtil.ExecLog(sModuleInfo, "Extra              records:%s" % len(ActMissing), 1)
                for i in range(len(ActMissing)):
                    CommonUtil.ExecLog(sModuleInfo, "Extra              record #%s" % (i + 1), 2)
                    CommonUtil.ExecLog(sModuleInfo, "%s" % (str(ActMissing[i])), 2)

                print "Duplicated         records:", len(ExpDuplicate)
                CommonUtil.ExecLog(sModuleInfo, "Duplicated         records:%s" % len(ExpDuplicate), 1)
                for i in range(len(ExpDuplicate)):
                    CommonUtil.ExecLog(sModuleInfo, "Duplicated         record #%s" % (i + 1), 2)
                    CommonUtil.ExecLog(sModuleInfo, "%s" % (str(ExpDuplicate[i])), 2)

                print "Key Field Matching records:", len(ExpKeyFieldMatch)
                CommonUtil.ExecLog(sModuleInfo, "Key Field Matching records:%s" % len(ExpKeyFieldMatch), 1)
                NMF = []
                for i in range(len(ExpKeyFieldMatch)):
                    CommonUtil.ExecLog(sModuleInfo, "Key Field Matching record #%s" % (i + 1), 2)
                    CommonUtil.ExecLog(sModuleInfo, "%s" % (str(ExpKeyFieldMatch[i])), 2)
                    CommonUtil.ExecLog(sModuleInfo, "Expected            field #%s" % (i + 1), 2)
                    CommonUtil.ExecLog(sModuleInfo, "%s" % (str(ExpNonKeyFieldMisMatch[i])), 2)
                    CommonUtil.ExecLog(sModuleInfo, "Actual values of    field #%s" % (i + 1), 2)
                    CommonUtil.ExecLog(sModuleInfo, "%s" % (str(ExpNonKeyFieldActual[i])), 2)
                    for eachData in ExpNonKeyFieldMisMatch[i]:
                        if len(eachData) > 0:
                            for eachtup in eachData:
                                if isinstance(eachtup, tuple):
                                    NMF.append(eachtup[0])
                                else:
                                    NMF.append(eachtup)

                    for eachData in ExpNonKeyFieldActual[i]:
                        if len(eachData) > 0:
                            for eachtup in eachData:
                                if isinstance(eachtup, tuple):
                                    NMF.append(eachtup[0])
                                else:
                                    NMF.append(eachtup)

                if len(ExpError) > 0:
                    print "Unknown error in verifying expected:", ExpError
                    print "Unknown error in verifying actual  :", ActError

                if len(ExpMissing) > 0 and len(ActMissing) > 0:
                    print "%s of the expected records is not found. %s extra record" % (len(ExpMissing), len(ActMissing))
                    CommonUtil.ExecLog(sModuleInfo, "%s of the expected records is not found. %s extra record" % (len(ExpMissing), len(ActMissing)), 3)
                elif len(ExpMissing) > 0:
                    print "%s of the expected records is not found" % (len(ExpMissing))
                    CommonUtil.ExecLog(sModuleInfo, "%s of the expected records is not found" % (len(ExpMissing)), 3)
                elif len(ActMissing) > 0:
                    print "%s extra records which is not expected" % (len(ActMissing))
                    CommonUtil.ExecLog(sModuleInfo, "%s extra records which is not expected" % (len(ActMissing)), 3)

                NMF = list(set(NMF))
                if len(NMF) > 0:
                    print "Verification failed for following expected fields %s" % (",".join(NMF))
                    CommonUtil.ExecLog(sModuleInfo, "Verification failed for following expected fields %s" % (",".join(NMF)), 3)
                else:
                    print "Verification of expected and actual  data did not match"
                    CommonUtil.ExecLog(sModuleInfo, "Verification of expected and actual data did not match", 3)
                sVerificationStatus = "Critical"


            return sVerificationStatus
        except Exception, e:
            return CommonUtil.LogCriticalException(sModuleInfo, e)


def main():
    pass
#    ExpectedList = [
#                    [('Title', u'Apple iPod mini 16GB With Wi-Fi - Black & Slate'), ('Model', u'MD528C/A'), ('Web ID', u'10229777'), ('Sale Price', u'309.99'), ('Saving', u'$20'), ('Details', [(u'Display', u''), (u'Display Type', u'LCD'), (u'Screen Size', u'7.9 Inches'), (u'Native Screen Resolution', u'1024 x 768'), (u'Touchscreen', u'Yes'), (u'3D Capable Display', u'No'), (u'Screen Finish', u'Glossy'), (u'Storage', u''), (u'Built-in Storage Capacity', u'16 GB'), (u'Built-in Storage Type', u'Flash Memory'), (u'Built-in Memory Card Reader', u'No'), (u'Compatible Memory Card Types', u'Not Applicable'), (u'Max Memory Card Capacity', u'Not Applicable'), (u'RAM Size', u'Information Not Available'), (u'Cameras', u''), (u'Rear Camera Still Resolution', u'5 MP'), (u'Rear Camera Video Resolution', u'1920 x 1080 @ 30 fps'), (u'Rear Camera Autofocus', u'Yes'), (u'Rear Camera Flash', u'No'), (u'Front Camera Still Resolution', u'1.2 MP'), (u'Front Camera Video Resolution', u'1280 \xd7 720 @ 30 fps'), (u'Front Camera Autofocus', u'No'), (u'Front Camera Flash', u'No'), (u'Video Calling (WiFi)', u'Yes'), (u'Video Calling (Cellular)', u'No'), (u'3D Photos', u'No'), (u'3D Video Recording', u'No'), (u'Processor', u''), (u'Processor Type', u'Apple A5'), (u'Processor Speed', u'Information Not Available'), (u'Processor Cores', u'2'), (u'Software', u''), (u'Operating System', u'iOS 6'), (u'Operating System Language', u'Bilingual'), (u'Pre-loaded Software', u'Information Not Available'), (u'App Store Compatibility', u'Apple App Store'), (u'Audio', u''), (u'Built-in Speaker', u'Yes'), (u'Speaker Wattage', u'Information Not Available'), (u'Integrated Microphone', u'Yes'), (u'Microphone Input', u'No'), (u'Hardware Volume Control', u'Yes'), (u'Headphone Jack Size', u'3.5 mm'), (u'Connectivity', u''), (u'Integrated WiFi', u'802.11 a/b/g/n'), (u'Integrated Bluetooth', u'Yes - 4.0'), (u'3G', u'No'), (u'4G', u'No'), (u'Cellular Provider', u'NIL'), (u'Assisted GPS Navigation', u'No'), (u'Unassisted GPS Navigation', u'No'), (u'HDMI Output', u'Yes - Adapter Sold Separately'), (u'DLNA Certified', u'No'), (u'USB 3.0 Ports', u'No'), (u'USB 2.0 Ports', u'Yes (Via Lightning Connector)'), (u'Thunderbolt Ports', u'No'), (u'Other Inputs/Outputs', u'Not Applicable'), (u'Power', u''), (u'Approximate In-use Battery Life', u'Up To 10 Hours'), (u'Approximate Standby Battery Life', u'Information Not Available'), (u'Battery - Number of Cells', u'Information Not Available'), (u'Battery - Capacity', u'16.3 Wh'), (u'Charge over USB', u'Yes'), (u'Physical Features', u''), (u'Sensors', u'3-axis Gyro; Accelerometer; Ambient Light'), (u'Hard-key QWERTY Keyboard', u'No'), (u'Colour', u'Black'), (u'Height', u'20 cm'), (u'Depth', u'0.72 cm'), (u'Width', u'13.47 cm'), (u'Height (Inches)', u'7.9 Inches'), (u'Depth (Inches)', u'0.3 Inches'), (u'Width (Inches)', u'5.3 Inches'), (u'Weight', u'308 g'), (u'Warranty Labour', u'1 Year(s)'), (u'Warranty Parts', u'1 Year(s)')])],
#                    ]
#    ActualList = [
#                    [('Title', u'Apple iPad mini 16GB With Wi-Fi - Black & Slate'), ('Model', u'MD528C/A'), ('Web ID', u'10229777'), ('Sale Price', u'309.99'), ('Saving', u'$20'), ('Details', [(u'Display', u''), (u'Display Type', u'LCD'), (u'Screen Size', u'7.8 Inches'), (u'Native Screen Resolution', u'1024 x 768'), (u'Touchscreen', u'Yes'), (u'3D Capable Display', u'No'), (u'Screen Finish', u'Glossy'), (u'Storage', u''), (u'Built-in Storage Capacity', u'16 GB'), (u'Built-in Storage Type', u'Flash Memory'), (u'Built-in Memory Card Reader', u'No'), (u'Compatible Memory Card Types', u'Not Applicable'), (u'Max Memory Card Capacity', u'Not Applicable'), (u'RAM Size', u'Information Not Available'), (u'Cameras', u''), (u'Rear Camera Still Resolution', u'5 MP'), (u'Rear Camera Video Resolution', u'1920 x 1080 @ 30 fps'), (u'Rear Camera Autofocus', u'Yes'), (u'Rear Camera Flash', u'No'), (u'Front Camera Still Resolution', u'1.2 MP'), (u'Front Camera Video Resolution', u'1280 \xd7 720 @ 30 fps'), (u'Front Camera Autofocus', u'No'), (u'Front Camera Flash', u'No'), (u'Video Calling (WiFi)', u'Yes'), (u'Video Calling (Cellular)', u'No'), (u'3D Photos', u'No'), (u'3D Video Recording', u'No'), (u'Processor', u''), (u'Processor Type', u'Apple A5'), (u'Processor Speed', u'Information Not Available'), (u'Processor Cores', u'2'), (u'Software', u''), (u'Operating System', u'iOS 6'), (u'Operating System Language', u'Bilingual'), (u'Pre-loaded Software', u'Information Not Available'), (u'App Store Compatibility', u'Apple App Store'), (u'Audio', u''), (u'Built-in Speaker', u'Yes'), (u'Speaker Wattage', u'Information Not Available'), (u'Integrated Microphone', u'Yes'), (u'Microphone Input', u'No'), (u'Hardware Volume Control', u'Yes'), (u'Headphone Jack Size', u'3.5 mm'), (u'Connectivity', u''), (u'Integrated WiFi', u'802.11 a/b/g/n'), (u'Integrated Bluetooth', u'Yes - 4.0'), (u'3G', u'No'), (u'4G', u'No'), (u'Cellular Provider', u'NIL'), (u'Assisted GPS Navigation', u'No'), (u'Unassisted GPS Navigation', u'No'), (u'HDMI Output', u'Yes - Adapter Sold Separately'), (u'DLNA Certified', u'No'), (u'USB 3.0 Ports', u'No'), (u'USB 2.0 Ports', u'Yes (Via Lightning Connector)'), (u'Thunderbolt Ports', u'No'), (u'Other Inputs/Outputs', u'Not Applicable'), (u'Power', u''), (u'Approximate In-use Battery Life', u'Up To 10 Hours'), (u'Approximate Standby Battery Life', u'Information Not Available'), (u'Battery - Number of Cells', u'Information Not Available'), (u'Battery - Capacity', u'16.3 Wh'), (u'Charge over USB', u'Yes'), (u'Physical Features', u''), (u'Sensors', u'3-axis Gyro; Accelerometer; Ambient Light'), (u'Hard-key QWERTY Keyboard', u'No'), (u'Colour', u'Black'), (u'Height', u'20 cm'), (u'Depth', u'0.72 cm'), (u'Width', u'13.47 cm'), (u'Height (Inches)', u'7.9 Inches'), (u'Depth (Inches)', u'0.3 Inches'), (u'Width (Inches)', u'5.3 Inches'), (u'Weight', u'308 g'), (u'Warranty Labour', u'1 Year(s)'), (u'Warranty Parts', u'1 Year(s)')])],
#                    ]
#
#     ExpectedList= [[('On Sale','12')]]
#     ActualList= [[('On Sale','12')]]
#     objCompare = Compare()
#     retValue = objCompare.FieldCompare(ExpectedList, ActualList, [], [])
#     print retValue

if __name__ == "__main__":
    main()

#Jacob Urick
#The Ohio State University
#urick.9@osu.edu



#TODO fix path finding; on each device, after finding the head of a path chain the rest follows
#TODO cache metadata header and cache path
import os
import glob
import sys


#checks the sanity check bytes
def checkForObfuscation(filename):
    header = []
    with open(filename, "rb") as f:
        chunk = f.read(4)
        for b in chunk:
            header.append(b)
        sanity = int.from_bytes(header, byteorder = 'little')
        if(hex(sanity) == "0xfab11baf"):
            return False
        return True
#checks the version
def checkVersion(filename):
    header = []
    with open(filename, "rb") as f:
        chunk = f.read(8)
        for b in chunk:
            header.append(b)
        del header[0:4]
        version = int.from_bytes(header, byteorder = 'little')
        return version
#Given an open & readble file, read bytes until a null byte is found
def readUntilNullByte(file):
    word = []
    while True:
        b = file.read(1)
        #I think we're trying to read too many methods? Idk ignore for now
        b = b.decode("utf-8", errors="ignore")
        if b != '\0' and b!= '':
            word.append(b)
        else:
            break
    return word

#Given a list and an open & writable file, write the list contents
def writeList(lst, file):
    for i in range(len(lst)):
        file.write(lst[i])
    file.write("\n")
#Get method names from file
def getMethodNames(path, start, count):
    methods = []
    with open(path, 'rb') as reader:
        #Move reading location to the start of the structs
        reader.seek(start, 0)
        #We now read in count many IL2CPPMethodDefinition structs
        #These are 32 bytes
        #I only care about the first int, the StringIndex nameIndex,
        #The second int, the TypeDefinitionIndex declaringType,
        #the third int, the TypeIndex returnType, and
        #the fourth int, the ParamaterIndex parameterStart,
        #and the 10th, the 2 byte paramaterCount

        for i in range(int(count/32)):
            method = []
            method.append(int.from_bytes(reader.read(4), byteorder='little'))
            method.append(int.from_bytes(reader.read(4), byteorder='little'))
            method.append(int.from_bytes(reader.read(4), byteorder='little'))
            method.append(int.from_bytes(reader.read(4), byteorder='little'))
            #Move 14 bytes forward
            reader.seek(14, 1)
            method.append(int.from_bytes(reader.read(2), byteorder='little'))
            methods.append(method)
    return methods

#Get method names from file
def getFieldNames(path, start, count):
    fields = []
    with open(path, 'rb') as reader:
        #Move reading location to the start of the structs
        reader.seek(start, 0)
        #We now read in count many IL@Il2CppTypeDefinition structs
        #These are 32 bytes
        #I only care about the first int, the StringIndex nameIndex,
        #The second int, the typeIndexe,  may be interesting soon

        for i in range(int(count/12)):
            field = []
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            fields.append(field)
    return fields

#Todo: future optimization would be to only check for the head of the directory chain
#i.e. only look for "assets" on android file or "il2cpp" on windows file
#after the known file is found, the rest of the chain never(?) changes
def outputMethods(paths):
    for path in paths:
        with open(path, 'rb') as reader:
            sanity = int.from_bytes(reader.read(4), byteorder='little')
            version = int.from_bytes(reader.read(4), byteorder='little')
            stringLiteralOffset = int.from_bytes(reader.read(4), byteorder='little')             #         string data for managed code
            stringLiteralCount = int.from_bytes(reader.read(4), byteorder='little')
            stringLiteralDataOffset = int.from_bytes(reader.read(4), byteorder='little')
            stringLiteralDataCount = int.from_bytes(reader.read(4), byteorder='little')
            stringOffset = int.from_bytes(reader.read(4), byteorder='little')             #         string data for metadata
            stringCount = int.from_bytes(reader.read(4), byteorder='little')
            eventsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppEventDefinition
            eventsCount = int.from_bytes(reader.read(4), byteorder='little')
            propertiesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppPropertyDefinition
            propertiesCount = int.from_bytes(reader.read(4), byteorder='little')
            methodsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppMethodDefinition
            methodsCount = int.from_bytes(reader.read(4), byteorder='little')
            parameterDefaultValuesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppParameterDefaultValue
            parameterDefaultValuesCount = int.from_bytes(reader.read(4), byteorder='little')
            fieldDefaultValuesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppFieldDefaultValue
            fieldDefaultValuesCount = int.from_bytes(reader.read(4), byteorder='little')
            fieldAndParameterDefaultValueDataOffset = int.from_bytes(reader.read(4), byteorder='little')             #         uint8_t
            fieldAndParameterDefaultValueDataCount = int.from_bytes(reader.read(4), byteorder='little')
            fieldMarshaledSizesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppFieldMarshaledSize
            fieldMarshaledSizesCount = int.from_bytes(reader.read(4), byteorder='little')
            parametersOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppParameterDefinition
            parametersCount = int.from_bytes(reader.read(4), byteorder='little')

            fieldsOfoffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppFieldDefinition
            fieldsCount = int.from_bytes(reader.read(4), byteorder='little')
            genericParametersOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppGenericParameter
            genericParametersCount = int.from_bytes(reader.read(4), byteorder='little')
            genericParameterConstraintsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeIndex
            genericParameterConstraintsCount = int.from_bytes(reader.read(4), byteorder='little')
            genericContainersOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppGenericContainer
            genericContainersCount = int.from_bytes(reader.read(4), byteorder='little')
            nestedTypesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeDefinitionIndex
            nestedTypesCount = int.from_bytes(reader.read(4), byteorder='little')                             #
            interfacesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeIndex
            interfacesCount = int.from_bytes(reader.read(4), byteorder='little')
            vtableMethodsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         EncodedMethodIndex
            vtableMethodsCount = int.from_bytes(reader.read(4), byteorder='little')
            interfaceOffsetsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppInterfaceOffsetPair
            interfaceOffsetsCount = int.from_bytes(reader.read(4), byteorder='little')
            typeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppTypeDefinition
            typeDefinitionsCount = int.from_bytes(reader.read(4), byteorder='little')
            imagesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppImageDefinition
            imagesCount = int.from_bytes(reader.read(4), byteorder='little')
            assembliesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppAssemblyDefinition
            assembliesCount = int.from_bytes(reader.read(4), byteorder='little')
            fieldRefsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppFieldRef
            fieldRefsCount = int.from_bytes(reader.read(4), byteorder='little')
            referencedAssembliesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         int32_t
            referencedAssembliesCount = int.from_bytes(reader.read(4), byteorder='little')
            attributesInfoOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppCustomAttributeTypeRange
            attributesInfoCount = int.from_bytes(reader.read(4), byteorder='little')
            attributeTypesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeIndex
            attributeTypesCount = int.from_bytes(reader.read(4), byteorder='little')
            unresolvedVirtualCallParameterTypesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeIndex
            unresolvedVirtualCallParameterTypesCount = int.from_bytes(reader.read(4), byteorder='little')
            unresolvedVirtualCallParameterRangesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppMetadataRange                unresolvedVirtualCallParameterRangesCount = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeTypeNamesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppWindowsRuntimeTypeNamePair
            windowsRuntimeTypeNamesSize = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeStringsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         const char*
            windowsRuntimeStringsSize = int.from_bytes(reader.read(4), byteorder='little')                    #
            exportedTypeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeDefinitionIndex
            exportedTypeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little') #typeDefinitionIndex
            methods = getMethodNames(path, methodsOffset, methodsCount)
            with open("Methods_"+str(path[2:7])+".txt", "w") as methodFile:
                #Move location to the method string name
                with open(path, 'rb') as reader:
                    for i in range(len(methods)):
                        reader.seek(stringOffset + methods[i][0], 0)
                        writeList(readUntilNullByte(reader),methodFile)

def outputFields(paths):
    for path in paths:
        with open(path, 'rb') as reader:
            sanity = int.from_bytes(reader.read(4), byteorder='little')
            version = int.from_bytes(reader.read(4), byteorder='little')
            stringLiteralOffset = int.from_bytes(reader.read(4), byteorder='little')             #         string data for managed code
            stringLiteralCount = int.from_bytes(reader.read(4), byteorder='little')
            stringLiteralDataOffset = int.from_bytes(reader.read(4), byteorder='little')
            stringLiteralDataCount = int.from_bytes(reader.read(4), byteorder='little')
            stringOffset = int.from_bytes(reader.read(4), byteorder='little')             #         string data for metadata
            stringCount = int.from_bytes(reader.read(4), byteorder='little')
            eventsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppEventDefinition
            eventsCount = int.from_bytes(reader.read(4), byteorder='little')
            propertiesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppPropertyDefinition
            propertiesCount = int.from_bytes(reader.read(4), byteorder='little')
            methodsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppMethodDefinition
            methodsCount = int.from_bytes(reader.read(4), byteorder='little')
            parameterDefaultValuesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppParameterDefaultValue
            parameterDefaultValuesCount = int.from_bytes(reader.read(4), byteorder='little')
            fieldDefaultValuesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppFieldDefaultValue
            fieldDefaultValuesCount = int.from_bytes(reader.read(4), byteorder='little')
            fieldAndParameterDefaultValueDataOffset = int.from_bytes(reader.read(4), byteorder='little')             #         uint8_t
            fieldAndParameterDefaultValueDataCount = int.from_bytes(reader.read(4), byteorder='little')
            fieldMarshaledSizesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppFieldMarshaledSize
            fieldMarshaledSizesCount = int.from_bytes(reader.read(4), byteorder='little')
            parametersOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppParameterDefinition
            parametersCount = int.from_bytes(reader.read(4), byteorder='little')

            fieldsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppFieldDefinition
            fieldsCount = int.from_bytes(reader.read(4), byteorder='little')
            genericParametersOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppGenericParameter
            genericParametersCount = int.from_bytes(reader.read(4), byteorder='little')
            genericParameterConstraintsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeIndex
            genericParameterConstraintsCount = int.from_bytes(reader.read(4), byteorder='little')
            genericContainersOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppGenericContainer
            genericContainersCount = int.from_bytes(reader.read(4), byteorder='little')
            nestedTypesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeDefinitionIndex
            nestedTypesCount = int.from_bytes(reader.read(4), byteorder='little')                             #
            interfacesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeIndex
            interfacesCount = int.from_bytes(reader.read(4), byteorder='little')
            vtableMethodsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         EncodedMethodIndex
            vtableMethodsCount = int.from_bytes(reader.read(4), byteorder='little')
            interfaceOffsetsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppInterfaceOffsetPair
            interfaceOffsetsCount = int.from_bytes(reader.read(4), byteorder='little')
            typeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppTypeDefinition
            typeDefinitionsCount = int.from_bytes(reader.read(4), byteorder='little')
            imagesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppImageDefinition
            imagesCount = int.from_bytes(reader.read(4), byteorder='little')
            assembliesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppAssemblyDefinition
            assembliesCount = int.from_bytes(reader.read(4), byteorder='little')
            fieldRefsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppFieldRef
            fieldRefsCount = int.from_bytes(reader.read(4), byteorder='little')
            referencedAssembliesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         int32_t
            referencedAssembliesCount = int.from_bytes(reader.read(4), byteorder='little')
            attributesInfoOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppCustomAttributeTypeRange
            attributesInfoCount = int.from_bytes(reader.read(4), byteorder='little')
            attributeTypesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeIndex
            attributeTypesCount = int.from_bytes(reader.read(4), byteorder='little')
            unresolvedVirtualCallParameterTypesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeIndex
            unresolvedVirtualCallParameterTypesCount = int.from_bytes(reader.read(4), byteorder='little')
            unresolvedVirtualCallParameterRangesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppMetadataRange                unresolvedVirtualCallParameterRangesCount = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeTypeNamesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppWindowsRuntimeTypeNamePair
            windowsRuntimeTypeNamesSize = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeStringsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         const char*
            windowsRuntimeStringsSize = int.from_bytes(reader.read(4), byteorder='little')                    #
            exportedTypeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeDefinitionIndex
            exportedTypeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little') #typeDefinitionIndex

            fields = getFieldNames(path, fieldsOffset, fieldsCount)
            with open("Fields_"+str(path[2:7])+".txt", "w") as fieldFile:
                #Move location to the method string name
                with open(path, 'rb') as reader:
                    for i in range(len(fields)):
                        reader.seek(stringOffset + fields[i][0], 0)
                        writeList(readUntilNullByte(reader),fieldFile)

def outputObfStatus(paths):
    numberObfuscated = 0
    with open("Obfuscation_information.txt", "w") as f:
        for path in paths:
            f.write("The metadata file at ")
            f.write(path)
            f.write(" is version ")
            f.write(str(checkVersion(path)))
            if checkForObfuscation(path):
                f.write(". It is obfuscated.\n")
                numberObfuscated += 1
            else:
                f.write(". It is not obfuscated.\n")
    return numberObfuscated
args = sys.argv[1:]
goodArgs = ['m', 'o', 'fields']
if len(args) == 0 or (len(set(goodArgs) & set(args)) == 0):
    print("usage: python parser.py m [or] o [or] fields")
    print("The \'m\' flag will output the methods to a file")
    print("The \'fields\' flag will output the fields  to a file")
    print("The \'o\' flag will output the obfuscation status")
    exit(0)
print("Finding all paths to \"global-metadata.dat\"")
paths = glob.glob("./**/global-metadata.dat", recursive = True)
if len(paths) == 0:
    print("Error. No paths detected. The file is missing or obfuscated.")
if('m' in args):
    print("Outputting methods.")
    outputMethods(paths)
if('fields' in args):
    print("Outputting fields.")
    outputFields(paths)
if('o' in args):
    print("Outputting obfuscation status.")
    numberOfFiles = 0
    numberOfDirectories = 0
    numberOfItems = 0
    for item in os.listdir():
        numberOfItems += 1
        if os.path.isfile(item):
            numberOfFiles += 1
    numberOfDirectories = numberOfItems - numberOfFiles
    numberObfuscated = numberOfDirectories - len(paths)
    numberObfuscated += outputObfStatus(paths)
    print("Of " + str(numberOfDirectories) +" directories, " + str(numberObfuscated) +" have either missing or obfuscated global-metadata.dat file.")
    print("All files not listed in the output text file should be considered to have either missing or obfuscated global-metadata.dat file.")
exit(0)

#Jacob Urick
#The Ohio State University
#urick.9@osu.edu



#TODO fix path finding; on each device, after finding the head of a path chain the rest follows
#TODO cache metadata header and cache path
import os
import glob
import sys
from varname import nameof



#checks for obfuscation
def checkForObfuscation(filename):
    header = []
    obfuscated = False
    with open(filename, "rb") as f:
        chunk = f.read(4)
        for b in chunk:
            header.append(b)
        sanity = int.from_bytes(header, byteorder = 'little')
        if(hex(sanity) != "0xfab11baf"):
            obfuscated = True
        version = checkVersion(filename)
        if version > 30 or version < 1:
            obfuscated = True
        if not verifySigniture(filename, version):
            obfuscated = True
        return obfuscated
#checks the version
def checkVersion(filename):
    with open(filename, "rb") as reader:
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
        unresolvedVirtualCallParameterRangesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppMetadataRange
        unresolvedVirtualCallParameterRangesCount = int.from_bytes(reader.read(4), byteorder='little')
        windowsRuntimeTypeNamesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppWindowsRuntimeTypeNamePair
        windowsRuntimeTypeNamesSize = int.from_bytes(reader.read(4), byteorder='little')
        windowsRuntimeStringsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         const char*
        windowsRuntimeStringsSize = int.from_bytes(reader.read(4), byteorder='little')                    #
        exportedTypeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeDefinitionIndex
        exportedTypeDefinitionsCount = int.from_bytes(reader.read(4), byteorder='little') #typeDefinitionIndex
    if version == 24:
        if stringLiteralOffset == 264:
            version = 24.2
        elif isVersion24point1(filename):
            version = 24.1
    return version
#Given an open & readble file, read bytes until a null byte is found
def readUntilNullByte(file):
    word = []
    while True:
        b = file.read(1)
        #Ignore errors for now
        try:
            b = b.decode("utf-8", errors="strict")
        except UnicodeError:
            print("There has been an error trying to parse " + file.name)
        if b != '\0':
            word.append(b)
        else:
            break
    return word

#verify that.ctor, the IL constructor, is the first method listed.
def verifySigniture(path, version):
    with open(path, 'rb') as reader:
        #read header up to the methodsOffset
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
        version = checkVersion(path)
        #Move the reading location to the first method
        methods = getMethodNames(path, methodsOffset, methodsCount, version)
        #Check that there is a constructor in the first few thousand bytes of method structs
        names = []
        for method in methods:
            reader.seek(stringOffset + method[0], 0)
            name = readUntilNullByte(reader)
            if ['.', 'c', 't', 'o', 'r'] == name:
                return True
        return False


#Given a list and an open & writable file, write the list contents
def writeList(lst, file):
    for i in range(len(lst)):
        file.write(lst[i])
    file.write("\n")
#Get method names from file
def getMethodNames(path, start, count, version):
    methods = []
    with open(path, 'rb') as reader:
        #Move reading location to the start of the structs
        reader.seek(start, 0)
        #We now read in count many IL2CPPMethodDefinition structs
        #These are 32 bytes in version 27, 52 bytes in a previous version
        #I only care about the first int, the StringIndex nameIndex,
        #The second int, the TypeDefinitionIndex declaringType,
        #the third int, the TypeIndex returnType, and
        #the fourth int, the ParamaterIndex parameterStart,
        #and the last, the 2 byte paramaterCount
        print("The version being checked is " + str(version))
        if version > 24.1:
            Il2CppMethodDefinitionSize = 32
            for i in range(int(count/Il2CppMethodDefinitionSize)):
                method = []
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                #Move 14 bytes forward
                reader.seek(14, 1)
                method.append(int.from_bytes(reader.read(2), byteorder='little'))
                methods.append(method)
        if version == 24:
            Il2CppMethodDefinitionSize = 56
            for i in range(int(count/Il2CppMethodDefinitionSize)):
                method = []
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                #Move 38 bytes forward
                reader.seek(38, 1)
                method.append(int.from_bytes(reader.read(2), byteorder='little'))
                methods.append(method)
        if version == 24.1:
            Il2CppMethodDefinitionSize = 52
            for i in range(int(count/Il2CppMethodDefinitionSize)):
                method = []
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                method.append(int.from_bytes(reader.read(4), byteorder='little'))
                #Move 34 bytes forward
                reader.seek(34, 1)
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

def listToString(myList):
    out = ""
    for x in myList:
        out += x
    return out
#Get typeStructs from file
def getTypes(path, start, count):
    fields = []
    with open(path, 'rb') as reader:
        #Move reading location to the start of the structs
        reader.seek(start, 0)
        #We now read in count many IL@Il2CppTypeDefinition structs
        #These are 32 bytes
        #I only care about the first int, the StringIndex nameIndex,
        #The second int, the typeIndexe,  may be interesting soon

        for i in range(int(count/(22*4))):
            field = []
            field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little')) #4
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little')) #9
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little'))
            field.append(int.from_bytes(reader.read(4), byteorder='little')) #14
            field.append(int.from_bytes(reader.read(4), byteorder='little'))

            field.append(int.from_bytes(reader.read(2), byteorder='little'))
            field.append(int.from_bytes(reader.read(2), byteorder='little'))
            field.append(int.from_bytes(reader.read(2), byteorder='little'))
            field.append(int.from_bytes(reader.read(2), byteorder='little'))
            field.append(int.from_bytes(reader.read(2), byteorder='little'))
            field.append(int.from_bytes(reader.read(2), byteorder='little'))
            field.append(int.from_bytes(reader.read(2), byteorder='little'))
            field.append(int.from_bytes(reader.read(2), byteorder='little'))

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
            unresolvedVirtualCallParameterRangesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppMetadataRange
            unresolvedVirtualCallParameterRangesCount = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeTypeNamesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppWindowsRuntimeTypeNamePair
            windowsRuntimeTypeNamesSize = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeStringsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         const char*
            windowsRuntimeStringsSize = int.from_bytes(reader.read(4), byteorder='little')                    #
            exportedTypeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeDefinitionIndex
            exportedTypeDefinitionsCount = int.from_bytes(reader.read(4), byteorder='little') #typeDefinitionIndex
            methods = getMethodNames(path, methodsOffset, methodsCount, checkVersion(path))
            with open("Methods_"+str(path[2:7])+".txt", "w") as methodFile:
                #Move location to the method string name
                with open(path, 'rb') as reader:
                    for i in range(len(methods)):
                        reader.seek(stringOffset + methods[i][0], 0)
                        writeList(readUntilNullByte(reader),methodFile)
def writeDictionaryToFile(dictionary, path):
    with open(path, 'w') as writer:
        for key in dictionary.keys():
            if key is not None:
                writer.write(key + "\n")
                val = dictionary[key]
                if val is not None:
                    for x in val:
                        if x is not None:
                            writer.write(x + "\n")
#Given a version 24.0 or 24.1 metadata file, this returns false if the image definitions tell us
#we have a version 24.0 and returns true if we have version 24.1
def isVersion24point1(path):
    #the Il2CppImageDefinition struct is 32 bytes in version 24, and 40 bytes in version 24.1
    #In the file, Il2CppAssemblyDefinition structs are listed right after the Il2CppImageDefinition typeStructs
    #It follows that we can check if the total length of the image definitions(Assuming 40 byte structs!) is greater than
    #the offet that should give us an assembly.
     with open(path, 'rb') as reader:
        sanity = int.from_bytes(reader.read(4), byteorder='little')
        version = int.from_bytes(reader.read(4), byteorder='little')
        stringLiteralOffset = int.from_bytes(reader.read(4), byteorder='little')             #         string data for managed code
        stringLiteralCount = int.from_bytes(reader.read(4), byteorder='little')
        stringLiteralDataOffset = int.from_bytes(reader.read(4), byteorder='little')
        stringLiteralDataCount = int.from_bytes(reader.read(4), byteorder='little')
        stringOffset = int.from_bytes(reader.read(4), byteorder='little')             #         string data for metadata
        tringCount = int.from_bytes(reader.read(4), byteorder='little')
        eventsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppEventDefinition
        eventsCount = int.from_bytes(reader.read(4), byteorder='little')
        propertiesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppPropertyDefinition
        propertiesCount = int.from_bytes(reader.read(4), byteorder='little')
        methodsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppMethodDefinition
        methodsCount = int.from_bytes(reader.read(4), byteorder='little')
        arameterDefaultValuesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppParameterDefaultValue
        parameterDefaultValuesCount = int.from_bytes(reader.read(4), byteorder='little')
        fieldDefaultValuesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppFieldDefaultValue
        fieldDefaultValuesCount = int.from_bytes(reader.read(4), byteorder='little')
        fieldAndParameterDefaultValueDataOffset = int.from_bytes(reader.read(4), byteorder='little')             #         uint8_t
        ieldAndParameterDefaultValueDataCount = int.from_bytes(reader.read(4), byteorder='little')
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
        enericContainersOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppGenericContainer
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
        if(version == 24 and imagesOffset+40*imagesCount >= assembliesOffset):
            return True
        else:
            return False
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
            unresolvedVirtualCallParameterRangesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppMetadataRange
            unresolvedVirtualCallParameterRangesCount = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeTypeNamesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppWindowsRuntimeTypeNamePair
            windowsRuntimeTypeNamesSize = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeStringsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         const char*
            windowsRuntimeStringsSize = int.from_bytes(reader.read(4), byteorder='little')                    #
            exportedTypeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeDefinitionIndex
            exportedTypeDefinitionsCount = int.from_bytes(reader.read(4), byteorder='little') #typeDefinitionIndex

            fields = getFieldNames(path, fieldsOffset, fieldsCount)
            with open("Fields_"+str(path[2:7])+".txt", "w") as fieldFile:
                #Move location to the method string name
                with open(path, 'rb') as reader:
                    for i in range(len(fields)):
                        reader.seek(stringOffset + fields[i][0], 0)
                        writeList(readUntilNullByte(reader),fieldFile)

def outputFileStructure(path):

    names = []
    names.append("sanity") # int.from_bytes(reader.read(4), byteorder#'little')
    names.append("version") # int.from_bytes(reader.read(4), byteorder#'little')
    names.append("stringLiteralOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         string data for managed code
    names.append("stringLiteralCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("stringLiteralDataOffset")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("stringLiteralDataCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("stringOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         string data for metadata
    names.append("stringCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("eventsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppEventDefinition
    names.append("eventsCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("propertiesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppPropertyDefinition
    names.append("propertiesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("methodsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppMethodDefinition
    names.append("methodsCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("parameterDefaultValuesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppParameterDefaultValue
    names.append("parameterDefaultValuesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("fieldDefaultValuesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppFieldDefaultValue
    names.append("fieldDefaultValuesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("fieldAndParameterDefaultValueDataOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         uint8_t
    names.append("fieldAndParameterDefaultValueDataCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("fieldMarshaledSizesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppFieldMarshaledSize
    names.append("fieldMarshaledSizesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("parametersOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppParameterDefinition
    names.append("parametersCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("fieldsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppFieldDefinition
    names.append("fieldsCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("genericParametersOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppGenericParameter
    names.append("genericParametersCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("genericParameterConstraintsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         TypeIndex
    names.append("genericParameterConstraintsCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("genericContainersOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppGenericContainer
    names.append("genericContainersCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("nestedTypesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         TypeDefinitionIndex
    names.append("nestedTypesCount")# int.from_bytes(reader.read(4), byteorder#'little')                             #
    names.append("interfacesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         TypeIndex
    names.append("interfacesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("vtableMethodsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         EncodedMethodIndex
    names.append("vtableMethodsCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("interfaceOffsetsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppInterfaceOffsetPair
    names.append("interfaceOffsetsCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("typeDefinitionsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppTypeDefinition
    names.append("typeDefinitionsCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("imagesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppImageDefinition
    names.append("imagesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("assembliesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppAssemblyDefinition
    names.append("assembliesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("fieldRefsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppFieldRef
    names.append("fieldRefsCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("referencedAssembliesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         int32_t
    names.append("referencedAssembliesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("attributesInfoOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppCustomAttributeTypeRange
    names.append("attributesInfoCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("attributeTypesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         TypeIndex
    names.append("attributeTypesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("unresolvedVirtualCallParameterTypesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         TypeIndex
    names.append("unresolvedVirtualCallParameterTypesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("unresolvedVirtualCallParameterRangesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppMetadataRange
    names.append("unresolvedVirtualCallParameterRangesCount")# int.from_bytes(reader.read(4), byteorder#'little')
    names.append("windowsRuntimeTypeNamesOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         Il2CppWindowsRuntimeTypeNamePair
    names.append("windowsRuntimeTypeNamesSize") # int.from_bytes(reader.read(4), byteorder#'little')
    names.append("windowsRuntimeStringsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         const char*
    names.append("windowsRuntimeStringsSize") # int.from_bytes(reader.read(4), byteorder#'little')                    #
    names.append("exportedTypeDefinitionsOffset")# int.from_bytes(reader.read(4), byteorder#'little')             #         TypeDefinitionIndex
    names.append("exportedTypeDefinitionsCount ")# int.from_bytes(reader.read(4), byteorder#'little') #typeDefinitionIndex
    file = []
    offsetNames = {}
    stringsToPrint = []
    for path in paths:
        with open(path, 'rb') as reader:
            offsets = []
            for i in range(64):
                offsets.append(int.from_bytes(reader.read(4), byteorder='little'))
            with open("Offsets"+str(path[2:7])+".txt", "w") as offsetFile:
                for i in range(31):
                    offsetNames[names[2*i]] = offsets[2*i]
                sortedOffsetNames = sorted(offsetNames, key = offsetNames.get)
                for x in sortedOffsetNames:
                    stringsToPrint.append(x + ": " + hex(offsetNames[x]) + '\n')
                writeList(stringsToPrint,offsetFile)

def outputTypes(paths):
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
            unresolvedVirtualCallParameterRangesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppMetadataRange
            unresolvedVirtualCallParameterRangesCount = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeTypeNamesOffset = int.from_bytes(reader.read(4), byteorder='little')             #         Il2CppWindowsRuntimeTypeNamePair
            windowsRuntimeTypeNamesSize = int.from_bytes(reader.read(4), byteorder='little')
            windowsRuntimeStringsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         const char*
            windowsRuntimeStringsSize = int.from_bytes(reader.read(4), byteorder='little')                    #
            exportedTypeDefinitionsOffset = int.from_bytes(reader.read(4), byteorder='little')             #         TypeDefinitionIndex
            exportedTypeDefinitionsCount = int.from_bytes(reader.read(4), byteorder='little') #typeDefinitionIndex
            types = getTypes(path, typeDefinitionsOffset, typeDefinitionsCount)

            with open("Types_"+str(path[2:7])+".txt", "w") as typesFile:
                #Move location to the method string name
                toPrint = []
                for i in range(1):
                    nameIndex = types[i][0]
                    namespaceIndex = types[i][1]
                    fieldStart = types[i][8]
                    methodStart = types[i][9]
                    popertyStart = types[i][11]
                    method_count = types[i][16]
                    property_count = types[i][17]
                    field_count = types[i][18]
                    reader.seek(stringOffset + nameIndex)
                    toPrint.append(readUntilNullByte(reader))
                    reader.seek(stringOffset + namespaceIndex)
                    toPrint.append(readUntilNullByte(reader))

                    #We've read in nameIndex and namespaceIndex
                    #Now we will read in some fields/methods
                    fields = getFieldNames(path, (fieldStart*12) + fieldsOffset , field_count*12)
                    methods = getMethodNames(path, (methodStart*32) + methodsOffset, method_count*32, version)
                    #if i == len(types) - 1:
                        #print("value")
                        #print(hex(methods[1][0] + stringOffset))
                        #print(hex(stringOffset))
                    if(len(fields)):
                        for field in fields:
                            reader.seek( stringOffset + field[0], 0)
                            toPrint.append([" Fields: "]+readUntilNullByte(reader))
                        toPrint.append("\n")
                    if(len(methods)):
                        for method in methods:
                            reader.seek(stringOffset + method[0], 0)
                            toPrint.append([" Methods: "]+readUntilNullByte(reader))
                        toPrint.append("\n")
                    toPrint.append("\n------------------------------------\n")
                printListToFile(toPrint, typesFile)
def printListToFile(listName, file):
    for x in listName:
        if(isinstance(x, list)):
            for i in range(len(x)):
                file.write(x[i])
        else:
            file.write(x)



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
goodArgs = ['m', 'o', 'fields', 'structure', 'types']
if len(args) == 0 or (len(set(goodArgs) & set(args)) == 0):
    print("usage: python parser.py m [or] o [or] fields [or] structure [or] types")
    print("The \'types\' flag will output the types with methods and fields to a file(only working for latest version)")
    print("The \'m\' flag will output the methods to a file")
    print("The \'fields\' flag will output the fields  to a file(only working for latest version)")
    print("The \'structure\' flag will output the structure  to a file(only working for latest version)")
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
if('structure' in args):
    print("Outputting metadata structure(offsets and count).")
    outputFileStructure(paths)
if('types' in args):
    print("Outputting type information with methods and offsets")
    outputTypes(paths)
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

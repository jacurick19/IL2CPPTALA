#Jacob Urick
#The Ohio State University
#urick.9@osu.edu



#TODO fix path finding; on each device, after finding the head of a path chain the rest follows
#TODO cache metadata header and cache path
import os
import glob
import sys
from varname import nameof
import time
import json
import zipfile
import tempfile
#checks for obfuscation
def checkForObfuscation(filename, quick = False, filePath = None, zipped = False, zipObject = None):

    header = []
    obfuscated = False
    if zipped:
        reader = zipObject.open(filename, 'r')
        reader.seek(0)
        chunk = reader.read(4)
        reader.close()
        for b in chunk:
            header.append(b)
        sanity = int.from_bytes(header, byteorder = 'little')

        if(hex(sanity) != "0xfab11baf"):
            obfuscated = True
        version = checkVersion(filename, zipped, zipObject)
        if (not obfuscated) and (version > 30 or version < 1):
            obfuscated = True
        if (not obfuscated) and not verifySigniture(filename, version, quick, filePath, zipped, zipObject):
            obfuscated = True
        reader.close()
        return obfuscated
    else:
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
            if not verifySigniture(filename, version, quick):
                obfuscated = True
            return obfuscated
#checks the version
def checkVersion(filename, zipped = False, zipObject = None):
    if zipped:
        reader = zipObject.open(filename, 'r')
        reader.seek(0)
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
        reader.close()
        if version == 24:
            if stringLiteralOffset == 264:
                version = 24.2
            elif isVersion24point1(filename, zipped, zipObject):
                version = 24.1
        return version

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
def verifySigniture(path, version, quick = False, typeFilePath = None, zipped = False, zipObject = None):
    if quick and typeFilePath:
        print("Error! You cannot do a quick check with a type path specified.")
        exit(0)
    if zipped:
        reader = zipObject.open(path, 'r')
        reader.seek(0)
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
        version = checkVersion(path, zipped, zipObject)

        #Move the reading location to the first method
        if quick:
            methods = getMethodNames(path, methodsOffset, methodsCount, version, zipped, zipObject)
            #Check that there is a constructor in the first few thousand bytes of method structs
            names = []
            for method in methods:
                reader.seek(stringOffset + method[0], 0)
                name = readUntilNullByte(reader)
                if ['.', 'c', 't', 'o', 'r'] == name:
                    reader.close()
                    return True
            reader.close()
            return False
        start = time.perf_counter()
        types = getTypes(path, typeDefinitionsOffset, typeDefinitionsCount, version, zipped, zipObject)
        if typeFilePath == None:
            nameSeek = list("RuntimeClassHandle")
            methodsSeek = [list(".ctor"), list("get_Value"), list("GetHashCode")]
            fieldsSeek = [list("value")]
        else:
            with open(typeFilePath) as jsonFile:
                file = json.load(jsonFile)
                nameSeek  = list(file['Signature']['nameSeek'])
                methodsSeek = file['Signature']['methodsSeek']
                newMethods = []
                newFields = []
                for x in methodsSeek:
                    newMethods.append(list(x))
                fieldsSeek = file['Signature']['fieldsSeek']
                for x in fieldsSeek:
                    newFields.append(list(x))
                fieldsSeek = newFields
                methodsSeek = newMethods
        foundName = False
        foundAllMethods = False
        foundAllFields = False
        cur = ""
        for i in range(len(types)):
            nameIndex = types[i][0]
            if stringOffset + nameIndex > eventsOffset:
                return False
            reader.seek(stringOffset + nameIndex)
            cur = readUntilNullByte(reader)
            if cur == nameSeek:
                foundName = True
            if foundName:
                fieldStart = types[i][8]
                field_count = types[i][18]
                fields = getFieldNames(path, (fieldStart*getSizeOfIl2CppFieldDefinition(version)) + fieldsOffset , field_count*getSizeOfIl2CppFieldDefinition(version), zipped, zipObject)
                listOfFieldNames = []
                for field in fields:
                    if(time.perf_counter() - start > 5):
                        return False
                    nameIndex = field[0]
                    reader.seek(stringOffset + nameIndex)
                    listOfFieldNames.append(readUntilNullByte(reader))
                foundAllFields = True
                for field in fieldsSeek:
                    foundAllFields = foundAllFields and field in listOfFieldNames
            if foundAllFields:
                if(time.perf_counter() - start > 5):
                    return False
                methodStart = types[i][9]
                method_count = types[i][16]
                methods = getMethodNames(path, (methodStart*getSizeOfIl2CppMethodDefinition(version)) + methodsOffset, method_count*getSizeOfIl2CppMethodDefinition(version), version, zipped, zipObject)
                listOfMethodNames = []
                for method in methods:
                    if(time.perf_counter() - start > 5):
                        return False
                    nameIndex = method[0]
                    reader.seek(stringOffset + nameIndex)
                    listOfMethodNames.append(readUntilNullByte(reader))
                foundAllMethods = True
                for method in methodsSeek:
                    foundallMethods = foundAllMethods and method in listOfMethodNames
                break

        reader.close()

        return foundAllMethods and foundAllFields and foundName
    else:
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
            version = checkVersion(path)
            #Move the reading location to the first method
            if quick:
                methods = getMethodNames(path, methodsOffset, methodsCount, version)
                #Check that there is a constructor in the first few thousand bytes of method structs
                names = []
                for method in methods:
                    reader.seek(stringOffset + method[0], 0)
                    name = readUntilNullByte(reader)
                    if ['.', 'c', 't', 'o', 'r'] == name:
                        return True
                return False
            types = getTypes(path, typeDefinitionsOffset, typeDefinitionsCount, version)
            if typeFilePath == None:
                nameSeek = list("RuntimeClassHandle")
                methodsSeek = [list(".ctor"), list("get_Value"), list("GetHashCode")]
                fieldsSeek = [list("value")]
            else:
                with open(typeFilePath) as jsonFile:
                    file = json.load(jsonFile)
                    nameSeek  = list(file['Signature']['nameSeek'])
                    methodsSeek = file['Signature']['methodsSeek']
                    newMethods = []
                    newFields = []
                    for x in methodsSeek:
                        newMethods.append(list(x))
                    fieldsSeek = file['Signature']['fieldsSeek']
                    for x in fieldsSeek:
                        newFields.append(list(x))
                    fieldsSeek = newFields
                    methodsSeek = newMethods
            foundName = False
            foundAllMethods = False
            foundAllFields = False
            cur = ""

            for i in range(len(types)):
                nameIndex = types[i][0]
                reader.seek(stringOffset + nameIndex)
                cur = readUntilNullByte(reader)
                if cur == nameSeek:
                    foundName = True
                if foundName:
                    fieldStart = types[i][8]
                    field_count = types[i][18]
                    fields = getFieldNames(path, (fieldStart*getSizeOfIl2CppFieldDefinition(version)) + fieldsOffset , field_count*getSizeOfIl2CppFieldDefinition(version))
                    listOfFieldNames = []
                    for field in fields:
                        nameIndex = field[0]
                        reader.seek(stringOffset + nameIndex)
                        listOfFieldNames.append(readUntilNullByte(reader))
                    foundAllFields = True
                    for field in fieldsSeek:
                        foundAllFields = foundAllFields and field in listOfFieldNames
                if foundAllFields:
                    methodStart = types[i][9]
                    method_count = types[i][16]
                    methods = getMethodNames(path, (methodStart*getSizeOfIl2CppMethodDefinition(version)) + methodsOffset, method_count*getSizeOfIl2CppMethodDefinition(version), version)
                    listOfMethodNames = []
                    for method in methods:
                        nameIndex = method[0]
                        reader.seek(stringOffset + nameIndex)
                        listOfMethodNames.append(readUntilNullByte(reader))
                    foundAllMethods = True
                    for method in methodsSeek:
                        foundallMethods = foundAllMethods and method in listOfMethodNames
                    break

            return foundAllMethods and foundAllFields and foundName


#Given a list and an open & writable file, write the list contents
def writeList(lst, file):
    for i in range(len(lst)):
        file.write(lst[i])
    file.write("\n")
#Get method names from file
def getMethodNames(path, start, count, version, zipped = False, zipObject = None):
    methods = []
    if zipped:
        reader = tempfile.TemporaryFile()
        reader.write(zipObject.read(path))
        reader.seek(start, 0)
        #We now read in count many IL2CPPMethodDefinition structs
        #These are 32 bytes in version 27, 52 bytes in a previous version
        #I only care about the first int, the StringIndex nameIndex,
        #The second int, the TypeDefinitionIndex declaringType,
        #the third int, the TypeIndex returnType, and
        #the fourth int, the ParamaterIndex parameterStart,
        #and the last, the 2 byte paramaterCount
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
        reader.close()
    else:
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

def getSizeOfIl2CppMethodDefinition(version):
    if version > 24.1:
        return 8*4
    if version == 24.1:
        return 13*4
    if version == 24:
        return 14*4

def getSizeOfIl2CppFieldDefinition(version):
    if version >= 19 and version <= 24:
        return 4*4
    if version < 19 or version > 24:
        return 3*4

#Get method names from file
def getFieldNames(path, start, count, zipped, zipObject):
    fields = []
    if zipped:
        reader = zipObject.open(path, 'r')

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

        reader.close()
    else:
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
def getTypes(path, start, count, version, zipped = False, zipObject = None):
    fields = []

    if zipped:
        reader = zipObject.open(path, 'r')
        #Move reading location to the start of the structs
        reader.seek(start, 0)
        #We now read in count many IL@Il2CppTypeDefinition structs
        #These are 32 bytes
        #I only care about the first int, the StringIndex nameIndex,
        #The second int, the typeIndexe,  may be interesting soon
        if(version > 24.4):
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
        if(version > 24.1 and version <= 24.4):

            for i in range(int(count/(23*4))):
                field = []
                field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                reader.seek(4,1)
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
        if(version > 24 and version <= 24.1):

            for i in range(int(count/(25*4))):
                field = []
                field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                reader.seek(4,1)

                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                field.append(int.from_bytes(reader.read(4), byteorder='little')) #4
                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                reader.seek(4,1)
                reader.seek(4,1)
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
        if version == 24:
            for i in range(int(count/(23*4))):
                field = []
                field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                reader.seek(4,1)
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
        return fields

    else:
        with open(path, 'rb') as reader:

            #Move reading location to the start of the structs
            reader.seek(start, 0)
            #We now read in count many IL@Il2CppTypeDefinition structs
            #These are 32 bytes
            #I only care about the first int, the StringIndex nameIndex,
            #The second int, the typeIndexe,  may be interesting soon
            if(version > 24.4):
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
            if(version > 24.1 and version <= 24.4):
                for i in range(int(count/(23*4))):
                    field = []
                    field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    reader.seek(4,1)
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
            if(version > 24 and version <= 24.1):
                for i in range(int(count/(25*4))):
                    field = []
                    field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    reader.seek(4,1)
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    field.append(int.from_bytes(reader.read(4), byteorder='little')) #4
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    reader.seek(4,1)
                    reader.seek(4,1)
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
            if version <= 24 and version > 22:
                for i in range(int(count/(26*4))):
                    field = []
                    field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    reader.seek(4,1)
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    reader.seek(4,1)
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    field.append(int.from_bytes(reader.read(4), byteorder='little')) #4
                    field.append(int.from_bytes(reader.read(4), byteorder='little'))
                    reader.seek(4,1)
                    reader.seek(4,1)
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

                    if version <=22 and version >= 21:
                        for i in range(int(count/(30*4))):
                            field = []
                            field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
                            field.append(int.from_bytes(reader.read(4), byteorder='little'))
                            reader.seek(4,1)
                            field.append(int.from_bytes(reader.read(4), byteorder='little'))
                            reader.seek(4,1)
                            field.append(int.from_bytes(reader.read(4), byteorder='little'))
                            field.append(int.from_bytes(reader.read(4), byteorder='little')) #4
                            field.append(int.from_bytes(reader.read(4), byteorder='little'))
                            reader.seek(4,1)
                            reader.seek(4,1)
                            field.append(int.from_bytes(reader.read(4), byteorder='little'))

                            field.append(int.from_bytes(reader.read(4), byteorder='little'))
                            field.append(int.from_bytes(reader.read(4), byteorder='little'))
                            field.append(int.from_bytes(reader.read(4), byteorder='little')) #9
                            field.append(int.from_bytes(reader.read(4), byteorder='little'))
                            reader.seek(4,1)
                            reader.seek(4,1)
                            reader.seek(4,1)
                            reader.seek(4,1)
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
                        if version < 21 and version >= 19:
                            for i in range(int(count/(28*4))):
                                field = []
                                field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                reader.seek(4,1)
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                reader.seek(4,1)
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                field.append(int.from_bytes(reader.read(4), byteorder='little')) #4
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                reader.seek(4,1)
                                reader.seek(4,1)
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))

                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                field.append(int.from_bytes(reader.read(4), byteorder='little')) #9
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                reader.seek(4,1)
                                reader.seek(4,1)
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
                        if version < 19:
                            for i in range(int(count/(28*4))):
                                field = []
                                field.append(int.from_bytes(reader.read(4), byteorder='little')) #0
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                reader.seek(4,1)
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                reader.seek(4,1)
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                field.append(int.from_bytes(reader.read(4), byteorder='little')) #4
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                reader.seek(4,1)
                                reader.seek(4,1)
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))

                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                field.append(int.from_bytes(reader.read(4), byteorder='little')) #9
                                field.append(int.from_bytes(reader.read(4), byteorder='little'))
                                reader.seek(4,1)
                                reader.seek(4,1)
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
def isVersion24point1(path, zipped = False, zipObject = None):
    #the Il2CppImageDefinition struct is 32 bytes in version 24, and 40 bytes in version 24.1
    #In the file, Il2CppAssemblyDefinition structs are listed right after the Il2CppImageDefinition typeStructs
    #It follows that we can check if the total length of the image definitions(Assuming 40 byte structs!) is greater than
    #the offet that should give us an assembly.
    if zipped:
        reader = zipObject.open(path, 'r')

        reader.seek(0)
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
        reader.close()
        if(version == 24 and imagesOffset+40*imagesCount >= assembliesOffset):
            return True
        else:
            return False
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

#Note well: this only works on version 25+
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

def outputTypes(paths, zipped = False, zipObject = None):
    if zipped:
        for path in paths:
            reader = zipObject.open(path, 'r')

            reader.seek(0)
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
            version = checkVersion(path)
            types = getTypes(path, typeDefinitionsOffset, typeDefinitionsCount, version)
            with open("Types_"+str(path[2:7])+".txt", "w") as typesFile:
                #Move location to the method string name
                toPrint = []
                for i in range(len(types)):
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
                    #toPrint.append(readUntilNullByte(reader))

                    #We've read in nameIndex and namespaceIndex
                    #Now we will read in some fields/methods
                    fields = getFieldNames(path, (fieldStart*getSizeOfIl2CppFieldDefinition(version)) + fieldsOffset , field_count*getSizeOfIl2CppFieldDefinition(version))
                    methods = getMethodNames(path, (methodStart*getSizeOfIl2CppMethodDefinition(version)) + methodsOffset, method_count*getSizeOfIl2CppMethodDefinition(version), version)

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
    else:
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
                version = checkVersion(path)
                types = getTypes(path, typeDefinitionsOffset, typeDefinitionsCount, version)
                with open("Types_"+str(path[2:7])+".txt", "w") as typesFile:
                    #Move location to the method string name
                    toPrint = []
                    for i in range(len(types)):
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
                        #toPrint.append(readUntilNullByte(reader))

                        #We've read in nameIndex and namespaceIndex
                        #Now we will read in some fields/methods
                        fields = getFieldNames(path, (fieldStart*getSizeOfIl2CppFieldDefinition(version)) + fieldsOffset , field_count*getSizeOfIl2CppFieldDefinition(version))
                        methods = getMethodNames(path, (methodStart*getSizeOfIl2CppMethodDefinition(version)) + methodsOffset, method_count*getSizeOfIl2CppMethodDefinition(version), version)

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



def outputObfStatus(paths, quick = False, filePath = None, zipped = False, zipPaths = []):
    total = 0
    numberObfuscated = 0
    if zipped:
        with open("Obfuscation_information.txt", "w") as f:
            for zipPath in zipPaths:
                path = paths[zipPaths.index(zipPath)]
                f.write(zipPath)
                f.write(" ")
                zipPath = zipPath.replace('\n', '')
                zipObject = zipfile.ZipFile(zipPath, 'r')
                obf = False
                if quick == True:
                    obf = checkForObfuscation(path, True, None, zipped, zipObject)
                elif path != None:
                    obf = checkForObfuscation(path, False, filePath, zipped, zipObject)
                else:
                    obf = checkForObfuscation(path, False, None, zipped, zipObject)
                if obf:
                    total += 1
                    f.write("yes\n")
                    numberObfuscated += 1
                else:
                    total += 1
                    f.write("no ")
                    f.write(str(checkVersion(path, zipped, zipObject))+'\n')
    else:
        with open("Obfuscation_information.txt", "w") as f:
            for path in paths:
                f.write("The metadata file at ")
                f.write(path)
                f.write(" is version ")
                f.write(str(checkVersion(path)))
                obf = False
                if quick == True:
                    obf = checkForObfuscation(path, True, None, zipped)
                elif path != None:
                    obf = checkForObfuscation(path, False, filePath, zipped)
                else:
                    obf = checkForObfuscation(path, False, None, zipped)
                if obf:
                    f.write(". It is obfuscated.\n")
                    total += 1
                    numberObfuscated += 1
                else:
                    total +=1
                    f.write(". It is not obfuscated.\n")
    return total, numberObfuscated
args = sys.argv[1:]
goodArgs = ['m', 'o', 'os', 'of', 'o' 'fields', 'structure', 'types', 'defaultPath', 'oz', '-pf']
if len(args) == 0:
    print("usage: python parser.py m [or] o [or] fields [or] structure [or] types")
    print("The \'types\' flag will output the types with methods and fields to a file(only working for latest version)")
    print("The \'m\' flag will output the methods to a file")
    print("The \'fields\' flag will output the fields  to a file(only working for latest version)")
    print("The \'structure\' flag will output the structure  to a file(only working for latest version)")
    print("The \'o\' flag will output the obfuscation status")
    exit(0)
paths = []
if 'defaultPath' in args:
    preName = "../apks/2020.06/"
    pathName = "assets/bin/Data/Managed/Metadata/global-metadata.dat"
    for fileName in [pathName for name in os.listdir("../apks/2020.06/") if name.endswith(".apk")]:
        paths.append(fileName)
else:
    print("Finding all paths to \"global-metadata.dat\"")
    paths = glob.glob("./**/global-metadata.dat", recursive = True)
apkPaths = []
if '-pf' in args:
    i = args.index('-pf') + 1
    while i < len(args):
        with open(args[i], 'r') as file:
            lines = file.readlines()
        for line in lines:
            apkPaths.append(line)
        i += 1

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
if('os' in args):
    print("Outputting obfuscation status using simple checks")
    numberOfFiles = 0
    numberOfDirectories = 0
    numberOfItems = 0
    for item in os.listdir():
        numberOfItems += 1
        if os.path.isfile(item):
            numberOfFiles += 1
    numberOfDirectories = numberOfItems - numberOfFiles
    numberObfuscated = numberOfDirectories - len(paths)
    numberObfuscated += outputObfStatus(paths, True)
    print("Of " + str(numberOfDirectories) +" directories, " + str(numberObfuscated) +" have either missing or obfuscated global-metadata.dat file.")
    print("All files not listed in the output text file should be considered to have either missing or obfuscated global-metadata.dat file.")
if('of' in args):
    print("Outputting obfuscation status using input file")
    fileName = args[args.index('of')+1]
    numberOfFiles = 0
    numberOfDirectories = 0
    numberOfItems = 0
    for item in os.listdir():
        numberOfItems += 1
        if os.path.isfile(item):
            numberOfFiles += 1
    numberOfDirectories = numberOfItems - numberOfFiles
    numberObfuscated = numberOfDirectories - len(paths)
    numberObfuscated += outputObfStatus(paths, False, fileName)
    print("Of " + str(numberOfDirectories) +" directories, " + str(numberObfuscated) +" have either missing or obfuscated global-metadata.dat file.")
    print("All files not listed in the output text file should be considered to have either missing or obfuscated global-metadata.dat file.")
if('oz' in args):
    print("Outputting obfuscation status of a zipped/apk file")
    total = 0
    for item in os.listdir():
        if item.endswith(".apk"):
            numberOfFiles += 1
    if apkPaths == [] and "20" in args:
        apkPaths = [name for name in os.listdir("../apks/2020.06/") if name.endswith(".apk")]
    if apkPaths == [] and "19" in args:
        apkPaths = [name for name in os.listdir("../apks/2019.01/") if name.endswith(".apk")]
    total, numberObfuscated = outputObfStatus(paths, False, None, True, apkPaths)
    print("Of " + str(total) +" apk files, " + str(numberObfuscated) +" have either missing or obfuscated global-metadata.dat file.")
    print("All files not listed in the output text file should be considered to have either missing or obfuscated global-metadata.dat file.")
exit(0)

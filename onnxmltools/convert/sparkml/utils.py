# -------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
# --------------------------------------------------------------------------
'''
Utility functions for Spark ML to Onnx conversion intended for the end user mainly
'''
from onnxmltools.convert.common.data_types import StringTensorType, FloatTensorType


def buildInitialTypesSimple(dataframe):
    types = []
    for field in dataframe.schema.fields:
        types.append((field.name, getTensorTypeFromSpark(str(field.dataType))))
    return types


def getTensorTypeFromSpark(sparktype):
    if sparktype == 'StringType':
        return StringTensorType([1, 1])
    elif sparktype == 'DecimalType' \
            or sparktype == 'DoubleType' \
            or sparktype == 'FloatType' \
            or sparktype == 'LongType' \
            or sparktype == 'IntegerType' \
            or sparktype == 'ShortType' \
            or sparktype == 'ByteType' \
            or sparktype == 'BooleanType':
        return FloatTensorType([1, 1])
    else:
        raise TypeError("Cannot map this type to Onnx types: " + sparktype)


def buildInputDictSimple(dataframe):
    import numpy
    result = {}
    for field in dataframe.schema.fields:
        if str(field.dataType) == 'StringType':
            result[field.name] = dataframe.select(field.name).toPandas().values
        else:
            result[field.name] = dataframe.select(field.name).toPandas().values.astype(numpy.float32)
    return result


class SparkMlConversionError(Exception):
    pass

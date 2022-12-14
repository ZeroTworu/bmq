from typing import TYPE_CHECKING

from app._types import CompressorType
from app.compress.gzip import GzipCompressor
from app.compress.protobuf.protobuf import ProtobufCompressor
from app.config.app import COMPRESSOR_TYPE

if TYPE_CHECKING:
    from app.compress.icompress import ICompressor


def get_compressor() -> 'ICompressor':
    match COMPRESSOR_TYPE:
        case CompressorType.GZIP:
            return GzipCompressor()
        case CompressorType.PROTOBUF:
            return ProtobufCompressor()
        case _:
            raise ValueError(f'Compressor {COMPRESSOR_TYPE} not supported')

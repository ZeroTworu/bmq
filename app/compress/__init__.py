from app.compress.gzip import GzipCompressor
from app.compress.icompress import ICompressor
from app.config.types import COMPRESSOR_TYPE, CompressorType


def get_compressor() -> 'ICompressor':
    match COMPRESSOR_TYPE:
        case CompressorType.GZIP:
            return GzipCompressor()
        case _:
            raise ValueError(f'Compressor {COMPRESSOR_TYPE} not supported')

class Inverter:
    translation_table = bytes.maketrans(
        bytes([x for x in range(0, 256)]),
        bytes([255 - x for x in range(0, 256)])
    )

    @classmethod
    def invert(cls, buffer, byte_count=None):
        """
        Invert the first byte_count bytes or the whole stream
        Except the last x bytes, where x is the file size mod 4
        :param buffer:
        :param byte_count:
        :return:
        """
        byte_count = len(buffer) if byte_count is None else byte_count

        inverted = buffer[:byte_count].translate(
            cls.translation_table
        ) + buffer[byte_count:]

        padding = len(buffer) % 4
        if padding > 0:
            return inverted[:-padding] + buffer[-padding:]

        return inverted

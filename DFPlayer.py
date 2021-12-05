import random
import time
import serial



class DFPlayer:

    def __init__(self):
        self.is_playing = False
        self.serial = serial.Serial(port='/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=5)
        self.set_up()

    def set_up(self):
        self.stop_playback()
        self.set_volume()
        self.set_random_playback()
        self.play_track(random.randint(2, 156))

    @staticmethod
    def convert_dfplayer_response_to_hex(received_bytes):
        converted_string = received_bytes.hex()
        for i in range(int(len(converted_string) / 20)):
            single_message = converted_string[i*20: (i*20) + 20]
            single_message_array = []
            for x in range(20):
                two_characters = single_message[x*2:(x*2) + 2]
                if two_characters != '':
                    single_message_array.append(single_message[x*2:(x*2) + 2])
            print(single_message_array)

    @staticmethod
    def generate_command(command_one, parameter_1, parameter_2):
        """
        DFPlayer requires a special command set.
        Found though https://github.com/DFRobot/DFRobotDFPlayerMini/blob/master/doc/FN-M16P%2BEmbedded%2BMP3%2BAudio%2BModule%2BDatasheet.pdf
        :param command_one: Hexadecimal command for DF Player.
        :param parameter_1: Command param from above URL.
        :param parameter_2: Command param from above URL.
        :return: DFPlayer compatible code.
        """

        start_byte = 0x7E
        version_byte = 0xFF
        command_length = 0x06
        end_byte = 0xEF
        feedback = 0x01

        #   generate checksum.
        checksum = 65535 + -(version_byte + command_length + command_one + feedback + parameter_1 + parameter_2) + 1

        #   checksum is the high byte and low bite of the checksum.
        high_byte, low_byte = divmod(checksum, 0x100)

        array_of_bytes = [start_byte, version_byte, command_length, command_one, feedback, parameter_1, parameter_2, high_byte, low_byte, end_byte]

        command_bytes = bytes(array_of_bytes)
        return command_bytes

    def send_command(self, command):
        print('sending', command)

        self.serial.write(command)
        time.sleep(0.05)
        message = self.serial.readline()
        self.convert_dfplayer_response_to_hex(message)

    def stop_playback(self):
        self.send_command(self.generate_command(0x16, 0x00, 0x00))

    def set_volume(self, volume_level=15):
        self.send_command(self.generate_command(0x06, 0x00, int(volume_level)))

    def play_track(self, track_number):
        self.send_command(self.generate_command(0x12, 0x00, int(track_number)))

    def play_blank_space(self):
        pass

    def set_random_playback(self):
        self.send_command(self.generate_command(0x18, 0x00, 0x00))


if __name__ == '__main__':
    serial_music_player = DFPlayer()